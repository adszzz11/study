---
date: 2026-11-27
tags: [tech]
type: tech-tool-study
status: draft
---

# 터미널 Docker 실습과 상시 운영 서버 활용

> **한 줄 정의**: 터미널에서 Docker를 연습하는 것을 출발점으로, 상시 켜 두는 서버에서 앱 배포와 자동화 도구 운영으로 학습을 확장하는 주제다.

## Overview

이 학습의 중심은 **상시 사용할 서버를 마련한 뒤 실습 → 배포 → 업무 운영으로 확장하는 흐름**이다. Docker 자체의 상세 강의가 아니라 서버 활용 사례를 정리한다.

- 기반: Oracle Always Free. 영상에 메모리 12GB·코어 2개가 제시된다.
- 실습·배포: 터미널 Docker 실습, Coolify를 통한 앱·대학 프로젝트 배포.
- 업무 활용: Twenty 고객 관리, n8n 문의 자동 응답.
- 검증: 실행 성공과 외부 접속 성공을 각각 확인한다.

Always Free에는 정해진 자원 범위가 있다. 영상의 사양이 모든 계정에 보장되거나 여러 앱의 동시 운영에 충분하다는 뜻은 아니다. 모든 도구가 같은 서버에서 Docker로 실행됐는지도 확인되지 않았다.

## Learning Path

- [ ] [[tech/infra/terminal-docker-practice/01-overview|Overview]] — 배경, 역할 구성, 자료의 한계 이해
- [ ] [[tech/infra/terminal-docker-practice/02-ecosystem|Ecosystem]] — 인프라·배포·업무 도구 구분
- [ ] [[tech/infra/terminal-docker-practice/03-references|References]] — 원본 부재와 공식 문서 확인 항목 정리
- [ ] [[tech/infra/terminal-docker-practice/04-learning/01-getting-started|시작하기]] — 환경과 실행 결과 기록
- [ ] [[tech/infra/terminal-docker-practice/04-learning/02-deep-dive|심화 학습]] — 접속 검증과 운영 확장
- [ ] [[tech/infra/terminal-docker-practice/05-projects|Projects]] — 세 가지 실전 과제 수행
- [ ] [[tech/infra/terminal-docker-practice/cheatsheet|Cheatsheet]] — 실습 중 점검표 활용

## When To Use

- 로컬 실습에서 상시 서버 배포 경험으로 넘어갈 때.
- 작은 앱 하나의 실행·외부 접속을 단계별로 검증할 때.
- 고객 관리 또는 문의 자동화라는 목적을 정해 서버를 활용할 때.

## When Not To Use

- 이 자료만으로 Docker 설치 명령이나 운영 설정을 확정하려 할 때.
- 무료 자원 확보, 비용, 성능 또는 동시 운영 용량의 보장이 필요할 때.
- 특정 접속 장애의 원인이나 검증된 해결 절차를 찾을 때.

## Related Notes

- [[MOCs/Index]]
- [[MOCs/Infra]]
- [[tech/infra/terminal-docker-practice/01-overview|Docker 실습과 상시 서버 개요]] — 이 폴더의 관련 tech 노트

## Sources

- 제공 dossier: 영상·문서 발췌의 요약. 원본 URL 미제공으로 직접 대조할 수 없다.
- 아래 공식 문서는 후속 확인용이다. dossier 속 영상의 실행 과정이나 성공 결과를 입증하는 출처는 아니다.
- Docker 공식 문서: https://docs.docker.com/
- Oracle Always Free 공식 문서: https://docs.oracle.com/en-us/iaas/Content/FreeTier/freetier_topic-Always_Free_Resources.htm
- Coolify 공식 문서: https://coolify.io/docs/
- Twenty 공식 문서: https://docs.twenty.com/
- n8n 공식 문서: https://docs.n8n.io/
