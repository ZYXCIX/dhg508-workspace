/**
 * JSON viewer for slides: <div class="json" data-src="url or label"><pre>…raw JSON…</pre></div>
 *
 * Renders like a browser's JSON viewer: a top bar with the URL/label, syntax colours from
 * the stylesheet (keys, strings, numbers/booleans/null, grey punctuation and … elisions),
 * one line per source line with a hanging indent when a long line wraps.
 * - Accepts partial or annotated JSON (…, comments, non-JSON lines): it never parses, only
 *   tokenizes, so it cannot fail; unknown text stays plain.
 * - Keeps <span class="hl"> (and any other span) from the source: the coloured tokens inside it
 *   are wrapped in a copy of that span, so highlights still work.
 * - Never edits React's nodes: it appends its own view inside .json and the stylesheet hides
 *   the original <pre> once the view exists. If this script fails, the raw <pre> stays visible.
 */

interface Run { text: string, cls: string, wrap: Element | null }

const TOKEN = /^(\s+|[{}[\],:]|…|\.\.\.|-?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?\b|true\b|false\b|null\b|")/

function tokenize(pre: HTMLPreElement): Run[] {
  // flatten the <pre> into (text, wrapper) segments
  const segs: { text: string, wrap: Element | null }[] = []
  pre.childNodes.forEach((n) => {
    if (n.nodeType === Node.TEXT_NODE)
      segs.push({ text: n.textContent ?? '', wrap: null })
    else if (n.nodeType === Node.ELEMENT_NODE)
      segs.push({ text: (n as Element).textContent ?? '', wrap: n as Element })
  })
  const runs: Run[] = []
  let inStr = false
  let escape = false
  let strRuns: Run[] = [] // runs of the string being read
  let lastStr: Run[] = [] // runs of the last closed string, until something other than space follows
  const push = (text: string, cls: string, wrap: Element | null) => {
    if (!text)
      return null
    const r = { text, cls, wrap }
    runs.push(r)
    return r
  }
  for (const { text, wrap } of segs) {
    let i = 0
    while (i < text.length) {
      if (inStr) {
        let j = i
        for (; j < text.length; j++) {
          const c = text[j]
          if (escape) { escape = false; continue }
          if (c === '\\') { escape = true; continue }
          if (c === '"') break
        }
        const closed = j < text.length
        const r = push(text.slice(i, closed ? j + 1 : j), 'j-str', wrap)
        if (r)
          strRuns.push(r)
        i = closed ? j + 1 : j
        if (closed) { inStr = false; lastStr = strRuns; strRuns = [] }
        continue
      }
      const rest = text.slice(i)
      const m = rest.match(TOKEN)
      if (m) {
        const t = m[1]
        if (t === '"') {
          inStr = true
          const r = push('"', 'j-str', wrap)
          if (r)
            strRuns = [r]
        }
        else if (/^\s+$/.test(t)) {
          push(t, '', wrap)
        }
        else if (t === ':') {
          lastStr.forEach(r => (r.cls = 'j-key'))
          lastStr = []
          push(t, 'j-pun', wrap)
        }
        else {
          lastStr = []
          push(t, /^[{}[\],]$/.test(t) ? 'j-pun' : t === '…' || t === '...' ? 'j-ell' : /^(true|false|null)$/.test(t) ? 'j-lit' : 'j-num', wrap)
        }
        i += t.length
      }
      else {
        // plain text (non-JSON line, e.g. a viewer caption): up to the next token start
        const k = rest.search(/[\s{}[\],:"…]/)
        const t = k <= 0 ? rest.slice(0, Math.max(k, 1)) : rest.slice(0, k)
        lastStr = []
        push(t, 'j-txt', wrap)
        i += t.length
      }
    }
  }
  return runs
}

function build(pre: HTMLPreElement, label: string): HTMLElement {
  const view = document.createElement('div')
  view.className = 'json-view'
  if (label) {
    const bar = document.createElement('div')
    bar.className = 'json-bar'
    const url = document.createElement('span')
    url.className = 'url'
    url.textContent = label
    bar.appendChild(url)
    view.appendChild(bar)
  }
  const body = document.createElement('div')
  body.className = 'json-body'
  view.appendChild(body)
  // split runs into lines
  const lines: Run[][] = [[]]
  for (const r of tokenize(pre)) {
    const parts = r.text.split('\n')
    parts.forEach((p, idx) => {
      if (idx > 0)
        lines.push([])
      if (p)
        lines[lines.length - 1].push({ ...r, text: p })
    })
  }
  // the JSX pipeline keeps the newline right after <pre>: drop leading/trailing empty lines
  while (lines.length && !lines[0].map(r => r.text).join('').trim()) lines.shift()
  while (lines.length && !lines[lines.length - 1].map(r => r.text).join('').trim()) lines.pop()
  for (const line of lines) {
    const el = document.createElement('div')
    el.className = 'j-line'
    const text = line.map(r => r.text).join('')
    const lead = text.match(/^[  ]*/)?.[0].length ?? 0
    if (!text.replace(/ /g, '').trim()) {
      el.innerHTML = '&nbsp;'
      body.appendChild(el)
      continue
    }
    el.style.setProperty('--ind', String(lead))
    // drop the leading spaces (they become the indent), keep everything else
    let drop = lead
    let group: Element | null = null
    let groupSrc: Element | null = null
    for (const r of line) {
      let t = r.text
      if (drop > 0) {
        const n = Math.min(drop, t.length - t.replace(/^[  ]+/, '').length)
        t = t.slice(n)
        drop -= n
        if (!t)
          continue
        drop = 0
      }
      const span = document.createElement('span')
      if (r.cls)
        span.className = r.cls
      span.textContent = t
      if (r.wrap) {
        if (groupSrc !== r.wrap) {
          group = r.wrap.cloneNode(false) as Element
          groupSrc = r.wrap
          el.appendChild(group)
        }
        group!.appendChild(span)
      }
      else {
        group = groupSrc = null
        el.appendChild(span)
      }
    }
    body.appendChild(el)
  }
  return view
}

function renderAll(root: ParentNode = document) {
  root.querySelectorAll<HTMLElement>('.json').forEach((box) => {
    const pre = box.querySelector<HTMLPreElement>(':scope > pre')
    if (!pre)
      return
    const sig = `${box.dataset.src ?? ''}\u0000${pre.innerHTML}`
    const old = box.querySelector<HTMLElement>(':scope > .json-view')
    if (old && old.dataset.sig === sig)
      return
    try {
      const view = build(pre, box.dataset.src ?? '')
      view.dataset.sig = sig
      if (old)
        old.replaceWith(view)
      else
        box.appendChild(view)
    }
    catch (err) {
      console.warn('[json-view] left as plain text:', err)
    }
  })
}

let started = false
/** Start once: render now and whenever slides (re)render. */
export function startJsonView() {
  if (started || typeof document === 'undefined')
    return
  started = true
  let queued = false
  const run = () => { queued = false; renderAll() }
  const obs = new MutationObserver((records) => {
    // ignore our own changes
    if (records.every(r => (r.target as Element).closest?.('.json-view')))
      return
    if (!queued) { queued = true; requestAnimationFrame(run) }
  })
  obs.observe(document.body, { childList: true, subtree: true, characterData: true })
  run()
}
