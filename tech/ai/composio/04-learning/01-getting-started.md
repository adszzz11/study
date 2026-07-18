---
date: 2026-07-19
tags: [tech]
type: tech-tool-study
status: draft
---

# Composio — Getting Started

> [[../03-references|이전: References]] · [[../README|목차]] · [[02-deep-dive|다음: Deep Dive]]

## Goal

첫 실습의 목표는 “agent가 Gmail을 쓴다”가 아니라 다음 경계를 확인하는 것이다.

1. application user를 안정적인 `user_id`로 매핑한다.
2. 허용할 toolkit/tool을 좁힌 Session을 만든다.
3. 해당 user의 Connected Account를 hosted link/OAuth로 연결한다.
4. read-only action으로 schema와 execution log를 확인한다.
5. Session ID를 저장하고 다음 turn에서 복구한다.

> [!warning] Version-aware 실습
> Composio SDK는 pre-1.0이고 API가 바뀔 수 있다. 아래 흐름과 pseudocode를 mental model로 사용하고, 실제 method signature는 설치한 version의 공식 quickstart/changelog에 맞춘다.

## 1. Choose the Path

| 질문 | 선택 |
|---|---|
| application process에서 hook/custom tool이 필요한가? | Provider SDK |
| MCP-compatible client에 빠르게 붙일 것인가? | Hosted MCP |
| backend가 tool과 arguments를 정확히 아는가? | Direct execution |
| 사용자의 자유형 intent를 여러 app에 연결할 것인가? | Dynamic Session |

이 실습은 **Provider SDK + Dynamic Session**을 기준으로 한다.

## 2. Install and Pin

```bash
# Python 예시: 조사 시점 version을 명시적으로 pin
python -m pip install "composio==0.18.0"

# TypeScript 예시: 실제 project package manager로 lockfile 생성
npm install @composio/core@0.13.1
```

API key는 source code나 vault에 저장하지 않는다.

```bash
export COMPOSIO_API_KEY="..."
```

production에서는 secret manager를 사용하고 log/redaction policy를 확인한다.

## 3. Define Identity and Access

`user_id`는 email처럼 바뀔 수 있는 display identifier보다 application DB의 immutable ID를 사용한다.

```yaml
session_policy:
  user_id: "usr_01J..."
  allowed_toolkits:
    - gmail
  allowed_tools:
    - GMAIL_FETCH_EMAILS
  write_actions: false
  connected_account: null  # 연결 후 의도한 account를 pin
```

첫 실습에서 `GMAIL_SEND_EMAIL` 같은 write action을 열지 않는다. 먼저 read-only tool로 tenant isolation과 log를 검증한다.

## 4. Create a Session

현재 SDK의 exact signature 대신 변하지 않는 설계 순서를 pseudocode로 표현하면 다음과 같다.

```python
# Pseudocode — installed SDK version의 공식 docs에 맞게 치환
composio = Composio(api_key=env("COMPOSIO_API_KEY"))

session = composio.sessions.create(
    user_id=current_user.id,
    toolkits=["gmail"],
    tools=["GMAIL_FETCH_EMAILS"],
)

database.save_session(
    app_user_id=current_user.id,
    composio_session_id=session.id,
)
```

중요한 invariant:

```text
authenticated app user == stored session owner == Composio session user_id
```

Session ID를 client가 임의로 전달하게 두지 말고 server-side mapping을 통해 복구한다.

## 5. Authorize the User

연결이 없다면 Session의 `authorize()` 또는 hosted `link()` 흐름으로 Connect Link를 만들고 browser OAuth를 완료한다.

```python
# Pseudocode
link = session.authorize(toolkit="gmail", redirect_url=CALLBACK_URL)
return redirect(link.url)
```

OAuth callback 후 확인할 것:

- callback의 application state/nonce가 일치하는가?
- Connected Account의 owner가 현재 user와 일치하는가?
- 요청 scope가 최소 권한인가?
- 복수 account가 있으면 선택한 Connected Account를 Session에 pin했는가?

오래된 `initiate()` 예제를 그대로 사용하지 말고 현재 `authorize()`/`link()` 문서를 확인한다.

## 6. Discover and Execute

Agent에게 주는 instruction은 tool 이름을 강제하기보다 authorization과 side-effect boundary를 명확히 한다.

```text
최근 Gmail 메시지의 subject만 조회하라.
읽기 작업만 허용된다.
연결이 없으면 connection flow를 요청하라.
어떤 메시지도 전송, 수정, 삭제하지 마라.
```

Dynamic Session의 개념적 흐름:

```text
COMPOSIO_SEARCH_TOOLS
  -> GMAIL_FETCH_EMAILS 발견
COMPOSIO_GET_TOOL_SCHEMAS
  -> required input 확인
COMPOSIO_MULTI_EXECUTE_TOOL
  -> pinned Connected Account로 실행
```

관찰할 log:

- session/user/connected-account 식별자가 예상과 일치하는가?
- 검색된 tool이 allowlist 안에 있는가?
- input/output schema가 예상과 같은가?
- token, email body 등 sensitive field가 log에 노출되는가?
- timeout/rate limit/error가 structured하게 반환되는가?

## 7. Reuse the Session

다음 turn에서는 새 Session을 무조건 만들지 않고 저장한 ID를 복구한다.

```python
# Pseudocode
session_id = database.get_session_id(app_user_id=current_user.id)
assert database.owner_of(session_id) == current_user.id

session = composio.use(session_id)
```

재사용 시 tool memory, MCP state, sandbox files가 이어질 수 있으므로 retention과 conversation boundary를 명시한다.

## 8. Safe Write Action

read-only 검증 후에만 write tool을 별도 단계로 연다.

```text
draft -> show exact recipients/body -> human approval -> execute once -> audit
```

```yaml
approval_record:
  user_id: usr_01J...
  tool: GMAIL_SEND_EMAIL
  arguments_hash: sha256:...
  approved_at: 2026-07-19T12:00:00Z
  idempotency_key: msg_...
```

approval 이후 arguments가 달라지면 재승인한다. timeout 뒤 무조건 retry하지 말고 remote side effect가 이미 발생했는지 먼저 확인한다.

## Completion Checklist

- [ ] SDK version을 pin하고 changelog를 확인했다.
- [ ] immutable application `user_id`를 사용했다.
- [ ] 한 toolkit과 read-only tool만 허용했다.
- [ ] Connect Link/OAuth callback의 state와 owner를 검증했다.
- [ ] 복수 account를 명시적으로 pin했다.
- [ ] Session ID를 server-side user mapping으로 저장·복구했다.
- [ ] write action에 preview, approval, idempotency를 설계했다.

## Sources

- https://docs.composio.dev/docs
- https://docs.composio.dev/docs/how-composio-works
- https://docs.composio.dev/docs/configuring-sessions
- https://docs.composio.dev/docs/auth-configuration/connected-accounts
- https://docs.composio.dev/reference/changelog

