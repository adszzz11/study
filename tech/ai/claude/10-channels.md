---
date: 2026-03-28
tags:
  - tech
  - ai
  - claude
  - claude-code
  - channels
  - workflow
status: learning
type: tech-series
---

# Claude Code Channels

## 1. What - 개념 정의

> **한 줄 정의**: Claude Code 세션을 Telegram, Discord, iMessage 등 메시징 앱과 연결하여 모바일에서 원격으로 코딩 지시를 내릴 수 있는 기능

### 핵심 개념

- **2026년 3월 20일** 리서치 프리뷰로 발표
- 로컬에서 실행 중인 Claude Code 세션에 메시징 앱을 통해 메시지를 보내면, Claude가 로컬 환경(파일, 도구, git 등)을 활용해 작업을 수행하고 같은 채널로 응답
- MCP(Model Context Protocol) 서버 기반 양방향 통신 아키텍처
- 세션은 로컬 머신에서 유지되고, 메시징 앱은 단순히 인터페이스 역할

### 주요 용어

| 용어 | 설명 |
|------|------|
| Channel | Claude Code와 메시징 플랫폼을 연결하는 통신 경로 |
| MCP Server | 메시징 플랫폼과 Claude Code 간의 메시지를 중계하는 서버 |
| Pairing Code | 메시징 앱 계정을 Claude Code 세션에 연결하는 6자리 인증 코드 |
| Sender Allowlist | 메시지를 보낼 수 있는 허용된 사용자 목록 |
| Permission Relay | 도구 승인 프롬프트를 휴대폰으로 전달하는 기능 |

---

## 2. Why - 등장 배경 & 필요성

### 해결하려는 문제

- 개발자가 터미널 앞에 없을 때도 Claude Code에 작업을 지시하고 싶은 니즈
- CI 결과, 모니터링 알림 등 이벤트 발생 시 Claude가 자동 대응하도록 하고 싶음
- 이동 중에도 코드 리뷰, 빌드 트리거 등 개발 워크플로우 관리 필요

### 기존 방식의 한계

- Claude Code는 터미널 직접 접근이 필수
- 모바일에서 SSH 접속은 불편하고 제한적
- 비동기 작업 관리가 불가능

---

## 3. How - 동작 원리

### 아키텍처

```
┌─────────────┐     ┌─────────────┐     ┌──────────────────┐
│   Mobile     │     │  MCP Server  │     │  Claude Code     │
│  (Telegram/  │────▶│  (Plugin)    │────▶│  (Local Session) │
│   Discord/   │◀────│              │◀────│                  │
│   iMessage)  │     └─────────────┘     │  - 파일시스템     │
└─────────────┘                          │  - Git            │
                                         │  - MCP Tools      │
                                         └──────────────────┘
```

### 동작 흐름

1. 로컬에서 `claude --channels plugin:telegram@claude-plugins-official` 로 세션 시작
2. 메시징 앱에서 봇에게 DM으로 메시지 전송
3. MCP 서버가 메시지를 수신하여 Claude Code 세션으로 전달
4. Claude가 로컬 환경(파일, 도구, git)을 사용해 작업 수행
5. 결과를 같은 채널로 응답

### 지원 플랫폼별 특징

| 플랫폼 | 특징 | 제한 |
|--------|------|------|
| **Telegram** | 5분 설정, 파일 첨부(50MB), 사진 자동 다운로드 | 메시지 히스토리 API 없음 |
| **Discord** | 메시지 히스토리(100개), 길드 채널 지원, 스레드 지원 | 설정 10분, 봇 권한 설정 필요 |
| **iMessage** | 외부 서비스 불필요, 네이티브 macOS 통합 | macOS 전용, Full Disk Access 필요 |

---

## 4. 실무 적용

### Telegram 설정 (5분)

```bash
# 1. @BotFather에서 봇 생성 → 토큰 복사

# 2. 플러그인 설치
/plugin install telegram@claude-plugins-official

# 3. 토큰 설정
/telegram:configure [your-token]

# 4. 채널 모드로 재시작
claude --channels plugin:telegram@claude-plugins-official

# 5. 텔레그램에서 봇에 DM → 페어링 코드 받기
/telegram:access pair [6자리코드]

# 6. 보안 설정 (허용 목록 모드)
/telegram:access policy allowlist
```

### Discord 설정 (10분)

```bash
# 1. Discord Developer Portal에서 앱/봇 생성
#    - Message Content Intent 활성화
#    - OAuth2로 서버에 봇 초대 (bot scope + 필요 권한)

# 2. 플러그인 설치 & 설정
/plugin install discord@claude-plugins-official
/discord:configure [bot-token]

# 3. 채널 모드로 재시작
claude --channels plugin:discord@claude-plugins-official

# 4. Discord에서 봇에 DM → 페어링
/discord:access pair [6자리코드]
```

### iMessage 설정 (macOS 전용)

```bash
# 1. System Settings → Privacy & Security → Full Disk Access → 터미널 앱 활성화

# 2. 플러그인 설치
/plugin install imessage@claude-plugins-official

# 3. 채널 모드로 재시작
claude --channels plugin:imessage@claude-plugins-official

# 4. 자신에게 메시지 보내서 테스트 (별도 설정 불필요)

# 5. 다른 발신자 허용
/imessage:access allow +821012345678
```

### 사용 사례

- 이동 중 코드 리뷰 요청: "PR #42 리뷰해줘"
- CI 실패 시 원격 디버깅: "최근 테스트 실패 원인 분석해줘"
- 빠른 코드 수정: "config.ts에서 API URL 스테이징으로 변경해줘"
- 모니터링 알림 대응: 웹훅으로 알림 수신 → 자동 분석

### Best Practices

- `policy allowlist`로 허용된 사용자만 접근 가능하게 설정
- 프로덕션 환경에서는 `--dangerously-skip-permissions` 사용 금지
- 중요 작업은 권한 승인 프롬프트를 통해 확인 후 실행

### Anti-patterns (주의사항)

- ❌ 세션이 종료되면 채널도 중단됨 (백그라운드 상시 실행 모드 없음)
- ❌ API 키 로그인은 지원하지 않음 (claude.ai 계정만 가능)
- ❌ 리서치 프리뷰 단계에서 `claude-plugins-official`만 허용

---

## 5. 요구사항 & 제한

| 항목 | 내용 |
|------|------|
| Claude Code 버전 | v2.1.80 이상 |
| 런타임 | Bun 설치 필요 |
| 인증 | claude.ai Pro/Max 구독 (API 키 미지원) |
| 조직 | Teams/Enterprise는 관리자가 명시적으로 활성화 필요 |
| 상태 | 리서치 프리뷰 (2026-03) |

---

## 6. 학습 체크리스트

### 이해도 점검

- [ ] Channels가 무엇이고 어떤 문제를 해결하는지 설명할 수 있다
- [ ] MCP 기반 아키텍처를 이해하고 동작 흐름을 설명할 수 있다
- [ ] Telegram/Discord/iMessage 중 하나를 설정해볼 수 있다
- [ ] 보안 설정(allowlist, permission relay)을 이해한다

### 실습 과제

- [ ] Telegram 봇 생성 후 Claude Code Channels 연동해보기
- [ ] 모바일에서 간단한 코드 수정 지시해보기
- [ ] 권한 승인 프롬프트 동작 확인하기

---

## 7. References

- [Claude Code Channels 공식 문서](https://code.claude.com/docs/en/changelog)
- [The Decoder - Claude Code Channels 소개](https://the-decoder.com/anthropic-turns-claude-code-into-an-always-on-ai-agent-with-new-channels-feature/)
- [Claude Code Channels 가이드](https://claudefa.st/blog/guide/development/claude-code-channels)
- 관련 노트: [[03-claude-code]], [[07-mcp]], [[11-cowork-dispatch]]
