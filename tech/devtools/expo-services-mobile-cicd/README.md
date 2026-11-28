---
date: 2026-11-18
tags: [tech, devtools, expo, mobile, cicd]
type: tech-tool-study
status: researched
---

# Expo Services — EAS로 이해하는 모바일 CI/CD

Expo Services는 모바일 앱의 바이너리 빌드, 스토어 제출, 호환되는 JavaScript·asset 업데이트와 배포 워크플로우를 연결하는 서비스다. 이전 이름은 EAS(Expo Application Services)이며 CLI와 설정 파일은 여전히 `eas`, `eas-cli`, `eas.json`을 사용한다. 이름 변경 때문에 기존 설정을 일괄 치환할 필요는 없다. [공식 명칭 안내](https://docs.expo.dev/eas-to-expo/)

핵심은 **바이너리 배포와 OTA 업데이트의 경계를 구분하는 것**이다. 네이티브 코드가 바뀌면 새 빌드가 필요하다. 채널 이름이 같다고 모든 설치본에 같은 업데이트를 적용할 수 있는 것은 아니다.

## 학습 경로

- [[tech/devtools/expo-services-mobile-cicd/01-overview|전체 구조]]
- [[tech/devtools/expo-services-mobile-cicd/02-ecosystem|도입 판단]]
- [[tech/devtools/expo-services-mobile-cicd/04-learning/01-getting-started|시작하기]]
- [[tech/devtools/expo-services-mobile-cicd/04-learning/02-deep-dive|OTA·환경 심화]]
- [[tech/devtools/expo-services-mobile-cicd/05-projects|적용 프로젝트]]
- [[tech/devtools/expo-services-mobile-cicd/03-references|공식 근거]]
- [[tech/devtools/expo-services-mobile-cicd/cheatsheet|빠른 확인표]]

## 도입 판단

Expo/React Native 팀이 서명·빌드 환경과 배포 과정을 표준화하려 할 때 검토할 만하다. 이미 자체 네이티브 파이프라인이 안정적이라면 전체 교체보다 Build, Submit, Update 중 필요한 부분의 통합 비용을 먼저 비교한다. 비용·대기 시간·지원 플랜은 실제 사용량과 최신 계약 조건으로 별도 평가해야 하며 이 노트는 특정 가격을 보장하지 않는다.

## 검증 범위

2026-11-18 공식 문서를 확인한 개념 연구다. 계정 생성, CLI 설치, 자격증명 등록, 실제 빌드·스토어 제출·OTA 배포는 수행하지 않았다. 아래 실습은 실행 결과가 아니라 학습 설계다.

## 연결

- [[MOCs/Devtools|개발 도구 지도]]
- [[MOCs/Infra|인프라 지도]]
