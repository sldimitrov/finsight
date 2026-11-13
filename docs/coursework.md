# Coursework — requirements summary & working outline

Original brief: `курсова работа_2026.docx`. This file is a working summary; the actual
coursework text is written by me.

## Brief (summary)
- General theme: *„Разработване и изследване на програмни решения"* — I pick a concrete
  problem and an individual topic.
- Result may be a program, algorithm, model, simulation, experiment, comparison or analysis;
  a finished application is not mandatory. Any programming language.
- Structure:
  1. **Увод** — problem, goal, tasks.
  2. **Основна част** — approaches, algorithms, tools, implementation, experiments/analysis.
  3. **Заключение** — results and conclusions.
  4. **Използвани източници** — literature, docs, libraries.
- Illustrations recommended: flowcharts/diagrams, screenshots, essential code fragments,
  tables/charts with results, input/output examples, experiment results.
- Code submitted separately; only essential fragments go in the text.
- Length: 6–12 standard pages (1800 chars/page), can be more.
- Graded on: quality & complexity, **independence**, creativity & effort, implementation /
  analysis quality, clear results & conclusions, structure & layout. May need a defence.

## Working outline (to fill in gradually)
- [ ] Topic title (BG):
- [ ] Problem & goal — see `problem-definition.md`
- [ ] Tasks (numbered list)
- [ ] Architecture — `high-level-system-architecture.md`
- [ ] Data model — `entity-relationship-diagram.md`
- [ ] Key algorithms / decisions to explain (candidates: balance updates & atomic transfers,
      financial overview aggregations, data isolation)
- [ ] Experiment / analysis idea (candidate: ORM query performance — N+1 vs
      `select_related`, stored vs computed balance, measured with `assertNumQueries` / timing
      on 1 000–10 000 rows)
- [ ] Testing approach & results
- [ ] Screenshots
- [ ] Conclusion
- [ ] Sources (Django docs, PostgreSQL docs, …)
