---
date: 2026-11-27
tags: [tech]
type: tech-tool-study
status: draft
---

# Projects

## 프로젝트 1: 터미널 Docker 실습 기록

- **목적:** 상시 서버 실습을 재현 가능한 기록으로 남긴다.
- **산출물:** 서버 환경, 명령 출처와 실행 입력, 결과, 실패와 수정 기록.
- **완료 기준:** 각 실행 단계와 결과가 연결되고 dossier 정보와 직접 확인한 정보가 구분된다.

진행: [[tech/infra/terminal-docker-practice/04-learning/01-getting-started|시작하기]]의 기록 양식을 사용해 실행 대상 하나를 검증한다.

## 프로젝트 2: 소규모 앱 배포와 접속 점검

- **목적:** 대학 프로젝트 배포 사례를 참고해 앱 하나의 배포·접속을 확인한다.
- **산출물:** 배포 작업 기록, 외부 접속 결과, 접속 설정 변경 이력.
- **완료 기준:** 배포와 외부 접속 결과를 각각 기록한다. 실패가 남으면 해결 여부, 확인된 현상, 미확인 원인을 분명히 남긴다.

진행: Coolify 작업과 터미널 작업을 구분한다. 접속 실패 장면을 특정 원인의 장애 사례로 재구성하지 않는다.

## 프로젝트 3: 업무 도구 운영 시범

- **목적:** Twenty 고객 관리 또는 n8n 문의 응답 중 하나를 선택해 서버 활용 목적을 구체화한다.
- **산출물:** 선택한 업무 시나리오, 구성 기록, 실제 동작 결과.
- **완료 기준:** 고객 관리 작업 하나 또는 문의 응답 흐름 하나가 의도대로 수행되는지 확인한다.

진행: 테스트용 데이터를 사용해 입력과 기대 결과를 정하고 실제 결과와 비교한다. 자료에 직접 연동 근거가 없으므로 Twenty와 n8n의 연동을 필수로 두지 않는다.

## 공통 제출 점검

- [ ] 환경, 확인 날짜, 참고 URL을 기록했다.
- [ ] 예상과 관찰 결과를 분리했다.
- [ ] 비용·용량·접속 원인을 근거 없이 단정하지 않았다.
- [ ] 공개 기록에서 민감한 값을 제거했다.

## 연결

[[tech/infra/terminal-docker-practice/04-learning/02-deep-dive|심화 학습]] · [[tech/infra/terminal-docker-practice/README|학습 진입점]]

## Sources

- 제공 dossier: 영상·문서 발췌의 요약. 원본 URL 미제공으로 직접 대조할 수 없다.
- 아래 공식 문서는 후속 확인용이다. dossier 속 영상의 실행 과정이나 성공 결과를 입증하는 출처는 아니다.
- Docker 공식 문서: https://docs.docker.com/
- Oracle Always Free 공식 문서: https://docs.oracle.com/en-us/iaas/Content/FreeTier/freetier_topic-Always_Free_Resources.htm
- Coolify 공식 문서: https://coolify.io/docs/
- Twenty 공식 문서: https://docs.twenty.com/
- n8n 공식 문서: https://docs.n8n.io/
