---
date: 2026-11-25
tags: [tech]
type: tech-tool-study
status: draft
---

# ADB Deep Dive — 연결·권한·자동화 경계

## 실패를 계층으로 분리하기

| 계층 | 관찰 | 다음 확인 |
|---|---|---|
| Client / server | adb 실행 또는 server 통신 실패 | 실행 경로·버전·server 설정 |
| Transport | 기기가 목록에 없음 또는 offline | USB·네트워크·호스트 권한 |
| Authorization | unauthorized | 올바른 기기에서 호스트 승인 |
| Shell / service | shell 가능, 파일 접근 거부 | sandbox·파일 권한·SELinux |
| App | 설치 후 실행 실패 | 실행 로그·앱 설정·권한 |
| Network | 앱 실행 후 서버 접근 실패 | 매핑·서버·앱 네트워크 정책 |

`adb kill-server`를 반복하기 전에 상태, 실패 명령, 종료 코드와 시각을 남긴다. Server 재시작은 같은 host의 다른 ADB 작업에도 영향을 줄 수 있다.

## 연결과 readiness

```bash
adb -s SERIAL wait-for-device
adb -s SERIAL shell getprop sys.boot_completed
```

`wait-for-device`는 ADB 연결을 기다린다. `sys.boot_completed`는 부팅 완료 판단에 흔히 쓰는 관찰값이지만 실제 build에서 의미·출력은 **확인 필요**다. 이 값만으로 앱·네트워크 준비를 보장하지 않는다.

CI에서는 각 단계에 유한한 timeout을 두고, OS 준비 후 앱의 실제 응답이나 테스트 assertion을 별도로 확인한다. 위 명령 자체에 무한 대기가 생기지 않도록 실행 환경의 timeout 기능을 적용한다.

## 권한 실습

```bash
adb -s SERIAL shell id
# PACKAGE를 본인의 debuggable 앱 ID로 교체
adb -s SERIAL shell run-as PACKAGE id
```

일반 shell과 앱 사용자 문맥의 차이를 관찰한다. `run-as`가 거부되면 debuggable 설정과 build 정책을 확인한다. 임의 앱의 private data에 접근할 수 있다고 가정하지 않는다. `adb root` 지원은 **확인 필요**다.

## Forward와 Reverse

| 명령 | 연결의 출발점 → 목적지 | 예시 |
|---|---|---|
| `forward tcp:9000 tcp:9000` | Host localhost:9000 → device 서비스:9000 | 기기에 실행한 테스트 서비스 접근 |
| `reverse tcp:8080 tcp:8080` | Device localhost:8080 → host 서비스:8080 | 앱에서 로컬 backend 접근 |

매핑은 서버 프로세스를 실행해 주지 않는다. 각 endpoint에서 실제 서비스가 수신 중이어야 한다. endpoint 종류·옵션 지원은 **확인 필요**다.

```bash
adb -s SERIAL forward --list
adb -s SERIAL reverse --list
adb -s SERIAL forward --remove tcp:9000
adb -s SERIAL reverse --remove tcp:8080
```

## Wireless debugging

Pairing 기반 Wireless debugging은 기존 TCP/IP 연결과 절차가 다르다. 기기 UI와 공식 문서로 지원 Android 버전·현재 pairing port·연결 port를 확인한다. 두 포트가 같다고 가정하지 않는다.

```bash
# pairing을 지원하고 기기에서 표시한 주소·포트를 확인한 경우
adb pair DEVICE_IP:PAIRING_PORT
adb connect DEVICE_IP:CONNECT_PORT
adb devices -l
adb disconnect DEVICE_IP:CONNECT_PORT
```

Pairing code는 기기 UI에서 확인하고 프롬프트에 입력한다. 신뢰할 수 있는 개발 네트워크에서만 사용하며 실습 후 연결과 기기의 debugging 설정을 정리한다. 기존 TCP/IP 방식으로의 전환 절차와 노출 범위는 **확인 필요**다.

## 자동화 설계

- Serial을 필수 입력으로 받아 잘못된 기기 선택을 막는다.
- 연결·OS 준비·설치·앱 검증마다 timeout과 실패 사유를 분리한다.
- stdout, stderr, 종료 코드, 시각, adb/Android 버전을 기록한다.
- dumpsys 등 시스템 출력 parsing은 버전 변화에 취약하므로 실제 대상에서 검증한다.
- 로그 공유 전 개인정보와 token을 점검하고 필요한 범위만 보관한다.

## 다음 단계

[[tech/devtools/android-debug-bridge/05-projects|실전 프로젝트]] · [[tech/devtools/android-debug-bridge/README|학습 경로]]
## Sources

- Android Developers — Android Debug Bridge: https://developer.android.com/tools/adb
- Android SDK Platform-Tools: https://developer.android.com/tools/releases/platform-tools
- Android Developers — Logcat CLI: https://developer.android.com/tools/logcat

> **검증 상태:** 제공된 dossier는 기존 기술 지식에 기반하며 외부 자료로 검증되지 않았다. 아래 URL은 추가 검증용 공식 문서이며 이번 작성에서 열람하지 않았다. 버전·기기·OS에 의존하는 동작은 **확인 필요**다.
