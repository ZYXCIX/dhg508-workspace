---
minutes: 1
---

# Never expose an API key in browser code—put a Cloudflare Worker in front.

<div class="frame fit"><span class="label">Frontend key leak vs. Cloudflare Pages + Worker proxy</span><div class="pic"><Figure id="diag-cloudflare-worker" /></div></div>

<!--
部署的时候有一条绝对红线，看这张图就懂了：上面红框是新手最常踩的坑——把 OpenRouter 或 DeepSeek 的 API Key 写进前端 JS 里，别人按一下 F12 打开网络面板就能把你的 Key 拷走，一晚上刷光两百美金！下面绿框是标准免费做法：静态网页放 Cloudflare Pages，中间放一个二十行的 Cloudflare Worker 代理，真正的 API Key 加密锁在 Cloudflare 云端后台！
-->

::read::
Never ship an LLM API key inside browser JavaScript; host static assets on Cloudflare Pages and route `/api/chat` through a free 20-line Cloudflare Worker holding `env.OPENROUTER_API_KEY`.
