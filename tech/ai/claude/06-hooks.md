---
date: 2026-01-24
tags:
  - tech
  - claude
  - hooks
  - automation
parent: "[[README]]"
---

# Claude Code - Hooks

> ⬅️ [[05-skills|이전: Skills]] | [[README|목차]] | ➡️ [[07-mcp|다음: MCP]]

---

## 1. Hooks란?

> Claude Code 라이프사이클의 특정 시점에서 실행되는 셸 명령어

### LLM vs Hooks

| 구분 | LLM 제안 | Hooks |
|------|----------|-------|
| 실행 | 비결정적 | 결정적 (항상 실행) |
| 신뢰도 | 가변적 | 100% |
| 용도 | 복잡한 판단 | 자동화, 검증 |

---

## 2. Hook 이벤트

### 사용 가능한 이벤트

| 이벤트 | 시점 | 용도 |
|--------|------|------|
| `PreToolUse` | 도구 실행 전 | 입력 수정, 차단 |
| `PostToolUse` | 도구 실행 후 | 포맷팅, 로깅 |
| `PermissionRequest` | 권한 요청 시 | 자동 승인/거부 |
| `UserPromptSubmit` | 사용자 입력 시 | 입력 전처리 |
| `PreCompact` | 컨텍스트 압축 전 | 보존할 내용 지정 |
| `Stop` | 에이전트 종료 시 | 정리 작업 |
| `SubagentStop` | 서브에이전트 종료 시 | 서브에이전트 정리 |
| `SessionStart` | 세션 시작 시 | 초기화 |
| `SessionEnd` | 세션 종료 시 | 정리 |
| `Notification` | 알림 발생 시 | 커스텀 알림 |

---

## 3. Hook 설정

### 설정 파일 위치

```
~/.claude/settings.json        # 전역
.claude/settings.local.json    # 프로젝트
```

### 기본 구조

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write",
        "command": "echo 'Writing file...'"
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Write",
        "command": "prettier --write $CLAUDE_FILE_PATH"
      }
    ]
  }
}
```

---

## 4. Hook 필드

### 주요 필드

| 필드 | 타입 | 설명 |
|------|------|------|
| `matcher` | string | 대상 도구 이름 (정규식 가능) |
| `command` | string | 실행할 셸 명령어 |
| `timeout` | number | 타임아웃 (ms) |

### Matcher 패턴

```json
{
  "matcher": "Write",           // 정확히 Write
  "matcher": "Write|Edit",      // Write 또는 Edit
  "matcher": ".*",              // 모든 도구
  "matcher": "Bash"             // Bash 명령어
}
```

---

## 5. 환경 변수

### PreToolUse / PostToolUse

| 변수 | 설명 |
|------|------|
| `$CLAUDE_TOOL_NAME` | 도구 이름 |
| `$CLAUDE_TOOL_INPUT` | 도구 입력 (JSON) |
| `$CLAUDE_FILE_PATH` | 파일 경로 (해당 시) |

### PostToolUse 전용

| 변수 | 설명 |
|------|------|
| `$CLAUDE_TOOL_OUTPUT` | 도구 출력 |
| `$CLAUDE_TOOL_EXIT_CODE` | 종료 코드 |

### 전역

| 변수 | 설명 |
|------|------|
| `$CLAUDE_SESSION_ID` | 세션 ID |
| `$CLAUDE_PROJECT_DIR` | 프로젝트 디렉터리 |

---

## 6. Hook 응답

### 응답 형식 (JSON)

```json
{
  "continue": true,
  "message": "사용자에게 표시할 메시지"
}
```

### 차단하기

```json
{
  "continue": false,
  "message": "이 작업은 허용되지 않습니다"
}
```

### 입력 수정하기 (v2.0.10+)

```json
{
  "continue": true,
  "modifiedInput": {
    "file_path": "/corrected/path.js"
  }
}
```

---

## 7. 실전 예시

### 자동 코드 포맷팅

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "command": "prettier --write $CLAUDE_FILE_PATH 2>/dev/null || true"
      }
    ]
  }
}
```

### 파일 보호

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write|Edit",
        "command": "node scripts/check-protected-files.js"
      }
    ]
  }
}
```

**check-protected-files.js:**

```javascript
const input = JSON.parse(process.env.CLAUDE_TOOL_INPUT);
const protectedFiles = ['.env', 'secrets.json', 'credentials.yaml'];

if (protectedFiles.some(f => input.file_path?.includes(f))) {
  console.log(JSON.stringify({
    continue: false,
    message: '보호된 파일은 수정할 수 없습니다'
  }));
} else {
  console.log(JSON.stringify({ continue: true }));
}
```

### 커밋 메시지 검증

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "command": "node scripts/validate-commit.js"
      }
    ]
  }
}
```

### 작업 로깅

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": ".*",
        "command": "echo \"$(date): $CLAUDE_TOOL_NAME\" >> ~/.claude/audit.log"
      }
    ]
  }
}
```

### 자동 권한 승인

```json
{
  "hooks": {
    "PermissionRequest": [
      {
        "matcher": "Read",
        "command": "echo '{\"decision\": \"allow\"}'"
      }
    ]
  }
}
```

---

## 8. 고급 패턴

### 조건부 실행

```bash
#!/bin/bash
# scripts/conditional-format.sh

FILE_PATH="$CLAUDE_FILE_PATH"
EXT="${FILE_PATH##*.}"

case "$EXT" in
  js|ts|jsx|tsx)
    prettier --write "$FILE_PATH"
    ;;
  py)
    black "$FILE_PATH"
    ;;
  go)
    gofmt -w "$FILE_PATH"
    ;;
esac

echo '{"continue": true}'
```

### 슬랙 알림

```json
{
  "hooks": {
    "Notification": [
      {
        "matcher": ".*",
        "command": "curl -X POST -d \"text=$CLAUDE_NOTIFICATION\" $SLACK_WEBHOOK"
      }
    ]
  }
}
```

---

## 9. 디버깅

### 로그 확인

```bash
# Hook 실행 로그
tail -f ~/.claude/logs/hooks.log
```

### 테스트 실행

```bash
# 환경 변수 설정 후 직접 테스트
CLAUDE_TOOL_NAME=Write \
CLAUDE_FILE_PATH=/tmp/test.js \
node scripts/my-hook.js
```

---

## 10. Best Practices

### DO ✅

- 빠른 실행 (타임아웃 주의)
- 에러 핸들링 철저히
- 로깅으로 디버깅 용이하게
- 멱등성 보장

### DON'T ❌

- 무거운 작업 (빌드 전체 등)
- 네트워크 의존 작업 (타임아웃)
- 사용자 입력 대기
- 무한 루프 가능성

---

## 다음 단계

> [!tip] 다음으로
> Hooks를 이해했다면 [[07-mcp|MCP]]에서 외부 도구 연동을 배워보세요.

---

## References

- [Claude Code Hooks 공식 문서](https://docs.anthropic.com/claude/docs/claude-code-hooks)
- [Hooks Quickstart Guide](https://code.claude.com/docs/en/hooks-guide.md)
