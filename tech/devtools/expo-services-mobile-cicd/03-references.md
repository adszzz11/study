---
date: 2026-11-18
tags: [tech, devtools, expo, mobile, cicd]
type: tech-tool-study
status: researched
---

# 공식 자료와 검증 범위

확인일: 2026-11-18. 보존된 리서치의 기술 주장을 다음 공식 문서로 재검증했다. 문서 확인과 실제 배포 검증은 구분한다.

| 공식 문서 | 이 연구에서 확인한 범위 |
|---|---|
| [EAS and Expo service names](https://docs.expo.dev/eas-to-expo/) | 이름 변경, eas CLI·설정 유지 |
| [Expo Build](https://docs.expo.dev/build/introduction/) | 빌드 역할, 기존 React Native 지원, 내부 배포 |
| [Submit to app stores](https://docs.expo.dev/deploy/submit-to-app-stores/) | 업로드와 심사·공개 구분 |
| [How Expo Update works](https://docs.expo.dev/eas-update/how-it-works/) | channel/branch/platform/runtimeVersion 관계 |
| [Runtime versions](https://docs.expo.dev/eas-update/runtime-versions/) | 네이티브 변경, appVersion/fingerprint 정책 |
| [Environment variables](https://docs.expo.dev/eas/environment-variables/) | 환경 집합과 visibility 개념 |
| [Environment variable usage](https://docs.expo.dev/eas/environment-variables/usage/) | SDK 55+ 환경 지정, 공개 변수와 secret 제약 |
| [Workflows getting started](https://docs.expo.dev/eas/workflows/get-started/) | YAML 경로, 실패 작업 재실행, deploy 템플릿의 게시 효과 |

## 포함하지 않은 주장

최저 Node.js 버전, 고정 가격, 최신 CLI 버전 번호, 부가 제품의 GA/beta 상태와 경쟁 제품의 최신 지원 종료 일자는 이 연구의 필수 범위가 아니므로 확정하지 않았다. 사용 전 해당 프로젝트 SDK와 공식 설치 안내를 별도로 확인한다.

## 남은 실증 과제

플랫폼별 테스트 기기 적용, 실제 서명 설정, 빌드 시간·비용, 스토어 승인, OTA 복구 효과는 측정하지 않았다. 학습 문서가 완성되었다는 것과 운영 배포가 검증되었다는 것은 다른 상태다.

## 관련 노트

- [[tech/devtools/expo-services-mobile-cicd/README|연구 목차]]
