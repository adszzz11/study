---
date: 2026-04-01
tags:
  - tech
  - symphony
  - codex
  - app-server
  - json-rpc
parent: "[[README]]"
---

# Codex App Server 연동

> [[03-orchestrator|이전: 오케스트레이터]] | [[README|목차로 돌아가기]] | [[05-workspace-management|다음: 워크스페이스 관리]]

---

## 📌 핵심 개념

Symphony는 Codex를 **App Server 모드**로 실행한다. App Server는 Codex의 프로그래밍 인터페이스로, stdio를 통한 **JSON-RPC 2.0** 프로토콜로 통신한다. 이를 통해 Symphony가 Codex 세션의 전체 생명주기(초기화 -> 스레드 생성 -> 턴 실행 -> 스트리밍 -> 종료)를 프로그래밍적으로 제어한다.

### 프로토콜 아키텍처

```
Symphony (클라이언트)         Codex App Server (서버)
       │                           │
       │── initialize ──────────►  │ 초기화 + 능력 협상
       │◄── initialize result ──── │
       │── initialized ─────────►  │ 초기화 완료 알림
       │── thread/start ────────►  │ 스레드 생성
       │◄── thread/start result ── │ (thread_id 반환)
       │── turn/start ──────────►  │ 첫 번째 턴 (전체 프롬프트)
       │◄── 스트리밍 이벤트 ─────── │ (진행 상황, 토큰 등)
       │◄── turn/completed ─────── │ 턴 완료
       │                           │
       │── turn/start ──────────►  │ 연속 턴 (continuation guidance)
       │◄── turn/completed ─────── │
       │                           │
       │  (프로세스 종료)             │
```

### 핵심 용어

| 용어 | 설명 |
|------|------|
| **Thread** | Codex 대화 스레드. 하나의 워커 실행 동안 유지됨 |
| **Turn** | 스레드 내 단일 실행 턴. 프롬프트 전송 -> 결과 수신 |
| **Session** | `<thread_id>-<turn_id>` 조합으로 식별 |
| **Approval Policy** | 명령 실행/파일 변경 승인 정책 (never, on-failure 등) |
| **Sandbox** | 에이전트 실행 범위 제한 (workspace-write 등) |
| **Dynamic Tool** | 런타임에 제공되는 클라이언트 사이드 도구 (linear_graphql 등) |

---

## 💻 코드

### 세션 시작 핸드셰이크

```json
// 1단계: initialize (클라이언트 -> 서버)
{"id": 1, "method": "initialize", "params": {
  "clientInfo": {"name": "symphony", "version": "1.0"},
  "capabilities": {}
}}

// 서버 응답 대기 (read_timeout_ms 이내)
{"id": 1, "result": {"serverInfo": {"name": "codex", "version": "..."}}}

// 2단계: initialized 알림 (응답 없음)
{"method": "initialized", "params": {}}

// 3단계: thread/start
{"id": 2, "method": "thread/start", "params": {
  "approvalPolicy": "never",
  "sandbox": "workspace-write",
  "cwd": "/home/user/workspaces/ABC-123"
}}

// 서버 응답 (thread_id 획득)
{"id": 2, "result": {"thread": {"id": "thrd_abc123"}}}

// 4단계: turn/start (첫 번째 턴 - 전체 프롬프트)
{"id": 3, "method": "turn/start", "params": {
  "threadId": "thrd_abc123",
  "input": [{"type": "text", "text": "렌더링된 프롬프트 내용..."}],
  "cwd": "/home/user/workspaces/ABC-123",
  "title": "ABC-123: 로그인 페이지 유효성 검사",
  "approvalPolicy": "never",
  "sandboxPolicy": {"type": "workspaceWrite"}
}}

// 서버 응답 (turn_id 획득)
{"id": 3, "result": {"turn": {"id": "turn_xyz789"}}}
```

### 연속 턴(Continuation Turn)

```json
// 이슈가 여전히 활성이면 동일 thread에서 다음 턴 시작
// 첫 턴과 달리 continuation guidance만 전송 (원래 프롬프트는 스레드 히스토리에 있음)
{"id": 4, "method": "turn/start", "params": {
  "threadId": "thrd_abc123",
  "input": [{"type": "text", "text": "이전 턴이 완료되었지만 이슈가 아직 활성 상태입니다. 계속 진행하세요."}],
  "cwd": "/home/user/workspaces/ABC-123",
  "title": "ABC-123: 로그인 페이지 유효성 검사",
  "approvalPolicy": "never",
  "sandboxPolicy": {"type": "workspaceWrite"}
}}
```

### Elixir 구현: AppServer 클라이언트

```elixir
defmodule SymphonyElixir.Codex.AppServer do
  @initialize_id 1
  @thread_start_id 2
  @turn_start_id 3

  # 세션 시작: initialize -> initialized -> thread/start
  def start_session(workspace, opts) do
    worker_host = Keyword.get(opts, :worker_host)

    with {:ok, expanded_workspace} <- validate_workspace_cwd(workspace, worker_host),
         {:ok, port} <- start_port(expanded_workspace, worker_host),
         {:ok, session_policies} <- session_policies(expanded_workspace, worker_host),
         {:ok, thread_id} <- do_start_session(port, expanded_workspace, session_policies) do
      {:ok, %{
        port: port,
        thread_id: thread_id,
        workspace: expanded_workspace,
        approval_policy: session_policies.approval_policy,
        thread_sandbox: session_policies.thread_sandbox,
        turn_sandbox_policy: session_policies.turn_sandbox_policy,
        auto_approve_requests: session_policies.approval_policy == "never"
      }}
    end
  end

  # 턴 실행: turn/start -> 스트리밍 -> turn/completed
  def run_turn(session, prompt, issue, opts) do
    on_message = Keyword.get(opts, :on_message, &default_on_message/1)

    case start_turn(session.port, session.thread_id, prompt, issue,
                    session.workspace, session.approval_policy,
                    session.turn_sandbox_policy) do
      {:ok, turn_id} ->
        session_id = "#{session.thread_id}-#{turn_id}"
        # 스트리밍 루프: 라인별 JSON 파싱 -> 이벤트 처리
        stream_until_completion(session.port, on_message, opts)

      {:error, reason} ->
        {:error, reason}
    end
  end
end
```

### AgentRunner의 멀티턴 루프

```elixir
defmodule SymphonyElixir.AgentRunner do
  defp run_codex_turns(workspace, issue, codex_update_recipient, opts, worker_host) do
    max_turns = Keyword.get(opts, :max_turns, Config.settings!().agent.max_turns)

    # 세션 시작 (initialize + thread/start)
    {:ok, session} = AppServer.start_session(workspace, worker_host: worker_host)

    try do
      # 첫 번째 턴: 전체 프롬프트
      prompt = PromptBuilder.build(issue, Config.settings!())
      run_turn_loop(session, prompt, issue, codex_update_recipient, opts, 1, max_turns)
    after
      AppServer.stop_session(session)
    end
  end

  defp run_turn_loop(session, prompt, issue, recipient, opts, turn_num, max_turns)
       when turn_num <= max_turns do
    case AppServer.run_turn(session, prompt, issue, opts) do
      {:ok, %{status: :completed}} ->
        # 이슈 상태 재확인
        case Tracker.fetch_issue_state(issue.id) do
          {:ok, state} when state in active_states ->
            # 활성 -> 연속 턴 (continuation guidance)
            continuation = "이전 턴 완료. 이슈 여전히 활성. 계속 진행."
            run_turn_loop(session, continuation, issue, recipient, opts, turn_num + 1, max_turns)

          _ ->
            # 비활성 -> 정상 종료
            :ok
        end

      {:ok, %{status: :failed}} ->
        raise "Turn #{turn_num} failed"

      {:error, reason} ->
        raise "Turn #{turn_num} error: #{inspect(reason)}"
    end
  end

  # max_turns 도달 -> 정상 종료 (Orchestrator가 continuation retry로 재확인)
  defp run_turn_loop(_session, _prompt, _issue, _recipient, _opts, _turn_num, _max_turns) do
    :ok
  end
end
```

### 스트리밍 이벤트 처리

턴 실행 중 stdout에서 수신하는 주요 이벤트:

```elixir
# 턴 완료 이벤트
defp handle_event(%{"method" => "turn/completed"} = msg, state) do
  usage = extract_usage(msg)
  emit(:turn_completed, %{usage: usage})
  {:completed, state}
end

# 턴 실패 이벤트
defp handle_event(%{"method" => "turn/failed"} = msg, state) do
  emit(:turn_failed, %{error: msg["params"]["error"]})
  {:failed, state}
end

# 승인 요청 -> 자동 승인 (approval_policy: "never"일 때)
defp handle_event(%{"method" => "notifications/approval_request"} = msg, state)
     when state.auto_approve_requests do
  approve(state.port, msg["params"]["id"])
  {:continue, state}
end

# 도구 호출 -> 지원 도구면 실행, 아니면 에러 반환
defp handle_event(%{"method" => "item/tool/call"} = msg, state) do
  tool_name = msg["params"]["name"]
  arguments = msg["params"]["arguments"]

  result = DynamicTool.execute(tool_name, arguments)
  send_tool_result(state.port, msg["id"], result)
  {:continue, state}
end
```

### Dynamic Tool: linear_graphql

Symphony가 Codex 세션에 제공하는 클라이언트 사이드 도구:

```elixir
defmodule SymphonyElixir.Codex.DynamicTool do
  @spec execute(String.t(), map()) :: {:ok, map()} | {:error, String.t()}
  def execute("linear_graphql", %{"query" => query} = args) do
    variables = Map.get(args, "variables", %{})

    # Symphony의 Linear API 키로 GraphQL 쿼리 실행
    case Linear.Client.graphql(query, variables) do
      {:ok, %{"data" => data}} ->
        {:ok, %{success: true, data: data}}

      {:ok, %{"errors" => errors}} ->
        {:ok, %{success: false, errors: errors}}

      {:error, reason} ->
        {:error, "Linear API error: #{inspect(reason)}"}
    end
  end

  # 미지원 도구 -> 에러 반환 (세션 유지)
  def execute(unknown_tool, _args) do
    {:error, "Unsupported tool: #{unknown_tool}"}
  end
end
```

### 샌드박스 정책 옵션

```yaml
# WORKFLOW.md에서 설정

codex:
  # 승인 정책 (AskForApproval)
  approval_policy: never              # 모든 것 자동 승인
  # approval_policy: on-failure       # 실패 시에만 승인 요청
  # approval_policy: on-request       # 매번 승인 요청
  # approval_policy:                  # 객체 형식 (세분화)
  #   reject:
  #     sandbox_approval: true
  #     rules: true
  #     mcp_elicitations: true

  # 세션 샌드박스 (SandboxMode)
  thread_sandbox: workspace-write     # 워크스페이스 내 쓰기만 허용
  # thread_sandbox: read-only         # 읽기 전용
  # thread_sandbox: danger-full-access # 전체 접근 (위험)

  # 턴별 샌드박스 정책 (SandboxPolicy)
  turn_sandbox_policy:
    type: workspaceWrite              # 워크스페이스 루트 기반 쓰기 제한
```

---

## ✅ 체크포인트

- [ ] App Server 핸드셰이크 4단계(initialize -> initialized -> thread/start -> turn/start)를 설명할 수 있는가?
- [ ] 첫 번째 턴과 연속 턴의 input 차이를 알고 있는가?
- [ ] session_id가 어떻게 구성되는지 아는가? (`<thread_id>-<turn_id>`)
- [ ] max_turns에 도달하면 어떻게 되는지 아는가?
- [ ] linear_graphql 동적 도구의 역할과 동작을 이해하는가?
- [ ] approval_policy "never"의 의미와 보안 영향을 이해하는가?

---

## ⚠️ 흔한 실수

| 실수 | 올바른 이해 |
|------|------------|
| 매 턴마다 Codex 프로세스를 새로 시작 | 동일 워커 실행 동안 **하나의 프로세스**에서 여러 턴 실행 |
| 연속 턴에서 전체 프롬프트를 다시 전송 | 연속 턴은 continuation guidance만 전송, 원래 프롬프트는 스레드 히스토리에 존재 |
| stderr를 프로토콜 메시지로 파싱 | stderr는 진단 용도. 프로토콜은 **stdout만** 사용 |
| 미지원 도구 호출 시 세션이 종료된다고 생각 | 에러 반환 후 세션은 **계속** 유지됨 |
| approval_policy "never"가 안전하다고 생각 | 고신뢰 환경 전용. 프로덕션에서는 신중하게 설정 필요 |

---

## 🔗 더 알아보기

- [[05-workspace-management|워크스페이스 관리]] - Codex가 실행되는 격리 환경
- [[03-orchestrator|오케스트레이터]] - Codex 이벤트를 처리하는 상위 레이어
- [Codex App Server 공식 문서](https://developers.openai.com/codex/app-server/)
- [Codex Harness 아키텍처](https://openai.com/index/unlocking-the-codex-harness/)
- [SPEC.md - Section 10: Agent Runner Protocol](https://github.com/openai/symphony/blob/main/SPEC.md#10-agent-runner-protocol-coding-agent-integration)
