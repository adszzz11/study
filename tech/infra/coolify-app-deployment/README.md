---
date: 2026-11-27
tags: [tech]
type: tech-tool-study
status: draft
---

# Coolify를 이용한 앱 배포와 Always Free 서버 운영

> **한 줄 정의**: Coolify를 이용한 앱 배포는 서버에 애플리케이션을 배포하는 운영 방식으로, 제공 자료에서는 Oracle Always Free 서버를 활용한 앱·대학 프로젝트 배포 사례로 소개된다.

## Overview

개발한 앱을 지속적으로 공개하려면 실행할 서버, 배포 과정, 외부 접속을 각각 확인해야 한다. 이 학습 노트는 Oracle Always Free를 실행 자원의 맥락으로, Coolify를 앱 배포의 맥락으로 구분한다.

- **인프라:** 영상 제시 사양은 메모리 12GB·코어 2개다. 모든 계정의 확보 가능 사양을 뜻하지 않는다.
- **배포:** Coolify로 앱과 대학 프로젝트를 배포하는 활용이 소개된다.
- **주변 도구:** Docker 실습, Twenty 고객 관리, n8n 문의 자동 응답 사례가 함께 등장한다.
- **운영:** 배포 결과와 외부 접속을 별도로 검증한다. 80·443 및 `ports`는 조사 단서다.
- **근거 한계:** 상세 설치 절차, 내부 아키텍처, 성능과 경쟁 제품 비교는 자료에 없다.

## Learning Path

- [ ] [[tech/infra/coolify-app-deployment/01-overview|Overview]] — 역할과 확인된 특징 구분
- [ ] [[tech/infra/coolify-app-deployment/02-ecosystem|Ecosystem]] — 등장 도구의 역할 비교
- [ ] [[tech/infra/coolify-app-deployment/03-references|References]] — 근거와 추가 확인 항목 정리
- [ ] [[tech/infra/coolify-app-deployment/04-learning/01-getting-started|시작하기]] — 작은 앱의 배포·접속 기록 준비
- [ ] [[tech/infra/coolify-app-deployment/04-learning/02-deep-dive|심화 학습]] — 접속 진단과 무료 자원 검증
- [ ] [[tech/infra/coolify-app-deployment/05-projects|Projects]] — 대학 프로젝트 배포 및 운영 설계
- [ ] [[tech/infra/coolify-app-deployment/cheatsheet|Cheatsheet]] — 실습 중 점검표 활용
- [ ] [[tech/infra/coolify-app-deployment/README|학습 진입점]] — 학습 결과와 완료 기준 다시 확인

## When To Use

- 개인 PC를 계속 켜 두지 않고 앱을 운영할 서버 활용 경로를 학습할 때.
- 대학 프로젝트를 배포하고 다른 사람의 접근 가능 여부까지 검증할 때.
- 서버 확보, 앱 배포, 접속 성공을 나누어 운영 기록을 만들 때.

## When Not To Use

- 이 노트만으로 Coolify 설치 명령이나 버전별 조작법이 필요할 때: 공식 문서 확인이 선행되어야 한다.
- 비용 0원, 자원 할당, 성능 또는 가용성 보장이 필요한 운영 판단을 할 때.
- 다른 배포 플랫폼과의 기능·가격 우열을 결정할 때: 비교 근거가 부족하다.

## Related Notes

- [[MOCs/Index]]
- [[MOCs/Infra]]
- [[tech/infra/coolify-app-deployment/01-overview|Coolify와 실행 환경의 역할]]

MOC 링크는 요청된 vault 구조를 따른다. 현재 작업 폴더에는 기존 vault가 없어 대상 MOC의 존재는 확인하지 못했다.

## Sources

- 제공된 dossier: Oracle Always Free 서버 활용 및 Coolify 앱 배포 영상 요약. 원본 URL·영상 제목·게시일은 제공되지 않았다.
- 출처 URL: 미제공. 원본 영상과 공식 문서를 확보한 뒤 URL 및 확인일을 추가한다.
- 이 노트는 제공된 요약만을 근거로 작성했다. 설치 절차, 버전별 기능, 현재 무료 정책은 검증하지 않았다.
