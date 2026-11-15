/**
 * Tables inside a frame (.frame .text table) always fit the frame's inner width.
 * 1. Start from the stylesheet size (30 px; 26 px with class compact).
 * 2. If the table is wider than the frame's text area, step the font down, never below 26 px.
 * 3. If it still does not fit at 26 px, let cells wrap at spaces ([data-wrap]); short values
 *    such as $20.00 have no spaces and stay whole.
 * Only an inline font-size and a data attribute are set on the table; both are cleared before
 * each measurement, so the table returns to normal when it fits again.
 */
const MIN_PX = 26

function fitTable(table: HTMLTableElement) {
  const box = table.parentElement
  if (!box || !box.clientWidth)
    return
  table.style.fontSize = ''
  table.removeAttribute('data-wrap')
  const avail = box.clientWidth
  if (table.offsetWidth <= avail + 1)
    return
  let px = Math.round(parseFloat(getComputedStyle(table).fontSize))
  while (px > MIN_PX && table.offsetWidth > avail + 1) {
    px -= 1
    table.style.fontSize = `${px}px`
  }
  if (table.offsetWidth > avail + 1)
    table.setAttribute('data-wrap', '')
}

function fitAll() {
  document.querySelectorAll<HTMLTableElement>('.dh .frame .text table').forEach((t) => {
    if (t.getClientRects().length)
      fitTable(t)
  })
}

let started = false
export function startFitTables() {
  if (started || typeof document === 'undefined')
    return
  started = true
  let queued = false
  const run = () => { queued = false; fitAll() }
  const queue = () => { if (!queued) { queued = true; requestAnimationFrame(run) } }
  // slide changes (a slide becomes visible through attribute changes) and hot reloads;
  // ignore our own changes on tables
  new MutationObserver((records) => {
    if (records.every(r => r.type === 'attributes' && (r.target as Element).tagName === 'TABLE'))
      return
    queue()
  }).observe(document.body, { childList: true, subtree: true, attributes: true, attributeFilter: ['class', 'style', 'data-overflow'] })
  window.addEventListener('resize', queue)
  document.fonts?.ready.then(queue)
  queue()
  // the theme's fit settles after first paint; measure again shortly after
  setTimeout(queue, 400)
}
