---
minutes: 1
---

# Rent a VPS only when your project needs persistent databases or heavy compute.

<div class="body">
<div class="frame"><span class="label">What is a Virtual Machine (VPS)?</span><div class="text">

- a rented Linux slice running 24/7 with its own IP, disk, and RAM (**Hetzner**, **DigitalOcean**, **AWS Lightsail** · `~$4.50–$6/mo`)
- you SSH in, run **Caddy / Nginx**, and keep Python (`uvicorn`) or Node running under `systemd` or Docker

</div></div>
<div class="frame hot"><span class="label">When you actually need one</span><div class="text">

- multi-user persistent database writes (**PostgreSQL / SQLite**)
- heavy Python libraries (`scipy`, `spacy`, custom C extensions) that exceed Worker CPU limits
- stateful multiplayer WebSocket rooms

</div></div>
</div>

<!--
如果有的同学项目特别重，Worker 塞不下怎么办？那就认识一下什么是虚拟机（VM / VPS）：比如在 Hetzner 或 DigitalOcean 花每个月四五美金租一台 2 核 4G 的小 Linux 服务器，24 小时开机，你可以 SSH 上去跑 FastAPI、跑 SQLite/Postgres 数据库、挂反向代理。只有当你需要持久化写数据库或跑重型 Python 库时才需要上虚拟机。
-->

::read::
A Virtual Private Server (VPS, `~$5/month` on Hetzner or DigitalOcean) provides a 24/7 Linux machine for stateful databases, heavy Python libraries, or multiplayer WebSockets when Workers are not enough.
