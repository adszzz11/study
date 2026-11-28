---
date: 2026-11-26
tags: [tech]
type: tech-tool-study
status: draft
---

# EAS — Expo Application Services 잠정 분석

> **한 줄 정의**: EAS를 Expo Application Services로 해석하면, Expo·React Native 앱의 Build·Submit·Update 작업을 지원하는 서비스 모음이다. 단, ‘Eas’가 이 제품을 뜻하는지는 확인 필요하다.

## Overview

> **검증 범위:** EAS = Expo Application Services라는 잠정 해석이다. ‘Eas’의 정확한 의미와 현재 기능·요금·정책·명령어는 확인이 필요하다. 제공된 자료·URL은 없으며 웹 검색이나 URL 열기는 수행하지 않았다.

모바일 배포는 소스코드 외에도 Native toolchain, Signing, Store 제출, 설치된 앱과의 Update 호환성을 관리해야 한다. EAS의 잠정적 가치는 이 작업을 공통 설정과 자동화 흐름으로 연결해 팀의 운영 부담을 줄이는 데 있다.

| 영역 | 역할 | 먼저 확인할 경계 |
|---|---|---|
| Build | Native binary 생성 | Native dependencies와 Signing |
| Submit | Store 제출 과정 자동화 | 심사·출시 절차와의 구분 |
| Update | JavaScript·Asset 배포 | 설치된 Binary의 Runtime compatibility |

## Learning Path

- [ ] [[tech/devtools/expo-application-services/01-overview|Overview]]
- [ ] [[tech/devtools/expo-application-services/02-ecosystem|Ecosystem 비교]]
- [ ] [[tech/devtools/expo-application-services/03-references|References]]
- [ ] [[tech/devtools/expo-application-services/04-learning/01-getting-started|시작하기]]
- [ ] [[tech/devtools/expo-application-services/04-learning/02-deep-dive|심화 학습]]
- [ ] [[tech/devtools/expo-application-services/05-projects|실전 프로젝트]]
- [ ] [[tech/devtools/expo-application-services/cheatsheet|Cheatsheet]]

각 노트는 이 README로 돌아오는 링크를 제공한다. 학습은 주제 확인 → Native build와 Update 구분 → 환경 분리 → 재현성·호환성·복구 검증 순서로 진행한다.

## When To Use

- Expo·React Native 팀이 Build·Signing·Store 제출 운영을 통합하려는 경우
- Preview와 Production 배포를 재현 가능한 절차로 만들려는 경우
- 호환되는 JavaScript·Asset 업데이트를 운영하고 추적하려는 경우

## When Not To Use

- ‘Eas’가 무엇을 뜻하는지 확인되지 않은 상태에서 도입을 결정하려는 경우
- Native 변경까지 Update로 해결할 수 있다고 가정하는 경우
- 요구되는 Native customization·Credential 정책이 지원되는지 확인하지 않은 경우
- 비용·대기 시간·장애 대응 책임을 검토하지 않은 채 운영을 맡기려는 경우

## Related Notes

- [[MOCs/Index]]
- [[MOCs/Devtools]]
- [[tech/devtools/expo-application-services/02-ecosystem|모바일 CI/CD 접근 방식 비교]]

현재 작업 폴더에는 기존 vault 파일이 없어 위 필수 MOC 두 개의 존재 여부는 확인하지 못했다. 통합 시 대상 확인이 필요하며, MOC 파일은 생성·수정하지 않는다.

## Sources

제공 dossier를 기반으로 작성했다. 아래 URL은 후속 확인용 공식 문서 후보이며, 본문을 직접 열어 확인한 근거는 아니다.

- Expo EAS 문서: https://docs.expo.dev/eas/
- EAS Build: https://docs.expo.dev/build/introduction/
- EAS Submit: https://docs.expo.dev/submit/introduction/
- EAS Update: https://docs.expo.dev/eas-update/introduction/
