---
date: 2026-03-28
tags:
  - tech
  - conductor
  - ecosystem
parent: "[[README]]"
---

# Conductor - 생태계

> [[01-overview|이전: 개요]] | [[README|목차로 돌아가기]] | [[03-references|다음: 참고자료]]

---

## 1. 관련 기술 맵

```
                    [AI 에이전트 오케스트레이션]
                              │
              ┌───────────────┼───────────────┐
              │               │               │
        [GUI 기반]      [CLI 기반]      [하이브리드]
              │               │               │
        Conductor       Claude Squad     Vibe Kanban
                        cmux
                        OMC
```

---

## 2. 대안 도구 비교

| 비교 항목 | Conductor | Claude Squad | cmux |
|-----------|-----------|-------------|------|
| 주요 특징 | GUI 대시보드 | tmux 세션 관리 | 범용 터미널 |
| 격리 | git worktree | git worktree | 없음 |
| 지원 에이전트 | Claude Code만 | CC/Codex/Aider | 모든 CLI |
| 러닝커브 | 낮음 (GUI) | 중간 (CLI) | 낮음 (터미널) |
| 가격 | 유료 | 무료 (OSS) | 무료 (OSS) |
| 커스터마이즈 | 제한적 | 높음 | 중간 |
| 적합한 상황 | GUI 선호, macOS | CLI 선호, 가벼운 관리 | 다양한 에이전트 사용 |

### Conductor만의 강점

- 유일한 **풀 GUI** 경험 — 비개발자도 접근 가능
- 시각적 diff 리뷰 내장
- 가장 낮은 진입 장벽

### Conductor의 약점

- 에이전트 록인 (Claude Code만)
- 오픈소스가 아닌 유일한 메이저 도구
- macOS 플랫폼 제한

---

## 3. 함께 사용하면 좋은 도구

| 도구 | 역할 | 연동 방식 |
|------|------|----------|
| Claude Code | 실행 에이전트 | Conductor가 직접 관리 |
| GitHub | 코드 리뷰/머지 | worktree → branch → PR |
| CLAUDE.md | 에이전트 컨텍스트 | 프로젝트 루트에 배치 |

---

## 4. 트렌드

- GUI 기반 오케스트레이션 수요 증가 — 비터미널 사용자 접근성
- 다만 CLI 기반 도구(Squad, cmux)가 OSS 커뮤니티에서 더 빠르게 성장
- 향후 다중 에이전트 지원 확대 예상 (Gemini CLI, Codex 등)

---

## 다음 단계

> [!tip] 다음으로
> [[03-references|참고자료]]에서 학습 자료를 확인하세요.
