---
date: 2026-11-18
tags: [tech, devtools, expo, mobile, cicd]
type: tech-tool-study
status: researched
---

# 시작하기 — 실행 전 설정을 읽는 연습

이 페이지는 향후 실습 절차이며 여기서 실제 명령을 실행하지 않았다. 첫 연습은 production 계정이나 배포 채널을 건드리지 않는 설정 검토로 제한한다.

## 세 가지 이름을 분리한다

- build profile: `eas.json`의 설정 묶음 이름.
- environment: 빌드·업데이트에서 사용하는 환경 변수 집합.
- channel: 설치된 빌드와 업데이트 경로를 연결하는 이름.

세 이름을 모두 `preview`로 맞추면 읽기는 편하지만 의미까지 같아지는 것은 아니다. 아래는 설명용 일부 설정이며 기존 앱에 그대로 덮어쓰는 파일이 아니다.

```json
{
  "build": {
    "preview": {
      "distribution": "internal",
      "channel": "preview",
      "environment": "preview"
    },
    "production": {
      "channel": "production",
      "environment": "production"
    }
  }
}
```

`environment`를 명시하면 profile 이름과 별개로 변수 집합을 선택할 수 있다. SDK 55 이상에서는 `eas update`에 `--environment`가 필요하다. `--environment`를 사용한 업데이트는 선택한 서비스 환경을 사용하며 로컬 `.env`를 사용하지 않는다. [환경 변수 사용](https://docs.expo.dev/eas/environment-variables/usage/)

## 나중에 수행할 실습의 합격 조건

1. 별도 테스트 앱과 preview 배포 대상을 정한다.
2. 플랫폼별 서명·배포 자격과 프로젝트 연결을 확인한다.
3. preview 빌드를 만들 때 선택한 profile/environment/channel과 runtimeVersion을 기록한다.
4. 호환되는 UI 문구 변경을 preview 업데이트로 테스트한다.
5. 앱 재시작 후 실제 적용 버전을 확인한다. 명령 종료 코드만으로 기기 적용을 판정하지 않는다.

계정·자격증명·스토어 제출과 네트워크 배포는 각각 별도 실행 결정이 필요한 단계다.

## 관련 노트

- [[tech/devtools/expo-services-mobile-cicd/README|연구 목차]]
