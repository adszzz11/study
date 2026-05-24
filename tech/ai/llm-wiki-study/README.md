# LLM Wiki 심층 스터디

> "Obsidian is the IDE, the LLM is the programmer, the wiki is the codebase." — Andrej Karpathy (2026.4.2)

## 한 줄 정의

**LLM Wiki**는 Andrej Karpathy가 2026년 4월 제안한 **자가 유지 지식 베이스 패턴**. raw/(원본) → wiki/(LLM 작성) → CLAUDE.md(스키마) 3-layer로 구성되며, **새 문서를 넣을 때마다 wiki가 더 똑똑해지는 compounding** 구조가 핵심이다.

## 3줄 요약

1. **3-Layer 아키텍처**: raw/(불변 원본), wiki/(LLM이 작성·갱신하는 마크다운 페이지), CLAUDE.md(LLM 운영 매뉴얼).
2. **RAG와의 차이**: 매번 검색 ✗ → **새 문서마다 wiki 통합** → 비용 ↓·정확도 ↑·교차 참조 자동.
3. **Obsidian의 공식 대응**: CEO Steph Ango가 2026.3 **kepano/obsidian-skills** 공개 (13.9k★) — obsidian-cli·bases·json-canvas·defuddle 5종 공식 Skill로 LLM 통합 가속.

## 핵심 키워드

`#llm-wiki` `#karpathy` `#second-brain` `#obsidian` `#obsidian-skills` `#kepano` `#claude-skills` `#mcp` `#beyond-rag` `#compounding-knowledge` `#wikilinks`

## ⚡ Quick Start (본 vault에서 5분)

```bash
# 본 vault에 LLM Wiki 구조 추가 (이미 설치된 skill 사용)
/wiki init

# 원본 1개 ingest
cp ~/Downloads/my-paper.pdf raw/
/wiki ingest raw/my-paper.pdf

# 질문
/wiki query "이 논문의 핵심 주장과 본 vault의 X 노트와의 관계"

# 건강 검진
/wiki lint
```

> 본 환경(`~/.claude/skills/llm-wiki/`)에 `/wiki` skill이 이미 설치돼 있음. 본 vault에서 즉시 시작 가능.

## 📑 전체 목차

| 파일 | 내용 |
|------|------|
| [01-overview.md](01-overview.md) | Karpathy 패턴 — 3-layer 아키텍처, compounding 개념 |
| [02-ecosystem.md](02-ecosystem.md) | **Obsidian의 공식 대응 (Skills 5종)** + 커뮤니티 구현 비교 |
| [03-references.md](03-references.md) | Karpathy gist · Obsidian Skills · 튜토리얼 |
| [04-learning/01-bootstrap-vault.md](04-learning/01-bootstrap-vault.md) | 본 vault에 raw/, wiki/, CLAUDE.md 셋업 |
| [04-learning/02-ingest-query-lint.md](04-learning/02-ingest-query-lint.md) | 3대 연산 깊이 |
| [04-learning/03-obsidian-skills.md](04-learning/03-obsidian-skills.md) | obsidian-skills 5종 + Bases + JSON Canvas 통합 |
| [04-learning/04-mcp-and-cli.md](04-learning/04-mcp-and-cli.md) | Obsidian CLI + 커뮤니티 MCP server 연결 |
| [05-projects.md](05-projects.md) | 본 vault에 적용하는 실전 시나리오 |
| [cheatsheet.md](cheatsheet.md) | `/wiki` 명령어 + 디렉터리 컨벤션 |

## 🗓️ 학습 플랜

| Day | 목표 |
|-----|------|
| 1 | 01-overview + 02-ecosystem 정독 → 패턴 이해 + Obsidian의 공식 입장 파악 |
| 2 | Quick Start로 본 vault에 `/wiki init` 실행 + 첫 ingest |
| 3 | 04-learning/02 — ingest/query/lint 3대 연산 익숙해지기 |
| 4 | 04-learning/03 — kepano/obsidian-skills 설치 + Bases·Canvas 통합 |
| 5 | 04-learning/04 — Obsidian CLI + MCP server 연결로 Claude Code에서 직접 vault 조작 |
| 6+ | 실전 시나리오 (05-projects) — 본 study 자료를 LLM Wiki로 컴파운딩 |

## 🎯 본 vault에 이걸 적용하면

| 비포 | 애프터 |
|------|-------|
| `study/tech/ai/*/` 100+ 노트 흩어져 있음 | wiki/concepts/ 통합 — 자동 cross-ref |
| 새 자료 추가 시 수동 wikilink | LLM이 자동으로 모든 관련 페이지 갱신 |
| RAG로 매번 검색 | wiki가 미리 통합된 답 보유 |
| 모순/누락 인지 못함 | `/wiki lint`로 정기 점검 |
| 한 번 본 자료 잊음 | log.md에 영구 기록 + 새 자료가 옛 결론 갱신 |
