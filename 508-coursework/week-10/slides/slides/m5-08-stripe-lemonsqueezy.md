---
minutes: 1.5
class: compact
---

# Compare standard Stripe, Lemon Squeezy, and Stripe Managed Payments.

| Option | Legal seller (MoR) | Company & global tax burden | Typical fee |
|---|---|---|---|
| **Standard Stripe** | **You** (requires eligible business / HK or US entity) | You remain legally responsible for global VAT/GST registration & filings (Stripe Tax only calculates) | `~2.9% + $0.30` |
| **Lemon Squeezy** | **Lemon Squeezy** (acts as Merchant of Record) | **Handled for you**: individuals can sell globally; platform collects & remits taxes and takes a cut | `5% + $0.50` |
| **Stripe Managed Payments** | **Stripe's MoR entity** (built after acquiring Lemon Squeezy) | **Handled inside Stripe**: native Merchant-of-Record compliance, global tax remittance & fraud liability | `~6.4% + $0.30` |

<!--
大家把这张对比表记住，以后自己做独立产品绝对用得上：传统的 Stripe 只管帮你刷信用卡（手续费低，约 2.9%），但法律上的收款主体（Merchant of Record）还是你自己，你得自己搞定公司资质和全球报税；后来火起来的 Lemon Squeezy 走的是代理经销模式（MoR），它替你当收款主体，把税务、发票、合规全包了，从里面抽 5% 佣金，个人开发者拿身份证就能卖全球！而且 Stripe 收购 Lemon Squeezy 之后，现在 Stripe 自己里面也推出了原生的 Stripe Managed Payments，同样帮你包办收款主体和税务。
-->

::read::
Standard Stripe processes cards while leaving you as the legal seller; **Lemon Squeezy** and **Stripe Managed Payments** act as the **Merchant of Record (MoR)**, handling global taxes and compliance for solo creators in exchange for a slightly higher commission.
