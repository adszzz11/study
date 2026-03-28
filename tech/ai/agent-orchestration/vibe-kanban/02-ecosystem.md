---
date: 2026-03-28
tags:
  - tech
  - vibe-kanban
  - ecosystem
parent: "[[README]]"
---

# Vibe Kanban - 생태계

> [[01-overview|이전: 개요]] | [[README|목차로 돌아가기]] | [[03-references|다음: 참고자료]]

---

## 1. 관련 기술 맵

```
              [AI 에이전트 오케스트레이션]
                        │
         ┌──────────────┼──────────────┐
         │              │              │
   [터미널 중심]   [GUI 중심]     [프로젝트 관리]
         │              │              │
   Claude Squad    Conductor      Vibe Kanban
   cmux                          Composio
```

---

## 2. 대안 도구 비교

| 비교 항목 | Vibe Kanban | Conductor | Claude Squad |
|-----------|-------------|-----------|-------------|
| 주요 특징 | 칸반 + diff 리뷰 | GUI 대시보드 | CLI 세션 관리 |
| 인터페이스 | Web UI + CLI | macOS 앱 | 터미널 (tmux) |
| 코드 리뷰 | ✓ (내장 diff) | ✓ (GUI) | △ (diff view) |
| 프로젝트 관리 | ✓ (칸반) | ✗ | ✗ |
| 크로스 플랫폼 | ✓ | macOS만 | macOS/Linux |
| 에이전트 | CC/Gemini/Amp | Claude Code만 | CC/Codex/Aider |
| 가격 | 무료 (OSS) | 유료 | 무료 (OSS) |

### Vibe Kanban만의 강점

- **유일한 칸반 보드** — 작업을 프로젝트 관리 관점으로 시각화
- **가장 강력한 코드 리뷰** — GitHub PR 수준의 diff 리뷰어 내장
- **크로스 플랫폼** — macOS 외에도 Linux, Windows 지원

### Vibe Kanban의 약점

- 가장 높은 진입 장벽 (칸반 + 리뷰어 + 에이전트 모두 이해 필요)
- Web UI 실행이 필요 (순수 CLI 워크플로우에 부적합)

---

## 3. 함께 사용하면 좋은 도구

| 도구 | 역할 | 연동 방식 |
|------|------|----------|
| Claude Code | AI 에이전트 | Vibe Kanban이 worktree에서 실행 |
| Gemini CLI | AI 에이전트 | Vibe Kanban이 worktree에서 실행 |
| GitHub | 추가 코드 리뷰 | worktree → branch → PR |
| Linear/Jira | 프로젝트 관리 | 칸반 카드와 이슈 동기화 가능 |

---

## 4. 트렌드

- AI 에이전트 결과물의 **코드 리뷰** 중요성이 부각되는 추세
- 프로젝트 관리 + AI 오케스트레이션 통합 방향으로 발전
- BloopAI(YC)의 기업 지원으로 안정적 개발 기대

---

## 다음 단계

> [!tip] 다음으로
> [[03-references|참고자료]]에서 학습 자료를 확인하세요.
