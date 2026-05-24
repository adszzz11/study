# LLM Wiki Cheat Sheet

## 🚀 본 환경에 이미 설치된 /wiki Skill

```bash
/wiki init                          # 본 vault에 raw/, wiki/, CLAUDE.md 셋업
/wiki ingest <source>                # 원본 1개를 wiki에 통합
/wiki query <question>               # wiki에 질의
/wiki lint                           # 모순·고아·누락 점검
```

위치: `~/.claude/skills/llm-wiki/SKILL.md`

## 📂 표준 디렉터리 구조

```
vault/
├── raw/                       # 불변 원본 (LLM read-only)
│   ├── assets/
│   ├── articles/
│   └── papers/
├── study/wiki/                # LLM이 작성·갱신
│   ├── concepts/              # 개념 페이지
│   ├── entities/              # 사람·프로젝트·도구
│   ├── comparisons/           # 비교
│   ├── canvas/                # JSON Canvas
│   ├── index.md               # 카탈로그
│   └── log.md                 # 작업 이력
└── CLAUDE.md                  # LLM 운영 매뉴얼 (스키마)
```

## 📝 wiki 페이지 frontmatter

```yaml
---
tags: [llm-wiki, concept, category]
date: 2026-05-23
source_count: 3
maintained_by: llm-wiki
last_ingested: 2026-05-23
---
```

## 📓 log.md 한 줄 형식

```markdown
## [2026-05-23] ingest | karpathy-llm-wiki-gist.md → +5 -2 pages
## [2026-05-23] lint | 0 contradictions, 4 orphans
## [2026-05-23] query | "RAG vs LLM Wiki" → comparisons/rag-vs-llm-wiki.md
```

## 🛠️ Obsidian CLI

```bash
# 설치
brew install obsidian-cli

# Vault
obsidian vault list
obsidian vault add /Users/sm/code/leetangle/Note --alias leetangle

# 검색
obsidian search "키워드" --vault leetangle --json
obsidian search-content "본문 키워드" --max 10

# 노트
obsidian note create "path/to/note.md" --content "..."
obsidian note read "path.md" --json
obsidian note append "path.md" --content "..."
obsidian note rename "old.md" "new.md"

# Daily
obsidian daily --vault leetangle
obsidian daily --path-only

# 백링크 / 그래프
obsidian backlinks "path.md"
obsidian graph export --vault leetangle --format json

# Tag
obsidian tag list
obsidian tag rename "ai" "artificial-intelligence"
```

## 🔌 Obsidian Skills (kepano/obsidian-skills)

```bash
# 설치
git clone https://github.com/kepano/obsidian-skills ~/.claude/skills/obsidian
```

5종:
- `obsidian-cli` — CLI 명령 자동화
- `obsidian-bases` — DB views
- `json-canvas` — 비주얼 화이트보드
- `defuddle` — 웹 → 깨끗한 마크다운
- `obsidian-markdown` — Obsidian 마크다운 스펙

## 🌐 MCP server (선택)

### marcelmarais/obsidian-mcp-server
```json
{
  "mcpServers": {
    "obsidian": {
      "command": "npx",
      "args": ["-y", "marcelmarais/obsidian-mcp-server"],
      "env": {"OBSIDIAN_VAULT_PATH": "/Users/sm/code/leetangle/Note"}
    }
  }
}
```

## 🧹 Lint 항목

| 항목 | 의미 |
|------|------|
| Contradiction | 두 페이지가 같은 사실을 다르게 |
| Stale | 새 자료가 옛 주장 뒤집음 |
| Orphan | 인바운드 wikilink 0 |
| Missing concept | 자주 언급되는데 페이지 없음 |
| Missing cross-ref | 언급만 하고 [[link]] 없음 |
| Data gap | TODO / 확인 필요 표시 |

## 💰 비용 가이드 (Claude Opus 4.7)

| 작업 | 토큰 | 비용 |
|------|------|------|
| 짧은 글 ingest | 5K/3K | $0.30 |
| 논문 (20p) ingest | 30K/8K | $1.10 |
| 책 chapter ingest | 60K/15K | $2.20 |
| query (간단) | 3K/1K | $0.08 |
| query (복잡 합성) | 10K/3K | $0.30 |
| lint (전체 vault) | 50K/5K | $1.10 |

→ 권장 월 한도: $10-30

## ⚡ 자주 쓰는 패턴

### 새 자료 빠르게 ingest
```bash
# 웹 글
defuddle https://example.com/article > raw/articles/$(date +%Y-%m-%d)-example.md
/wiki ingest raw/articles/2026-05-23-example.md

# PDF
cp ~/Downloads/paper.pdf raw/papers/
/wiki ingest raw/papers/paper.pdf

# 트위터 thread
twitter-to-md https://x.com/user/status/123 > raw/twitter/2026-05-23-thread.md
/wiki ingest raw/twitter/2026-05-23-thread.md
```

### 일일 루틴
```bash
# 아침
obsidian daily --vault leetangle    # 데일리 노트 열기

# 작업
/wiki ingest raw/...                # 새 자료 1-2개 통합

# 저녁
/wiki lint --since 24h              # 오늘 변경된 페이지만 점검
```

### 주간 루틴
```bash
# 일요일 23:00 (cron)
/wiki lint                          # 전체 점검
obsidian graph export > graph-$(date +%Y-W%V).json   # 그래프 스냅샷
```

## 🛡️ 안전 장치

### Git pre-commit hook (raw/ 보호)
```bash
# .git/hooks/pre-commit
#!/bin/bash
if git diff --cached --name-only | grep -E '^raw/' > /dev/null; then
  echo "WARNING: raw/ 변경 감지. 본인이 의도한 것인가?"
  read -p "계속? (y/N) " -n 1 -r
  [[ $REPLY =~ ^[Yy]$ ]] || exit 1
fi
```

### CLAUDE.md 필수 항목
- `raw/`는 read-only
- wiki link는 `[[한국어 OK]]`
- frontmatter 필수
- 500단어 이내 요약
- 모순은 flag (자동 삭제 ✗)

## 🔗 빠른 링크

- Karpathy gist: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
- kepano/obsidian-skills: https://github.com/kepano/obsidian-skills
- Obsidian CLI 공식: https://help.obsidian.md/Plugins/Obsidian+CLI
- 본 study: `study/tech/ai/llm-wiki-study/`
- 인접: [[study/tech/ai/autoresearch-study]] · [[study/tech/ai/multi-agent-platforms]]
