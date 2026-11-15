#!/usr/bin/env node
// Serve the built deck, including the Bashan Unity bundle.
//
// The Unity loader asks for `.gz` files directly (Build/*.data.gz), and a
// production static server answers them with `Content-Encoding: gzip` plus the MIME
// type of the underlying file.
// Python's http.server does neither, and ignores Range; this does both, so the
// build loads the same way locally as it does in production.
//
//   node scripts/serve-dist.mjs [port] [root]
//
// Defaults: port 3090, root ./dist. Binds 0.0.0.0 for local device testing.

import { createServer, request as httpRequest } from 'node:http'
import { createReadStream, existsSync, statSync } from 'node:fs'
import { extname, join, normalize, resolve } from 'node:path'

const port = Number(process.argv[2] ?? 3090)
const root = resolve(process.argv[3] ?? 'dist')
const apiUpstreamPort = Number(process.env.BASHAN_API_PORT ?? 18770)

const TYPES = {
  '.html': 'text/html; charset=utf-8',
  '.js': 'application/javascript; charset=utf-8',
  '.mjs': 'application/javascript; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
  '.wasm': 'application/wasm',
  '.data': 'application/octet-stream',
  '.jpg': 'image/jpeg',
  '.jpeg': 'image/jpeg',
  '.png': 'image/png',
  '.webp': 'image/webp',
  '.svg': 'image/svg+xml',
  '.woff2': 'font/woff2',
  '.woff': 'font/woff',
  '.pdf': 'application/pdf',
  '.vtt': 'text/vtt; charset=utf-8',
  '.txt': 'text/plain; charset=utf-8',
}

// A .gz file is served with the type of the file inside it, and the gzip
// content-coding header, exactly as the Caddy config does for the Unity build.
function describe(file) {
  if (!file.endsWith('.gz'))
    return { type: TYPES[extname(file).toLowerCase()] ?? 'application/octet-stream', encoding: undefined }
  const inner = extname(file.slice(0, -3)).toLowerCase()
  const type = inner === '.wasm'
    ? 'application/wasm'
    : inner === '.js'
      ? 'application/javascript'
      : inner === '.data'
        ? 'application/octet-stream'
        : TYPES[inner] ?? 'application/octet-stream'
  return { type, encoding: 'gzip' }
}

const server = createServer((req, res) => {
  const rawUrl = req.url ?? '/'
  if (
    rawUrl.startsWith('/bashan-game/api/') ||
    rawUrl.startsWith('/bashan/game/api/') ||
    rawUrl.startsWith('/api/')
  ) {
    const upstreamPath = rawUrl.startsWith('/bashan-game/api/')
      ? rawUrl.slice('/bashan-game'.length)
      : rawUrl.startsWith('/bashan/game/api/')
        ? rawUrl.slice('/bashan/game'.length)
        : rawUrl
    const proxyReq = httpRequest(
      {
        hostname: '127.0.0.1',
        port: apiUpstreamPort,
        path: upstreamPath,
        method: req.method,
        headers: { ...req.headers, host: `127.0.0.1:${apiUpstreamPort}` },
      },
      (proxyRes) => {
        res.writeHead(proxyRes.statusCode ?? 502, proxyRes.headers)
        proxyRes.pipe(res)
      },
    )
    proxyReq.on('error', (err) => {
      res.writeHead(502, { 'Content-Type': 'application/json' })
      res.end(JSON.stringify({ error: 'Upstream world-agent unreachable', detail: err.message }))
    })
    req.pipe(proxyReq)
    return
  }

  let path = decodeURIComponent(rawUrl.split('?')[0])
  if (path.endsWith('/'))
    path += 'index.html'
  const file = normalize(join(root, path))
  if (!file.startsWith(root) || !existsSync(file) || statSync(file).isDirectory()) {
    res.writeHead(404, { 'Content-Type': 'text/plain' })
    res.end('not found')
    return
  }

  const size = statSync(file).size
  const { type, encoding } = describe(file)
  const headers = { 'Content-Type': type, 'Accept-Ranges': 'bytes', 'Cache-Control': 'no-store' }
  if (encoding)
    headers['Content-Encoding'] = encoding

  const range = req.headers.range?.match(/^bytes=(\d*)-(\d*)$/)
  if (range) {
    const start = range[1] ? Number(range[1]) : 0
    const end = range[2] ? Math.min(Number(range[2]), size - 1) : size - 1
    if (start > end || start >= size) {
      res.writeHead(416, { 'Content-Range': `bytes */${size}` })
      res.end()
      return
    }
    res.writeHead(206, { ...headers, 'Content-Range': `bytes ${start}-${end}/${size}`, 'Content-Length': end - start + 1 })
    createReadStream(file, { start, end }).pipe(res)
    return
  }

  res.writeHead(200, { ...headers, 'Content-Length': size })
  if (req.method === 'HEAD')
    res.end()
  else
    createReadStream(file).pipe(res)
})

server.listen(port, '0.0.0.0', () => {
  console.log(`serving ${root} on http://0.0.0.0:${port}/`)
})
