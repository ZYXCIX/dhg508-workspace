import { useContext, useEffect, useRef, useState } from 'react'
import { CurrentPageContext } from '@slidev/client/context.tsx'
import { useNav } from '@slidev/client/hooks/useNav.ts'

function resolveAssetUrl(u?: string): string | undefined {
  if (!u) return u
  if (/^(https?:|data:|blob:)/.test(u)) return u
  const base = (import.meta.env?.BASE_URL || '/').replace(/\/?$/, '/')
  if (u.startsWith('./')) return base + u.slice(2)
  if (u.startsWith('/') && !u.startsWith(base)) return base + u.slice(1)
  return u
}

interface LazyDemoProps {
  src: string
  title: string
  badge?: string
  summary?: string
  previewImg?: string
  presets?: string
  height?: number
  openHref?: string
}

export default function LazyDemo({
  src,
  title,
  badge = 'DYNAMIC EMBED · ZERO IDLE OVERHEAD',
  summary = 'Unloaded by default so WebGL and canvas workers never slow down the slide deck.',
  previewImg,
  presets,
  height = 680,
  openHref,
}: LazyDemoProps) {
  const { currentSlideNo, isPrintMode } = useNav()
  const myPage = useContext(CurrentPageContext)
  const resolvedSrc = resolveAssetUrl(src) ?? src
  const resolvedPreview = resolveAssetUrl(previewImg)
  const resolvedOpen = resolveAssetUrl(openHref)
  const [loaded, setLoaded] = useState(false)
  const [activeSrc, setActiveSrc] = useState(resolvedSrc)
  const wrapRef = useRef<HTMLDivElement | null>(null)

  // Automatically unmount heavy WebGL / Canvas iframe as soon as we leave this slide
  useEffect(() => {
    if (loaded && currentSlideNo !== myPage) {
      setLoaded(false)
    }
  }, [currentSlideNo, myPage, loaded])

  const parsedPresets = (presets ?? '')
    .split('|')
    .map(s => s.trim())
    .filter(Boolean)
    .map((item) => {
      const idx = item.indexOf('::')
      return idx === -1
        ? { label: item, url: resolveAssetUrl(item) ?? item }
        : { label: item.slice(0, idx).trim(), url: resolveAssetUrl(item.slice(idx + 2).trim()) ?? item.slice(idx + 2).trim() }
    })

  const launch = (nextUrl?: string) => {
    if (nextUrl) setActiveSrc(nextUrl)
    setLoaded(true)
  }

  const goFullscreen = () => {
    wrapRef.current?.requestFullscreen?.().catch(() => {})
  }

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '10px', width: '100%' }}>
      <div
        ref={wrapRef}
        style={{
          position: 'relative',
          width: '100%',
          height: `${height}px`,
          border: '1.5px solid #111111',
          background: '#f7f7f5',
          overflow: 'hidden',
        }}
      >
        {loaded && !isPrintMode ? (
          <iframe
            src={activeSrc}
            title={title}
            style={{ width: '100%', height: '100%', border: 0, background: '#ffffff' }}
            allow="fullscreen; autoplay; gamepad; pointer-lock"
          />
        ) : (
          <div
            style={{
              width: '100%',
              height: '100%',
              display: 'grid',
              gridTemplateColumns: resolvedPreview ? '1.25fr 0.85fr' : '1fr',
              background: '#faf9f6',
            }}
          >
            {resolvedPreview && (
              <div
                style={{
                  padding: '18px',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  background: '#ffffff',
                  borderRight: '1.5px solid #dededc',
                  overflow: 'hidden',
                }}
              >
                <img
                  src={resolvedPreview}
                  alt={title}
                  style={{ maxWidth: '100%', maxHeight: '100%', objectFit: 'contain' }}
                />
              </div>
            )}
            <div
              style={{
                padding: '28px 32px',
                display: 'flex',
                flexDirection: 'column',
                justifyContent: 'center',
                gap: '14px',
              }}
            >
              <div
                style={{
                  font: '700 12px/1 var(--dh-mono)',
                  letterSpacing: '.11em',
                  textTransform: 'uppercase',
                  color: '#e31f27',
                }}
              >
                {badge}
              </div>
              <div style={{ font: '600 26px/1.25 var(--dh-serif)', color: '#111111' }}>{title}</div>
              <div style={{ font: '400 16.5px/1.55 var(--dh-sans)', color: '#3f3f3a' }}>{summary}</div>
              <div style={{ display: 'flex', gap: '10px', flexWrap: 'wrap', marginTop: '6px' }}>
                <button
                  type="button"
                  onClick={e => { e.stopPropagation(); launch() }}
                  style={{
                    padding: '11px 20px',
                    border: '1.5px solid #111111',
                    background: '#e31f27',
                    color: '#ffffff',
                    font: '700 14.5px/1.2 var(--dh-mono)',
                    cursor: 'pointer',
                  }}
                >
                  ▶ Load Interactive Demo
                </button>
                {parsedPresets.slice(0, 3).map(p => (
                  <button
                    key={p.label}
                    type="button"
                    onClick={e => { e.stopPropagation(); launch(p.url) }}
                    style={{
                      padding: '10px 14px',
                      border: '1.5px solid #111111',
                      background: '#ffffff',
                      color: '#111111',
                      font: '600 13px/1.2 var(--dh-mono)',
                      cursor: 'pointer',
                    }}
                  >
                    {p.label}
                  </button>
                ))}
              </div>
            </div>
          </div>
        )}
      </div>

      <div
        onPointerDown={e => e.stopPropagation()}
        style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          gap: '10px',
          flexWrap: 'wrap',
          font: '600 13px/1.2 var(--dh-mono)',
        }}
      >
        <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap', alignItems: 'center' }}>
          {!loaded ? (
            <button
              type="button"
              onClick={() => launch()}
              style={{
                padding: '6px 12px',
                border: '1.5px solid #111',
                background: '#111',
                color: '#fff',
                font: 'inherit',
                cursor: 'pointer',
              }}
            >
              ▶ Mount iframe
            </button>
          ) : (
            <button
              type="button"
              onClick={() => setLoaded(false)}
              style={{
                padding: '6px 12px',
                border: '1.5px solid #e31f27',
                background: '#fff0f0',
                color: '#e31f27',
                font: 'inherit',
                cursor: 'pointer',
              }}
            >
              ■ Unload (Free GPU / RAM)
            </button>
          )}
          {parsedPresets.map(p => (
            <button
              key={p.label}
              type="button"
              onClick={() => launch(p.url)}
              style={{
                padding: '6px 11px',
                border: '1.5px solid #111',
                background: loaded && activeSrc === p.url ? '#e31f27' : '#ffffff',
                color: loaded && activeSrc === p.url ? '#ffffff' : '#111111',
                font: 'inherit',
                cursor: 'pointer',
              }}
            >
              {p.label}
            </button>
          ))}
        </div>

        <div style={{ display: 'flex', gap: '10px', alignItems: 'center' }}>
          {loaded && (
            <button
              type="button"
              onClick={goFullscreen}
              style={{
                padding: '6px 12px',
                border: '1.5px solid #111',
                background: '#ffffff',
                color: '#111',
                font: 'inherit',
                cursor: 'pointer',
              }}
            >
              ⛶ Fullscreen
            </button>
          )}
          <a
            href={resolvedOpen ?? activeSrc}
            target="_blank"
            rel="noreferrer"
            style={{ color: '#e31f27', textDecoration: 'none', padding: '4px 6px' }}
          >
            Open in new tab ↗
          </a>
        </div>
      </div>
    </div>
  )
}
