---
minutes: 1.5
---

# Deploy your project to Cloudflare Pages (+ Worker) in three steps this week.

<div class="body">
<div class="term">
<div class="term-bar"><span>Terminal · Cloudflare deploy commands</span></div>
<pre>
<span class="dim"># 1. Log in once (opens browser):</span>
<span class="blk">$ npx wrangler login</span>
&nbsp;
<span class="dim"># 2. Deploy static site / WebGL folder (dist/ or public/):</span>
<span class="blk">$ npx wrangler pages deploy dist --project-name=my-dh-project</span>
<span class="ok">🌎 Live: https://my-dh-project.pages.dev</span>
&nbsp;
<span class="dim"># 3. Optional: if calling an LLM API, deploy Worker + secret:</span>
<span class="blk">$ npx wrangler secret put OPENROUTER_API_KEY</span>
<span class="blk">$ npx wrangler deploy worker.js</span>
</pre>
<div class="term-foot">Or connect GitHub repo in dash.cloudflare.com → Workers &amp; Pages</div>
</div>
<div class="frame hot"><span class="label">Zero-card setup notes</span><div class="text">

- **Free forever** for static sites (`$0/mo`, global CDN, HTTPS)
- **Alternative:** in `dash.cloudflare.com` → **Workers &amp; Pages → Create → Connect to Git** (auto-deploys on every `git push`)
- **Unity / Godot WebGL:** export uncompressed or `.br` HTML5 folder into `dist/` and run Step 2

</div></div>
</div>

<!--
因为这周作业第一条就是要求大家先把项目 Deploy 上线，我专门用一页把 Cloudflare 部署的完整操作写清楚：只有三步！第一步 `npx wrangler login` 扫码登录你的免费 Cloudflare 账号；第二步 `npx wrangler pages deploy dist --project-name=你的项目名`，两秒钟就会吐出一个全球可访问的 `.pages.dev` 网址（如果你不想敲命令，去 Cloudflare 网页后台点 Connect to Git 绑上你的 GitHub 仓库也行，每次 push 自动部署）；第三步，只有当你的网页需要实时调大模型 API 时，才需要跑下面两行把密钥存进 Worker。
-->

::read::
Deploy to Cloudflare in minutes: run `npx wrangler login` and `npx wrangler pages deploy <folder> --project-name=<name>` (or connect your GitHub repository in `dash.cloudflare.com`), adding `wrangler secret put` only if your app calls a live LLM API.
