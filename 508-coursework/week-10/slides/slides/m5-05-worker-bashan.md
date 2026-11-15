---
minutes: 1.5
---

# Twenty lines of Worker code proxy Bashan's live NPC chat safely.

```javascript {1-5|7-15|17-20}
// worker.js — Deploy with: npx wrangler deploy
export default {
  async fetch(req, env) {
    if (req.method !== "POST") return new Response("Method Not Allowed", { status: 405 })
    const { npcId, message } = await req.json()

    const upstream = await fetch("https://openrouter.ai/api/v1/chat/completions", {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${env.OPENROUTER_API_KEY}`, // Stored via: wrangler secret put
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        model: "deepseek/deepseek-chat",
        messages: [{ role: "system", content: loadNpcPrompt(npcId) }, { role: "user", content: message.slice(0, 400) }],
      }),
    })
    return new Response(upstream.body, { headers: { "Content-Type": "application/json" } })
  }
}
```

<!--
大家看一个真实的 Cloudflare Worker 有多短——就二十行 JS！密钥通过 wrangler secret put OPENROUTER_API_KEY 存进云端加密环境变量，代码里用 env.OPENROUTER_API_KEY 读取；顺手把用户输入 slice(0, 400) 截断防止恶意刷超长文本。免费额度每天十万次请求，我们课程作业和作品集完全免费。
-->

::read::
A 20-line Cloudflare Worker reads `env.OPENROUTER_API_KEY` from encrypted edge secrets, caps prompt length, forwards NPC chat to OpenRouter, and runs within Cloudflare's free 100,000-requests/day tier.
