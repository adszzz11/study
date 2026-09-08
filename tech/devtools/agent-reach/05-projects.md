---
date: 2026-09-09
tags: [tech]
type: tech-tool-study
status: draft
---

# Agent Reach — 실전 프로젝트

[[tech/devtools/agent-reach/README|목차]] · [[tech/devtools/agent-reach/cheatsheet|다음: Cheatsheet]]

## 프로젝트 사용법

아래는 학습용 프로젝트 제안이다. 아직 실행하지 않았으며 성공률이나 산출물이 존재한다는 뜻이 아니다. 원문 다운로드와 진단 로그는 개인 실습 디렉터리에 두고, 이 공개 노트에는 비밀정보를 제거한 관찰·출처·한계만 정리한다.

## 1. 공개 개발 도구 조사 카드

**목표**: 저장소 정보와 공식 설명을 읽어 서로 검증 가능한 작은 조사 결과를 만든다.

- 입력: 공개 GitHub repository 하나와 공식 문서 URL 하나.
- 경로: `gh`로 repository 정보 확인, Jina Reader로 공개 문서 읽기.
- 절차: 실제 결과 확보 → 주장별 출처 연결 → 문서와 소스가 다른 부분 표시.
- 산출물: 정의, 사용 조건, 확인 날짜, 사용 backend, 근거 URL, 미검증 항목 표.
- 완료 기준: 핵심 주장 3개를 원문에서 다시 확인할 수 있고, 읽지 못한 내용을 추측으로 채우지 않는다.

```text
주장 | 근거 URL | 실제 사용 도구 | 확인 시각 | 한계
```

**학습 질문**: 이미 `gh`와 `curl` 사용법을 안다면 Agent Reach가 줄여 주는 작업은 무엇인가? 결과 자체와 설치·진단·실행 지식의 가치를 나눠 평가한다.

## 2. 강의 영상 한 편의 자막 기반 요약

**목표**: metadata·자막·전사를 구분하고 fallback을 증거와 함께 기록한다.

1. 공개 영상 한 개를 선택하고 URL·제목을 확인한다.
2. `yt-dlp`로 자막을 시도한다.
3. 실패하면 [[tech/devtools/agent-reach/04-learning/02-deep-dive|Deep dive의 fallback]]을 적용한다.
4. 실제 얻은 자막 또는 전사에 근거해 핵심 내용 5개와 시간 위치를 정리한다.
5. 원래 자막인지 새로 생성한 ASR 전사인지 표시한다.

- 산출물: 출처 URL, backend별 시도, 실패 이유, 요약, 확인 가능한 timestamp.
- 완료 기준: 비어 있지 않은 관련 텍스트가 있고, 주요 주장과 숫자를 영상의 해당 구간에서 확인한다.
- 중단 조건: 필요한 인증·provider key가 없거나 데이터 전송 조건을 충족하지 못하면 실패 이유를 기록하고 종료한다.

## 3. 진단과 실제 호출의 차이 기록

**목표**: `doctor`를 모니터링 신호로 활용하면서 end-to-end 확인을 별도로 설계한다.

| 항목 | 기록할 내용 |
|---|---|
| 환경 | OS, Agent Reach tag/SHA, upstream 버전 |
| 진단 | channel, status, message, active_backend |
| 실제 작업 | 공개 target URL 또는 검색어, 실행 명령 |
| 결과 | 관련 콘텐츠 확보 여부, 빈 결과·인증·오류 구분 |
| 결론 | 진단과 실제 결과의 일치·불일치 및 원인 가설 |

- 먼저 Web과 GitHub처럼 범위가 작은 두 작업으로 시작한다.
- 기존에 구성한 Exa가 있다면 실제 검색을 추가해 #623 같은 차이가 있는지 관찰한다.
- 설정 파일을 일부러 파괴하지 않는다. 장애 비교가 필요하면 별도 실습 환경에서 수행한다.
- 산출물: 비밀정보를 제거한 결과 표와 재현 절차.
- 완료 기준: `ok`를 성공의 유일한 기준으로 쓰지 않고, `warn`의 이유도 기록한다.

반복 모니터링은 이 기록 방식이 유용한지 확인한 뒤 설계한다. 노트 작성 자체가 cron이나 외부 알림 설정을 의미하지 않는다.

## 평가 기준

- [ ] 주장에 대응하는 원문 URL과 확인 날짜가 있다.
- [ ] release 설명, 현재 소스, 실제 관찰을 구분했다.
- [ ] 실패를 “자료 없음”으로 바꾸지 않았다.
- [ ] fallback의 도구·횟수·종료 이유가 남아 있다.
- [ ] credentials와 개인 session 정보가 공개 산출물에 없다.

## Sources

- [Upstream 명령·설치 모델](https://github.com/Panniantong/Agent-Reach/blob/main/docs/install.md)
- [Video fallback](https://github.com/Panniantong/Agent-Reach/blob/main/agent_reach/skill/references/video.md)
- [doctor 구현](https://github.com/Panniantong/Agent-Reach/blob/main/agent_reach/doctor.py)
- [Exa 진단 오류 보고 #623](https://github.com/Panniantong/Agent-Reach/issues/623)
