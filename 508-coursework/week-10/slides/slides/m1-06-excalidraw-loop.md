---
minutes: 1.5
preload: false
fit: false
---

# Live demo: edit rooms on Excalidraw and inspect the `get_scene` JSON sent back.

<LazyDemo
  src="./demos/excalidraw-app/index.html?scene=round29"
  previewImg="./demos/vmocc-round29-rooms.svg"
  presets="320m Mountain Plan::./demos/excalidraw-app/index.html?scene=draft15|1989 Hillock ①–⑩::./demos/excalidraw-app/index.html?scene=round24|1987 Home + Lab::./demos/excalidraw-app/index.html?scene=round29|Blank Canvas::./demos/excalidraw-app/index.html?scene=blank"
  badge="LIVE EXCALIDRAW CANVAS · CO-DRAW WITH YOUR AGENT"
  title="Virtual Museum of Chinese Computing · Interactive Canvas"
  summary="Click Load to open Excalidraw inside this slide. Switch between the 320m plan and room layouts, drag boxes or sketch red marks (P), and click get_scene JSON (bottom right) to see what the agent reads back."
  height={555}
/>

<!--
我直接把完整的 Excalidraw 画板内嵌在这页课件里了。点一下 Load，既可以切到刚才那张最大的 320 米山体总图，也可以看 1987 年 3.5×3.8 米小家和中学微机室的家具平面。我在画板上直接拖一下房间位置、用画笔框出要改的地方，Agent 调一下 `get_scene` 就能把右下角这份精确到像素坐标的 JSON 读回去修改设计文档！
-->

::read::
Open the embedded Excalidraw editor to switch across *VMOCC* scenes, move or annotate rooms by hand, and inspect the live `get_scene` JSON coordinates returned to the agent.
