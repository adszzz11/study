---
date: 2026-11-27
tags: [tech]
type: tech-tool-study
status: draft
---

# Oracle Always Free의 무료 범위와 서버 사양 분석

> **한 줄 정의**: Oracle Always Free는 제공된 문서 발췌상 계정 유지 기간 동안 정해진 범위의 자원을 무료로 제공하는 방식이며, 영상은 메모리 12GB·2코어 서버 활용 사례를 소개한다.

## Overview

개인 컴퓨터를 꺼도 앱과 자동화 도구를 실행할 서버가 필요할 때 검토할 수 있는 Infrastructure 선택지다. 자료는 Docker 실습에서 Coolify 배포, Twenty 고객 관리, n8n 문의 자동 응답으로 이어지는 활용을 소개한다.

| 구분 | 자료가 뒷받침하는 내용 | 해석의 경계 |
|---|---|---|
| 무료 조건 | 계정 유지 기간 동안 정해진 자원 범위에서 무료 | 무제한 사용이나 모든 비용의 면제를 의미하지 않음 |
| 서버 사양 | 영상에서 메모리 12GB·2코어 제시 | 전체 무료 한도인지 개별 구성인지 불명 |
| 운영 사례 | 앱·자동화 도구를 실행하는 활용 | 동시 운영 성능, 가동률, SLA는 미확인 |

이 노트는 제공 자료를 정리한 draft이며 현재 Oracle 정책을 검증한 사양표가 아니다. 12GB·2코어를 누구나 즉시 확보할 수 있다는 근거는 없다.

## Learning Path

- [ ] [[tech/infra/oracle-always-free/01-overview|Overview]] — 정의, 특징, 사양 해석의 경계
- [ ] [[tech/infra/oracle-always-free/02-ecosystem|Ecosystem 비교]] — Infrastructure와 도구의 역할 구분
- [ ] [[tech/infra/oracle-always-free/03-references|References]] — 근거와 미확인 정보 확인
- [ ] [[tech/infra/oracle-always-free/04-learning/01-getting-started|시작하기]] — 단일 앱 실행·배포·접속 확인
- [ ] [[tech/infra/oracle-always-free/04-learning/02-deep-dive|Deep Dive]] — 부하·자원 경쟁·장애 관찰
- [ ] [[tech/infra/oracle-always-free/05-projects|Projects]] — 배포·자동화·고객 관리 실험
- [ ] [[tech/infra/oracle-always-free/cheatsheet|Cheatsheet]] — 실습 전후 점검

## When To Use

- 무료 조건을 확인하면서 작은 앱의 상시 실행과 배포를 학습할 때
- Docker, Coolify, Twenty, n8n의 역할을 구분하며 단계적으로 실험할 때
- 자신의 부하를 측정해 서버 적합성을 판단하려 할 때

## When Not To Use

- 자료만으로 무료 한도·확보 가능성·무중단 운영 보장을 확정해야 할 때
- 동시 접속자 수나 여러 앱의 수용량을 12GB·2코어만으로 산정할 때
- 검증 없이 실제 고객 데이터나 복구가 중요한 서비스를 운영할 때

## Related Notes

- [[MOCs/Index]]
- [[MOCs/Infra]]
- [[tech/infra/oracle-always-free/01-overview|관련 tech 노트: Oracle Always Free 개요]]

현재 작업 폴더에는 기존 vault 노트가 없다. 위 MOC 링크는 요청된 탐색 연결이며 대상의 존재는 확인하지 못했다. 관리 파일은 생성하거나 수정하지 않는다.

## Sources

- 사용자 제공 dossier: 문서 발췌 및 영상 내용의 요약. 원문 URL, 영상 제목·시점, 정책 기준일은 제공되지 않았다.
- 출처 URL: 미제공. 실제 무료 한도와 운영 조건은 사용 시점의 공식 문서에서 별도로 확인해야 한다.
