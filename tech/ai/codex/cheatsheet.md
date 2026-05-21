---
date: 2026-05-20
tags:
  - tech
  - Codex
  - cheatsheet
parent: "[[README]]"
---

# Codex - 치트시트 (v0.130)

> [[README|목차로 돌아가기]]

---

## 설치 & 인증

```bash
npm install -g @openai/codex          # 설치
codex login                            # ChatGPT OAuth
export OPENAI_API_KEY=sk-...           # API 키 방식
codex --version                        # 버전 확인
```

---

## 자주 사용하는 명령어

| 명령어 | 설명 |
|--------|------|
| `codex` | 대화형 TUI 시작 |
| `codex exec "..."` | 비대화형, stdout 출력 |
| `codex exec --json "..."` | JSON 출력 |
| `codex /init` | AGENTS.md 스캐폴드 |
| `codex mcp add <name> <url>` | MCP 서버 등록 |
| `codex mcp list` | MCP 서버 목록 |
| `codex remote-control --port 8080` | 헤드리스 원격 제어 (v0.130+) |

### 옵션 플래그

| 플래그 | 설명 |
|--------|------|
| `--model gpt-5.3-codex`, `-m` | 모델 지정 |
| `--effort <low\|medium\|high\|extra-high>` | 추론 강도 |
| `--approval <untrusted\|on-failure\|trusted>` | 권한 정책 |
| `--sandbox <read-only\|workspace-write\|danger-full-access>` | 샌드박스 |
| `--add-dir <path>` | 추가 작업 디렉토리 |
| `--json` | JSON 출력 (`exec`와 함께) |

### 슬래시 커맨드 (TUI 내)

| 커맨드 | 용도 |
|--------|------|
| `/init` | AGENTS.md 생성 |
| `/plan` | 계획 모드 |
| `/resume` | 세션 재개 |
| `/fork` | 세션 분기 |
| `/compact` | 컨텍스트 압축 |
| `/agent` | 서브에이전트 전환 |
| `/review --base main` | PR 스타일 리뷰 |
| `/vim` | Vim 모달 편집 토글 (v0.129+) |
| `/hooks` | 훅 브라우저 (v0.129+) |
| `/keymap debug` | 키 이벤트 inspect |

### 키 단축키

| 키 | 동작 |
|-----|------|
| `Alt+,` | reasoning 낮춤 |
| `Alt+.` | reasoning 높임 |
| `Ctrl+C` | 현재 동작 중단 |
| `Ctrl+D` | 세션 종료 |
| Vim 모드 | `i`/`Esc`/`dd`/`yy`/`w`/`b` 등 표준 |

---

## 핵심 코드 패턴

### 패턴 1: CI lint 자동 수정

```bash
codex exec "Fix all lint. Don't break tests."
```

### 패턴 2: 테스트 실패 자율 디버그

```bash
codex exec --effort high "Run tests. Diagnose any failure. Fix and re-run."
```

### 패턴 3: Skill 호출

```bash
codex exec "release-notes 스킬로 v1.3.0 노트 생성"
```

### 패턴 4: 헤드리스 원격 제어

```bash
codex remote-control --port 8080
```

### 패턴 5: 특정 디렉토리만 대상

```bash
codex --add-dir src/auth exec "Add OAuth flow"
```

### 패턴 6: 신뢰 모드 (위험)

```bash
codex exec --approval trusted --sandbox workspace-write "..."
# ⚠️ 신뢰 저장소에서만!
```

---

## 설정 옵션 (`~/.codex/config.toml`)

```toml
model = "gpt-5.3-codex"
model_reasoning_effort = "medium"
approval_policy = "untrusted"
sandbox_mode = "workspace-write"

[tui]
default_keymaps = "vim"              # 또는 "default"

[mcp_servers.github]
url = "https://mcp.example.com/github"
auth_token_env = "GITHUB_TOKEN"

[model_providers.amazon-bedrock]
name = "Amazon Bedrock"

[model_providers.amazon-bedrock.aws]
profile = "default"                   # v0.130+: aws login 캐시 자동 인식
```

### 주요 옵션

| 옵션 | 기본값 | 설명 |
|------|--------|------|
| `model` | gpt-5.3-codex | 기본 모델 |
| `model_reasoning_effort` | medium | 기본 추론 강도 |
| `approval_policy` | untrusted | 명령 실행 권한 |
| `sandbox_mode` | workspace-write | 파일 접근 범위 |
| `tui.default_keymaps` | default | Vim 또는 default |

### 환경 변수

| 변수 | 용도 |
|------|------|
| `OPENAI_API_KEY` | API 키 (OAuth 미사용 시) |
| `CODEX_MCP_TOOL_TIMEOUT` | MCP 툴 timeout (초) |
| `CODEX_LOG_LEVEL` | 디버그 로그 |

---

## 파일 / 디렉토리

```
~/.codex/
├── config.toml              ← 개인 설정
├── AGENTS.md                ← 개인 기본 지시
└── auth/                    ← OAuth 토큰

~/.agents/skills/            ← 개인 스킬
└── <skill-name>/
    └── SKILL.md

<repo>/
├── AGENTS.md                ← 저장소 표준
├── .codex/
│   ├── config.toml          ← 저장소 설정 (선택)
│   └── code-review.md       ← 리뷰 가이드
└── .agents/skills/          ← 팀 공유 스킬
```

---

## AGENTS.md 최소 템플릿

```markdown
# AGENTS.md

## Setup
<install/run cmds>

## Test
<test cmd>

## Conventions
- <rule 1>
- <rule 2>

## Architecture
<dir 설명>

## Don't
- <금지 사항>
```

## Skill 최소 템플릿

```markdown
---
name: <kebab-case-name>
description: <한 줄 설명>
---

# <Skill 이름>

## When to use
<언제 트리거되는지>

## How
<단계별 동작>

## Output
<결과 형식>
```

---

## 트러블슈팅

| 증상 | 해결 |
|------|------|
| 명령 못 찾음 | `npm config get prefix` 후 PATH 확인 |
| 느림 | `Alt+,`로 effort 낮추기 |
| MCP 60초 컷 | `CODEX_MCP_TOOL_TIMEOUT=300` |
| 권한 매번 묻기 | `approval_policy = "on-failure"` |
| Bedrock 인증 | `aws login` 후 v0.130+ 자동 인식 |
| 컨텍스트 폭주 | `/compact`로 압축 |
| AGENTS.md 무시됨 | 프로젝트 루트 또는 `.codex/AGENTS.md` 경로 확인 |

---

## 관련 노트

- [[README]]
- [[01-overview]]
- [[04-learning/01-getting-started]]
- [[05-projects]]
- [[../claude/13-2026-05-latest|Claude 최신 비교]]
