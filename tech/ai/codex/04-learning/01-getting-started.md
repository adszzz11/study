---
date: 2026-05-20
tags:
  - tech
  - Codex
  - learning
parent: "[[README]]"
---

# Codex - 시작하기

> [[README|목차로 돌아가기]]

---

## 1. 설치

```bash
# npm 전역 설치
npm install -g @openai/codex

# 버전 확인 (2026-05 기준 권장: v0.130.0)
codex --version
```

## 2. 인증

```bash
# 대화형 로그인 (ChatGPT 계정 OAuth)
codex login

# 또는 OpenAI API 키 사용
export OPENAI_API_KEY=sk-...
```

ChatGPT Plus/Pro/Team 구독이 있으면 OAuth 권장. 엔터프라이즈는 API 키 + 별도 결제.

---

## 3. 첫 번째 실행 (대화형 TUI)

```bash
cd ~/my-project
codex
```

TUI가 열리면:
```
> Add a /health endpoint to src/server.ts that returns OK
```

Codex가 작업 계획 → 파일 편집 → 테스트 → 요약 순으로 진행. 권한이 필요한 명령은 confirm 프롬프트.

---

## 4. 핵심 개념 실습

### AGENTS.md 초기화

```bash
codex /init
```

생성된 `AGENTS.md`를 본인 프로젝트에 맞게 편집:

```markdown
# AGENTS.md

## Setup
pnpm install

## Test
pnpm test --watch

## Lint
pnpm lint:fix

## Conventions
- TypeScript strict mode
- 모든 export는 named export
- 테스트는 vitest 사용

## Architecture
- src/api: HTTP 핸들러
- src/core: 도메인 로직
- src/infra: DB/외부 시스템 어댑터

## Don't
- src/legacy/는 수정 금지 (마이그레이션 중)
```

다음부터 모든 Codex 세션이 이 컨텍스트 자동 로딩.

### 스택형 AGENTS.md
```
~/.codex/AGENTS.md                  ← 개인 기본값
<repo>/.codex/AGENTS.md             ← 저장소 표준
<repo>/src/api/.codex/AGENTS.md     ← 디렉토리별 로컬 규칙
```

가까운 디렉토리가 우선.

### 비대화형 실행 (CI/CD)

```bash
codex exec "Run npm test, if any fail, write a fix and re-run until passing"
codex exec --json "..."
codex exec --model gpt-5.3-codex --effort high "..."
```

GitHub Actions:
```yaml
- name: Auto-fix lint
  run: codex exec "Fix all lint errors. Don't break tests."
  env:
    OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
```

### Skills 만들기

```bash
mkdir -p ~/.agents/skills/release-notes
cat > ~/.agents/skills/release-notes/SKILL.md <<'EOF'
---
name: release-notes
description: git log 기반 한국어 릴리스 노트 생성
---

# Release Notes Skill

`git log v1.2.0..HEAD` 출력을 읽고 다음 구조로 작성:

## 신규 기능
## 버그 수정
## 변경
## 제거

각 항목은 한 줄, 한국어로.
EOF
```

세션에서: `> release-notes 스킬로 v1.3.0 노트 만들어줘`

### MCP 서버 연결

```bash
codex mcp add github https://mcp.example.com/github
codex mcp list
```

영구 저장 (`~/.codex/config.toml`):
```toml
[mcp_servers.github]
url = "https://mcp.example.com/github"
auth_token_env = "GITHUB_TOKEN"
```

### 권한 / 샌드박스

**Approval 모드**:
| 값 | 동작 |
|----|------|
| `untrusted` | 명령마다 확인 (기본 권장) |
| `on-failure` | 실패 후 재시도 시 확인 |
| `trusted` | 자동 실행 (위험) |

**Sandbox 모드**:
| 값 | 동작 |
|----|------|
| `read-only` | 파일 읽기만 |
| `workspace-write` | 현재 디렉토리 쓰기 |
| `danger-full-access` | 전체 접근 (위험) |

```toml
# config.toml
approval_policy = "untrusted"
sandbox_mode = "workspace-write"
```

### Vim 모드 (v0.129+)

```
/vim
```
세션 중 토글. 기본으로 켜기:
```toml
[tui]
default_keymaps = "vim"
```

### Reasoning 레벨 조정 (TUI 내)

- `Alt+,` — 낮춤 (Low ← Medium ← High ← Extra High)
- `Alt+.` — 높임

### 세션 관리

| 커맨드 | 용도 |
|--------|------|
| `/resume` | 이전 세션 picker 재개 |
| `/fork` | 현재 세션 분기 (히스토리 보존) |
| `/compact` | 긴 컨텍스트 요약 |
| `/plan` | 복잡 태스크 계획 모드 |

### 헤드리스 원격 제어 (v0.130+)

```bash
codex remote-control --port 8080
```

다른 도구가 HTTP/WS로 제어. 멀티 에이전트 빌딩 블록.

### PR 리뷰

```bash
codex /review --base main
```

GitHub Cloud 통합: Settings → Integrations → Codex 활성화하면 자동 PR 리뷰.

---

## 5. 트러블슈팅

| 문제 | 원인 | 해결 |
|------|------|------|
| `codex: command not found` | PATH 누락 | `npm config get prefix` 후 PATH 추가 |
| 모델 응답 느림 | 높은 reasoning | `Alt+,`로 낮추기 |
| MCP 60초 timeout | 기본 캡 | `CODEX_MCP_TOOL_TIMEOUT=300` 환경변수 |
| 권한 매번 묻기 | `untrusted` 모드 | `on-failure`로 완화 (신뢰 저장소만) |
| Bedrock 인증 실패 | v0.130 이전 | v0.130+로 업데이트, `aws login` 후 자동 인식 |
| 컨텍스트 폭주 | 긴 세션 | `/compact`로 요약 |
| AGENTS.md 무시됨 | 경로 오류 | 프로젝트 루트 또는 `.codex/AGENTS.md` |

---

## 다음 단계

> [!tip] 다음으로
> 기본 사용법을 익혔다면 [[../05-projects|실전 프로젝트]]로 워크플로우 구축해보세요.
