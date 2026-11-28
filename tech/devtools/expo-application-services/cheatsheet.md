---
date: 2026-11-26
tags: [tech]
type: tech-tool-study
status: draft
---

# Cheatsheet — EAS 잠정 분석

> **검증 범위:** EAS = Expo Application Services라는 잠정 해석이다. ‘Eas’의 정확한 의미와 현재 기능·요금·정책·명령어는 확인이 필요하다. 제공된 자료·URL은 없으며 웹 검색이나 URL 열기는 수행하지 않았다.

## 역할 빠르게 보기

| 용어 | 역할 | 주의점 |
|---|---|---|
| Build | Native binary 생성 | Native dependencies·Signing 확인 |
| Submit | Store 제출 자동화 | 제출과 심사·출시는 구분 |
| Update | JavaScript·Asset 배포 | 설치된 Binary와 호환 필요 |
| Runtime | Update 호환성 판단의 핵심 개념 | 현재 식별·분기 동작 확인 필요 |

## 배포 전 체크

- [ ] ‘Eas’의 의미를 확인했다.
- [ ] Native 변경에 새 Binary가 필요한지 판단했다.
- [ ] Development·Preview·Production 설정을 구분했다.
- [ ] Commit·Lockfile·Toolchain·Build profile을 기록했다.
- [ ] Update 대상과 Native 기능 호환성을 검증했다.
- [ ] Credential 권한과 앱에 포함되는 값을 점검했다.
- [ ] Artifact·Release·Update 연결 기록과 복구 경로가 있다.
- [ ] 현재 요금·정책·명령어를 공식 자료에서 확인했다.

## 혼동 방지

- 같은 Commit만으로 Build 재현성이 확보되지는 않는다.
- 환경변수에 넣은 값이 모두 Secret은 아니다.
- Update는 Store 배포의 완전한 대체 수단이 아니다.
- 서비스 도입 효과는 속도뿐 아니라 운영 부담으로 평가한다.

## 기술스택 요약

- 잠정 대상: Expo Application Services — ‘Eas’의 정확한 의미 확인 필요.
- 관련 기술: Expo·React Native, JavaScript/TypeScript, iOS·Android Native build.
- 주요 영역: Build 자동화, Signing, Store 제출, JavaScript·Asset 업데이트.
- 도입 판단: 운영 부담 감소와 서비스 의존성·비용·Native 제어 요구를 함께 평가.
- 근거 한계: 제공 자료·URL이 없어 현재 기능·가격·지원 정책은 검증되지 않음.

## 명령어

검증된 CLI 문법과 설정 자료가 없어 실행용 명령을 제시하지 않는다. [[tech/devtools/expo-application-services/03-references|References의 검증 목록]]부터 확인한다.

## 연결

[[tech/devtools/expo-application-services/README|학습 진입점]]

## Sources

제공 dossier를 기반으로 작성했다. 아래 URL은 후속 확인용 공식 문서 후보이며, 본문을 직접 열어 확인한 근거는 아니다.

- Expo EAS 문서: https://docs.expo.dev/eas/
- EAS Build: https://docs.expo.dev/build/introduction/
- EAS Submit: https://docs.expo.dev/submit/introduction/
- EAS Update: https://docs.expo.dev/eas-update/introduction/
