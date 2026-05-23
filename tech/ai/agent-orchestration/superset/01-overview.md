---
date: 2026-03-29
tags:
  - tech
  - superset
  - overview
parent: "[[README]]"
---

# Superset - 개요

> [[README|목차로 돌아가기]]

---

## 1. What - Superset란?

> **한 줄 정의**: 10+ 에이전트를 병렬 실행하고 IDE와 원클릭 연동하는 에이전트 시대의 IDE (8k+ stars)

### 핵심 개념

Superset은 "AI 에이전트 시대의 IDE"를 표방하는 데스크톱 앱으로, 모든 CLI 기반 코딩 에이전트를 10개 이상 동시 실행할 수 있다. 각 에이전트는 독립 git worktree에서 격리되며, 결과를 내장 diff 뷰어로 확인한 후 VS Code, Cursor, Xcode, JetBrains 등에서 원클릭으로 열 수 있다. "터미널에서 돌아가면 Superset에서 돌아간다"가 핵심 철학.

### 지원 에이전트

| 에이전트 | 상태 |
|----------|------|
| **Claude Code** | Fully supported |
| **Codex** (OpenAI) | Fully supported |
| **Gemini CLI** | Fully supported |
| **Cursor Agent** | Fully supported |
| **GitHub Copilot** | Fully supported |
| **OpenCode** | Fully supported |
| **Pi** | Fully supported |
| 기타 CLI 도구 | 터미널에서 실행 가능하면 OK |

> API 키를 프록시하지 않음 — 직접 프로바이더에 연결

### Claude Code 고유기능 보존

네이티브 터미널에서 `claude` CLI를 그대로 실행하므로:

- **OAuth**: ✅ (직접 인증, 프록시 없음)
- **CLAUDE.md**: ✅ (worktree에서 자동 읽기)
- **Skills/Hooks**: ✅ (풀 CLI 경험)
- **MCP 서버**: ✅ (MCP 직접 연동 + Superset MCP 서버도 제공)

### 동작 방식

```
Superset (데스크톱 앱)
├── Workspace 1: Claude Code (worktree-1)
│   └── [Open in VS Code] [Open in Cursor]
├── Workspace 2: Codex (worktree-2)
│   └── [Open in JetBrains]
├── Workspace 3: Gemini CLI (worktree-3)
│   └── [Open in Xcode]
│
├── 내장 diff 뷰어: 변경사항 인라인 편집
├── 내장 브라우저: 서비스 프리뷰
├── 포트 포워딩: workspace별 포트 관리
└── Workspace Presets: .superset/config.json으로 환경 자동화
```

---

## 2. 핵심 특징

### 장점

- **IDE 연동**: VS Code, Cursor, Xcode, JetBrains 원클릭 오픈
- **범용성**: 모든 CLI 에이전트 지원, API 프록시 없음
- **Workspace Presets**: `.superset/config.json`으로 환경 설정 자동화
- **내장 diff 뷰어**: 변경사항 확인 + 인라인 편집
- **내장 브라우저**: 서비스 프리뷰 (포트 포워딩 포함)
- **세션 지속**: 노트북 닫아도 세션 유지
- **커뮤니티**: 8k+ GitHub stars (오케스트레이터 중 최다)
- **YC 백킹**: superset-sh

### 단점

- **macOS 전용** (현재): Windows/Linux "coming soon"
- **Elastic License 2.0**: 완전한 OSS가 아님 (호스팅 서비스 제공 불가)
- **비용 추적 없음**: Agent Deck 대비
- **Best-of-N 없음**: Emdash 대비
- **Electron 기반**: 네이티브 대비 리소스 사용

---

## 3. 설치

```bash
# macOS (Apple Silicon + Intel)
# superset.sh에서 DMG 다운로드

# 소스 빌드 (Bun 1.0+ 필요)
git clone https://github.com/superset-sh/superset
cd superset && bun install && bun run build
```

요구사항: Git 2.20+, GitHub CLI (`gh`)

---

## 4. 개발 현황

| 항목 | 값 |
|------|-----|
| 버전 | v1.4.4 (2026-03-27) |
| Stars | ~8,120 |
| 라이선스 | Elastic License 2.0 |
| 언어 | TypeScript (Electron, React, TailwindCSS) |
| 핵심 팀 | Kitenite (1,249), saddlepaddle (440), AviPeltz (237) |
| 생성일 | 2025-10-21 |

---

## References

- [공식 사이트](https://superset.sh)
- [GitHub](https://github.com/superset-sh/superset)
- [공식 문서](https://docs.superset.sh)
