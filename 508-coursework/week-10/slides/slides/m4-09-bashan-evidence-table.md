---
minutes: 1
---

# Integration starts from the shared Bashan evidence table.

<DataTable from="data/bashan-evidence.csv" labels="Claim | Evidence | Locator | Level | Limit" mark="0" caption="data/bashan-evidence.csv — single source of truth across research, game JSON, and paper" />

<!--
用 reslides 的 DataTable 组件直接读取我们仓库里的 data/bashan-evidence.csv。大家看这三行：托宾讲宏观工具需要制度前提（据，pp. 152, 157-158）；财政官员询问冬季信贷与物价（推断，Weber 2021 p. 195 / 项怀诚自述）；Talbot 和程在巫山船头相遇（设，bashan-anchor）。我们的集成测试就要保证游戏运行时真能跟这张表严丝合缝对上。
-->

::read::
`data/bashan-evidence.csv` serves as the shared contract across research notes, game JSON records, and the paper; integration tests verify every cross-file reference against this table.
