---
date: 2026-11-27
tags: [tech]
type: tech-tool-study
status: draft
---

# Cheatsheet

## 핵심 구분

| 표현 | 안전한 해석 |
|---|---|
| Always Free | 계정 유지 기간 동안 정해진 자원 범위에서 무료라는 발췌 |
| 12GB·2코어 | 영상에서 제시한 서버 구성 수치; 전체 한도 여부 불명 |
| 배포 완료 | 실행 상태와 외부 접속 성공을 별도로 확인해야 함 |
| 80·443 / ports | 접속 설정을 점검하는 단서; 정상 서비스나 실패 원인의 증명 아님 |
| 여러 도구 등장 | 같은 서버에서 동시 안정 운영되었다는 측정 근거 없음 |

## 역할 빠른 참조

- **Oracle Always Free:** Infrastructure
- **Docker:** 실행 환경 실습
- **Coolify:** 배포 관리
- **Twenty:** 고객 관리
- **n8n:** 문의 자동 응답 Workflow

## 실행 전후 체크

- [ ] 자원별 무료 한도·초과 처리·계정 유지 조건 확인
- [ ] 개별 사양과 전체 할당량 구분
- [ ] CPU architecture·이미지 호환성 확인
- [ ] Storage·Network·외부 연동 비용 확인
- [ ] 배포 / 실행 / 외부 접속 각각 확인
- [ ] 단일 앱 측정 후 도구를 하나씩 추가
- [ ] 접근 제어·백업·복구·가용성 조건 검토

## 보고용 기술스택 요약

- **Infrastructure:** 계정 유지 기간 동안 정해진 자원 범위에서 무료로 제공된다고 소개된다.
- **서버 사양:** 영상의 메모리 12GB·2코어 외에 전체 무료 한도·CPU architecture·Storage·Network 조건은 확인되지 않는다.
- **배포·업무 도구:** Docker 실습, Coolify 앱 배포, Twenty 고객 관리, n8n 문의 자동 응답이 등장한다.
- **운영 검증:** 외부 접속과 80·443 관련 설정을 확인하고 실제 부하 측정으로 동시 운영 가능성을 판단한다.

돌아가기: [[tech/infra/oracle-always-free/README|학습 경로]] · [[tech/infra/oracle-always-free/03-references|출처의 한계]]

## Sources

- 사용자 제공 dossier: 문서 발췌 및 영상 내용의 요약. 원문 URL, 영상 제목·시점, 정책 기준일은 제공되지 않았다.
- 출처 URL: 미제공. 실제 무료 한도와 운영 조건은 사용 시점의 공식 문서에서 별도로 확인해야 한다.
