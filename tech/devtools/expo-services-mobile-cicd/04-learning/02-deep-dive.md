---
date: 2026-11-18
tags: [tech, devtools, expo, mobile, cicd]
type: tech-tool-study
status: researched
---

# OTA 호환성과 환경 격리

업데이트 선택에는 빌드의 platform과 runtimeVersion이 일치해야 한다. 빌드의 channel은 서버의 branch와 연결되고, 그 branch에서 호환되는 업데이트를 찾는다. channel과 Git branch가 우연히 같은 문자열이어도 서로 다른 객체다. [Update 동작](https://docs.expo.dev/eas-update/how-it-works/)

## 네이티브 변경은 왜 새 빌드가 필요한가

설치된 바이너리는 네이티브 기능을 이미 포함한다. 새 JS가 그 바이너리에 없는 네이티브 모듈을 호출하면 JS만 전달해도 기능은 생기지 않는다. native dependency를 추가하거나 네이티브 코드가 바뀌면 새 빌드와 호환 버전 관리가 필요하다.

runtimeVersion의 `appVersion` 정책은 앱 버전 관리에 의존하므로 네이티브 변경 때 버전 증가를 빠뜨리지 않아야 한다. `fingerprint` 정책은 네이티브 런타임에 영향을 줄 수 있는 변경을 반영해 호환성 판단을 더 보수적으로 만들지만 빌드 횟수가 늘 수 있다. 플랫폼별 runtimeVersion도 가능하다. [런타임 정책](https://docs.expo.dev/eas-update/runtime-versions/)

## 환경 변수는 비밀 저장소와 다르다

`development`, `preview`, `production`은 기본 환경 집합이다. 환경 선택과 변수 visibility는 별개의 축이다. [환경 변수 개념](https://docs.expo.dev/eas/environment-variables/)

`EXPO_PUBLIC_` 값은 앱 코드에 들어가므로 서버 전용 비밀값을 넣으면 안 된다. `secret` visibility의 값은 로컬 CLI의 동적 앱 설정 해석 단계에서 읽을 수 없다. 서버에서 필요한 값과 클라이언트에 포함될 값을 구분한 뒤 Build와 Update의 환경을 일치시킨다. [사용 시 제약](https://docs.expo.dev/eas/environment-variables/usage/)

## 장애 분류 연습

| 증상 | 먼저 확인할 조건 |
|---|---|
| 업데이트가 보이지 않음 | platform/runtimeVersion, channel 연결, 실제 앱 재시작 |
| 새 네이티브 기능 호출 실패 | 기존 바이너리에 해당 네이티브 모듈이 있는지 |
| preview가 운영 API를 호출 | environment 선택 및 번들에 포함된 값 |
| 제출 성공 후 스토어에서 안 보임 | 스토어 처리·심사·출시 상태 |

이는 진단 순서 제안이며 특정 사고에 대한 실제 검증 결과가 아니다.

## 관련 노트

- [[tech/devtools/expo-services-mobile-cicd/README|연구 목차]]
