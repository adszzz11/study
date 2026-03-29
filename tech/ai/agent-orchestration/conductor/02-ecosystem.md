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

| 비교 항목 | Conductor | Claude Squad | ccmanager | Agent Deck | Emdash |
|-----------|-----------|-------------|-----------|------------|--------|
| 주요 특징 | GUI 대시보드 | tmux 세션 관리 | PTY 세션 관리 | TUI + 비용 추적 | GUI + Best-of-N |
| 격리 | git worktree | git worktree | git worktree | tmux 세션 | git worktree |
| 지원 에이전트 | CC + Codex | CC/Codex/Aider | 8종 (CC/Codex/Gemini 등) | CC/Codex/Gemini 등 | 23종 |
| Claude 고유기능 | ✅ 100% | ✅ 100% | ✅ 100% | ✅ 100% | ✅ 100% |
| 러닝커브 | 낮음 (GUI) | 중간 (CLI) | 낮음 (CLI) | 중간 (TUI) | 낮음 (GUI) |
| 가격 | 현재 무료 | 무료 (OSS) | 무료 (MIT) | 무료 (MIT) | 무료 (MIT) |
| 플랫폼 | macOS | macOS/Linux | macOS/Linux | macOS/Linux/Win | 전체 |

### Conductor만의 강점

- **풀 GUI** 경험 — macOS 네이티브 앱
- **Checkpoint + 롤백**: 자동 스냅샷으로 안전한 실험
- **GitHub 양방향 동기화**: diff 코멘트, Actions 로그 직접 확인
- **`.context` 공유**: 에이전트 간 파일 기반 컨텍스트 공유
- **프로바이더 유연성**: OpenRouter, Bedrock, Vertex 등

### Conductor의 약점

- 2종 에이전트만 (Claude Code + Codex) — Gemini CLI 등 미지원
- 폐쇄 소스 — 커스터마이즈 제한
- macOS 플랫폼 제한 (Linux/Windows 미정)

---

## 3. 함께 사용하면 좋은 도구

| 도구 | 역할 | 연동 방식 |
|------|------|----------|
| Claude Code | 실행 에이전트 | Conductor가 직접 관리 (OAuth 지원) |
| Codex | 실행 에이전트 | v0.18.0부터 지원, GPT-5.3 |
| GitHub | 코드 리뷰/머지 | worktree → branch → PR, 코멘트 양방향 동기화 |
| CLAUDE.md | 에이전트 컨텍스트 | 프로젝트 루트에 배치, worktree에 자동 복사 |
| OpenRouter | 프로바이더 | Claude/OpenAI 외 다양한 모델 접근 |
| MCP 서버 | 도구 확장 | Conductor 설정에서 MCP 서버 연결 |

---

## 4. 트렌드

- GUI 기반 오케스트레이션 시장 확대 — Conductor, Emdash, Superset 등 경쟁
- CLI 기반 도구(Squad, ccmanager, dmux)도 OSS 커뮤니티에서 빠르게 성장
- "Best-of-N" 패턴 부상 — 같은 작업을 여러 모델로 비교 (Emdash)
- 에이전트 지원 범위 확대 경쟁 — ccmanager 8종, Emdash 23종

---

## 다음 단계

> [!tip] 다음으로
> [[03-references|참고자료]]에서 학습 자료를 확인하세요.
