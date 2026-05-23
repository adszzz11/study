# 4-3. Obsidian Skills 5종 통합

> 사용자가 물으신 "Obsidian의 대책" — 핵심은 이거.

## 🏢 Steph Ango (kepano)의 결정

```
2026.3  Obsidian CEO가 직접 5종 Agent Skills 발표
        → 메시지: "AI 통합은 플러그인이 아니라 Skill이 표준"
        → MCP server는 만들지 않는다 (커뮤니티 위임)
        → Skills + CLI + Bases + JSON Canvas로 충분하다는 입장
```

리포: https://github.com/kepano/obsidian-skills (13.9k★, MIT)

## 📦 5종 Skills

### 1. `obsidian-cli`

```bash
# 설치
brew install obsidian-cli

# 또는 npm
npm install -g @obsidianmd/cli
```

핵심 명령어 (100+ 중 자주 쓰는 것):
```bash
# Vault 조작
obsidian vault list
obsidian vault open leetangle

# 노트
obsidian note create "회의록 2026-05-23" --folder activity --template meeting
obsidian note read "study/tech/ai/llm-wiki-study/README.md" --json
obsidian note append "log.md" --content "오늘 ingest 완료"
obsidian note rename "old.md" "new.md"

# 검색 (LLM에게 가장 유용)
obsidian search "LLM Wiki" --vault leetangle --json | jq '.results[]'
obsidian search-content "compounding" --max 10

# Daily note
obsidian daily --vault leetangle

# Tag 관리
obsidian tag list --vault leetangle
obsidian tag rename "ai" "artificial-intelligence"

# Backlinks
obsidian backlinks "concepts/llm-wiki-pattern.md"

# Graph 데이터
obsidian graph export --vault leetangle --format json > graph.json
```

**LLM에서 활용**:
```bash
# Claude Code에서
"obsidian search-content 'multi-agent' 해서 결과 3개 가져와줘"
# → LLM이 자동으로 CLI 호출
```

### 2. `obsidian-bases`

Bases = 마크다운 frontmatter를 **데이터베이스**처럼.

```yaml
# bases/wiki-pages.base
---
filters:
  - and:
      - file.folder.contains("study/wiki/concepts")
      - file.tag.contains("active")
views:
  - type: table
    columns: [file.name, source_count, date]
    sort: -date
  - type: cards
    group: tags
```

→ Bases가 wiki/index.md를 **동적으로 대체**. LLM이 frontmatter만 갱신하면 view 자동 갱신.

**Skill 활용**:
LLM에게 "스프린트 트래커 Base 만들어줘" → 자동으로 `.base` 파일 생성 + 필터 + 뷰 설정.

### 3. `json-canvas`

JSON Canvas (Obsidian 공동 후원 표준) = 시각 화이트보드.

```json
{
  "nodes": [
    {"id": "1", "type": "text", "x": 0, "y": 0, "text": "LLM Wiki"},
    {"id": "2", "type": "file", "x": 200, "y": 0, "file": "concepts/compounding-knowledge.md"}
  ],
  "edges": [
    {"id": "e1", "fromNode": "1", "toNode": "2"}
  ]
}
```

LLM이 이걸 직접 작성 → Obsidian Canvas로 시각화. 마인드맵·시스템 다이어그램 자동 생성.

### 4. `defuddle`

웹 → 깨끗한 마크다운.

```bash
# 단독
defuddle https://aaronfulkerson.com/...karpathys-pattern/ > raw/aaron-fulkerson.md

# Obsidian Web Clipper와 결합
# → 브라우저에서 클립 → defuddle 자동 정리 → raw/ 투입
```

`raw/` 파이프라인의 **입구**. 지저분한 HTML/JS 페이지를 LLM ingest 가능한 형태로 정제.

### 5. `obsidian-markdown`

Obsidian 마크다운 스펙을 LLM이 정확히 따르게:
- `[[wikilink]]` 형식
- `[[wikilink|alias]]`
- `![[embed]]`
- `> [!note] Callout` 등 callout 종류
- `^block-id` 블록 참조
- frontmatter YAML 컨벤션

LLM이 wiki/ 페이지 작성 시 vault 그래프와 자연스럽게 통합.

## 🛠️ Claude Code에서 설치

```bash
# kepano/obsidian-skills 클론
git clone https://github.com/kepano/obsidian-skills ~/.claude/skills/obsidian

# 또는 plugin이 있으면 marketplace에서
```

`~/.claude/skills/obsidian/SKILL.md` 위치에 따라 Skill 디스커버리.

설치 후 Claude Code 안에서:
```
/obsidian-cli search "LLM Wiki"
/obsidian-bases create "회의록 추적용 Base"
/json-canvas create "LLM Wiki 아키텍처 다이어그램"
/defuddle https://example.com/article
```

## 🔀 LLM Wiki 패턴 + obsidian-skills 결합

```
1. raw/ 입력 → defuddle (웹 클립 자동 정리)
                 ↓
2. /wiki ingest → LLM이 wiki/ 페이지 생성·갱신
                 ↓
3. obsidian-cli search → 다른 LLM 호출에서 wiki 활용
                 ↓
4. obsidian-bases → index.md 대체, 동적 뷰
                 ↓
5. json-canvas → wiki 페이지 간 관계 시각화
                 ↓
6. /wiki lint → 정기 점검
```

전체가 하나의 파이프라인.

## ✅ 체크포인트

- [ ] obsidian-cli 설치 + `obsidian search` 동작
- [ ] kepano/obsidian-skills clone + SKILL.md 인식
- [ ] Base 1개 생성 → wiki/index.md 대체 시도
- [ ] JSON Canvas로 본 study 자료 관계도 1개 그리기
- [ ] defuddle로 웹 글 1개 raw/ 투입

## ⚠️ 함정

| 함정 | 대응 |
|------|------|
| Obsidian CLI 권한 누락 | macOS Security & Privacy에 obsidian-cli 추가 |
| Bases 파일 수동 작성 어려움 | Skill에게 자연어로 요청 → 생성 |
| JSON Canvas 좌표 깨짐 | LLM에 "그리드 100단위" 같은 명시 |
| defuddle이 일부 페이지 실패 | --fallback 옵션, 또는 ReadabilityJS 대안 |
| Skills 충돌 | 기존 `/wiki` skill과 obsidian-skills의 명령어 겹침 — 별칭 사용 |

## 🔗 다음

→ Obsidian CLI + 커뮤니티 MCP → [04-mcp-and-cli.md](04-mcp-and-cli.md)
