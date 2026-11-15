---
minutes: 1.5
---

# Ideation 3 · The agent draws a full spatial plan onto Excalidraw automatically.

<div class="body">
<div class="frame fit wide"><span class="label">Agent-drawn Excalidraw canvas · Virtual Museum of Chinese Computing (Draft 15)</span><div class="pic"><Figure id="vmocc-draft15" /></div></div>
<div class="frame hot"><span class="label">Agent draws; you co-edit</span><div class="text">

- **Not drawn by hand:** the agent calls `create_from_svg` / `batch_create_elements` to draw this entire `320 m` mountain plan + `1m = 1.8px` section automatically
- **Instant spatial check:** contour lines, buried vs. open halls, and USSR / Japan / US link wings

</div></div>
</div>

<!--
大家看左边这张大图——这是我这周正在做的《中国计算机虚拟博物馆》（Virtual Museum of Chinese Computing）第十五稿总平面和纵剖面图。重点来了：**这张图不是我手画的，是 Agent 通过 Excalidraw MCP 自动画在画布上的！** 你跟它讨论完构想，让它直接把 320 米依山爬坡的展厅等高线平面、苏联/日本/美国侧翼连廊、以及右侧 1米=1.8像素的纵剖面直接画出来。哪些展厅埋在山体里、哪些露在地面、比例对不对，它一画出来你一眼就能看清！
-->

::read::
With `mcp-excalidraw-server`, the agent programmatically generates complex floor plans and elevation sections—such as this 320-meter *Virtual Museum of Chinese Computing* layout—directly onto a shared canvas for human review.
