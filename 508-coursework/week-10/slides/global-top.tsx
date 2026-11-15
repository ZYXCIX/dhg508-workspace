/**
 * Time mark: a small grey "1.5′" at the top right of every slide, showing that slide's planned
 * minutes so the speaker knows how long to spend on it.
 *
 * Source: the slide's effective frontmatter `minutes`, the same value `reslides check` adds up and
 * the pacing bar uses (deck.yaml's edition list wins over the slide file's own frontmatter).
 * Slides without minutes (backups) show nothing.
 *
 * Switch: VITE_TIME_MARK=on|off. Unset → shown in dev, hidden in build.
 *   VITE_TIME_MARK=on npm run build    # build that keeps the marks (e.g. a speaker copy)
 *   VITE_TIME_MARK=off npm run dev     # rehearse without them
 *
 * Picked up automatically by reslides as a global layer (deck-root global-top.tsx).
 */
import { useEffect } from 'react'
import { useNav } from '@slidev/client/hooks/useNav.ts'
import { startJsonView } from './json-view.ts'
import { startFitTables } from './fit-tables.ts'

interface Meta { slide?: { frontmatter?: { minutes?: number } } }

const flag = String(import.meta.env.VITE_TIME_MARK ?? '').toLowerCase()
const enabled = flag === 'on' || flag === '1' || flag === 'true'
  ? true
  : flag === 'off' || flag === '0' || flag === 'false' ? false : import.meta.env.DEV

export default function TimeMark() {
  const { slides, currentSlideNo } = useNav()
  // JSON viewer (.json boxes): see json-view.ts
  useEffect(() => { startJsonView(); startFitTables() }, [])  // fit-tables.ts: tables in frames fit their frame
  if (!enabled)
    return null
  const minutes = (slides.find(route => route.no === currentSlideNo)?.meta as Meta | undefined)?.slide?.frontmatter?.minutes
  if (typeof minutes !== 'number')
    return null
  return (
    <div
      className="dh-time-mark"
      aria-hidden="true"
      title={`Planned: ${minutes} min`}
      style={{
        position: 'absolute',
        top: 30,
        right: 120,
        zIndex: 20,
        pointerEvents: 'none',
        font: '500 15px/1 var(--dh-mono, ui-monospace, monospace)',
        letterSpacing: '0.04em',
        color: '#a1a1aa',
      }}
    >
      {minutes}
      ′
    </div>
  )
}
