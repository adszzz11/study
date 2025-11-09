# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a personal knowledge management repository containing study notes, documentation, and presentations organized in markdown format. It uses Obsidian as the primary note-taking tool.

## Repository Structure

- **study/**: Technical study notes organized by topic
  - `Java/`: JVM, GC, and Java-related documentation
  - `HTTP/`: Network protocols, HTTP headers, caching, cookies
  - `Spring/`: Spring framework notes
  - `ELK/`: Elasticsearch, Logstash, Kibana stack documentation
  - `QA/`: Quality assurance and testing documentation
  - `jenkins/`: CI/CD pipeline documentation

- **marp/**: Presentation files created with Marp (Markdown Presentation Ecosystem)
  - Contains markdown presentations and supporting images
  - Example: "Backend 개발자가 보는 AI - 우리는 어떻게 적응하고 있는가?.md"

- **conference/**: Conference and meetup notes taken during attendance
  - Contains technical talks and presentations from various tech events
  - Examples: AWS Network Service, Prometheus Operator, 인프런 퇴근길 밋업, etc.

- **book/**: Book reviews and reading notes
  - Organized by book title with individual concept notes
  - Examples: "UX_UI의 10가지 심리학 법칙", "오브젝트"

- **conventions/**: Development conventions and standards
  - `github convention/`: Git commit message conventions using gitmoji
  - Commit format: `✨ [feature/#42] 기능 설명`

- **side-project/**: Personal project documentation
  - `idea_bank/`: Project ideas and planning documents

- **auto-commit/**: Automation scripts for repository management
  - Contains shell scripts for automated commits

- **templates/**: Obsidian note templates
  - `컨퍼런스-노트-템플릿.md`: Template for conference and meetup notes
  - See `templates/README.md` for usage guide

- **글쓰기/**: Writing and content creation materials
- **업무/**: Work-related documentation
- **인터뷰/**: Interview preparation materials
- **.obsidian/**: Obsidian vault configuration
- **.claude/**: Claude Code configuration and context

- **Daily Notes**: Files with `YYYY-MM-DD.md` format (e.g., `2025-10-05.md`) for daily journaling

## Obsidian Configuration

This repository is configured as an Obsidian vault with the following enabled features:
- Daily notes and templates
- Graph view and backlinks
- Canvas for visual note organization
- Slides plugin for presentations
- File explorer and search capabilities

## Working with Notes

- All documentation is in Korean markdown format
- Files use descriptive Korean names following the subject matter
- The repository follows a topic-based organization structure
- Notes may contain cross-references and backlinks typical of Obsidian usage
- Obsidian wiki-link style `[[]]` is used for internal linking

## Git Commit Convention

This repository uses **Gitmoji** for commit messages to improve readability and consistency.

**Format:** `<emoji> [type/#issue] <description>`

**Common Gitmoji:**
- ✨ `:sparkles:` - New feature (feat)
- 🐛 `:bug:` - Bug fix (fix)
- 📝 `:memo:` - Documentation (docs)
- ♻️ `:recycle:` - Refactoring (refactor)
- 🎨 `:art:` - Code style improvements
- ✅ `:white_check_mark:` - Tests
- 🔧 `:wrench:` - Configuration changes
- 📦 `:package:` - Package/dependency updates

**Example:** `✨ [feature/#42] 로그인 API 기능 추가`

See `conventions/github convention/` for detailed guidelines.

## Development Notes

- No build/test/lint commands are required as this is a documentation repository
- Content is primarily markdown files with supporting images
- Git is used for version control with standard markdown file tracking