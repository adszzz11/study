---
date: 2026-11-25
tags: [tech]
type: tech-tool-study
status: draft
---

# ADB Projects — 실전 적용

## 프로젝트 선택

| 프로젝트 | 구현 범위 | 검증 기준 |
|---|---|---|
| 기기 상태 수집 CLI | Serial·상태·OS·앱 설치 여부 수집 | 여러 기기 구분, 일부 실패도 결과 기록 |
| APK smoke-test pipeline | 대상 → 준비 → 설치 → 실행 → 로그 보관 | 연결 성공과 앱 성공 분리 |
| 장애 재현 자료 수집기 | 재현 시간대 로그·필요한 dumpsys | 분석 가능, 개인정보·token 점검 |
| 로컬 backend 연결 도우미 | reverse 설정·조회·해제 | 실제 요청 성공, 종료 후 mapping 제거 |
| UI 자동화 진단 보조 | 실패 시 로그·기기 상태 수집 | assertion 실패와 연결 장애 구분 |

## 추천 첫 프로젝트: 기기 상태 수집 CLI

1. `adb devices -l`로 대상을 확인하고 명시적인 Serial 입력을 받는다.
2. 연결 상태에 따라 진행 가능 여부를 기록한다.
3. `shell getprop ro.build.version.release`로 OS 정보를 수집한다.
4. `shell pm path PACKAGE` 등으로 앱 설치 여부를 조사한다. 출력·권한은 **확인 필요**다.
5. 명령별 timeout, 종료 코드, stderr를 포함해 JSON 또는 텍스트로 보관한다.

```json
{
  "serial": "USER_SELECTED_SERIAL",
  "connection_state": "device",
  "os_version": null,
  "app_check": "not_run",
  "steps": []
}
```

이 예시는 결과 구조이며 성공을 나타내지 않는다. 수집 실패를 빈 문자열이나 성공으로 덮어쓰지 않는다.

## Smoke-test 확장

```text
Serial 확인 → ADB 연결 → OS 준비 → APK 설치
→ 앱 실행 → 앱별 성공 조건 확인 → 자료 보관 → mapping 정리
```

- 앱 실행 방식과 성공 조건은 대상 앱에 맞게 정의한다.
- 연결 성공·부팅 완료·설치 성공·앱 성공을 서로 다른 결과로 보고한다.
- 정상 기기, 승인되지 않은 기기, 여러 기기, 설치 실패, 서버 미실행 상황을 시험한다.
- 정리 단계는 실패한 실행에서도 수행하며 본인이 생성한 mapping만 제거한다.

## 완료 기준

- [ ] 대상 선택이 명시적이다.
- [ ] 모든 대기에 timeout이 있다.
- [ ] 오류 계층과 종료 코드를 보관한다.
- [ ] 앱의 성공 조건을 실제로 검사한다.
- [ ] 공개 결과에 민감한 로그가 포함되지 않는다.

## 관련 학습

[[tech/devtools/android-debug-bridge/04-learning/02-deep-dive|진단과 자동화 설계]] · [[tech/devtools/android-debug-bridge/README|학습 경로]]
## Sources

- Android Developers — Android Debug Bridge: https://developer.android.com/tools/adb
- Android SDK Platform-Tools: https://developer.android.com/tools/releases/platform-tools
- Android Developers — Logcat CLI: https://developer.android.com/tools/logcat

> **검증 상태:** 제공된 dossier는 기존 기술 지식에 기반하며 외부 자료로 검증되지 않았다. 아래 URL은 추가 검증용 공식 문서이며 이번 작성에서 열람하지 않았다. 버전·기기·OS에 의존하는 동작은 **확인 필요**다.
