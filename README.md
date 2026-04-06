# PSYCH QBANK

UWorld-style банк вопросов по психиатрии. Board-level.

## Структура

- `data/pretest/` — 304 спарсенных вопроса из PreTest Psychiatry 14th Ed
- `data/generated/` — оригинальные UWorld-style вопросы с детальными объяснениями
- `data/topics.json` — карта тем для генерации (seed data из 5 учебников)
- `src/app.jsx` — React UI (standalone, persistent storage)
- `scripts/` — валидация и статистика

## Использование с Claude Code

```bash
cd psych-qbank
claude
# > прочитай CLAUDE.md, потом сгенерируй 15 вопросов по наркологии
```

## Валидация

```bash
python scripts/validate.py
python scripts/stats.py
```

## Источники

- PreTest Psychiatry Self-Assessment 14th Ed (Klamen, 2015)
- Stahl's Case Studies Vol 1-2 (Stahl, 2011/2016)
- First Aid for Psychiatry Clerkship 6th Ed (Kaufman, 2021)
- MGH Psychiatry Update & Board Prep 4th Ed (Stern, 2017)
- DSM-5-TR, Maudsley 15th Ed, CANMAT/APA/NICE Guidelines
