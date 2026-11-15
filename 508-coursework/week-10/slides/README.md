# DHG508 · Session Ten (Week 10)

**Autonomous `/goal`, Feedback Loops, and Deployment.**

Built with [DAIHUM Reslides](https://github.com/boan-anbo/reslides) (`theme: exhibit`, OpenCode `.term` windows, `.json` viewer, `.tree` viewer, `<LazyDemo>` on-demand WebGL/Canvas embeds, `<DataTable>`, `<Tabs>`, `<Box>`, and line-stepped code blocks).

- **Read on phone or laptop (zero install):** open `read/index.html` in any browser
- **Present locally with Reslides:**
  ```bash
  # Point RESLIDES at your local clone of https://github.com/boan-anbo/reslides
  RESLIDES=/path/to/reslides npm run dev
  ```
  Opens <http://localhost:3100/> (presenter mode with speaker notes and timer at <http://localhost:3100/#/presenter/>).
- **Validate syntax, citations, figures, and timing:** `RESLIDES=/path/to/reslides npm run check`
- **Build static deck + reading edition:** `RESLIDES=/path/to/reslides npm run build` → `dist/` and `dist/read/`

## Structure (64 slides · 70 minutes)

1. **Autonomous `/goal` & Planning (`s01`–`s04`)**: OpenCode PR `#59437` `/goal` architecture (`idle` hook + internal reviewer), writing concrete `/goal` statements, locking `docs/plan.md` in `Plan` mode (`Tab`) to prevent goal drift, and the two-phase feedback loop map.
2. **Phase 01 · Ideation Loop Before Code (`m1-01`–`m1-07`)**: Verbal restatement + open questions in `Plan` mode, rendered Mermaid state machines (*Bashan*), agent-drawn Excalidraw floor plans & sections (*Virtual Museum of Chinese Computing*, `mcp-excalidraw-server` / `mcp.excalidraw.com`), live embedded Excalidraw canvas, and self-contained HTML architecture schematics (`nicobailon/visual-explainer`).
3. **Phase 02A · Agent ↔ Agent Coordination (`m2-01`–`m2-06`)**: Built-in OpenCode subagents (`.opencode/agents/researcher.md`), **MCP Agent Mail** (`Dicklesworthstone/mcp_agent_mail_rust`), and **agentchattr** (`bcurts/agentchattr`), while keeping `design-document.md` and `data/bashan-evidence.csv` in Git as the permanent source of truth.
4. **Phase 02B · Browser & Compile Feedback (`m3-01`–`m3-10`)**: `@playwright/mcp` two-step setup, exploratory browser observation vs. repeatable Playwright browser tests, and `0.15s` Python static gates (`compileall` + `ruff` + `mypy` + `pytest`).
5. **Phase 02C · Three-Tier Automated Testing (`m4-01`–`m4-13b`)**: 60-second `Vitest` / `pytest` + `Playwright` setup, decoupling logic from UI, Unit + Integration + Playwright E2E walked step by step on *Bashan* (plus LLM-as-a-Judge semantic drift rubric and interactive bug-injection workbench).
6. **Phase 03 · Deployment & Pre-Computing (`m5-01`–`m5-13`)**: Three-step Cloudflare Pages (+ Worker) deployment, hiding API keys behind a 20-line Worker, when to rent a VPS, **Standard Stripe vs. Lemon Squeezy vs. Stripe Managed Payments** (Merchant of Record), pre-computing static `float16` embeddings for a **comparative mythology database**, and 2026 cost benchmarks.
7. **Phase 04 · Final Two Weeks & Week 10→11 Deliverables (`m6-01`–`m6-06`)**: End-to-end upgrade bar, this week's deployment & testing setup, and next week's live showcase of all four feedback loops (`../instructions.md`).
