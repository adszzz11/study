---
date: 2026-11-18
tags: [tech, devtools, expo, mobile, cicd]
type: tech-tool-study
status: researched
---

# 적용 프로젝트 설계

## 1. 세 환경 배포 표

앱 식별자, API 환경, profile, channel, runtimeVersion 정책을 한 표로 정리한다. 검수 기준은 preview 설치본이 production API나 운영 업데이트 경로와 섞이지 않는 것이다. 이름을 나눈 것만으로 격리가 완료되었다고 판단하지 않는다.

## 2. 두 가지 변경의 배포 판단

테스트 시나리오 A는 기존 네이티브 기능만 사용하는 화면 문구 변경이다. 시나리오 B는 새 네이티브 모듈 추가다. A는 호환 조건 검토 후 OTA 후보, B는 새 바이너리 후보로 분류하고 그 이유를 기록한다. [네이티브와 업데이트 경계](https://docs.expo.dev/eas-update/runtime-versions/)

## 3. 빌드·제출 증빙 분리

빌드 산출물 해시, 플랫폼, 빌드 번호, 제출 상태, 스토어 심사 상태를 각각 기록하는 릴리스 표를 설계한다. 업로드 성공과 사용자 공개를 구분하는 것이 목표다. [제출 이후 단계](https://docs.expo.dev/deploy/submit-to-app-stores/)

## 4. 실패를 재현하는 대신 실패 처리를 설계

빌드 실패 시 제출을 진행하지 않는 조건, 승인 없는 production OTA를 막는 조건, 재실행 전 이미 만들어진 산출물을 확인하는 조건을 문서로 먼저 검토한다. Workflows의 실패 작업 재실행 기능이 있어도 모든 외부 동작이 자동으로 중복 방지되는 것은 아니므로 제출·게시 결과를 별도로 대조한다. [Workflows 안내](https://docs.expo.dev/eas/workflows/get-started/)

모든 항목은 미실행 프로젝트 제안이다. 실제 비용, 기기 테스트, 배포 성능 측정 결과는 아직 없다.

## 관련 노트

- [[tech/devtools/expo-services-mobile-cicd/README|연구 목차]]
