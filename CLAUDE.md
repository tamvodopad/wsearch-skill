# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

WSearch is a Claude Code skill for searching WW2 soldiers from **warsearch.ru** by location and exporting results to Excel. It automates genealogical research by collecting data about Great Patriotic War participants from a specific village/town.

The skill is invoked via `/wsearch` command or natural language requests about finding WW2 participants.

## Critical Lessons Learned

### 1. Site is VERY slow!

**warsearch.ru is extremely slow.** Always use extended timeouts:

| Operation | Minimum wait time |
|-----------|-------------------|
| Page load | 10-15 sec |
| Search results | 15-30 sec |
| Card on pamyat-naroda.ru | 10-15 sec |
| Between queries | 5 sec |

### 2. Same-name villages problem!

**CRITICAL:** Many villages have the same name in different districts!

Example: "Вишур" exists in:
- Кизнерский район (target)
- Шарканский район
- Можгинский район
- Нылгинский район
- etc.

**Solution:** Always search "Village + District" (e.g., "Вишур Кизнерский"), not just village name!

### 3. Browser context resets on navigation

When navigating to new URLs, `window.*` variables are lost.

**Solution:** For mass processing (>10 records), use Python/requests instead of browser automation.

### 4. Status extraction heuristics

Status can be determined from pamyat-naroda.ru URL type:
- `plen` → Prisoner of war
- `vpp` → Missing in action
- `donesenie` → Killed/Missing
- `card_ran` → Wounded
- `podvig` → Awarded (likely survived)

### 5. Excel clickable links

Use `cell.hyperlink` + `cell.style = "Hyperlink"` for clickable links:
```python
link_cell.hyperlink = url
link_cell.value = "Ссылка"
link_cell.style = "Hyperlink"
```

## Architecture

Two execution modes (automatic fallback):

1. **Chrome available** → Use browser automation (mcp__claude-in-chrome__*) for warsearch.ru
2. **Chrome NOT available** → Run `python3 wsearch.py` (Playwright script)

Check Chrome availability first with `mcp__claude-in-chrome__tabs_context_mcp`.

### Key Files

- `SKILL.md` - Skill definition with workflow instructions
- `create_excel.py` - Excel export utility
- `wsearch.py` - Standalone Playwright-based search script
- `enrich_status.py` - Python script for status enrichment via requests
- `make_final_excel.py` - Final Excel generator with statuses and colors

### Data Flow

```
User question → 5 parameter questions →
Search "Village + District" on warsearch.ru →
Set 500 items per page → Parse all pages →
Geographic filtering (exclude other districts) →
Verification (A/B/C levels) →
Status enrichment (Python/requests) →
Excel export with clickable links and color coding
```

### Excel Output Structure

- **Итог** - Confirmed records with statuses and color coding
- **Кандидаты** - Candidates requiring manual review
- **Статистика** - Status summary
- **Варианты** - Used spelling variants

## Dependencies

```bash
pip3 install openpyxl playwright requests
```

## Verification Levels

- **A** - Village + district in birth place (100% confidence)
- **B** - Village in birth place + district in draft place (high confidence)
- **C** - Village only, no district (needs verification → goes to Candidates)

## Status Colors in Excel

| Status | Color |
|--------|-------|
| Погиб | 🔴 Red |
| Умер от ран | 🔴 Light red |
| Пропал без вести | 🟡 Yellow |
| Плен | 🟠 Orange |
| Ранен | 🔵 Light blue |
| Награждён | 🟢 Green |
| Вернулся | 🟢 Light green |
| Неизвестен | ⬜ Gray |

## Language

All user-facing text, comments, and documentation are in Russian.
