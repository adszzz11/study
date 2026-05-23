---
date: 2026-04-01
tags:
  - tech
  - symphony
  - openai
  - projects
parent: "[[README]]"
---

# Symphony - 실전 프로젝트

> [[README|목차로 돌아가기]]

---

## 1. 프로젝트 아이디어

| 프로젝트 | 난이도 | 학습 포인트 |
|----------|--------|------------|
| Elixir 레퍼런스 구현 실행해보기 | ⭐ | 환경 설정, WORKFLOW.md 이해 |
| 자신의 저장소에 WORKFLOW.md 작성 | ⭐⭐ | 프롬프트 엔지니어링, 훅 설계 |
| SPEC.md 기반 Python 미니 구현 | ⭐⭐⭐ | 오케스트레이터 상태 머신 이해 |
| 커스텀 스킬 세트 개발 | ⭐⭐ | Codex 스킬 시스템 이해 |
| GitHub Issues 트래커 어댑터 구현 | ⭐⭐⭐ | Integration Layer 이해 |

---

## 2. 프로젝트 A: 레퍼런스 구현 실행

### 사전 준비

```bash
# 1. 필수 도구
brew install mise          # Elixir/Erlang 버전 관리
# npm install -g codex     # Codex CLI (OpenAI 계정 필요)

# 2. API 키 준비
# - Linear Personal API Key (Settings → Security & access → Personal API keys)
# - OpenAI API Key (Codex 사용을 위해)

# 3. Linear 프로젝트 설정
# - 새 프로젝트 생성
# - 커스텀 상태 추가: "Rework", "Human Review", "Merging"
# - 프로젝트 URL에서 slug 확인
```

### 실행 가이드

```bash
# 1. 저장소 클론
git clone https://github.com/openai/symphony
cd symphony/elixir

# 2. Elixir 환경 설정
mise trust
mise install
mise exec -- elixir --version   # 1.19.x 확인

# 3. 의존성 및 빌드
mise exec -- mix setup
mise exec -- mix build

# 4. 환경변수 설정
export LINEAR_API_KEY="lin_api_xxxxx"

# 5. WORKFLOW.md 수정
# - tracker.project_slug를 본인 프로젝트 slug로 변경
# - hooks.after_create의 git clone URL을 본인 저장소로 변경
# - workspace.root를 원하는 경로로 변경

# 6. 실행
mise exec -- ./bin/symphony ./WORKFLOW.md

# 7. (선택) 대시보드 포함 실행
mise exec -- ./bin/symphony ./WORKFLOW.md --port 4000
# http://localhost:4000 에서 대시보드 확인
```

### 검증 방법

```bash
# 1. Linear에 테스트 이슈 생성 (Todo 상태)
# 2. Symphony 로그에서 이슈 감지 확인
# 3. 워크스페이스 생성 확인
ls ~/code/workspaces/  # 이슈명으로 디렉토리 생성됨

# 4. 대시보드 확인 (포트 지정 시)
curl http://localhost:4000/api/v1/state | jq .

# 5. PR 생성 확인 (GitHub)
gh pr list --repo my-org/my-repo
```

---

## 3. 프로젝트 B: 나만의 WORKFLOW.md 작성

### 시나리오: Node.js 프로젝트용 워크플로우

```markdown
---
tracker:
  kind: linear
  project_slug: "my-nodejs-project"
  active_states:
    - Todo
    - In Progress
    - Rework
  terminal_states:
    - Done
    - Closed
    - Cancelled

polling:
  interval_ms: 10000

workspace:
  root: ~/code/symphony-workspaces

hooks:
  after_create: |
    git clone --depth 1 git@github.com:my-org/my-nodejs-app.git .
    npm ci
    echo "Workspace created successfully"
  before_run: |
    git fetch origin main
    git checkout -b feature/{{ issue.identifier | downcase }} origin/main 2>/dev/null || git checkout feature/{{ issue.identifier | downcase }}
    npm ci
  after_run: |
    npm run lint --fix || true
  timeout_ms: 180000

agent:
  max_concurrent_agents: 3
  max_turns: 15

codex:
  command: codex app-server
  approval_policy: never
  thread_sandbox: workspace-write
  turn_sandbox_policy:
    type: workspaceWrite
  turn_timeout_ms: 3600000
  stall_timeout_ms: 300000
---

You are working on issue `{{ issue.identifier }}` for a Node.js application.

{% if attempt %}
This is retry attempt #{{ attempt }}. Resume from workspace state.
{% endif %}

## Issue Details
- **Identifier**: {{ issue.identifier }}
- **Title**: {{ issue.title }}
- **Status**: {{ issue.state }}
- **Labels**: {{ issue.labels }}

## Description
{% if issue.description %}
{{ issue.description }}
{% else %}
No description provided. Analyze the title and implement accordingly.
{% endif %}

## Your Environment
- Runtime: Node.js 20
- Package manager: npm
- Test framework: Jest
- Linter: ESLint

## Instructions
1. Read the issue carefully and understand the requirements.
2. Implement the changes with proper TypeScript types.
3. Write unit tests (Jest) for your changes.
4. Run `npm test` and ensure all tests pass.
5. Run `npm run lint` and fix any issues.
6. Create a clean commit with a descriptive message.
7. Push your branch and create a PR.
8. Update the Linear issue status to "Human Review".

## Quality Standards
- All new functions must have JSDoc comments.
- Test coverage for new code must be > 80%.
- No TypeScript `any` types unless absolutely necessary.
- Follow existing code patterns and conventions.
```

---

## 4. 프로젝트 C: SPEC.md 기반 Python 미니 구현

> [!tip] 학습 목적
> SPEC.md의 핵심 로직을 Python으로 구현하면 오케스트레이터 설계를 깊이 이해할 수 있다.

### 핵심 컴포넌트만 구현

```python
"""
Symphony 미니 구현 (Python) - 학습 목적
핵심: Orchestrator + WorkspaceManager + MockTracker
"""

import os
import time
import yaml
import subprocess
import threading
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Optional

# ━━━ Domain Model ━━━

@dataclass
class Issue:
    id: str
    identifier: str
    title: str
    description: Optional[str]
    state: str
    priority: Optional[int] = None
    url: Optional[str] = None
    labels: list[str] = field(default_factory=list)

class OrchState(Enum):
    UNCLAIMED = "unclaimed"
    CLAIMED = "claimed"
    RUNNING = "running"
    RETRY_QUEUED = "retry_queued"
    RELEASED = "released"

# ━━━ Workflow Loader ━━━

@dataclass
class WorkflowConfig:
    tracker_kind: str = "linear"
    project_slug: str = ""
    api_key: str = ""
    active_states: list[str] = field(default_factory=lambda: ["Todo", "In Progress"])
    terminal_states: list[str] = field(
        default_factory=lambda: ["Closed", "Cancelled", "Done"]
    )
    poll_interval_ms: int = 30000
    workspace_root: str = "/tmp/symphony_workspaces"
    max_concurrent_agents: int = 10
    max_turns: int = 20
    hooks_after_create: Optional[str] = None
    hooks_before_run: Optional[str] = None

def load_workflow(path: str) -> tuple[WorkflowConfig, str]:
    """WORKFLOW.md를 파싱하여 config와 prompt_template 반환"""
    with open(path) as f:
        content = f.read()

    if content.startswith("---"):
        parts = content.split("---", 2)
        front_matter = yaml.safe_load(parts[1])
        prompt_template = parts[2].strip()
    else:
        front_matter = {}
        prompt_template = content.strip()

    config = WorkflowConfig()
    if tracker := front_matter.get("tracker"):
        config.tracker_kind = tracker.get("kind", "linear")
        config.project_slug = tracker.get("project_slug", "")
    if polling := front_matter.get("polling"):
        config.poll_interval_ms = int(polling.get("interval_ms", 30000))
    if workspace := front_matter.get("workspace"):
        config.workspace_root = os.path.expanduser(workspace.get("root", config.workspace_root))
    if hooks := front_matter.get("hooks"):
        config.hooks_after_create = hooks.get("after_create")
        config.hooks_before_run = hooks.get("before_run")

    return config, prompt_template

# ━━━ Workspace Manager ━━━

import re

def sanitize_key(identifier: str) -> str:
    """Safety Invariant #3: 안전한 문자만 허용"""
    return re.sub(r'[^A-Za-z0-9._-]', '_', identifier)

def validate_within_root(workspace_path: Path, root: Path) -> bool:
    """Safety Invariant #2: 경로 봉쇄"""
    return str(workspace_path.resolve()).startswith(str(root.resolve()) + os.sep)

def create_workspace(identifier: str, config: WorkflowConfig) -> tuple[Path, bool]:
    """워크스페이스 생성/재사용"""
    key = sanitize_key(identifier)
    root = Path(config.workspace_root)
    workspace = root / key

    # Safety Invariant #2
    assert validate_within_root(workspace, root), \
        f"Path safety violation: {workspace} outside {root}"

    created = not workspace.exists()
    workspace.mkdir(parents=True, exist_ok=True)

    if created and config.hooks_after_create:
        subprocess.run(
            ["bash", "-lc", config.hooks_after_create],
            cwd=str(workspace), check=True, timeout=60
        )

    return workspace, created

# ━━━ Orchestrator (핵심 상태 머신) ━━━

class MiniOrchestrator:
    def __init__(self, config: WorkflowConfig, prompt_template: str):
        self.config = config
        self.prompt_template = prompt_template
        self.running: dict[str, dict] = {}
        self.claimed: set[str] = set()
        self.retry_attempts: dict[str, dict] = {}
        self._stop = False

    def is_dispatch_eligible(self, issue: Issue) -> bool:
        """후보 선택 7가지 조건"""
        return all([
            issue.id and issue.identifier and issue.title and issue.state,
            issue.state.lower() in [s.lower() for s in self.config.active_states],
            issue.state.lower() not in [s.lower() for s in self.config.terminal_states],
            issue.id not in self.running,
            issue.id not in self.claimed,
            len(self.running) < self.config.max_concurrent_agents,
        ])

    def dispatch(self, issue: Issue):
        """이슈 디스패치: claim -> workspace -> agent 실행"""
        self.claimed.add(issue.id)

        workspace, created = create_workspace(issue.identifier, self.config)
        print(f"[DISPATCH] {issue.identifier} -> {workspace} (created={created})")

        # Safety Invariant #1: CWD를 워크스페이스로 설정
        entry = {
            "issue": issue,
            "workspace": workspace,
            "started_at": time.time(),
        }
        self.running[issue.id] = entry

        # 워커 스레드로 에이전트 실행 (실제로는 Codex App Server)
        thread = threading.Thread(
            target=self._run_agent, args=(issue, workspace)
        )
        thread.daemon = True
        thread.start()

    def _run_agent(self, issue: Issue, workspace: Path):
        """에이전트 실행 (워커 스레드)"""
        try:
            print(f"[AGENT] {issue.identifier}: 작업 시작 at {workspace}")
            # 실제 구현에서는 Codex App Server 핸드셰이크 + 턴 실행
            # 여기서는 시뮬레이션
            time.sleep(2)
            print(f"[AGENT] {issue.identifier}: 작업 완료")
        except Exception as e:
            print(f"[AGENT] {issue.identifier}: 실패 - {e}")
        finally:
            self.running.pop(issue.id, None)
            # 1초 후 continuation retry (이슈 재확인)
            self.claimed.discard(issue.id)

    def run_poll_loop(self, fetch_issues_fn):
        """메인 폴링 루프"""
        interval_sec = self.config.poll_interval_ms / 1000
        print(f"[ORCH] 폴링 시작 (간격: {interval_sec}초)")

        while not self._stop:
            # 1. 재조정 (생략: 트래커 상태 확인)
            # 2. 후보 페치
            issues = fetch_issues_fn()
            # 3. 정렬: priority asc -> created_at asc
            issues.sort(key=lambda i: (i.priority or 999, i.identifier))
            # 4. 디스패치
            for issue in issues:
                if self.is_dispatch_eligible(issue):
                    self.dispatch(issue)
            # 5. 대기
            time.sleep(interval_sec)

# ━━━ 사용 예시 ━━━

if __name__ == "__main__":
    config, prompt = load_workflow("WORKFLOW.md")

    orch = MiniOrchestrator(config, prompt)

    # Mock 이슈 데이터 (실제로는 Linear API에서 페치)
    def mock_fetch():
        return [
            Issue(id="1", identifier="TEST-1", title="로그인 버그 수정",
                  description="비밀번호 유효성 검사 추가", state="Todo", priority=1),
            Issue(id="2", identifier="TEST-2", title="대시보드 레이아웃",
                  description="모바일 반응형 추가", state="Todo", priority=2),
        ]

    orch.run_poll_loop(mock_fetch)
```

---

## 5. Best Practices

### WORKFLOW.md 작성

- **프롬프트에 환경 정보 포함**: 사용하는 언어, 프레임워크, 테스트 도구를 명시
- **품질 기준 명시**: 테스트 커버리지, 린트 규칙, 코드 스타일을 프롬프트에 포함
- **실패 시 행동 지시**: "블로커가 아닌 한 멈추지 말고 계속 진행" 등
- **상태 전환 규칙 정의**: 어떤 상태에서 어떤 행동을 할지 명확히 지시

### 저장소 준비 (Harness Engineering)

- **AGENTS.md / CLAUDE.md 작성**: 코드베이스 규칙, 테스트 방법, 아키텍처 설명
- **CI/CD 완비**: PR 생성 후 자동 테스트가 실행되도록 설정
- **명확한 이슈 작성**: 에이전트가 이해할 수 있도록 이슈 제목/설명을 구체적으로

### 운영

- **`max_concurrent_agents`를 점진적으로 증가**: 처음에는 1-2개로 시작하여 안정성 확인 후 증가
- **`stall_timeout_ms` 적절히 설정**: 너무 짧으면 정상 작업이 중단, 너무 길면 정체 감지 늦음
- **대시보드 활성화**: `--port` 옵션으로 Phoenix LiveView 대시보드 사용
- **로그 모니터링**: `--logs-root` 옵션으로 로그 디렉토리 지정 후 모니터링

---

## 6. 실무 적용 시 고려사항

### 비용

- Codex API 호출 비용이 에이전트 수 x 턴 수만큼 발생
- `max_concurrent_agents`와 `max_turns`로 비용 제어
- `codex_totals`로 토큰 사용량 모니터링

### 보안

- `approval_policy: never`는 고신뢰 환경에서만 사용
- `thread_sandbox: workspace-write`로 파일시스템 접근 제한
- Linear API 키는 환경변수로 관리 (`$LINEAR_API_KEY`)
- SSH 원격 워커 사용 시 키 관리 주의

### 모니터링

```bash
# Phoenix LiveView 대시보드
http://localhost:4000/

# JSON API - 전체 상태
curl http://localhost:4000/api/v1/state | jq .

# JSON API - 특정 이슈
curl http://localhost:4000/api/v1/ABC-123 | jq .

# JSON API - 수동 새로고침
curl -X POST http://localhost:4000/api/v1/refresh
```

---

## 7. 배포 가이드

### 로컬 개발

```bash
mise exec -- ./bin/symphony ./WORKFLOW.md --port 4000
```

### systemd 서비스 (Linux)

```ini
[Unit]
Description=Symphony Agent Orchestrator
After=network.target

[Service]
Type=simple
User=symphony
WorkingDirectory=/opt/symphony/elixir
Environment=LINEAR_API_KEY=lin_api_xxxxx
ExecStart=/opt/symphony/elixir/bin/symphony /opt/symphony/WORKFLOW.md --port 4000 --logs-root /var/log/symphony
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### Docker (커뮤니티 접근)

```dockerfile
FROM elixir:1.19-otp-28

WORKDIR /app
COPY elixir/ .

RUN mix setup && mix build

ENV LINEAR_API_KEY=""

ENTRYPOINT ["./bin/symphony"]
CMD ["./WORKFLOW.md", "--port", "4000"]
```

---

## 8. 프로젝트 구조 예시 (자체 구현 시)

```
my-symphony/
├── WORKFLOW.md              # 워크플로우 정의
├── SPEC.md                  # (참조) OpenAI SPEC
├── .codex/
│   └── skills/              # Codex 스킬
│       ├── commit/SKILL.md
│       └── push/SKILL.md
├── src/
│   ├── orchestrator.py      # 핵심 상태 머신
│   ├── tracker/
│   │   └── linear.py        # Linear API 클라이언트
│   ├── workspace.py         # 워크스페이스 관리
│   ├── agent_runner.py      # Codex App Server 클라이언트
│   └── config.py            # 설정 파싱
├── tests/
└── pyproject.toml
```
