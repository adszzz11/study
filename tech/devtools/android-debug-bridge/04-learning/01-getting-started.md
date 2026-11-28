---
date: 2026-11-25
tags: [tech]
type: tech-tool-study
status: draft
---

# ADB 시작하기 — 연결부터 파일 전송까지

## 준비

- Android SDK Platform-Tools의 ADB와 실습용 Android 기기 또는 Emulator를 준비한다.
- USB 기기는 Developer options와 USB debugging, 호스트 접근 승인이 필요하다. 설치 위치, 드라이버·호스트 권한·지원 환경은 **확인 필요**다.
- 아래 `SERIAL`은 `devices -l`에서 확인한 식별자로 바꾼다. APK는 본인이 테스트할 수 있는 debug build를 준비한다.

## 1. 버전·기기 발견·대상 지정

```bash
adb version
adb devices -l
adb -s SERIAL shell getprop ro.build.version.release
```

**완료 기준:** adb 버전, 대상 Serial, 연결 상태, Android 버전을 각각 기록한다. `unauthorized`면 기기 승인 화면을 확인한다. 대상이 없으면 케이블·USB 모드·호스트 드라이버/권한을 점검한다.

## 2. 설치와 로그

```bash
adb -s SERIAL install app-debug.apk
adb -s SERIAL logcat
```

앱을 기기에서 직접 실행해 로그 변화를 관찰한다. `Ctrl+C`로 logcat을 종료한다. 설치 실패 시 서명·기존 설치 상태·OS 정책을 확인하고, 앱 데이터 삭제를 전제로 해결하지 않는다.

**완료 기준:** 설치 결과와 실행 후 관찰을 별도로 기록한다. 설치 성공만으로 앱 성공을 판정하지 않는다.

## 3. 파일 왕복 전송

```bash
printf 'adb practice\n' > sample.txt
adb -s SERIAL push sample.txt /sdcard/Download/sample.txt
adb -s SERIAL pull /sdcard/Download/sample.txt ./sample-copy.txt
cmp sample.txt sample-copy.txt
```

`cmp` 종료 코드가 0이면 내용이 같다. `/sdcard/Download` 경로와 쓰기 정책은 **확인 필요**다. 권한 거부가 나오면 경로·권한을 먼저 확인한다. 실습 후 본인이 만든 파일만 정리한다.

## 4. 개발 서버 연결

Host의 개발 서버가 `8080`에서 실행 중이고, 앱이 `localhost:8080`에 접근하도록 설정됐다고 가정한다.

```bash
adb -s SERIAL reverse tcp:8080 tcp:8080
adb -s SERIAL reverse --list
# 앱에서 요청한 뒤 host 서버의 응답과 요청 기록을 확인
adb -s SERIAL reverse --remove tcp:8080
```

앱의 cleartext traffic 정책, 서버 준비 상태는 별도로 충족해야 한다. 지원 옵션·기기 동작은 **확인 필요**다.

## 완료 체크

- [ ] 명령마다 대상 Serial을 지정했다.
- [ ] 연결 성공·설치 성공·앱 성공을 분리해 기록했다.
- [ ] 파일 왕복 결과를 비교했다.
- [ ] reverse mapping을 제거했다.

## 다음 학습

[[tech/devtools/android-debug-bridge/04-learning/02-deep-dive|계층별 진단]] · [[tech/devtools/android-debug-bridge/cheatsheet|명령 요약]] · [[tech/devtools/android-debug-bridge/README|학습 경로]]
## Sources

- Android Developers — Android Debug Bridge: https://developer.android.com/tools/adb
- Android SDK Platform-Tools: https://developer.android.com/tools/releases/platform-tools
- Android Developers — Logcat CLI: https://developer.android.com/tools/logcat

> **검증 상태:** 제공된 dossier는 기존 기술 지식에 기반하며 외부 자료로 검증되지 않았다. 아래 URL은 추가 검증용 공식 문서이며 이번 작성에서 열람하지 않았다. 버전·기기·OS에 의존하는 동작은 **확인 필요**다.
