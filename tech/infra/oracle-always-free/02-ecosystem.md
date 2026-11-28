---
date: 2026-11-27
tags: [tech]
type: tech-tool-study
status: draft
---

# Ecosystem과 비교

## 역할 비교

| 요소 | 해결하는 문제 | 서버와의 관계 | 주의점 |
|---|---|---|---|
| Oracle Always Free | 서버 자원 확보 | Infrastructure 기반 | 무료 한도 전체 미제공 |
| Docker | 실행 환경 실습 | 서버 위에서 활용 | 서버 자원을 제공하는 대안 아님 |
| Coolify | 앱·프로젝트 배포 | 배포 관리 | 무료 자원 한도를 늘린다는 근거 없음 |
| Twenty | 고객 관리 | 업무 앱 | Infrastructure·배포 도구와 역할이 다름 |
| n8n | 문의 자동 응답 | Workflow 구성 | 처리량·연동 조건·비용 미확인 |
| 다른 Cloud·호스팅 | 대안 서버 확보 | 비교 후보 | 가격·사양·조건 자료 없음 |

이 Ecosystem은 경쟁 제품 순위보다 서로 다른 계층을 조합하는 구조로 읽는다. Docker나 Coolify를 Oracle 서버의 대체 상품으로 비교하면 비교 기준이 어긋난다.

## 대안 평가 시 수집할 정보

- 동일한 CPU architecture와 자원 단위인지 확인한다.
- Compute뿐 아니라 Storage, Network, 백업, 외부 연동 비용을 나눠 기록한다.
- 자원 확보 가능성, 회수 조건, 가용성 보장과 복구 방법을 확인한다.
- 동일 앱·동일 부하에서 측정한 결과로 비교한다.

위 항목은 후속 조사 기준이다. 제공 자료로 업체 간 가성비 순위나 다른 Cloud의 무료 한도를 결정할 수 없다.

다음: [[tech/infra/oracle-always-free/03-references|근거와 조사 공백]] · [[tech/infra/oracle-always-free/README|학습 경로]]

## Sources

- 사용자 제공 dossier: 문서 발췌 및 영상 내용의 요약. 원문 URL, 영상 제목·시점, 정책 기준일은 제공되지 않았다.
- 출처 URL: 미제공. 실제 무료 한도와 운영 조건은 사용 시점의 공식 문서에서 별도로 확인해야 한다.
