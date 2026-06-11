---
date: 2026-06-07
tags:
  - tech
  - ai
  - codex
  - agent-harness
  - reliability
  - lazy-codex
  - omo
status: published
type: tech-tool-study
---

# Lazy Codex — 종합 스터디 (tool-study)

> **한 줄**: 코딩 에이전트의 **게으름/거짓 완료** 문제(lazy codex 현상)와, 그걸 **검증 루프 하니스**로 극복하는 `lazycodex`/OmO를 정의부터 실습·비교까지 한 번에. hermes(내 인프라)와의 접점도 정리.

## ⚠️ "lazy codex" = 현상 + 도구
1. **현상**: Codex가 지시 무시·중도 포기·**거짓 완료** → 01-overview §1
2. **도구**: `code-yeongyu/lazycodex` (현상을 극복하는 하니스) → 본 스터디 전반 + 기존 [[lazycodex]]

## 학습 경로

| 순서 | 파일 | 무엇 |
|------|------|------|
| 1 | [[lazy-codex/01-overview\|01. Overview]] | 현상(What/Why) + lazycodex 정체성·핵심 특징 |
| 2 | [[lazy-codex/02-ecosystem\|02. Ecosystem]] | 코딩 하니스 landscape 비교 (Codex/Claude Code/Cursor/Devin/Aider/OmO/**hermes**) |
| 3 | [[lazy-codex/03-references\|03. References]] | 공식 문서·소스·벤치마크 |
| 4 | [[lazy-codex/04-learning/01-getting-started\|04-1. 시작하기]] | 설치·첫 실행·완화 프롬프트 |
| 5 | [[lazy-codex/04-learning/02-verified-completion\|04-2. 검증 완료]] | Oracle/Ralph/Hashline 동작 + 게이트 깨보기 |
| 6 | [[lazy-codex/05-projects\|05. Projects]] | PoC·hermes 통합 아이디어 |
| 7 | [[lazy-codex/cheatsheet\|cheatsheet]] | 명령·프롬프트·완화 빠른 참조 |

## 파일 구조
```
lazy-codex/
├── README.md            ← 개요 + 학습 경로(여기)
├── 01-overview.md       ← What/Why/핵심 특징
├── 02-ecosystem.md      ← 관련 기술·비교
├── 03-references.md     ← 공식 문서·학습 자료
├── 04-learning/
│   ├── 01-getting-started.md
│   └── 02-verified-completion.md
├── 05-projects.md       ← 실전·통합
└── cheatsheet.md        ← 빠른 참조
```

## 30초 핵심
- **문제**: agent가 "안 한 일을 했다고 보고"(false completion) → 위임 신뢰 붕괴. 정직성 문제.
- **3층 방어**: 모델(honesty RL+`phase`) · 프롬프트(persistence, preamble 제거) · **하니스(실행≠검증 루프)**.
- **하니스**: OmO/lazycodex(Oracle·Ralph·Hashline) / hermes(self-test 게이트+PR 사람-머지).

## 관련 노트
- [[lazycodex]] · [[lazycodex-poc]] (기존 도구/런북 노트) · [[codex]] · [[multi-agent-platforms]] · [[autoresearch-study]]
