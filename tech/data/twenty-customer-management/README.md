---
date: 2026-11-27
tags: [tech]
type: tech-tool-study
status: draft
---

# Twenty를 활용한 고객 관리와 상시 운영 환경

> **한 줄 정의**: Twenty는 제공 영상에서 고객 관리 도구로 소개되며, 상시 가동 서버에서 앱과 자동화 도구를 운영하는 활용 사례 중 하나다.

## Overview

영상의 출발점은 개인 컴퓨터의 실행 여부와 별개로 앱을 운영할 **상시 가동 서버**를 마련하는 것이다. Twenty는 이 환경의 고객 관리 사용처로 등장한다. 세부 기능이나 배포 구성은 확인되지 않았다.

- 업무: Twenty의 고객 관리, n8n의 문의 자동 응답.
- 운영: Oracle Always Free 서버, Docker 실습, Coolify 앱 배포.
- 두 업무 도구의 직접 연동이나 Twenty의 실제 배포 방식은 자료에 없다.
- 영상상 메모리 **12GB·2코어**는 당시 소개 조건이며, 현재 무료 제공 조건이나 Twenty 권장 사양이 아니다.

## Learning Path

- [ ] [[tech/data/twenty-customer-management/01-overview|Overview]] — 역할과 근거의 범위 이해
- [ ] [[tech/data/twenty-customer-management/02-ecosystem|Ecosystem]] — 업무·배포·실행 환경 비교
- [ ] [[tech/data/twenty-customer-management/03-references|References]] — 출처 한계와 추가 검증 경로 확인
- [ ] [[tech/data/twenty-customer-management/04-learning/01-getting-started|시작하기]] — 가상 고객 기반 최소 실습 설계
- [ ] [[tech/data/twenty-customer-management/04-learning/02-deep-dive|심화 학습]] — 접속·연동·운영 검증
- [ ] [[tech/data/twenty-customer-management/05-projects|Projects]] — 완료 기준에 따라 실습 결과 기록
- [ ] [[tech/data/twenty-customer-management/cheatsheet|Cheatsheet]] — 판단 기준과 점검표 활용

## When To Use

- 고객 관리 도입을 상시 운영 환경과 함께 학습할 때.
- 고객 관리 기능 검증과 서버·접속 검증을 별도 과제로 계획할 때.
- 문의 자동화와 고객 정보 연결의 가능성을 검토할 때.

## When Not To Use

- 이 자료만으로 Twenty의 기능·비용·권한·백업 지원을 확정하려 할 때.
- 무료 서버의 가용성이나 여러 도구의 동시 운영 용량을 보장해야 할 때.
- 검증 없이 실제 고객 정보를 저장하거나 자동 응답에 사용하려 할 때.

## Related Notes

- [[MOCs/Index]]
- [[MOCs/Data]]
- 관련 tech 주제: Docker, Coolify, n8n. 현재 작업 공간에 기존 vault 노트가 없어 대상 경로를 확인하지 못했으므로 링크 없이 표기한다.

## Sources

- 제공된 dossier: 영상 요약, 00:25·00:30. 원본 영상 URL은 제공되지 않았다.
- https://twenty.com/ — 추가 확인용 공식 사이트이며 영상의 세부 주장을 검증한 출처는 아니다.
