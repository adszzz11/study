---
date: 2026-03-29
updated: 2026-05-23
tags:
  - tech
  - superset
  - agent-orchestration
  - overview
parent: "[[README]]"
---

# Superset - 개요

> [[README|목차로 돌아가기]] | [[02-ecosystem|다음: 생태계]]

---

## 1. What - Superset란?

> **한 줄 정의**: 10+ CLI 코딩 에이전트를 격리된 git worktree에서 병렬 실행하고 IDE와 원클릭 연동하는 에이전트 시대의 데스크톱 IDE (11k+ stars)

### 핵심 개념

Superset은 "AI 에이전트 시대의 IDE"를 표방하는 macOS 데스크톱 앱이다. 모든 CLI 기반 코딩 에이전트를 10개 이상 동시 실행할 수 있고, 각 에이전트는 독립 git worktree에서 격리된다. 결과는 내장 diff 뷰어로 확인한 뒤 VS Code, Cursor, Xcode, JetBrains 등에서 원클릭으로 열 수 있다. "터미널에서 돌아가면 Superset에서 돌아간다"가 핵심 철학이며, API 키를 프록시하지 않고 각 에이전트가 직접 프로바이더에 연결한다.

### 주요 용어

| 용어 | 설명 |
|------|------|
| **Workspace** | 하나의 에이전트 세션 = 하나의 git worktree에서 격리 실행되는 작업 단위 |
| **Workspace Preset** | `.superset/config.json`에 저장하는 환경 자동화 설정 (포트, 명령어 등) |
| **Diff Viewer** | 내장 변경사항 뷰어 — 인라인 편집 가능 |
| **Superset MCP** | Superset이 자체 제공하는 MCP 서버 (외부 에이전트가 워크스페이스 제어 가능) |

### 동작 방식

```
Superset (데스크톱 앱)
│
├── Workspace 1: Claude Code (worktree-1)
│   └── [Open in VS Code] [Open in Cursor]
├── Workspace 2: Codex CLI (worktree-2)
│   └── [Open in JetBrains]
├── Workspace 3: Gemini CLI (worktree-3)
│   └── [Open in Xcode]
│
├── 내장 diff 뷰어: 변경사항 인라인 편집
├── 내장 브라우저: 서비스 프리뷰 (포트 포워딩)
├── Workspace Presets: .superset/config.json
└── Superset MCP 서버: 외부 에이전트가 워크스페이스 제어
```

### 지원 에이전트 (2026-05 기준 8종)

| 에이전트 | 상태 |
|----------|------|
| **Claude Code** | Fully supported |
| **OpenAI Codex CLI** | Fully supported |
| **Gemini CLI** | Fully supported |
| **Cursor Agent** | Fully supported |
| **GitHub Copilot** | Fully supported |
| **OpenCode** | Fully supported |
| **Amp Code** | Fully supported (2026-04 추가) |
| **Pi** | Fully supported |
| 기타 CLI 도구 | 터미널에서 실행 가능하면 OK |

> API 키 프록시 없음 — 직접 프로바이더에 연결

### Claude Code 고유 기능 보존

네이티브 터미널에서 `claude` CLI를 그대로 실행하므로 다음이 모두 유지된다:

- **OAuth**: 직접 인증, 프록시 없음
- **CLAUDE.md**: worktree에서 자동 읽기
- **Skills / Hooks**: 풀 CLI 경험
- **MCP 서버**: MCP 직접 연동 + Superset 자체 MCP 서버도 제공

---

## 2. Why - 왜 Superset인가?

### 해결하려는 문제

- **다중 에이전트 컨텍스트 충돌** — 한 머신에서 Claude/Codex/Gemini를 동시에 돌릴 때 디렉토리·파일 충돌
- **에이전트 결과 비교의 비용** — 누가 더 잘 짰는지 보려면 별도 클론/스크립트가 필요
- **IDE 연동 단절** — CLI 에이전트 결과물을 IDE에서 열어 검토하는 흐름이 끊김
- **세션 단절** — 노트북을 닫거나 터미널을 종료하면 진행 상황 손실

### 기존 방식의 한계

| 문제 | 기존 방식 | Superset |
|------|----------|----------|
| 다중 에이전트 격리 | tmux + 수동 worktree | workspace = worktree 자동 격리 |
| 결과 비교 | 개별 git diff | 내장 diff 뷰어 + 인라인 편집 |
| IDE 연동 | 수동 `code .` | 원클릭 (VS Code/Cursor/Xcode/JetBrains) |
| 세션 유지 | screen / tmux 학습 곡선 | 앱 차원에서 자동 유지 |
| 환경 자동화 | shell 스크립트 | `.superset/config.json` preset |

---

## 3. 핵심 특징

### 장점

- **IDE 원클릭 오픈**: VS Code, Cursor, Xcode, JetBrains
- **범용성**: 모든 CLI 에이전트 지원, API 프록시 없음
- **Workspace Presets**: `.superset/config.json` 환경 자동화
- **내장 diff 뷰어**: 변경 확인 + 인라인 편집
- **내장 브라우저**: 서비스 프리뷰 + 포트 포워딩
- **세션 지속**: 앱 차원의 자동 유지
- **커뮤니티 모멘텀**: 11k+ stars, 두 달 만에 8.1k → 11k
- **YC 백킹**: superset-sh

### 단점

- **macOS 정식 지원만**: Windows/Linux 빌드는 "untested" 상태
- **Elastic License 2.0**: 완전한 OSS 아님 — 호스팅 서비스 제공 불가
- **비용 추적 없음**: Agent Deck 등 대비 약점
- **Best-of-N 없음**: Emdash 등 대비 약점
- **Electron 기반**: 네이티브 대비 리소스 사용량 큼

---

## 4. 사용 사례

### 적합한 경우

| 사용 사례 | 설명 |
|----------|------|
| 다중 에이전트 비교 실험 | Claude / Codex / Gemini에 동일 문제를 던져 결과 비교 |
| 병렬 PR/이슈 작업 | 여러 작업을 각 worktree에서 동시 진행 |
| 다중 프로젝트 클라이언트 워크 | 프로젝트별 workspace + preset으로 환경 자동화 |
| 에이전트 결과의 IDE 검토 | CLI 자동화 → IDE 원클릭 오픈으로 사람이 마무리 |

### 적합하지 않은 경우

- Windows/Linux 전용 환경 (현재 untested)
- 호스팅형 SaaS 형태로 제공해야 하는 시나리오 (ELv2 제약)
- 토큰/비용 추적이 필수적인 엔터프라이즈 운영

---

## 5. 가격 정책

| 항목 | 가격 | 비고 |
|------|------|------|
| 데스크톱 앱 | 무료 | Elastic License 2.0 |
| 호스팅 SaaS | 제공 안 함 | ELv2 라이선스 제약 |

> 각 에이전트의 API 비용은 사용자가 프로바이더에 직접 결제 (Superset은 프록시하지 않음)

---

## 6. 개발 현황

| 항목 | 값 |
|------|-----|
| 최신 버전 | **desktop-v1.11.1** (2026-05-22) |
| Stars | **~11k** (2026-05-23) |
| 라이선스 | Elastic License 2.0 |
| 언어 | TypeScript 94.9% |
| 주요 스택 | Electron, React, TailwindCSS, **Bun**, **Turborepo**, **Vite**, **Biome**, **Drizzle ORM**, **Neon**, **tRPC** |
| 핵심 팀 | Kitenite, saddlepaddle, AviPeltz |
| 생성일 | 2025-10-21 |
| 백킹 | YC (superset-sh) |

> **2026-03 → 2026-05 변화**: v1.4.4 → v1.11.1 (약 두 달 만에 7 마이너 릴리즈), 8.1k → 11k stars, Amp Code 지원 추가

---

## 다음 단계

> [!tip] 다음으로
> Superset의 전체 그림을 파악했다면 [[02-ecosystem|에이전트 오케스트레이터 생태계 비교]]에서 Agent Deck / Emdash / cmux 등 대안과의 위치를 살펴보세요.

---

## References

- [공식 사이트](https://superset.sh)
- [GitHub](https://github.com/superset-sh/superset)
- [공식 문서](https://docs.superset.sh)
- 관련 노트: [[02-ecosystem]] · [[03-quickstart]]
