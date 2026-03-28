---
date: 2026-03-28
tags:
  - tech
  - claude-squad
  - ecosystem
parent: "[[README]]"
---

# Claude Squad - 생태계

> [[01-overview|이전: 개요]] | [[README|목차로 돌아가기]] | [[03-references|다음: 참고자료]]

---

## 1. 관련 기술 맵

```
                [git worktree 기반 격리]
                         │
          ┌──────────────┼──────────────┐
          │              │              │
    [CLI 관리]     [GUI 관리]     [칸반 관리]
          │              │              │
    Claude Squad    Conductor     Vibe Kanban
```

---

## 2. 대안 도구 비교

| 비교 항목 | Claude Squad | Conductor | Vibe Kanban |
|-----------|-------------|-----------|-------------|
| 인터페이스 | CLI (tmux) | GUI (macOS 앱) | CLI + Web UI |
| 격리 | git worktree | git worktree | git worktree |
| 설치 | brew install | DMG 다운로드 | npm install |
| 에이전트 | CC/Codex/Aider/Amp | Claude Code만 | CC/Gemini/Amp |
| 가격 | 무료 (OSS) | 유료 | 무료 (OSS) |
| 백그라운드 | ✓ (auto-accept) | ✓ | ✓ |
| 러닝커브 | 낮음 | 매우 낮음 | 중간 |
| 적합한 상황 | CLI 선호, 가벼운 관리 | GUI 선호 | 프로젝트/팀 관리 |

### Claude Squad만의 강점

- **가장 간단한 설치**: brew 한 줄
- **가장 가벼움**: tmux 기반 최소 리소스
- **다중 에이전트**: Conductor보다 더 많은 에이전트 지원

### Claude Squad의 약점

- GUI 없음 (Conductor 대비)
- 칸반/프로젝트 관리 없음 (Vibe Kanban 대비)
- 모델 라우팅 없음 (OMC 대비)

---

## 3. 함께 사용하면 좋은 도구

| 도구 | 역할 | 연동 방식 |
|------|------|----------|
| Claude Code | 기본 에이전트 | Squad가 worktree에서 실행 |
| Codex | 보조 에이전트 | Squad가 worktree에서 실행 |
| oh-my-claudecode | Claude Code 강화 | Squad worktree에서 OMC 실행 |
| GitHub | 코드 리뷰 | worktree → branch → PR |

---

## 4. 트렌드

- git worktree 기반 격리가 멀티에이전트의 사실상 표준으로 자리잡는 추세
- Claude Squad는 심플함으로 커뮤니티에서 빠르게 성장
- Homebrew 배포로 macOS 개발자 접근성 극대화

---

## 다음 단계

> [!tip] 다음으로
> [[03-references|참고자료]]에서 학습 자료를 확인하세요.
