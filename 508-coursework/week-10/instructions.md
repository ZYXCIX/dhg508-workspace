# Week 10 · Feedback Loops, Automated Testing, and Public Deployment

Prepare for the next class on **Wednesday 18 November 2026**.

**Session 10 slides:** [Reading edition (`slides/read/index.html`)](slides/read/index.html) · [Reslides deck & interactive demos (`slides/`)](slides/README.md)

**Mention your difficulties.**

## Assignment

Two weeks remain in the term. Move your project out of `localhost` and turn it into a complete, tested, publicly accessible work of genuine historical or cultural value—whether built in a game engine (**Unity**, **团结引擎 Tuanjie**, **Godot**) or as a thoroughly crafted web application. Half-finished scaffolding, dead buttons, raw JSON dumps, and unverified AI claims are no longer acceptable.

This week has two halves: **first**, deploy your project publicly on Cloudflare, wire up automated tests, and send the live link to two friends; **second**, come to next Wednesday's class ready to demonstrate **every feedback loop in action**—your ideation dialogue and agent-drawn schematic, your live-running test suite, your automatic browser loop, and how you turned real user feedback into permanent tests.

## 1. Ideation loop, `plan.md`, and your own project schematic

Before letting an agent run long autonomous edits with OpenCode `/goal`, lock down intent so the run cannot drift:

1. **Discuss and question in `Plan` mode (`Tab`).** Switch OpenCode from `Build` to `Plan` (`Tab`). Ask the agent to restate your project's scope, historical boundaries, and **three open questions** before touching any code. Answer its questions, push back where it guesses wrong, and save the agreed steps and non-goals into a written plan file (for example `docs/plan.md` or inside your design document).
2. **Generate a visual schematic of your own project.** Do not rely on terminal prose alone. Have your agent generate at least **one visual schematic of your project's architecture, spatial layout, or dialogue/state logic** using:
   - an **HTML schematic skill** such as [`nicobailon/visual-explainer`](https://github.com/nicobailon/visual-explainer) (or asking OpenCode to write a self-contained `docs/architecture-explainer.html` diagram page),
   - **Excalidraw MCP** ([`mcp-excalidraw-server`](https://github.com/yctimlin/mcp_excalidraw) on `http://localhost:3000` or [`https://mcp.excalidraw.com`](https://github.com/excalidraw/excalidraw-mcp)), or
   - a rendered **Mermaid** state/flow diagram in Markdown.
   Commit this schematic to your repository and bring it to show next week.
3. **Anchor `/goal` to your plan and checks.** When you launch OpenCode `/goal <objective>`, point it explicitly at your written plan, your source table (`据 / 推断 / 设`, or evidenced / inferred / invented), and your test command—never a vague wish. If you split research and implementation across agents, use OpenCode subagents (`.opencode/agents/researcher.md`), [`mcp_agent_mail_rust`](https://github.com/Dicklesworthstone/mcp_agent_mail_rust), or [`agentchattr`](https://github.com/bcurts/agentchattr), and always commit verified historical answers back into your repository files.

## 2. Deploy your project publicly

Put a working build on a public `https://` URL so anyone can open it without installing your development environment:

1. **Static site or exported WebGL build (`$0/month`).** Host HTML/JS/CSS, pre-computed JSON or binary embeddings, or an exported Unity / Godot HTML5 WebGL folder on **Cloudflare Pages**:
   - Either connect your GitHub repository in `dash.cloudflare.com` → **Workers & Pages → Create → Connect to Git**, or deploy from your terminal:
     ```bash
     npx wrangler login
     npx wrangler pages deploy dist --project-name=<your-project-name>
     ```
2. **If your project calls a live model API (OpenRouter, DeepSeek, Gemini).** **Never** place an API key inside browser JavaScript. Put a small **Cloudflare Worker** in front of the API, store the key with `npx wrangler secret put <KEY_NAME>`, and cap input length so visitors cannot drain your balance. Pre-compute fixed historical corpora, indexes, or embeddings locally at build time whenever possible so runtime stays fast and nearly free.
3. **Only rent a VPS if genuinely required.** Use a virtual machine (`~$5/month`) only if your project requires persistent multi-user database writes or heavy Python libraries that cannot run statically or in a Worker.

Check your live URL on another computer or phone to make sure every asset loads cleanly.

## 3. Set up automated testing and automatic browser verification

Separate your historical data (`.csv` / `.json`) and core rules (`src/`) from UI rendering so a machine can verify them in seconds. Set up and run all three layers appropriate to your stack:

1. **Compile / static gate (`< 1s`).** Record your project's one-line build or static check command in `AGENTS.md` (for example `python3 -m compileall -q . && uv run ruff check . && uv run mypy src/` for Python, `npx tsc --noEmit && npm run build` for TypeScript/Vite, or headless script checks for Godot/Unity).
2. **Unit and integration tests (`Vitest` or `pytest`).**
   - *Web / JS:* `npm i -D vitest @playwright/test` → `npx vitest run`
   - *Python:* `uv add --dev pytest httpx` → `uv run pytest -q`
   Test both your **technical logic** (state transitions, API contracts, cross-file IDs) and your **historical guardrails** (every claim or character record has valid `据 / 推断 / 设` tags, source locators, and anachronism/cutoff rules; add an LLM-as-a-Judge log check if live NPC dialogue risks drifting off-purpose).
3. **Automatic browser feedback (`@playwright/mcp` + `Playwright` E2E).**
   - Install Chromium once: `npx playwright install chromium`
   - Add `@playwright/mcp@latest` to `opencode.json` so your agent inspects live DOM geometry, console errors, `404` network requests, and screenshots itself—without you acting as a human copy-paste bridge.
   - Save repeatable end-to-end checks in `npx playwright test` (verifying `0` console/page errors, `0` broken assets, and key user interactions), and run your smoke test against your **deployed `https://` URL** as well as `localhost`.

## 4. Test with two friends and turn feedback into regression tests

1. Send your live deployed URL to **at least two friends outside your project** and ask them to use or play through it on their own devices.
2. Record what they tried, where they got confused, and what broke or drifted in `docs/user-feedback.md` (or in your research journal).
3. Fix at least **two concrete issues** they found, and **turn each fix into a permanent automated test** (unit, integration, or Playwright E2E) so that bug can never silently return.

## Bring to class (live showcase)

Be ready to demonstrate live on **Wednesday 18 November**:

1. **Your live public URL** running on Cloudflare Pages (+ Worker if applicable), opened in class.
2. **Your ideation feedback loop + your own project schematic:** show a real back-and-forth planning exchange (`plan.md` + `/goal` statement) and display **the HTML, Excalidraw, or Mermaid schematic of your project** generated with your agent.
3. **Your automated test suite running live:** run `pytest` / `vitest` and `npx playwright test` on screen, and explain clearly **what you tested** at the unit, integration, and E2E levels (both code behaviour and historical/source constraints).
4. **Your automatic browser loop:** show your `@playwright/mcp` configuration and saved Playwright browser check running automatically without manual eyeballing.
5. **External playtest → permanent test:** show the feedback from your **two friends**, the code/design changes you made in response, and the new regression test(s) that lock those fixes in.
6. **At least one real difficulty**, with its concrete example—what broke during deployment, browser automation, or testing, and how you diagnosed or worked around it.

Keep your repository README up to date with one-command test and run instructions, commit meaningful changes regularly, keep API keys and large binaries (`artifacts/`) out of Git, and record unresolved issues in `questions.md`.

---

# 第十週 · 反饋閉環、自動化測試與公開部署

請為 **2026 年 11 月 18 日（星期三）**的下次課堂做好準備。

**第十講投影片：** [閱讀版（`slides/read/index.html`）](slides/read/index.html) · [Reslides 課件源碼與互動演示（`slides/`）](slides/README.md)

**請務必說明你遇到的困難。**

## 本週作業

學期只剩最後兩週。請把你的專案從本機 `localhost` 真正推向公開網絡，打磨成一件完整、經過測試、具真實歷史或文化價值的作品——無論你選用遊戲引擎（**Unity**、**團結引擎 Tuanjie**、**Godot**），還是完整細緻地用純網頁（HTML / JavaScript / Three.js）製作，都完全歡迎；但不能再保留半成品骨架、失效按鈕、裸露的 JSON 輸出或未經核實的 AI 內容。

本週任務分為緊密相連的兩步：**第一步**，把專案部署到 Cloudflare 公開網址、配好自動化測試，並發給兩位朋友實測；**第二步**，在下週三課堂上**現場展示你用上的每一個反饋閉環（Feedback Loop）**——包括構思階段的來回探討與專案示意圖、現場跑起來的測試套件、自動運行的瀏覽器閉環，以及如何把真實用戶反饋轉化為永久防回歸測試。

## 1. 構思反饋閉環（Ideation Loop）、`plan.md` 與你自己的專案示意圖

在用 OpenCode `/goal` 讓 agent 長時間自主迭代之前，先鎖定設計邊界以防止目標偏移（Goal Drifting）：

1. **先用 `Plan` 模式（`Tab`）深入探討與反問。** 在 OpenCode 按 `Tab` 切到 `Plan` 模式（禁止直接改代碼），要求 agent 先複述你的專案範圍、歷史邊界，並向你提出**三個不確定的問題**。來回討論澄清後，把確認的分步計劃與紅線（Non-goals）寫入 `docs/plan.md`（或設計文件中）。
2. **讓 agent 生成一張你自己專案的視覺示意圖。** 不要只看終端機裏的大段文字，請要求 agent 為你的專案生成至少**一張架構圖、空間平面圖或對話／狀態流程示意圖**，可任選以下方式：
   - **HTML 示意圖技能**：安裝 [`nicobailon/visual-explainer`](https://github.com/nicobailon/visual-explainer)，或直接要求 OpenCode 輸出單文件 `docs/architecture-explainer.html` 視覺架構圖；
   - **Excalidraw MCP**：使用 [`mcp-excalidraw-server`](https://github.com/yctimlin/mcp_excalidraw)（本地 `http://localhost:3000`）或官方 [`https://mcp.excalidraw.com`](https://github.com/excalidraw/excalidraw-mcp)，讓 agent 自動把平面／結構畫到畫布上共同修改；
   - **Mermaid 狀態／流程圖**：在 Markdown 中繪製並渲染完整分支邏輯。
   將生成的示意圖存入儲存庫，下週課堂展示。
3. **用計劃與測試支撐 `/goal` 聲明。** 使用 OpenCode `/goal <目標>` 時，明確綁定你的計劃文件、史料證據表（標明**據／推斷／設**，即 evidenced / inferred / invented）以及可執行的測試命令。若拆分為研究與開發兩個角色，可使用 OpenCode 內建子代理（`.opencode/agents/researcher.md`）、[`mcp_agent_mail_rust`](https://github.com/Dicklesworthstone/mcp_agent_mail_rust) 或 [`agentchattr`](https://github.com/bcurts/agentchattr)，並將確認過的史實寫回正式文檔並提交 Git。

## 2. 將專案公開部署上線（Cloudflare）

把可運行的版本部署到公開的 `https://` 網址，讓任何人無需安裝開發環境就能直接打開：

1. **靜態網站或導出的 WebGL 版本（`$0/月`）。** 將 HTML/JS/CSS、預先計算好的 JSON／向量文件，或 Unity / Godot 導出的 HTML5 WebGL 資料夾部署到 **Cloudflare Pages**：
   - 可在 `dash.cloudflare.com` → **Workers & Pages → Create → Connect to Git** 綁定 GitHub 自動部署，或在終端機執行：
     ```bash
     npx wrangler login
     npx wrangler pages deploy dist --project-name=<你的專案名稱>
     ```
2. **若專案需要實時調用大模型 API（OpenRouter、DeepSeek、Gemini）。** **絕對不要**把 API Key 寫進前端 JavaScript。請在前端與 API 之間加一層輕量的 **Cloudflare Worker**，用 `npx wrangler secret put <KEY_NAME>` 加密保存密鑰，並限制輸入長度。固定不變的文獻語料、索引或 Embeddings 應盡量在本地預先計算（Pre-compute）後作為靜態文件發布。
3. **僅在確有必要時才租用虛擬機（VPS）。** 只有當專案必須持久化寫入多用戶數據庫或運行重型 Python 庫時，才考慮使用 VPS。

部署完成後，請在另一台設備或手機上打開公開網址，確認所有資源均能正常載入。

## 3. 配置自動化測試與瀏覽器自動反饋

將歷史數據（`.csv` / `.json`）和核心邏輯（`src/`）與畫面渲染解耦，按你的技術架構建立三層自動驗證：

1. **編譯／靜態檢查門檻（`< 1s`）。** 在 `AGENTS.md` 寫明每次修改後必跑的檢查命令（例如 Python 用 `python3 -m compileall -q . && uv run ruff check . && uv run mypy src/`；TypeScript/Vite 用 `npx tsc --noEmit && npm run build`；Godot/Unity 用無頭命令行檢查）。
2. **單元測試與集成測試（`Vitest` 或 `pytest`）。**
   - *前端／網頁遊戲：* `npm i -D vitest @playwright/test` → `npx vitest run`
   - *Python 後端／數據：* `uv add --dev pytest httpx` → `uv run pytest -q`
   同時測試**程式邏輯**（狀態流轉、接口格式、跨文件 ID 對齊）與**歷史證據邊界**（每條主張或人物卡是否具備有效的「據／推斷／設」標記、精確出處頁碼與年代防穿越規則；如有實時角色對話，可加入 LLM-as-a-Judge 日誌審計防止角色偏移）。
3. **自動運行的瀏覽器閉環（`@playwright/mcp` + `Playwright` E2E）。**
   - 安裝一次瀏覽器內核：`npx playwright install chromium`
   - 在 `opencode.json` 配置 `@playwright/mcp@latest`，讓 agent 自己讀取 DOM 尺寸裁切、控制台報錯、`404` 資源與截圖，不再靠人肉眼傳話。
   - 將關鍵操作寫成可重複執行的 `npx playwright test` 端到端測試，並針對**部署後的線上 `https://` 網址**同樣跑通冒煙測試。

## 4. 請兩位朋友實測，並將反饋轉化為防回歸測試

1. 把部署好的公開網址發給**至少兩位組外朋友**在他們自己的設備上試用或試玩。
2. 在 `docs/user-feedback.md`（或研究日誌）如實記錄他們的操作、困惑之處以及發現的錯誤或歷史偏移。
3. 針對他們提出的問題完成**至少兩處實質修復**，並**把每一處修復寫成永久的自動化測試**（單元、集成或 Playwright E2E），確保同類問題不再復發。

## 下週課堂現場展示（Bring to class）

請準備好在 **11 月 18 日（星期三）**課堂現場逐一演示：

1. **公開部署的線上網址**：現場打開你在 Cloudflare Pages（及 Worker）上的作品。
2. **Ideation 反饋閉環 + 你自己的專案示意圖**：展示你與 agent 真實的探討與規劃紀錄（`plan.md` 與 `/goal` 聲明），並展示 **agent 生成的你自己專案的 HTML、Excalidraw 或 Mermaid 示意圖**。
3. **現場運行你的自動化測試套件**：當場執行 `pytest` / `vitest` 與 `npx playwright test`，清楚說明**你測試了甚麼、覆蓋了哪幾層**（代碼邏輯與史料邊界）。
4. **自動運行的瀏覽器反饋閉環**：展示你的 `@playwright/mcp` 配置與 Playwright 瀏覽器自動檢查過程。
5. **外部用戶反饋 → 防回歸測試**：展示**兩位朋友的實測反饋**、你的代碼／設計修改，以及對應新增的測試用例。
6. **至少一個真實困難及其具體例子**：在部署、瀏覽器自動化或寫測試時踩到了甚麼坑，以及你如何排查或解決。

請保持儲存庫 `README.md` 更新（寫明一鍵運行與測試指令），定期提交有意義的 Git commit；切勿將 API 密鑰或大型二進制文件（放入 `artifacts/`）提交進 Git；未解決的問題記入 `questions.md`。
