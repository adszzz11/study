---
date: 2026-11-26
tags: [tech]
type: tech-tool-study
status: draft
---

# 시작하기 — 주제 확인과 배포 모델

> **검증 범위:** EAS = Expo Application Services라는 잠정 해석이다. ‘Eas’의 정확한 의미와 현재 기능·요금·정책·명령어는 확인이 필요하다. 제공된 자료·URL은 없으며 웹 검색이나 URL 열기는 수행하지 않았다.

## 1. 주제부터 확인

- [ ] 요청의 ‘Eas’가 Expo Application Services인지 확인한다.
- [ ] 다른 기술이라면 이 분석의 적용을 중단하고 대상을 다시 정한다.
- [ ] 공식 문서에서 현재 지원 범위·CLI·설정 문법을 확인한다.

## 2. 변경 유형 분류

| 연습 사례 | 판단할 내용 |
|---|---|
| 화면 문구 변경 | JavaScript 변경이 기존 Runtime과 호환되는가? |
| Native dependency 추가 | 새 Binary가 필요한가? |
| 앱 식별자 변경 | Binary·Signing·Store 설정에 어떤 영향이 있는가? |

문구 변경도 실제 Update 가능 여부는 호환성과 정책을 확인해야 한다. Native 변경을 Update만으로 전달할 수 있다고 가정하지 않는다.

## 3. 환경별 설정표 작성

아래는 실제 설정 문법이 아닌 설계용 표다.

| 항목 | Development | Preview | Production |
|---|---|---|---|
| 앱 식별자 | 개발용 값 기록 | 검증용 값 기록 | 운영용 값 기록 |
| Backend endpoint | 개발 서버 | 검증 서버 | 운영 서버 |
| Credential | 보관 위치·권한 기록 | 보관 위치·권한 기록 | 보관 위치·권한 기록 |
| Build profile | 이름·목적 기록 | 이름·목적 기록 | 이름·목적 기록 |

환경변수라는 이유만으로 값이 비밀이 되지는 않는다. 앱에 포함되는 값과 서버 측 Secret을 분리하고, 공개 노트에는 실제 Credential·Secret을 기록하지 않는다.

## 4. 첫 Build의 기록 계획

Commit, Lockfile, Dependency·Toolchain 버전, Build profile, 비밀값을 제외한 환경 설정, Artifact 식별자를 기록한다. 실제 명령 실행은 현재 공식 문법과 인증 요건을 확인한 뒤 진행한다.

## 완료 기준

- [ ] Build·Submit·Update의 역할을 각각 설명할 수 있다.
- [ ] Native 변경과 JavaScript 변경의 배포 경계를 설명할 수 있다.
- [ ] 세 환경의 설정과 Secret 경계를 문서화했다.

## 다음 단계

[[tech/devtools/expo-application-services/04-learning/02-deep-dive|재현성·호환성·복구 심화]] · [[tech/devtools/expo-application-services/README|학습 진입점]]

## Sources

제공 dossier를 기반으로 작성했다. 아래 URL은 후속 확인용 공식 문서 후보이며, 본문을 직접 열어 확인한 근거는 아니다.

- Expo EAS 문서: https://docs.expo.dev/eas/
- EAS Build: https://docs.expo.dev/build/introduction/
- EAS Submit: https://docs.expo.dev/submit/introduction/
- EAS Update: https://docs.expo.dev/eas-update/introduction/
