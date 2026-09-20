---
date: 2026-09-09
tags: [tech]
type: tech-tool-study
status: draft
---

# Agent Reach — Deep dive

[[tech/devtools/agent-reach/README|목차]] · [[tech/devtools/agent-reach/05-projects|다음: Projects]]

## 1. Channel에서 결과까지 추적하기

현재 `main`의 소스를 다음 순서로 읽는다.

| 코드 | 역할 | 읽으며 확인할 질문 |
|---|---|---|
| `channels/__init__.py` | registry | 어떤 15개 channel이 등록됐는가? |
| `channels/base.py` | URL 판별·후보 순서·진단 계약 | 선호 backend는 어떻게 앞으로 이동하는가? |
| `channels/twitter.py` | 플랫폼별 예외·인증 범위 | 실행을 생략하는 probe는 무엇인가? |
| `doctor.py` | channel 진단 결과 집계 | 예외와 stale active backend를 어떻게 처리하는가? |
| `config.py` | 로컬 설정과 환경변수 조회 | 설정 파일과 환경변수 중 무엇이 우선하는가? |

`ordered_backends()`는 설정한 후보를 앞에 옮긴다. 알 수 없는 override는 무시하며, 후보를 바꾸는 것과 upstream 프로세스를 실행하는 것은 별도 단계다. 현재 `Config.get()`은 파일에 값이 있으면 먼저 사용하고, 없을 때 대문자 환경변수를 조회한다. 환경변수가 언제나 설정 파일을 덮어쓴다고 가정하지 않는다.

`doctor`의 `backends` 필드는 선언된 목록이다. override가 적용된 실제 probe 순서와 같다고 단정하지 말고, channel 구현 및 `active_backend`를 함께 본다. [Channel](https://github.com/Panniantong/Agent-Reach/blob/main/agent_reach/channels/base.py), [Config](https://github.com/Panniantong/Agent-Reach/blob/main/agent_reach/config.py), [doctor](https://github.com/Panniantong/Agent-Reach/blob/main/agent_reach/doctor.py)

## 2. 진단의 경계

```text
binary 경로 존재
    ↓ 실제 실행 가능 여부는 별도
가벼운 command probe
    ↓ 인증과 특정 콘텐츠 접근은 별도
플랫폼 인증·연결 확인
    ↓ 목표 작업의 결과는 별도
대상 URL에서 관련 본문·자막 확보
```

v1.5.0은 단순 경로 확인 대신 실제 명령 probe를 도입했다. 하지만 현재 Twitter 구현은 upstream의 자동 Cookie 접근을 피하기 위해 live 인증 검증을 생략한다. 이때 credentials가 있어도 `warn`과 `active_backend: null`이 나올 수 있다.

반대 방향의 한계도 있다. [Exa #623](https://github.com/Panniantong/Agent-Reach/issues/623)은 MCP 서버가 미설정인데 `ok`였다는 사용자 보고다. 진단은 출발점으로 쓰고 **target URL 또는 실제 검색 명령의 결과**를 최종 검증한다.

개별 channel에서 예외가 발생하면 `doctor`는 해당 결과를 `error`로 만들고 나머지 보고서를 계속 생성한다. 예외 경로의 `active_backend`는 `None`으로 처리한다. 이는 보고서의 견고함에 관한 기능이며 실제 데이터 수집 재시도를 뜻하지 않는다.

## 3. YouTube fallback 실습 설계

아래는 공식 video reference의 흐름을 학습용으로 정리한 것이다. 먼저 자막을 읽고, 필요한 경우에만 전사한다.

```text
yt-dlp 자막 요청
  ├─ 관련 자막 확보 → 종료
  └─ 실패/빈 응답
       ↓ OpenCLI 연결 시 transcript 요청
       ├─ 관련 자막 확보 → 종료
       └─ Caption URL의 빈 응답이면 최대 3회 재시도
            ↓ 여전히 실패하거나 자막 없음
         API key·데이터 전송 조건 확인 후 transcribe
```

```bash
# VIDEO_URL을 실제 공개 영상 URL로 바꾼다.
# metadata 확인은 자막 확보와 별개다.
yt-dlp --dump-json 'VIDEO_URL'

# 사용 가능한 자막 언어 확인 후 필요한 언어만 선택
yt-dlp --list-subs 'VIDEO_URL'
yt-dlp --write-sub --write-auto-sub --sub-lang 'ko,en'   --skip-download -o '/tmp/agent-reach-%(id)s' 'VIDEO_URL'

# OpenCLI가 연결되어 있을 때의 다음 후보
opencli youtube transcript 'VIDEO_URL' -f yaml

# 선택적 최종 단계: provider key 필요, 오디오를 외부 provider로 전송
agent-reach transcribe 'VIDEO_URL'
```

반환된 파일의 내용·언어·영상 일치 여부를 확인한다. 자동 자막은 중복이 있을 수 있고, 자막 실패는 곧 “영상에 말이 없다”는 뜻이 아니다. 이 순서의 재시도는 Agent가 reference에 따라 수행하는 부분을 포함한다. [Video reference](https://github.com/Panniantong/Agent-Reach/blob/main/agent_reach/skill/references/video.md)

## 4. 인증과 provider 경계

| 경계 | 현재 동작 | 운영 시 의미 |
|---|---|---|
| 로컬 설정 | `~/.agent-reach/config.yaml` | 설정·비밀정보를 공개 vault에 복사하지 않음 |
| Twitter CLI | `configure`가 현재 shell 환경을 자동 설정하지 않음 | 직접 호출 프로세스에 명시적 credentials 필요 |
| XiaoHongShu OpenCLI | 사용자가 이미 제어하는 browser session 이용 | Cookie configure가 Chrome session에 주입되는 것은 아님 |
| Jina / Exa | 외부 서비스 요청 | 요청 URL·검색어의 공개 가능 범위 확인 |
| transcription auto | 첫 configured provider 사용, Groq 우선 후 OpenAI | 실패했다고 다른 provider에 자동 전송하지 않음 |
| cross-provider fallback | `--allow-provider-fallback`로 명시적 선택 | 같은 오디오가 두 provider로 전달되고 비용이 발생할 수 있음 |

마지막 두 행은 현재 video reference 기준이며 v1.5.0의 모든 설치에 동일하다고 가정하지 않는다.

## 5. 스스로 답해 보기

- `can_handle()`가 true이면 콘텐츠를 읽을 수 있다는 뜻인가? → URL 분류 결과이며 접근 성공 증거는 아니다.
- `active_backend`가 있으면 영상 자막도 검증됐는가? → probe가 수행한 범위만 확인된 것이다.
- `warn`이면 binary를 다시 설치해야 하는가? → message가 인증 미검증을 뜻할 수도 있다.
- backend 선호도를 바꾸면 모든 요청이 자동 retry되는가? → 후보 선택과 Agent의 runtime 절차를 따로 봐야 한다.
- provider를 바꾸는 fallback도 동일한 데이터 경계인가? → 처리 주체가 달라지므로 별도 선택이다.

## Sources

- [Channel base](https://github.com/Panniantong/Agent-Reach/blob/main/agent_reach/channels/base.py)
- [Registry](https://github.com/Panniantong/Agent-Reach/blob/main/agent_reach/channels/__init__.py)
- [doctor](https://github.com/Panniantong/Agent-Reach/blob/main/agent_reach/doctor.py)
- [Twitter](https://github.com/Panniantong/Agent-Reach/blob/main/agent_reach/channels/twitter.py)
- [Config](https://github.com/Panniantong/Agent-Reach/blob/main/agent_reach/config.py)
- [Social reference](https://github.com/Panniantong/Agent-Reach/blob/main/agent_reach/skill/references/social.md)
- [Video reference](https://github.com/Panniantong/Agent-Reach/blob/main/agent_reach/skill/references/video.md)
- [v1.5.0](https://github.com/Panniantong/Agent-Reach/releases/tag/v1.5.0)
- [Exa 진단 오류 보고 #623](https://github.com/Panniantong/Agent-Reach/issues/623)
