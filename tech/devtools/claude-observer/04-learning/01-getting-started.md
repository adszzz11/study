---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# Claude Observer Getting Started

## 목표

실제 업무 repository나 민감한 command를 사용하기 전에, 격리된 test repository에서 hook 등록·상태 전환·permission 처리·제거 절차를 검증한다.

## 1. 설치 전 확인

- [ ] macOS 환경인지 확인
- [ ] 현재 Claude Code version과 공식 hook event 지원 범위 확인
- [ ] repository의 최신 README와 source를 읽고 build/install 절차 확인
- [ ] license 존재 여부와 조직 내 사용 가능성 확인
- [ ] `~/.claude/settings.json` backup 준비
- [ ] Web Dashboard는 초기 평가에서 비활성화

설치 과정은 Python hook script를 `~/.claude-observer/hooks/`에 두고 Claude Code settings에 hook을 등록한다. 정확한 명령과 요구사항은 version에 따라 달라질 수 있으므로 repository의 최신 설치 안내를 따른다.

## 2. 변경 지점 이해

예상되는 local state는 다음과 같다.

```text
~/.claude/settings.json                  # Claude Code hook 등록
~/.claude-observer/hooks/               # Python hook handler
~/.claude-observer/sessions/            # session별 transient JSON
~/.claude-observer/personalities.json   # repository별 crab 이름
```

설치 전후에 settings diff를 확인한다. 기존 hook을 덮어쓰지 않고 event별 hook 배열에 병합되는지가 중요하다.

## 3. UI 실행 모드 선택

- 기본 mode: 화면 상단 중앙의 floating panel
- `--menubar` 또는 `--statusbar`: macOS status item과 dropdown panel

처음에는 Web Dashboard 없이 local UI만 실행해 권한 경계와 상태 흐름을 좁게 검증한다.

## 4. 상태 전환 실습

별도 test repository에서 Claude Code session 하나를 열고 다음 순서로 관찰한다.

| 실습 | 기대 상태 |
|---|---|
| session 시작 | crab/session 생성 |
| prompt 제출 | `working` |
| 응답 정상 완료 | `idle` |
| 사용자 입력 notification | `needs_input` |
| 승인 필요한 tool 요청 | `needs_permission` |
| session 종료 | session JSON 제거 |

상태 표시가 맞지 않으면 먼저 session JSON의 갱신 시각과 hook 등록을 확인한다. native app은 약 2초 polling을 사용하므로 즉시 반영되지 않을 수 있다.

## 5. Permission 안전 실습

처음에는 영향이 작은 read-only 요청으로 Yes/No 흐름을 시험한다.

- `No`가 tool 실행을 실제로 막는지 확인한다.
- Yes가 현재 요청에만 적용되는지 확인한다.
- `Allow all`은 test session에서도 가급적 사용하지 않는다.
- 기존 matching `deny` rule이 hook의 allow보다 우선하는지 공식 permissions 문서와 함께 확인한다.
- permission request가 120초 후 timeout될 때 기본 동작을 확인한다.

> [!warning]
> `Allow all Bash`는 넓은 실행 권한을 만들 수 있다. 가능하면 command, path, domain 단위의 좁은 rule을 사용한다.

## 6. Web Dashboard 평가

기본 port는 `9321`이다. mobile 접근을 켜기 전에 source와 실제 listen socket으로 다음을 확인한다.

- bind address가 loopback인지 LAN 전체인지
- authentication과 session protection이 있는지
- TLS를 어떻게 제공하는지
- HTTP action에 CSRF 방어가 있는지
- WebSocket이 Origin을 검증하는지
- port forwarding, public Wi-Fi, 회사 LAN 노출 가능성이 없는지

확인 전에는 Internet에 공개하거나 port forwarding하지 않는다.

## 7. Rollback 계획

1. Observer app과 Web Dashboard를 종료한다.
2. `~/.claude/settings.json`에서 Observer hook entry만 제거한다.
3. backup과 비교해 기존 hook이 보존됐는지 확인한다.
4. 더 이상 필요 없다면 Observer가 만든 local directory를 검토 후 제거한다.
5. 새 Claude Code session을 열어 hook error가 없는지 확인한다.

## Sources

- https://github.com/svenliebig/claude-observer#readme
- https://code.claude.com/docs/en/hooks
- https://code.claude.com/docs/en/permissions

