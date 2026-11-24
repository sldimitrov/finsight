# Coursework — requirements summary & writing plan

Original brief: `курсова работа_2026.docx`. Draft: `КурсоваРабота.DOCX` (my text).

## Brief (summary)
- General theme: *„Разработване и изследване на програмни решения"* — individual topic,
  covering both **development** and **research**.
- Structure: Увод → Основна част → Заключение → Използвани източници.
- Illustrations: diagrams, screenshots, essential code fragments, tables/charts, I/O examples,
  experiment results. Code is submitted separately.
- Length: 6–12 standard pages, 1 page = **1,800 characters** → target **≥ 10,800 chars of text**
  (aim ~12,600 ≈ 7 pages for a buffer). Figures and tables barely add to the count.
- Graded on: quality & complexity, **independence**, creativity, implementation/analysis,
  clear results & conclusions, structure & layout. May need a defence.

## Status
| Date | Characters | ≈ Pages |
|------|-----------:|--------:|
| 2026-11-19 | 1,984 | 1.1 |

## Section plan

| # | Section | Target chars | What to add | Figures / tables / code |
|---|---------|-------------:|-------------|--------------------------|
| 0 | **Увод** (new heading; "Проблем" moves here) | ~1,300 | Problem, goal, **4–6 numbered tasks**, one paragraph on the work's structure | — |
| 1 | **Анализ** | ~2,000 | Target users and usage scenario; functional requirements per MVP module; non-functional (20–100 users, 1k–10k rows, consistency, data isolation) | Table 1: requirements per module + status. Fig 1: use-case diagram (`use-case-diagram.md`) |
| 2 | **Дизайн** | ~2,800 | Each technology choice **with the alternative and the reason** (monolith vs microservices, PostgreSQL vs SQLite/NoSQL, SSR vs SPA); data model, each entity and relation; account types; transaction type → balance effect; decisions: immutable transactions (why + deferred full ledger), `PROTECT` on accounts, stored vs computed balance, `Decimal` for money | Fig 2: architecture (`high-level-system-architecture.md`). Fig 3: ERD (`entity-relationship-diagram.md`). Table 2: account types. Table 3: transaction types |
| 3 | **Имплементация** | ~3,000 | Apps and responsibilities; MTV request flow traced through one example (create transaction); key algorithms: balance update in `transaction.atomic`, data isolation, immutability in `save()`; filtering and overview queries once built | Fig 4: project tree. Fig 5: balance-update flowchart (`algorithm-flowchart.md`). 3–4 short code fragments. 2–3 screenshots |
| 4 | **Тестване и изследване** | ~2,500 | Test strategy + results. **Experiment:** method (seed command, 1k / 5k / 10k rows), metrics (query count, time), cases (N+1 vs `select_related`; stored vs `aggregate` balance; overview queries), interpretation | Table 4: tests. Table 5 + Fig 6: experiment results chart |
| 5 | **Заключение** | ~800 | Answer each task from the Introduction; limitations; future work (transfers, budgets, full ledger, imports) | — |
| 6 | **Източници** | — | Specific Django doc pages (DB optimisation, testing, transactions), PostgreSQL, Chart.js, anything else actually used | — |

**Writing order:** 0–2 now → 3 alongside code Phases 0–1 → 4 after Phase 2 (overview + experiment).

## Draft review checklist (2026-11-19)
- [ ] Add **Увод** heading and the **tasks (задачи)**; give the work an individual title, not the general theme.
- [ ] "MVP (most-valuable-product)" → **minimum viable product**.
- [ ] "подобна на MCP" → **MVC**.
- [ ] "1000-1000 транзакции" → 1000–10000.
- [ ] Typos: "платнирани", "олеснява".
- [ ] Distinguish financial transactions from DB transactions (`transaction.atomic`).
- [ ] Immutability decision: add *why* and the alternatives considered.
- [ ] Number and caption every figure/table and refer to them in the text ("фиг. 1").
- [ ] Conclusion: "CRUD is complete" is no longer accurate (edit removed); report against the tasks instead.
- [ ] English terms (services, FE app, server-rendering-UI): Bulgarian equivalent or one-time explanation.
