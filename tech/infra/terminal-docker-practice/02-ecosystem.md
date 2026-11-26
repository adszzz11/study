---
date: 2026-11-27
tags: [tech]
type: tech-tool-study
status: draft
---

# Ecosystem: 경쟁 제품보다 역할의 연결

## 비교 범위

자료에는 Docker의 직접 경쟁 제품이나 대체 기술이 없다. 성능·비용·편의성 순위를 만들 근거가 없으므로 함께 등장한 도구의 역할을 비교한다.

| 대상 | 주된 역할 | Docker와의 관계 | 가능한 판단 |
|---|---|---|---|
| Oracle Always Free | 서버 자원 제공 | 실습 기반 | Docker 대안이 아닌 인프라 선택지 |
| Coolify | 앱·프로젝트 배포 | 실습과 함께 소개 | 배포 활동으로 확장하는 예시 |
| Twenty | 고객 관리 | 서버 활용 목적의 앱 | Docker와 기능 비교 대상이 아님 |
| n8n | 문의 자동 응답 | 서버 활용 목적의 자동화 도구 | 업무 흐름 운영 예시 |
| Docker 경쟁·대안 | 자료에 없음 | 비교 근거 없음 | 우열 판단 불가 |

## 선택 질문

- 서버 자원이 필요한가: Oracle의 현재 제공 조건과 실제 할당 가능 여부를 확인한다.
- 앱 배포가 목적인가: Coolify의 공식 문서와 실제 배포 구성을 확인한다.
- 고객 관리가 목적인가: Twenty에서 검증할 작업 하나를 정한다.
- 문의 자동화가 목적인가: n8n의 입력·처리·출력을 구체화한다.

이 질문은 학습 계획이며 영상에서 검증된 구성 추천이 아니다. Twenty와 n8n의 직접 연동을 필수로 가정하지 않는다.

## 연결

[[tech/infra/terminal-docker-practice/04-learning/01-getting-started|시작하기]] · [[tech/infra/terminal-docker-practice/README|학습 진입점]]

## Sources

- 제공 dossier: 영상·문서 발췌의 요약. 원본 URL 미제공으로 직접 대조할 수 없다.
- 아래 공식 문서는 후속 확인용이다. dossier 속 영상의 실행 과정이나 성공 결과를 입증하는 출처는 아니다.
- Docker 공식 문서: https://docs.docker.com/
- Oracle Always Free 공식 문서: https://docs.oracle.com/en-us/iaas/Content/FreeTier/freetier_topic-Always_Free_Resources.htm
- Coolify 공식 문서: https://coolify.io/docs/
- Twenty 공식 문서: https://docs.twenty.com/
- n8n 공식 문서: https://docs.n8n.io/
