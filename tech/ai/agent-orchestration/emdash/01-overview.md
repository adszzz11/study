---
date: 2026-03-29
tags:
  - tech
  - emdash
  - overview
parent: "[[README]]"
---

# Emdash - 개요

> [[README|목차로 돌아가기]]

---

## 1. What - Emdash란?

> **한 줄 정의**: 23종 AI 에이전트를 지원하고 Best-of-N 비교가 가능한 오픈소스 Agentic Development Environment (YC W26)

### 핵심 개념

Emdash는 General Action(Y Combinator W26)이 개발한 **에이전트 개발 환경**으로, 23종 CLI 에이전트를 병렬 실행하고 결과를 비교할 수 있다. 킬러 피처는 **Best-of-N** — 같은 작업을 Claude Code, Codex, Gemini 등에게 동시에 주고 side-by-side diff로 결과를 비교하여 최선을 선택한다. Electron 기반 GUI로 전 플랫폼을 지원한다.

### 지원 에이전트 (23종)

| 주요 에이전트 | 제공사 |
|-------------|--------|
| **Claude Code** | Anthropic |
| **Codex** | OpenAI |
| **Gemini CLI** | Google |
| **Cursor CLI** | Cursor |
| **GitHub Copilot** | GitHub |
| **Amp** | Sourcegraph |
| **Kiro** | AWS |
| **Cline** | 오픈소스 |
| + 15종 더 | Qwen Code, Hermes, Goose, Droid 등 |

### Claude Code 고유기능 보존

실제 CLI를 PTY에서 네이티브 실행하므로:

- **OAuth**: ✅ (프로세스 환경변수 패스스루)
- **CLAUDE.md**: ✅ (worktree에서 자동 읽기)
- **Skills**: ✅ (**Skills sync** — `~/.claude/commands/`에 심링크)
- **Hooks**: ✅ (네이티브 동작)
- **MCP 서버**: ✅ (`~/.claude.json`에 MCP 설정 동기화)
- **Auto-approve**: ✅ (CLI 플래그 패스스루)
- **Session Resume**: ✅

### 동작 방식

```
Emdash (Electron GUI)
│
├── Best-of-N 모드
│   ├── Claude Code #1 (worktree-1) ─┐
│   ├── Codex #1 (worktree-2)        ├→ Side-by-side diff → 최선 선택 → 머지
│   └── Gemini #1 (worktree-3)      ─┘
│
├── 일반 병렬 모드
│   ├── [칸반] Task 1 → Claude Code (worktree-a)
│   ├── [칸반] Task 2 → Codex (worktree-b)
│   └── [칸반] Task 3 → Claude Code (worktree-c)
│
├── 티켓 연동: Linear / GitHub Issues / Jira
├── Skills 카탈로그: OpenAI, Anthropic, skills.sh
├── MCP 서버 관리: 40+ 서버 설정
└── SSH/SFTP 원격 프로젝트 지원
```

---

## 2. 핵심 특징

### 킬러 피처: Best-of-N

1. 태스크 생성 시 여러 에이전트 선택 또는 "runs per provider" 증가
2. 각 에이전트가 독립 git worktree에서 동시 실행
3. 완료 후 side-by-side diff로 파일별 변경량 비교
4. 최선의 브랜치 선택 → 머지, 나머지 폐기
5. 같은 에이전트를 여러 번 돌려 확률적 최적 결과도 가능

> 권장: 2-3개 에이전트로 시작. 너무 많으면 비교가 어려움.

### 기타 장점

- **23종 에이전트**: 가장 넓은 호환성
- **칸반 보드**: 태스크 시각화
- **Skills 카탈로그**: OpenAI/Anthropic/커뮤니티 스킬 browse/install
- **MCP 서버 관리**: 40+ 서버를 UI에서 설정
- **티켓 연동**: Linear, GitHub Issues, Jira
- **SSH/SFTP**: 원격 프로젝트 지원
- **tmux 지속성**: Emdash 재시작 시에도 세션 유지
- **알림 사운드**: 태스크 완료 시 사운드 프로필
- **크로스 플랫폼**: macOS, Windows, Linux, NixOS
- **무료 (MIT)**: YC W26 백킹

### 단점

- **Electron 기반**: 네이티브 대비 메모리 사용량 높음
- **비용 추적 없음**: Agent Deck 대비
- **상대적 복잡성**: 기능이 많아 초기 설정 시간 필요
- **텔레메트리**: 익명 수집 (비활성화 가능)

---

## 3. 설치

```bash
# macOS
brew install --cask emdash

# Windows
# .msi 또는 .exe 다운로드 (emdash.sh)

# Linux
# .AppImage 또는 .deb 다운로드

# NixOS
# Nix flake 패키지
```

---

## 4. 개발 현황

| 항목 | 값 |
|------|-----|
| 버전 | v0.4.42 (2026-03-28) |
| Stars | ~3,200 |
| 라이선스 | MIT |
| 언어 | TypeScript (Electron, React/Vite) |
| 회사 | General Action (YC W26) |
| 릴리스 속도 | ~1.4일마다 |
| 핵심 개발자 | arnestrickmann (2,118 commits), rabanspiegel (700) |

---

## References

- [공식 사이트](https://emdash.sh)
- [GitHub](https://github.com/generalaction/emdash)
