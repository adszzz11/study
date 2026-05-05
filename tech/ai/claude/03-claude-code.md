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

## 10. 릴리즈 노트

### v2.1.128 (2026-05-04)

**신규 기능:**
- `/color` (인자 없이) 실행 시 세션 색상 랜덤 선택
- `/mcp` 명령어에 연결된 서버별 툴 수 표시 및 툴 0개 서버 플래그 표시
- `--plugin-dir`이 디렉터리 외 `.zip` 플러그인 아카이브도 지원
- `--channels`가 콘솔(API 키) 인증과 함께 동작
- `/model` 피커에 Opus 4.7 항목 접힌 형태로 업데이트
- MCP 서버 재연결 시 전체 툴 목록 대신 서버 prefix 기준 요약 표시
- `EnterWorktree`가 로컬 HEAD에서 브랜치 생성 (미푸시 커밋 보존)
- Auto 모드 분류 오류에 힌트 포함 (retry, `/compact`, `--debug`)

**보안 수정:**
- 서브프로세스가 `OTEL_*` 환경변수 상속하지 않도록 수정
- MCP `workspace`를 예약 서버명으로 지정

**버그 수정:**
- Focus mode 딤 처리가 새 프롬프트 제출 시 발생하던 문제 수정
- 드래그 앤 드롭 이미지 업로드 멈춤 수정
- 대용량 stdin 입력(>10 MB) 크래시 루프 수정
- 풀스크린 모드에서 긴 URL 개별 클릭 불가 수정
- 읽기 전용 명령어 실패 시 병렬 셸 툴 호출 전체 취소 수정
- 재개된 세션에서 인자 없이 `/rename` 실행 시 오류 수정
- MCP stdio 서버가 공백/메타문자 포함 인자를 손상하여 수신하던 문제 수정
- 서브에이전트 진행 요약에서 프롬프트 캐시 정보 누락 수정
- `/plugin update`가 npm 소스 플러그인 신버전 미감지 수정

---

### v2.1.126 (2026-05-01)

**신규 기능:**
- `claude project purge [path]`: 프로젝트의 모든 Claude Code 상태 삭제 (`--dry-run`, `-y`, `-i`, `--all` 지원)
- `/model` 피커에서 게이트웨이(`ANTHROPIC_BASE_URL`) `/v1/models` 목록 표시
- `claude auth login`에서 WSL2/SSH/컨테이너 환경용 터미널 OAuth 코드 붙여넣기 지원
- Windows: PowerShell 7 (Store/MSI/.NET global tool) 자동 감지, 기본 셸로 사용
- Auto 모드에서 권한 확인 지연 시 스피너 빨간색으로 전환

**보안 수정:**
- `allowManagedDomainsOnly`/`allowManagedReadPathsOnly`가 상위 managed-settings에 `sandbox` 블록 없을 때 무시되던 버그 수정
- `--dangerously-skip-permissions`가 `.claude/`, `.git/`, `.vscode/`, 셸 설정 파일 쓰기 프롬프트 우회

**버그 수정:**
- 느린 연결/IPv6 전용 devcontainer OAuth 로그인 실패 수정
- Mac 슬립 후 "Stream idle timeout" 오류 수정
- 2000px 초과 이미지 붙여넣기 시 자동 다운스케일

---

### v2.1.123 (2026-04-29)

**버그 수정:**
- `CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS=1` 설정 시 OAuth 인증 401 재시도 루프 수정

---

### v2.1.122 (2026-04-28)

**신규 기능:**
- `ANTHROPIC_BEDROCK_SERVICE_TIER` 환경변수: Bedrock 서비스 티어 선택 지원
- `/resume` 검색창에 PR URL 붙여넣기로 GitHub·GitLab·Bitbucket 세션 탐색
- MCP 중복 서버 자동 감지 및 제거 힌트 제공

**버그 수정:**
- 이미지 리사이징 최대 크기 수정 (2576px → 2000px)
- Vertex AI·Bedrock 구조화 출력 오류 수정
- 보이스 모드 키바인딩 문제 수정

---

### v2.1.121 (2026-04-28)

**신규 기능:**
- MCP 서버 설정에 `alwaysLoad: true` 옵션 추가 (툴 검색 지연 건너뜀)
- `claude plugin prune` 명령어: 고아 플러그인 의존성 정리
- `/skills` 타입-to-필터 검색 박스
- PostToolUse 훅이 모든 툴의 출력 내용 교체 가능
- 풀스크린 스크롤 개선 및 스크롤 가능한 다이얼로그 지원

**버그 수정:**
- `/usage` 페이지 2GB+ 메모리 누수 수정
- 이미지 처리 관련 메모리 누수 수정

---

### v2.1.120 (2026-04-25)

**신규 기능:**
- Windows에서 Git Bash 없이 PowerShell을 Shell 툴로 사용 가능
- `claude ultrareview` CLI 명령어: CI/스크립트에서 `/ultrareview` 비인터랙티브 실행 지원
  - `--json` 플래그로 raw JSON 출력
  - 완료 시 exit code 0, 실패 시 exit code 1
- Skills에서 `${CLAUDE_EFFORT}` 변수로 현재 effort 레벨 참조 가능
- 서브프로세스에 `AI_AGENT` 환경변수 설정 (Claude Code 트래픽 귀속용)

**버그 수정:**
- stdio MCP 툴 호출 중 Esc 키가 서버 연결 전체를 닫던 문제 수정
- `--resume` 후 `/rewind` 및 인터랙티브 오버레이가 키보드 입력에 반응하지 않던 문제 수정
- 비풀스크린 모드에서 터미널 scrollback 중복 표시 수정
- `DISABLE_TELEMETRY`가 usage metrics를 억제하지 않던 문제 수정

---

### v2.1.119 (2026-04-23)

**신규 기능:**
- `/config` 설정이 `~/.claude/settings.json`에 영속 저장 (프로젝트/로컬/정책 우선순위 적용)
- `prUrlTemplate` 설정: 커스텀 코드 리뷰 URL 지정
- `CLAUDE_CODE_HIDE_CWD` 환경변수
- `--from-pr`이 GitLab, Bitbucket, GitHub Enterprise URL 허용
- 훅 페이로드에 `duration_ms` (툴 실행 시간) 추가
- PowerShell 툴 명령어 자동 승인 지원

**버그 수정:**
- CRLF 붙여넣기, MCP OAuth, 플러그인 관리 수정

---

### v2.1.118 (2026-04-23)

**신규 기능:**
- Vim visual mode: `v` (character), `V` (line)
- `/cost` + `/stats` → `/usage`로 통합
- 커스텀 테마 생성 (`/theme` 또는 `~/.claude/themes/`)
- 훅에서 MCP 툴 직접 호출: `type: "mcp_tool"`
- `DISABLE_UPDATES` 환경변수
- WSL에서 Windows 측 managed settings 상속
- Auto 모드 `"$defaults"` 지원

---

### v2.1.108 (2026-04-14)

**신규 기능:**
- 프롬프트 캐시 TTL 환경변수: `ENABLE_PROMPT_CACHING_1H` (1시간), `FORCE_PROMPT_CACHING_5M` (5분 강제)
- `/recap` 명령어: 세션 복귀 시 컨텍스트 요약 자동 제공
- Skill 툴로 `/init`, `/review`, `/security-review` 자동 발견·호출
- `/undo`: `/rewind` 별칭 추가
- `/resume` 피커: 현재 디렉토리 세션 기본 표시 (Ctrl+A로 전체)

**개선 사항:**
- 언어 문법 온디맨드 로딩으로 메모리 사용량 감소
- Ctrl+O 상세 뷰에 "verbose" 인디케이터

**버그 수정:**
- `/login` 붙여넣기 회귀 수정, 다이어크리틱 문자 누락 수정
- 프롬프트 캐싱 비활성 시 시작 경고 추가

---

### v2.1.107 (2026-04-14)

**개선 사항:**
- 장시간 작업 중 thinking 힌트 더 일찍 표시

---

### v2.1.105 (2026-04-13)

**신규 기능:**
- `EnterWorktree` 툴에 `path` 파라미터 추가 (기존 worktree 전환)
- PreCompact 훅 지원 (차단 가능, 종료 코드 2 또는 `{"decision":"block"}`)
- 플러그인 `monitors` manifest 키로 백그라운드 Monitor 지원
- 스킬 설명 길이 250자 → 1,536자로 확대
- API 스트림 5분 비활성 시 자동 중단

**개선 사항:**
- `WebFetch` 에서 `<style>`/`<script>` 내용 제거 (CSS 과다 페이지 대응)
- `/doctor` UI에 상태 아이콘 추가 (`f` 키로 자동 수정)
- MCP 대용량 출력 포맷별 스마트 축약 (JSON → `jq` 등)

**버그 수정:**
- 큐 메시지 이미지 첨부 소실, ASCII art 앞 공백 제거, 화면 blank, `alt+enter` 오작동 등 다수 UI 수정
- 429 rate-limit raw JSON 노출, stdio MCP hang, headless 세션 MCP 툴 누락 수정
- SSH/mosh 환경 16색 팔레트 바랜 색상, plan mode `acceptEdits` 권한 다운그레이드 수정

---

### v2.1.101 (2026-04-10)

**추가 기능:**
- `/team-onboarding` 명령어: 로컬 사용 기록 기반 팀원 온보딩 가이드 자동 생성
- OS CA 인증서 저장소 신뢰: 엔터프라이즈 TLS 프록시 기본 지원 (`CLAUDE_CODE_CERT_STORE=bundled`로 번들 CA만 사용)
- `/ultraplan` 및 원격 세션에서 클라우드 환경 자동 생성

**개선 사항:**
- Brief mode 재시도, Focus mode 자체 완결 요약, Rate-limit 피드백 상세화
- `/resume`이 세션 제목으로 검색 지원
- `allowManagedHooksOnly` 설정 시 강제 플러그인 훅 실행

**보안 수정:**
- LSP 바이너리 감지 `which` 폴백 커맨드 인젝션 취약점 수정

**버그 수정:**
- 메모리 누수(장시간 세션, Bedrock 인증 실패) 수정
- `permissions.deny` 규칙이 `PreToolUse` 훅 재정의하지 않던 문제 수정
- 서브에이전트 MCP 툴 상속, 격리 worktree 파일 접근, Bash 샌드박싱 수정
- `/resume` 피커 다수 UI 개선

---

### v2.1.97 (2026-04-08)

**추가 기능:**
- `Ctrl+O` Focus view 토글 (NO_FLICKER 모드에서 프롬프트·툴 요약·응답 집중 뷰)
- `refreshInterval` statusline 설정: N초마다 자동 재실행
- `/agents`에서 `● N running` 서브에이전트 수 표시기
- Cedar 정책 파일(`.cedar`, `.cedarpolicy`) 문법 강조

**보안 수정:**
- Bash 툴 권한 하드닝, permission rule JS 프로토타입 매칭 버그 수정
- MCP 연결 버퍼 관리 강화

**버그 수정:**
- `/resume` 피커 및 파일 편집 diff 사라지는 문제
- 서브에이전트 작업 디렉토리 부모 세션 누출
- NO_FLICKER 렌더링 다수 수정

---

### v2.1.96 (2026-04-08)

**버그 수정:**
- Bedrock 요청 403 "Authorization header is missing" 회귀 수정 (`AWS_BEARER_TOKEN_BEDROCK` / `CLAUDE_CODE_SKIP_BEDROCK_AUTH` 사용 시)

---

### v2.1.86 (2026-03-27)

**추가 기능:**
- API 요청에 `X-Claude-Code-Session-Id` 헤더 추가 → 프록시 집계 용이
- VCS 디렉터리 제외 목록에 `.jj` (Jujutsu), `.sl` (Sapling) 추가

**버그 수정:**
- `--resume` 시 "tool_use ids were found without tool_result blocks" 오류 수정
- 조건부 skill 설정 시 프로젝트 루트 외부 파일에서 Write/Edit/Read 실패 수정
- 불필요한 config 디스크 쓰기로 인한 Windows 성능 저하 및 잠재적 파일 손상 수정
- `/feedback` 사용 시 긴 세션에서 out-of-memory 크래시 수정
- `--bare` 모드에서 인터랙티브 세션의 MCP 도구가 드롭되는 문제 수정
- OAuth 로그인 URL이 ~20자로 잘려서 복사되던 문제 수정
- 좁은 터미널에서 마스킹된 입력이 토큰 시작 부분을 노출하는 문제 수정
- macOS/Linux에서 공식 marketplace 플러그인 스크립트 permission denied 오류 수정
- 멀티 인스턴스 환경에서 statusline이 잘못된 모델을 표시하는 문제 수정

---

### v2.1.85 (2026-03-26)

**추가 기능:**
- MCP 헬퍼를 위한 환경 변수 추가: `CLAUDE_CODE_MCP_SERVER_NAME`, `CLAUDE_CODE_MCP_SERVER_URL`
- 훅(hooks)에 조건부 `if` 필드 추가 (permission rule 문법 필터링 지원)
- 예약 작업(`/loop`, `CronCreate`)에 타임스탬프 마커 추가
- Deep link 쿼리 최대 5,000자 지원으로 확장

**버그 수정:**
- compaction, 플러그인, MCP OAuth 플로우 관련 다수 버그 수정

---

## 다음 단계

> [!tip] 다음으로
> Claude Code에 익숙해졌다면 [[04-advanced|심화 학습]]에서 프롬프트 엔지니어링을 배워보세요.

---

## References

- [Claude Code 공식 문서](https://docs.anthropic.com/claude/docs/claude-code)
- [GitHub - Claude Code](https://github.com/anthropics/claude-code)
