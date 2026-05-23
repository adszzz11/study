# Part 2. 생태계 — Obsidian의 공식 대응

> 사용자가 묻신 "Obsidian이 어떤 대책을 냈는지" — 가장 큰 사건은 **kepano/obsidian-skills**.

## 🏢 Obsidian의 공식 입장 (2026 정리)

| 결정 | 내용 | 시점 |
|------|------|------|
| ⭐ **Obsidian Skills 공개** | CEO **Steph Ango (kepano)** 본인이 직접 5종 Agent Skills 발표 | 2026.3 |
| ⭐ **Obsidian CLI 정식 출시** | 100+ 명령어, headless 자동화. AI 에이전트 친화 | 2026.2 |
| ⭐ **Bases 정식화** | 마크다운 메타를 DB 뷰로 — Skill로 LLM이 직접 조작 가능 | 2025-2026 |
| ⭐ **JSON Canvas 표준화** | LLM이 visual workspace 직접 생성 | 2025 |
| ⚠️ **공식 MCP server는 X** | 커뮤니티에 위임. 단 trademark 보호로 `mcp-obsidian` npm 패키지 rename 강제 | 2026.3 |
| ❌ **공식 RAG 플러그인 X** | "Skills로 충분" 입장 |

→ **Obsidian의 대답 = "MCP 만들기 ✗, Agent Skills 5종 공식 제공 ✅"**.

## 🛠️ kepano/obsidian-skills — 5종 디테일

```
https://github.com/kepano/obsidian-skills (13.9k★, MIT)
```

| Skill | 책임 | 결과 |
|-------|------|------|
| **obsidian-cli** | 터미널에서 vault 조작 | 노트 생성·검색·daily note·콘텐츠 추가 100+ 명령어 |
| **obsidian-bases** | 구조화 데이터 (typed property + filter + sort + view) | LLM이 자동으로 CRM 표, 스프린트 트래커, 리서치 DB 생성 |
| **json-canvas** | 비주얼 화이트보드 (노드·엣지·그룹·공간) | LLM이 다이어그램·마인드맵 직접 그림 |
| **defuddle** | 웹 콘텐츠 클린업 | 지저분한 HTML → 깨끗한 마크다운 (raw/ 투입용) |
| **obsidian-markdown** | Obsidian 마크다운 스펙 (wikilink, callout 등) | LLM이 vault에 native하게 작성 |

### "Skills"의 의미

Claude Skills 스펙 (Anthropic, 2025) 기반. CEO가 직접 만들었다는 게 메시지:
> "Agent Skills가 productivity tool의 통합 표준이다 — 우리가 먼저 한다."

## 🔌 Obsidian CLI (가장 중요한 1대 변화)

```bash
# 설치
brew install obsidian-cli

# 노트 생성
obsidian note create "회의록 2026-05-23" --vault leetangle

# 검색
obsidian search "LLM Wiki" --vault leetangle --json

# Daily note
obsidian daily --vault leetangle

# 파일 추가/append
echo "추가 내용" | obsidian note append "회의록.md"

# 100+ 명령어
obsidian --help
```

**효과**: LLM 에이전트가 GUI 없이도 vault 풀 조작. Karpathy 패턴에서 LLM이 wiki/를 직접 쓰는 게 가능해짐.

## 🆚 커뮤니티 구현 비교

LLM Wiki를 Obsidian에 박는 구현이 5일 안에 15개 이상 등장. 주요 4개:

| 구현 | 형태 | ★ | 특징 |
|------|------|------|------|
| **kepano/obsidian-skills** ⭐ | 공식 Skills 5종 | 13.9k | Obsidian CEO 발. 사실상 표준 |
| **2233admin/obsidian-llm-wiki** | MCP + CLI | 1k+ | 6-persona MCP team. "Cites, doesn't guess" |
| **ar9av/obsidian-wiki** | Framework | 신생 | Karpathy 패턴 충실 재현 |
| **karpathywiki** (community plugin) | Obsidian 플러그인 | 신생 | GUI 내 패턴 통합 |

## 🌐 MCP server 상황 (공식 X)

PulseMCP에 **Obsidian 관련 MCP 66개** 등록되어 있지만 의미 있는 것 ~8개:

| MCP server | 특징 |
|------------|------|
| `marcelmarais/obsidian-mcp-server` | 가장 인기 |
| `MarkusPfundstein/mcp-obsidian` | Local REST API 플러그인 사용 |
| `cyanheads/obsidian-mcp-server` | 노트·태그·frontmatter surgical edit |
| `@bitbonsai/mcpvault` | (구 mcp-obsidian, trademark로 rename) |

**선택 팁**: kepano/obsidian-skills + Obsidian CLI 조합이면 MCP 없이도 99% 케이스 커버. MCP는 Claude Code 등에서 "도구 호출" 형태가 필요할 때.

## 🌍 다른 도구 카테고리와의 관계

```
[LLM Wiki 패턴]  ←─ Karpathy
       │
       ├─► Obsidian Skills (공식, CEO 발)
       ├─► Notion AI / Reflect (벤더 클라우드)
       ├─► Logseq, RemNote (block-based 대안)
       └─► Khoj, Reor (검색 우선)

[같은 카테고리지만 다른 접근]
   ├─ Smart Connections (semantic search 우선)
   ├─ Copilot (chat + RAG)
   ├─ AnythingLLM (워크스페이스 RAG)
   └─ Mem0 / Letta (대화 메모리)
```

## 🔥 2026 Q2 동향

1. **kepano가 직접 만든 게 시그널**: "AI 통합은 플러그인이 아니라 Skill이 표준" 메시지
2. **MCP 공식화 거부**: "Skills + CLI로 충분" — vendor가 MCP 안 만드는 첫 사례
3. **Bases가 Karpathy wiki의 index.md를 대체**: 동적 데이터베이스로 진화
4. **JSON Canvas로 wiki의 시각적 레이어 추가**: 텍스트 wiki + 비주얼 다이어그램
5. **Web Clipper + defuddle 결합**: 웹 → 깔끔한 raw/ 자동 투입 파이프라인 완성

## 🎯 사용자 결정 가이드

| 의도 | 추천 |
|------|------|
| Karpathy 패턴 원본대로 | gist + 본인 vault + `/wiki` skill |
| Obsidian 공식 + 최대 통합 | **kepano/obsidian-skills** |
| Claude Code에서 도구로 vault 조작 | obsidian-skills + 커뮤니티 MCP 1개 |
| 기존 vault에 빠르게 얹기 | `/wiki init` (본 환경에 설치된 skill) |

## 🔗 다음

→ 공식·튜토리얼 → [03-references.md](03-references.md)
