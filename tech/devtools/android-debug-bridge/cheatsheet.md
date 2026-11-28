---
date: 2026-11-25
tags: [tech]
type: tech-tool-study
status: draft
---

# ADB Cheatsheet

## 사용 전

`SERIAL`, `PACKAGE`, APK와 파일 경로는 실제 값으로 바꾼다. 명령 지원과 권한은 설치된 `adb help` 및 대상 기기에서 **확인 필요**다.

## 연결과 대상 선택

```bash
adb version
adb help
adb devices -l
adb -s SERIAL shell getprop ro.build.version.release
adb -s SERIAL shell id
```

| 상태 | 의미 | 먼저 할 일 |
|---|---|---|
| device | ADB 연결 가능 | OS·앱 준비 별도 확인 |
| unauthorized | 승인 필요 | 기기 승인 화면 확인 |
| offline | 정상 통신 어려움 | transport·기기 상태 확인 |

## 설치·로그·파일

```bash
adb -s SERIAL install app-debug.apk
adb -s SERIAL logcat
# 유한한 로그 snapshot을 파일로 보관
adb -s SERIAL logcat -d > logcat.txt
adb -s SERIAL push sample.txt /sdcard/Download/sample.txt
adb -s SERIAL pull /sdcard/Download/sample.txt ./sample-copy.txt
adb -s SERIAL shell dumpsys SERVICE
adb -s SERIAL shell run-as PACKAGE id
```

`SERVICE`는 조사할 시스템 서비스 이름이다. dumpsys 출력은 안정적인 API가 아니며 접근 가능 범위는 **확인 필요**다. logcat 스트리밍은 `Ctrl+C`로 종료한다. 로그 공개 전 민감정보를 점검한다.

## 포트 매핑과 정리

```bash
# Host → device
adb -s SERIAL forward tcp:9000 tcp:9000
adb -s SERIAL forward --list
adb -s SERIAL forward --remove tcp:9000

# Device → host
adb -s SERIAL reverse tcp:8080 tcp:8080
adb -s SERIAL reverse --list
adb -s SERIAL reverse --remove tcp:8080
```

각 명령은 별도 예시다. 실제 요청을 확인한 후 해당 mapping을 제거한다.

## Wireless debugging: pairing 지원 기기

```bash
adb pair DEVICE_IP:PAIRING_PORT
adb connect DEVICE_IP:CONNECT_PORT
adb disconnect DEVICE_IP:CONNECT_PORT
```

주소·포트는 기기 UI에서 확인한다. 기존 TCP/IP 방식과 혼용하지 않는다. 버전·절차는 **확인 필요**다.

## 문제 해결 순서

1. adb client/server가 동작하는가?
2. USB/network transport로 대상이 발견되는가?
3. 호스트가 승인됐는가?
4. Shell/service 권한이 있는가?
5. 앱과 네트워크의 성공 조건이 충족됐는가?

```bash
# 상태 기록 후 host server 재시작이 필요할 때만 사용
adb kill-server
adb start-server
```

Server 재시작은 같은 host의 다른 ADB 세션에도 영향을 줄 수 있다. 반복 재시작 대신 실패 계층을 먼저 기록한다.

## 관련 노트

[[tech/devtools/android-debug-bridge/04-learning/01-getting-started|단계별 실습]] · [[tech/devtools/android-debug-bridge/04-learning/02-deep-dive|실패 진단]] · [[tech/devtools/android-debug-bridge/README|학습 경로]]
## Sources

- Android Developers — Android Debug Bridge: https://developer.android.com/tools/adb
- Android SDK Platform-Tools: https://developer.android.com/tools/releases/platform-tools
- Android Developers — Logcat CLI: https://developer.android.com/tools/logcat

> **검증 상태:** 제공된 dossier는 기존 기술 지식에 기반하며 외부 자료로 검증되지 않았다. 아래 URL은 추가 검증용 공식 문서이며 이번 작성에서 열람하지 않았다. 버전·기기·OS에 의존하는 동작은 **확인 필요**다.
