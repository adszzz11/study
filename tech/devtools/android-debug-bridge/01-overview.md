---
date: 2026-11-25
tags: [tech]
type: tech-tool-study
status: draft
---

# ADB Overview — What / Why / 특징

## What / Why

ADB는 Android 기기와 호스트 사이의 공통 CLI 접점이다. IDE에서 재현하기 어려운 작업을 명령으로 기록하고 반복할 수 있다.

| 문제 | ADB 활용 | 별도 판단이 필요한 것 |
|---|---|---|
| 빌드 후 설치 실패 | APK 설치와 오류 확인 | 서명·기존 설치·OS 정책 |
| 실행 중 이상 동작 | logcat, shell, dumpsys | 앱 정상 동작의 기준 |
| 특정 기기에서만 실패 | Serial 지정, OS 정보 수집 | 기기별 원인 분석 |
| CI 실패 재현 어려움 | 상태·로그·명령 결과 보관 | timeout과 성공 조건 |

## Client–Server–Daemon

```text
개발 호스트                              기기 / Emulator
adb client → adb server → USB / network → adbd → shell / service
```

| 요소 | 역할 | 의미 |
|---|---|---|
| adb client | 명령을 server로 전달 | CLI·스크립트마다 호출 |
| adb server | 연결과 명령 전달 중개 | 여러 client와 기기 관리 |
| adbd | 기기에서 요청 처리 | 기기 보안 정책 적용 |
| Transport | USB 또는 network 연결 | 연결 실패를 앱 실패와 구분 |

일반적인 host server 포트는 TCP `5037`이다. 별도 설정·실행 환경은 **확인 필요**다. 실패는 client/server → transport → authorization → shell/service → app 순으로 좁힌다.

## 연결 상태와 준비 상태

- `device`: ADB 통신 가능. 부팅 완료나 앱 준비 완료의 보장은 아니다.
- `unauthorized`: 기기에서 호스트의 디버깅 접근 승인을 확인한다.
- `offline`: 정상적인 명령 교환이 어려운 상태. 원인은 상태값만으로 단정하지 않는다.
- 여러 기기에서는 `adb -s SERIAL ...`을 사용한다.

## 권한 경계

`adb shell`에서도 앱 sandbox, 파일 권한, SELinux 정책이 유지된다. `adb root`는 build와 정책에 따라 허용 여부가 다르며 일반 production 기기에서 가능하다고 가정하지 않는다. `run-as PACKAGE`는 보통 debuggable 앱 조사에 사용한다. 실제 권한 범위는 **확인 필요**다.

## 기능 지도

| 기능 | 명령 | 주의 |
|---|---|---|
| 배포 | `install` | 서명·버전·정책 확인 |
| 로그 | `logcat` | 접근 범위·형식 확인 필요 |
| 파일 전송 | `push`, `pull` | 경로 존재와 접근 권한은 별개 |
| 시스템 조사 | `shell dumpsys` | 출력은 안정적인 API로 가정하지 않음 |
| Host → device | `forward` | endpoint 지원 확인 필요 |
| Device → host | `reverse` | 앱 네트워크 정책도 충족해야 함 |

## 다음 학습

[[tech/devtools/android-debug-bridge/README|학습 경로]] · [[tech/devtools/android-debug-bridge/04-learning/01-getting-started|연결 실습]]
## Sources

- Android Developers — Android Debug Bridge: https://developer.android.com/tools/adb
- Android SDK Platform-Tools: https://developer.android.com/tools/releases/platform-tools
- Android Developers — Logcat CLI: https://developer.android.com/tools/logcat

> **검증 상태:** 제공된 dossier는 기존 기술 지식에 기반하며 외부 자료로 검증되지 않았다. 아래 URL은 추가 검증용 공식 문서이며 이번 작성에서 열람하지 않았다. 버전·기기·OS에 의존하는 동작은 **확인 필요**다.
