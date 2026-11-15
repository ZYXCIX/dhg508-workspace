---
minutes: 1.5
---

# Level 3 · End-to-end Playwright tests walk the real bow deck like a player.

```typescript {1-6|8-14|16-22}
// tests/e2e_bow_deck.spec.ts — Run with: npx playwright test
import { test, expect } from '@playwright/test'

test('player talks to James Talbot on bow deck with zero errors', async ({ page }) => {
  const errors: string[] = []
  page.on('pageerror', e => errors.push(e.message))
  page.on('console', m => { if (m.type() === 'error') errors.push(m.text()) })

  await page.setViewportSize({ width: 1280, height: 720 })
  await page.goto('http://localhost:3090')
  await page.click('[data-testid="enter-bow-deck"]')
  await page.click('[data-testid="npc-expert-1"]')
  await page.fill('[data-testid="chat-input"]', 'What preconditions do macro tools need?')
  await page.click('[data-testid="chat-send"]')

  await expect(page.locator('[data-testid="chat-reply"]')).toContainText(/credit|institutions/i)
  const clipped = await page.evaluate(() => {
    const el = document.querySelector('#dialogue-panel')!
    return el.scrollHeight > el.clientHeight
  })
  expect(clipped).toBe(false)
  expect(errors).toEqual([])
  await page.screenshot({ path: 'test-results/bow-deck-verified.png' })
})
```

<!--
最后看第三层：End-to-End Testing（端到端测试）。这二十行 Playwright 代码干了以前你要花三分钟手动干的所有事：第一，挂上 pageerror 和 console 监听器，任何报错都不放过；第二，设成 1280×720 分辨率，自动点进船头、点开 James Talbot、输入问题、点击发送；第三，断言回复出来了、对话框没有文字截断（scrollHeight 不超过 clientHeight）、控制台零报错，顺手存下一张验证截图！
-->

::read::
A 20-line Playwright E2E test opens the real browser viewport, clicks into the *Bashan* bow-deck conversation, checks for zero console errors and zero text clipping, and saves a proof screenshot.
