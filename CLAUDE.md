# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a personal Obsidian vault containing study notes, documentation, and presentations in Korean markdown format.

## Key Directories

- **study/**: Technical study notes (Java, HTTP, Spring, ELK, QA, Jenkins)
- **conference/**: Conference and meetup notes
- **book/**: Book reviews and reading notes
- **marp/**: Marp presentations with supporting images
- **templates/**: Obsidian note templates (see `templates/README.md`)
- **conventions/**: Development conventions including git commit standards

Daily notes use `YYYY-MM-DD.md` naming format.

## Working with Notes

- All content is in Korean markdown
- Use Obsidian wiki-link syntax `[[link]]` for internal references
- Files use descriptive Korean names

## Git Commit Convention

**Format:** `<gitmoji> [type/#issue] <Korean description>`

**Allowed Gitmoji (only use these):**

| Emoji | Code | Purpose |
|-------|------|---------|
| ✨ | `:sparkles:` | New feature/content |
| 🐛 | `:bug:` | Bug fix/typo correction |
| ♻️ | `:recycle:` | Refactoring/reorganization |
| 🔥 | `:fire:` | Remove code/files |
| 📦 | `:package:` | Dependency updates |
| 🎨 | `:art:` | Code style improvements |
| ✅ | `:white_check_mark:` | Tests |
| 📝 | `:memo:` | Documentation (most common for this repo) |
| 🚀 | `:rocket:` | Deploy |
| 🚧 | `:construction:` | Work in progress |
| 🔧 | `:wrench:` | Configuration changes |
| ⬆️ | `:arrow_up:` | Version upgrade |
| ⬇️ | `:arrow_down:` | Version downgrade |

**Examples:**
- `📝 [docs] HTTP 캐시 전략 노트 추가`
- `✨ [feature] ELK 스택 학습 자료 작성`
- `🐛 [fix] JVM GC 노트 오타 수정`

See `conventions/github convention/` for complete guidelines.

## Auto-commit System

An automated commit system runs periodic commits with timestamp-based messages (see `auto-commit/autoCommit_shell.md`). Manual commits should use the Gitmoji convention above.

## Development Notes

- No build/test/lint commands - this is a pure documentation repository
- When creating conference notes, use the template in `templates/컨퍼런스-노트-템플릿.md`