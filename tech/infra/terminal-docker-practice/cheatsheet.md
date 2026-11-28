---
date: 2026-11-27
tags: [tech]
type: tech-tool-study
status: draft
---

# Cheatsheet: 실습·배포·접속 점검

## 역할 빠르게 보기

| 대상 | 기억할 역할 |
|---|---|
| Oracle Always Free | 상시 서버 선택지, 정해진 무료 범위 확인 |
| 터미널·Docker | 실행 입력과 결과를 남기는 실습 |
| Coolify | 앱·대학 프로젝트 배포 예시 |
| Twenty | 고객 관리 예시 |
| n8n | 문의 자동 응답 예시 |

## 실습 전

- [ ] 실제 환경과 영상의 12GB·2코어를 구분한다.
- [ ] 무료 범위·할당 조건을 현재 문서와 계정에서 확인한다.
- [ ] 실행 대상과 기대 결과를 하나씩 정한다.
- [ ] 설치·명령은 환경에 맞는 공식 문서로 별도 확인한다.

## 실행·배포 후

- [ ] 실행한 입력과 관찰 출력을 연결한다.
- [ ] 터미널 작업과 Coolify 작업을 구분한다.
- [ ] 앱 실행 결과와 외부 접속 결과를 따로 기록한다.
- [ ] 실패 시 현상 → 변경 → 변경 후 결과를 남긴다.

## 단정하지 않을 것

| 단서 | 허용되는 해석 | 미확인 사항 |
|---|---|---|
| 12GB·2코어 | 영상에서 제시한 사양 | 모든 계정 제공, 동시 운영 가능성 |
| Always Free | 정해진 범위 내 무료라는 설명 | 실제 계정의 조건과 자원 확보 |
| 80·443, `ports` | 접속 점검 단서 | 차단 여부, 실패 원인, 해결 방법 |
| 여러 도구 등장 | 서로 다른 활용 역할 | 동일 서버·Docker 실행, 직접 연동 |

자료에 Docker 명령이 없으므로 이 노트는 검증된 명령 모음이 아니다.

## 최소 기록 양식

```text
환경 / 실행 대상:
명령과 출처:
기대 결과 / 관찰 결과:
배포 결과 / 외부 접속 결과:
변경 내용 / 변경 후 결과:
확인 사실 / 추정 / 미확인:
```

## 연결

[[tech/infra/terminal-docker-practice/04-learning/01-getting-started|시작하기]] · [[tech/infra/terminal-docker-practice/04-learning/02-deep-dive|심화 학습]] · [[tech/infra/terminal-docker-practice/03-references|References]] · [[tech/infra/terminal-docker-practice/README|학습 진입점]]

## Sources

- 제공 dossier: 영상·문서 발췌의 요약. 원본 URL 미제공으로 직접 대조할 수 없다.
- 아래 공식 문서는 후속 확인용이다. dossier 속 영상의 실행 과정이나 성공 결과를 입증하는 출처는 아니다.
- Docker 공식 문서: https://docs.docker.com/
- Oracle Always Free 공식 문서: https://docs.oracle.com/en-us/iaas/Content/FreeTier/freetier_topic-Always_Free_Resources.htm
