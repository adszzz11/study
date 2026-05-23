---
date: 2026-03-28
tags:
  - tech
  - conductor
  - overview
parent: "[[README]]"
---

# Conductor - 개요

> [[README|목차로 돌아가기]] | [[02-ecosystem|다음: 생태계]]

---

## 1. What - Conductor란?

> **한 줄 정의**: Claude Code + Codex를 병렬 실행하고 시각적 대시보드로 관리하는 macOS 네이티브 앱

### 핵심 개념

Conductor는 Melty Labs(Y Combinator S24)가 개발한 macOS 전용 앱으로, **Claude Code와 Codex** 에이전트를 동시에 실행하면서 각각을 독립된 git worktree에서 격리한다. 하나의 대시보드에서 모든 에이전트의 상태를 모니터링하고, 결과물을 리뷰/머지할 수 있다. `.context` 디렉토리를 통해 에이전트 간 컨텍스트 공유도 가능하다.

### 주요 용어

| 용어 | 설명 |
|------|------|
| Workspace | 개별 에이전트 세션 (하나의 작업 단위, git worktree 격리) |
| Worktree | git worktree로 격리된 작업 디렉토리 |
| Dashboard | 모든 에이전트 상태를 한눈에 보는 GUI |
| Checkpoint | 자동 스냅샷 — 롤백 가능 |
| Spotlight Testing | worktree 변경사항을 메인 repo에 동기화하여 테스트 |
| `.context` 디렉토리 | 에이전트 간 파일 기반 컨텍스트 공유 (gitignored) |

### 지원 에이전트

| 에이전트 | 지원 시점 | 비고 |
|----------|----------|------|
| **Claude Code** | v0.1.0 (2025-07) | 기본 에이전트, OAuth/API 키 모두 지원 |
| **Codex** (OpenAI) | v0.18.0 (2025-10) | GPT-5.3-Codex 지원 (v0.34.0~), checkpointing, skills, plan mode |

> Gemini CLI, Aider 등은 아직 미지원. 공식 FAQ에서 "Want to see something else? Email us"로 확대 의지 표명.

### 프로바이더 유연성

Claude Code를 다양한 프로바이더를 통해 실행 가능:
- OpenRouter, AWS Bedrock, Google Vertex AI, Vercel AI Gateway, Azure AI Foundry, GLM

### 동작 방식

```
사용자 → Conductor 앱 → 작업 할당 (Cmd+N)
                         ├── Workspace 1 (worktree-1) → Claude Code (Opus 4.6)
                         ├── Workspace 2 (worktree-2) → Codex (GPT-5.3)
                         ├── Workspace 3 (worktree-3) → Claude Code (Sonnet)
                         │         ↑ .context 디렉토리로 컨텍스트 공유
                         ↓
                    Diff 리뷰 (GitHub 코멘트 연동) → 메인 브랜치 머지
```

---

## 2. Why - 왜 Conductor인가?

### 해결하려는 문제

- 에이전트 세션 하나로는 처리량에 한계
- 여러 터미널에서 수동으로 에이전트 관리하면 혼란
- 에이전트 간 코드 충돌 위험
- Claude vs Codex 결과를 비교하고 싶을 때

### 기존 방식의 한계

| 문제 | 기존 방식 | Conductor |
|------|----------|-----------|
| 병렬 실행 | 터미널 탭 수동 관리 | 대시보드에서 원클릭 실행 |
| 코드 충돌 | 같은 브랜치에서 작업 | git worktree 자동 격리 |
| 상태 파악 | 각 터미널 직접 확인 | 통합 대시보드 + GitHub 상태 |
| 결과 머지 | 수동 git merge | GUI에서 diff 리뷰 & 머지 |
| 모델 비교 | 별도 환경 세팅 | 같은 프롬프트를 Claude+Codex에 동시 전달 |
| 롤백 | git reset 수동 | Checkpoint로 원클릭 롤백 |

---

## 3. 핵심 특징

### 장점

- **시각적 UX**: GUI 대시보드로 에이전트 상태 한눈에 파악
- **git worktree 격리**: 에이전트 간 충돌 원천 차단
- **멀티 모델**: Claude Code + Codex를 같은 프롬프트로 비교 가능
- **Checkpoint**: 자동 스냅샷 + 롤백 (Claude, Codex 모두)
- **GitHub 통합**: diff 코멘트 양방향 동기화, GitHub Actions 로그 직접 확인
- **`.context` 공유**: 에이전트 간 파일 기반 컨텍스트 공유
- **프로바이더 유연성**: OpenRouter, Bedrock, Vertex 등 다양한 프로바이더 지원
- **MCP 지원**: Model Context Protocol 통합
- **YC 백킹**: Melty Labs (YC S24), Linear/Vercel/Notion/Stripe가 사용

### 단점

- **macOS 전용**: Linux/Windows 미지원 (개발 중이나 시기 불명)
- **2종 에이전트만**: Claude Code + Codex만 지원 (Gemini CLI, Aider 등 미지원)
- **폐쇄 소스**: 오픈소스가 아님 — 커스터마이즈 제한
- **GitHub 권한 이슈**: 출시 초기 과도한 GitHub 권한 요청으로 논란 (이후 개선)

---

## 4. 사용 사례

### 적합한 경우

| 사용 사례 | 설명 |
|----------|------|
| 대규모 리팩토링 | 모듈별로 에이전트 분배하여 병렬 작업 |
| 멀티 피처 개발 | 여러 기능을 동시에 각각의 에이전트가 구현 |
| Claude vs Codex 비교 | 같은 작업을 두 모델에 줘서 결과 비교 |
| 코드 리뷰 자동화 | diff 리뷰 + GitHub 코멘트 연동 |
| 마이그레이션 작업 | 파일/모듈 단위로 분할하여 병렬 마이그레이션 |

---

## 5. 가격 정책

| 플랜 | 가격 | 특징 |
|------|------|------|
| **현재 무료** | $0 | 전체 기능 사용 가능 |

> 향후 "팀 협업 기능에 대해 유료 전환 계획" — 현재는 시드 투자금으로 무료 제공
>
> ⚠️ AI 에이전트 자체 비용(Claude API/구독, OpenAI API 등)은 별도 발생

---

## 6. 주요 버전 이력

| 버전 | 날짜 | 주요 변경 |
|------|------|----------|
| v0.1.0 | 2025-07-24 | 최초 공개 릴리스 |
| v0.18.0 | 2025-10-31 | **Codex 에이전트 지원 추가** |
| v0.28.0 | 2025-12-22 | Workspace 도입, `.context` 디렉토리 |
| v0.29.0 | 2026-01-07 | Diff 코멘트 + GitHub 양방향 동기화 |
| v0.34.0 | 2026-02-05 | Opus 4.6 + GPT-5.3-Codex, deeplinks |
| v0.43.0 | 2026-03-20 | Codex skills/plan mode/fast mode |
| v0.44.0 | 2026-03-24 | 사이드바 리뉴얼, Codex checkpointing, `/add-dir` |

---

## 다음 단계

> [!tip] 다음으로
> Conductor의 개요를 이해했다면 [[02-ecosystem|생태계와 대안 도구 비교]]를 살펴보세요.

---

## References

- [공식 사이트](https://www.conductor.build/)
- [공식 문서](https://docs.conductor.build)
- [체인지로그](https://www.conductor.build/changelog)
- [프로바이더 가이드](https://docs.conductor.build/guides/providers)
- [The New Stack 리뷰](https://thenewstack.io/a-hands-on-review-of-conductor-an-ai-parallel-runner-app/)
- [Y Combinator 프로필](https://www.ycombinator.com/companies/conductor)
