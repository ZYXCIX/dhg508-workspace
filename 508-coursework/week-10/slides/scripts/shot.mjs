#!/usr/bin/env node
/**
 * shot: screenshot slides in one command.
 *
 *   npm run shot -- <targets> [options]
 *
 * Targets (any mix, space or comma separated):
 *   7          slide number          6-9    range of numbers
 *   m1-18      slide id (deck.yaml)  'm4-*' id pattern (quote it)    all
 *
 * Options:
 *   --size projector|laptop|small|WxH   viewport (1920x1080 | 1440x900 | 1280x720); default projector
 *   --scale 1|2                         device pixel ratio; default 1
 *   --sheet [N]                         also write contact-sheet.png, N per row (default 4)
 *   --out DIR                           default .shots/<date-time>/ in this deck folder
 *   --url URL|DIST                      default http://localhost:4381; a built dist folder is served locally
 *   --edition NAME                      deck.yaml edition (default: the first one)
 *
 * Each PNG path is printed. A slide is flagged when it shows the "not valid JSX" fallback or when
 * content runs past the slide body or the canvas (cut off, or over the foot line).
 *
 * Uses reslides' installed playwright-core and Chromium 1243 read-only: no downloads, no changes there.
 */
import { createServer } from 'node:http'
import { existsSync, mkdirSync, readFileSync, statSync, writeFileSync, createReadStream } from 'node:fs'
import { dirname, extname, join, resolve } from 'node:path'
import { fileURLToPath, pathToFileURL } from 'node:url'
import { homedir } from 'node:os'

const HOME = homedir()
const RESLIDES_DIR = existsSync(join(HOME, 'script/reslides')) ? join(HOME, 'script/reslides') : join(HOME, 'code/reslides')
const PW = existsSync(join(RESLIDES_DIR, 'node_modules/playwright-core/index.mjs'))
  ? join(RESLIDES_DIR, 'node_modules/playwright-core/index.mjs')
  : join(HOME, 'code/reslides/node_modules/.pnpm/playwright-core@1.57.0/node_modules/playwright-core/index.mjs')
const CHROME = existsSync('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome')
  ? '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
  : join(HOME, '.cache/ms-playwright/chromium-1243/chrome-linux64/chrome')
const YAML_LIB = existsSync(join(RESLIDES_DIR, 'node_modules/yaml/dist/index.js'))
  ? join(RESLIDES_DIR, 'node_modules/yaml/dist/index.js')
  : join(HOME, 'code/reslides/node_modules/.pnpm/yaml@2.8.2/node_modules/yaml/dist/index.js')
const DECK_DIR = resolve(dirname(fileURLToPath(import.meta.url)), '..')
const SIZES = { projector: [1920, 1080], laptop: [1440, 900], small: [1280, 720] }

function die(msg) {
  console.error(`shot: ${msg}`)
  process.exit(1)
}

// ---------- arguments ----------
const opts = { size: 'projector', scale: 1, sheet: 0, out: '', url: 'http://localhost:3100', edition: '' }
const tokens = []
const argv = process.argv.slice(2)
for (let i = 0; i < argv.length; i++) {
  const a = argv[i]
  const next = () => (i + 1 < argv.length ? argv[++i] : die(`${a} needs a value`))
  if (a === '--size') opts.size = next()
  else if (a === '--scale') opts.scale = Number(next())
  else if (a === '--sheet') opts.sheet = /^\d+$/.test(argv[i + 1] ?? '') ? Number(argv[++i]) : 4
  else if (a === '--out') opts.out = next()
  else if (a === '--url') opts.url = next()
  else if (a === '--edition') opts.edition = next()
  else if (a === '-h' || a === '--help') {
    console.log(readFileSync(fileURLToPath(import.meta.url), 'utf8').match(/\/\*\*([\s\S]*?)\*\//)[1].replace(/^ \* ?/gm, ''))
    process.exit(0)
  }
  else if (a.startsWith('--')) die(`unknown option ${a} (see --help)`)
  else tokens.push(...a.split(',').filter(Boolean))
}
if (!tokens.length) die('no targets. Example: npm run shot -- 3 6-9 m1-18 \'m4-*\' --sheet')
const [W, H] = SIZES[opts.size] ?? (/^\d+x\d+$/.test(opts.size) ? opts.size.split('x').map(Number) : die(`bad --size ${opts.size}`))
if (![1, 2].includes(opts.scale)) die('--scale must be 1 or 2')
if (!existsSync(PW)) die(`playwright-core not found at ${PW}`)
if (!existsSync(CHROME)) die(`Chromium not found at ${CHROME}`)

// ---------- deck order: number -> id ----------
async function deckIds() {
  const text = readFileSync(join(DECK_DIR, 'deck.yaml'), 'utf8')
  let raw
  try {
    raw = (await import(pathToFileURL(YAML_LIB).href)).parse(text)
  }
  catch {
    die('cannot read deck.yaml (yaml parser missing or file invalid)')
  }
  const editions = raw.editions ?? { default: { list: raw.list, backup: raw.backup } }
  const name = opts.edition || Object.keys(editions)[0]
  const ed = editions[name] ?? die(`no edition "${name}" in deck.yaml (have: ${Object.keys(editions).join(', ')})`)
  const id = item => (typeof item === 'string' ? item : item?.slide)
  return [...(ed.list ?? []), ...(ed.backup ?? [])].map(id)
}
const ids = await deckIds()
const total = ids.length

function resolveTargets() {
  const want = new Set()
  for (const t of tokens) {
    let m
    if (t === 'all') ids.forEach((_, i) => want.add(i + 1))
    else if (/^\d+$/.test(t)) want.add(Number(t))
    else if ((m = t.match(/^(\d+)(?:-|\.\.)(\d+)$/))) {
      const [a, b] = [Number(m[1]), Number(m[2])].sort((x, y) => x - y)
      for (let n = a; n <= b; n++) want.add(n)
    }
    else {
      const re = new RegExp(`^${t.replace(/[.+^${}()|[\]\\]/g, '\\$&').replace(/\*/g, '.*').replace(/\?/g, '.')}$`)
      const hit = ids.flatMap((id, i) => (re.test(id) ? [i + 1] : []))
      if (!hit.length) console.warn(`shot: "${t}" matches no slide id in deck.yaml`)
      hit.forEach(n => want.add(n))
    }
  }
  const out = [...want].sort((a, b) => a - b)
  const bad = out.filter(n => n < 1 || n > total)
  if (bad.length) console.warn(`shot: no slide ${bad.join(', ')} (deck has ${total})`)
  return out.filter(n => n >= 1 && n <= total)
}
const targets = resolveTargets()
if (!targets.length) die('nothing to shoot')

// ---------- source: dev server URL or a built dist folder ----------
const TYPES = { '.html': 'text/html', '.js': 'text/javascript', '.mjs': 'text/javascript', '.css': 'text/css', '.json': 'application/json', '.svg': 'image/svg+xml', '.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.webp': 'image/webp', '.gif': 'image/gif', '.woff': 'font/woff', '.woff2': 'font/woff2', '.ttf': 'font/ttf', '.pdf': 'application/pdf', '.ico': 'image/x-icon' }
async function serveDist(dir) {
  const server = createServer((req, res) => {
    let p = decodeURIComponent(new URL(req.url, 'http://x').pathname)
    let f = join(dir, p)
    if (!f.startsWith(dir)) return res.writeHead(403).end()
    if (!existsSync(f) || statSync(f).isDirectory()) f = existsSync(join(f, 'index.html')) ? join(f, 'index.html') : join(dir, 'index.html')
    res.writeHead(200, { 'content-type': TYPES[extname(f).toLowerCase()] ?? 'application/octet-stream' })
    createReadStream(f).pipe(res)
  })
  await new Promise(r => server.listen(0, '127.0.0.1', r)) // a free port, never 4381/4391
  return { base: `http://127.0.0.1:${server.address().port}/`, close: () => server.close() }
}
let base = opts.url
let closeServer = () => {}
const asDir = resolve(DECK_DIR, opts.url)
if (!/^https?:\/\//.test(opts.url)) {
  if (!existsSync(join(asDir, 'index.html'))) die(`--url ${opts.url}: not a URL and no index.html in that folder`)
  const s = await serveDist(asDir)
  base = s.base
  closeServer = s.close
}
base = base.replace(/#.*$/, '').replace(/\/?$/, '/')
try {
  await fetch(base, { signal: AbortSignal.timeout(5000) })
}
catch {
  die(`${base} is not reachable. Start the dev server first (npm run dev) or pass a built dist directory to --url.`)
}

// ---------- output folder ----------
const d = new Date(), p2 = v => String(v).padStart(2, '0')
const stamp = `${d.getFullYear()}-${p2(d.getMonth() + 1)}-${p2(d.getDate())}-${p2(d.getHours())}${p2(d.getMinutes())}${p2(d.getSeconds())}` // local time
// default folder: local date-time plus the process id, so two runs started in the same second never share it
const outDir = resolve(DECK_DIR, opts.out || join('.shots', `${stamp}-${process.pid}`))
mkdirSync(outDir, { recursive: true })

// ---------- capture ----------
const { chromium } = await import(pathToFileURL(PW).href)
const browser = await chromium.launch({ executablePath: CHROME })
const page = await browser.newPage({ viewport: { width: W, height: H }, deviceScaleFactor: opts.scale })

/** In the page: wait for fonts, images and the theme's fit to settle; then inspect the visible slide. */
async function settleAndInspect() {
  return page.evaluate(async () => {
    const sleep = ms => new Promise(r => setTimeout(r, ms))
    const frame = () => new Promise(r => requestAnimationFrame(() => r()))
    const visible = (e) => {
      if (!e || !e.getClientRects().length) return false
      const r = e.getBoundingClientRect(), s = getComputedStyle(e)
      return r.width > 0 && r.height > 0 && r.right > 0 && r.bottom > 0 && r.left < innerWidth && r.top < innerHeight && s.visibility !== 'hidden' && s.opacity !== '0'
    }
    const slide = () => [...document.querySelectorAll('.dh, .slidev-layout')].find(visible)
    const signature = () => {
      const s = slide()
      if (!s) return 'none'
      return [...s.querySelectorAll('*')].slice(0, 400).map((e) => { const r = e.getBoundingClientRect(); return `${r.x | 0},${r.y | 0},${r.width | 0},${r.height | 0}` }).join(';')
    }
    // wait for a visible slide
    for (let i = 0; i < 100 && !slide(); i++) await sleep(100)
    await document.fonts.ready
    // images in the visible slide
    const imgs = [...(slide()?.querySelectorAll('img') ?? [])]
    await Promise.all(imgs.map(i => (i.complete ? (i.decode?.() ?? Promise.resolve()).catch(() => {}) : new Promise(r => { i.onload = i.onerror = r }))))
    // layout settles when two samples 250 ms apart agree (fit zoom, transitions)
    let prev = ''
    for (let i = 0; i < 40; i++) {
      await frame(); await sleep(250)
      const cur = signature()
      if (cur === prev) break
      prev = cur
    }
    const s = slide()
    if (!s) return { ok: false, flags: ['NO SLIDE RENDERED'] }
    const flags = []
    // a capture taken mid-update (hot reload, transition) can show an empty page
    if (!s.innerText.trim()) return { ok: false, blank: true, flags: ['BLANK: the slide showed no text when captured'] }
    if ([...s.querySelectorAll('[data-reslides-raw="fallback"]')].some(visible)) flags.push('FALLBACK: not valid JSX, rendered as plain HTML')
    if (s.closest('[data-overflow]') || s.querySelector('[data-overflow]') || s.hasAttribute('data-overflow')) flags.push('OVERFLOW: theme could not fit the content')
    // own geometric check: visible part of any element beyond the slide body or the canvas
    const canvas = s.getBoundingClientRect()
    const main = s.querySelector('.main') ?? s
    const area = main.getBoundingClientRect()
    const past = []
    for (const e of main.querySelectorAll('*')) {
      if (!visible(e) || e.children.length > 0 && !e.matches('img, svg, video, canvas, pre')) continue
      let r = e.getBoundingClientRect()
      let box = { l: r.left, t: r.top, r: r.right, b: r.bottom }
      for (let a = e.parentElement; a && a !== main; a = a.parentElement) {
        const st = getComputedStyle(a)
        if (st.overflow !== 'visible' || st.overflowX !== 'visible' || st.overflowY !== 'visible') {
          const ar = a.getBoundingClientRect()
          box = { l: Math.max(box.l, ar.left), t: Math.max(box.t, ar.top), r: Math.min(box.r, ar.right), b: Math.min(box.b, ar.bottom) }
        }
      }
      if (box.r <= box.l || box.b <= box.t) continue
      const out = box.b > area.bottom + 2 || box.r > area.right + 2 || box.b > canvas.bottom + 1 || box.r > canvas.right + 1 || box.t < canvas.top - 1 || box.l < canvas.left - 1
      if (out) past.push(`${e.tagName.toLowerCase()}${e.className && typeof e.className === 'string' ? '.' + e.className.trim().split(/\s+/)[0] : ''} "${(e.getAttribute('alt') || e.textContent || '').trim().slice(0, 30)}"`)
    }
    if (past.length) flags.push(`OVERFLOW: ${past.length} element(s) past the slide body or canvas, e.g. ${past.slice(0, 2).join(', ')}`)
    return { ok: true, flags }
  })
}

const results = []
await page.goto(`${base}#/${targets[0]}`, { waitUntil: 'load', timeout: 60000 })
for (const n of targets) {
  const id = ids[n - 1]
  for (let attempt = 1; attempt <= 2; attempt++) {
    try {
      if (attempt === 2) // a hiccup (slow load, hot reload mid-capture): reload once and retry
        await page.goto(`${base}#/${n}`, { waitUntil: 'load', timeout: 60000 })
      await page.evaluate(no => { location.hash = `#/${no}` }, n)
      await page.waitForFunction(no => location.hash === `#/${no}`, n)
      await page.waitForTimeout(150)
      const { flags, blank } = await settleAndInspect()
      if (blank && attempt === 1)
        throw new Error('blank capture')            // reload and retry once
      const file = join(outDir, `${String(n).padStart(3, '0')}-${id}.png`)
      await page.screenshot({ path: file })
      results.push({ n, id, file, flags })
      console.log(`${file}${flags.length ? `\n    ⚠ ${flags.join('\n    ⚠ ')}` : ''}`)
      break
    }
    catch (err) {
      if (attempt === 1)
        continue
      results.push({ n, id, file: '', flags: [`ERROR: ${err.message.split('\n')[0]}`] })
      console.log(`slide ${n} ${id}: ⚠ ERROR ${err.message.split('\n')[0]}`)
    }
  }
}

// ---------- contact sheet ----------
if (opts.sheet) {
  const esc = s => s.replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' })[c])
  const cells = results.filter(r => r.file).map(r => `<figure${r.flags.length ? ' class="bad"' : ''}><img src="${pathToFileURL(r.file).href}"><figcaption><b>${r.n}</b> · ${esc(r.id)}${r.flags.length ? ` <i>${esc(r.flags.map(f => f.split(':')[0]).join(', '))}</i>` : ''}</figcaption></figure>`).join('')
  const html = `<!doctype html><meta charset="utf-8"><style>body{margin:0;padding:24px;background:#fff;font:600 18px/1.3 ui-monospace,monospace;color:#111}main{display:grid;grid-template-columns:repeat(${opts.sheet},480px);gap:24px}figure{margin:0}img{width:480px;display:block;border:1px solid #111}.bad img{border:3px solid #e31f27}figcaption{margin-top:6px}i{color:#e31f27;font-style:normal}</style><main>${cells}</main>`
  const sheetHtml = join(outDir, 'contact-sheet.html')
  writeFileSync(sheetHtml, html)
  const sp = await browser.newPage({ viewport: { width: opts.sheet * 504 + 24, height: 400 } })
  await sp.goto(pathToFileURL(sheetHtml).href, { waitUntil: 'load' })
  const sheet = join(outDir, 'contact-sheet.png')
  await sp.screenshot({ path: sheet, fullPage: true })
  console.log(`${sheet}  (contact sheet, ${opts.sheet} per row)`)
}

await browser.close()
closeServer()
const flagged = results.filter(r => r.flags.length)
console.log(`\n${results.length} slide(s) at ${W}x${H}${opts.scale === 2 ? ' @2x' : ''} from ${opts.url} -> ${outDir}`)
console.log(flagged.length ? `${flagged.length} flagged: ${flagged.map(r => `${r.n} ${r.id}`).join(', ')}` : 'no flags')
