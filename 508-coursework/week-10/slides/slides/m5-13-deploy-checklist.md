---
layout: process
kicker: Ship safely
minutes: 1
steps: false
items:
  - { label: "Step 1", what: "Pre-compute & test", how: "pytest / Vitest + local Playwright green" }
  - { label: "Step 2", what: "Deploy Pages + Worker", how: "wrangler pages deploy dist + secret key" }
  - { label: "Step 3", what: "Test the live URL!", how: "PLAYWRIGHT_BASE_URL=https://... npx playwright test", mark: true }
---

# Always run your Playwright smoke test one last time against the deployed URL.

<!--
部署的最后一步千万别漏掉：不要以为本地好使，推上去就一定好使（线上最容易漏配环境变量、大小写路径错或者跨域 CORS 报错）。推完拿到 https 链接后，把你刚才写的同一个 Playwright 测试直接指向线上真网址跑一遍！绿了，才算真正 deploy 成功。
-->

::read::
Deployment is only complete after pointing your Playwright E2E smoke test at the live `https://` URL to catch missing environment secrets, case-sensitive asset paths, or CORS errors.
