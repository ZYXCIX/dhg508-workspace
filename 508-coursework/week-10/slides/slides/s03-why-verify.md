---
layout: compare
kicker: The bottleneck
minutes: 1
steps: false
left:
  title: Manual eyeballing (now)
  items:
    - Agent edits five files blindly
    - You refresh, walk the ship for three minutes, spot a crash
    - You paste a vague complaint back into chat
right:
  title: Closed feedback loop
  items:
    - Agent runs compiler, unit tests, and headless browser itself
    - Agent sees exact line numbers, console errors, and screenshots
    - You inspect only when all checks pass
verdict: Never act as a human copy-paste bridge for errors a machine can read directly.
---

# Without a feedback loop, you are the agent's only pair of eyes.

<!--
大家前几周做项目最痛苦的地方是什么？就是每次让 OpenCode 改完代码，你得自己切到浏览器刷新、走三分钟走到船头、点开对话，发现崩了或者字超框了，再切回去跟它说“坏了”。这就叫没有 feedback loop——你成了它的肉眼传感器。一旦建立闭环，agent 改完自己跑检查、自己看报错和截图、自己修好，绿灯了再交给你审。
-->

::read::
When an agent cannot observe its own output, the student becomes a slow manual sensor. Giving the agent direct build, browser, and test feedback lets it iterate and fix regressions before human review.
