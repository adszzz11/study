---
date: 2026-11-18
tags: [tech, devtools, expo, mobile, cicd]
type: tech-tool-study
status: researched
---

# 빠른 확인표

| 개념 | 기억할 점 |
|---|---|
| Expo Services / EAS | 현재 서비스 명칭은 Expo, CLI·설정은 eas 유지 |
| Build | 바이너리 생성 |
| Submit | 스토어 업로드; 공개·심사 완료와 별개 |
| Update | 호환되는 JS·asset 전달 |
| profile | 빌드 설정 묶음 |
| environment | 변수 집합 선택 |
| channel | 빌드와 업데이트 branch 연결 |
| runtimeVersion | 네이티브 런타임과 업데이트 호환성 경계 |

## 업데이트 검토 순서

1. 네이티브 변경이 있는가?
2. 설치본과 업데이트의 platform/runtimeVersion이 맞는가?
3. 선택한 channel이 의도한 branch에 연결되는가?
4. 환경 변수 집합이 해당 빌드와 일치하는가?
5. 테스트 설치본에서 적용을 확인했는가?

## 명령 읽기 예제

```text
eas build --platform android --profile preview
  -> preview profile로 Android 클라우드 빌드 요청

eas update --channel preview --environment preview
  -> preview 채널 대상으로 업데이트 게시 요청
```

위 명령은 설명용이며 실행하지 않았다. 두 번째 명령은 원격 게시 효과가 있으므로 조회 명령으로 사용하지 않는다.

근거: [Build](https://docs.expo.dev/build/introduction/), [Update](https://docs.expo.dev/eas-update/how-it-works/), [환경](https://docs.expo.dev/eas/environment-variables/usage/).

## 관련 노트

- [[tech/devtools/expo-services-mobile-cicd/README|연구 목차]]
