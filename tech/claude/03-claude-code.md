---
date: 2026-01-24
tags:
  - tech
  - practice
  - claude
  - cli
parent: "[[README]]"
---

# Claude - Claude Code

> ⬅️ [[02-api|이전: API]] | [[README|목차]] | ➡️ [[04-advanced|다음: 심화]]

---

## 1. Claude Code란?

> Anthropic 공식 CLI 도구로, 터미널에서 Claude와 대화하며 코딩 작업 수행

### 주요 기능

- 터미널 기반 AI 어시스턴트
- 파일 읽기/쓰기/편집
- 명령어 실행
- 프로젝트 컨텍스트 이해

---

## 2. 설치

### macOS

```bash
# Homebrew로 설치
brew install anthropic/tap/claude-code

# 또는 npm으로 설치
npm install -g @anthropic-ai/claude-code
```

### 인증

```bash
# 대화형 로그인
claude login

# 또는 API Key 직접 설정
export ANTHROPIC_API_KEY="sk-ant-..."
```

---

## 3. 기본 사용법

### 시작하기

```bash
# 현재 디렉터리에서 시작
claude

# 특정 디렉터리에서 시작
claude /path/to/project
```

### 주요 슬래시 명령어

| 명령어 | 설명 |
|--------|------|
| `/help` | 도움말 표시 |
| `/clear` | 대화 내역 초기화 |
| `/compact` | 컨텍스트 압축 |
| `/cost` | 현재 세션 비용 확인 |
| `/doctor` | 설정 진단 |
| `/init` | CLAUDE.md 생성 |
| `/vim` | vim 모드 토글 |

### 키보드 단축키

| 단축키 | 설명 |
|--------|------|
| `Ctrl+C` | 현재 작업 중단 |
| `Ctrl+D` | 세션 종료 |
| `Escape` | 입력 취소 |
| `↑/↓` | 이전/다음 입력 |

---

## 4. CLAUDE.md

### 목적

프로젝트의 컨텍스트를 Claude에게 제공하는 설정 파일

### 생성

```bash
claude
> /init
```

### 예시 내용

```markdown
# CLAUDE.md

This file provides guidance to Claude Code.

## Project Overview
Node.js 기반 REST API 서버

## Commands
- `npm run dev`: 개발 서버 실행
- `npm test`: 테스트 실행
- `npm run build`: 프로덕션 빌드

## Architecture
- src/controllers/: API 컨트롤러
- src/services/: 비즈니스 로직
- src/models/: 데이터 모델
```

---

## 5. 실전 사용 예시

### 코드 분석

```
> 이 프로젝트의 구조를 설명해줘
```

### 파일 편집

```
> src/utils/helper.js에 formatDate 함수 추가해줘
```

### 버그 수정

```
> npm test 실행하고 실패하는 테스트 수정해줘
```

### Git 작업

```
> 변경사항 확인하고 커밋 메시지 작성해줘
```

---

## 6. 설정

### 전역 설정 위치

```
~/.claude/settings.json
```

### 주요 설정 항목

```json
{
  "model": "claude-sonnet-4-20250514",
  "theme": "dark",
  "permissions": {
    "allow_file_write": true,
    "allow_bash": true
  }
}
```

### 프로젝트별 설정

```
.claude/settings.local.json
```

---

## 7. 권한 모드

### 기본 권한

- 파일 읽기: 항상 허용
- 파일 쓰기: 확인 필요
- 명령어 실행: 확인 필요

### 권한 프롬프트

```
Claude wants to write to: src/index.js
Allow? [y/n/always]
```

### Trust 모드

```bash
# 모든 권한 자동 승인 (주의!)
claude --dangerously-skip-permissions
```

---

## 8. 팁

### DO ✅

- CLAUDE.md를 상세히 작성
- 작은 단위로 작업 요청
- 변경 전 확인 습관화
- 컨텍스트가 커지면 `/compact`

### DON'T ❌

- 민감한 정보 포함 금지 (API 키 등)
- 대규모 리팩토링 한 번에 요청
- 검증 없이 프로덕션 배포

---

## 9. 트러블슈팅

| 문제 | 원인 | 해결 |
|------|------|------|
| 인증 실패 | API 키 만료 | `claude logout` 후 재로그인 |
| 느린 응답 | 큰 컨텍스트 | `/compact` 실행 |
| 파일 못 찾음 | 잘못된 경로 | 절대 경로 사용 |

---

## 다음 단계

> [!tip] 다음으로
> Claude Code에 익숙해졌다면 [[04-advanced|심화 학습]]에서 프롬프트 엔지니어링을 배워보세요.

---

## References

- [Claude Code 공식 문서](https://docs.anthropic.com/claude/docs/claude-code)
- [GitHub - Claude Code](https://github.com/anthropics/claude-code)
