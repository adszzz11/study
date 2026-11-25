---
date: 2026-11-25
tags: [tech]
type: tech-tool-study
status: draft
---

# ADB References — 검증용 자료

## 자료 상태

제공 dossier에는 출처 URL이나 수집 자료가 없다. 아래는 추가 검증을 위한 공식 문서 후보이며 이번 작성에서 웹 검색이나 URL 열람을 수행하지 않았다. 따라서 본문을 이 문서들로 검증한 것으로 해석하지 않는다.

## 읽기 순서와 확인 질문

| 순서 | 자료 | 확인할 내용 |
|---|---|---|
| 1 | Platform-Tools 릴리스 문서 | 호스트 OS 지원, 설치·업데이트, adb 버전 |
| 2 | ADB 가이드 | client/server/adbd, 기기 선택, authorization |
| 3 | ADB Wireless debugging 절 | 지원 Android 버전, pairing·연결 포트 |
| 4 | Logcat CLI 가이드 | 필터·형식·버전별 접근 범위 |
| 5 | AOSP ADB 자료 | 프로토콜과 구현 구조 심화 |

## 검증 기록 양식

```text
확인 날짜:
Host OS / adb version:
Device model / Android version / build type:
확인한 URL 및 절:
실행 명령 / 종료 코드:
관찰 결과 / 남은 불확실성:
```

`adb help`와 실제 기기 결과도 함께 기록한다. 특히 `root`, `run-as`, 저장소 접근, dumpsys 출력, forward/reverse endpoint 지원은 **확인 필요**다.

## 관련 노트

[[tech/devtools/android-debug-bridge/04-learning/02-deep-dive|검증할 핵심 개념]] · [[tech/devtools/android-debug-bridge/README|학습 경로]]
## Sources

- Android Developers — Android Debug Bridge: https://developer.android.com/tools/adb
- Android SDK Platform-Tools: https://developer.android.com/tools/releases/platform-tools
- Android Developers — Logcat CLI: https://developer.android.com/tools/logcat

> **검증 상태:** 제공된 dossier는 기존 기술 지식에 기반하며 외부 자료로 검증되지 않았다. 아래 URL은 추가 검증용 공식 문서이며 이번 작성에서 열람하지 않았다. 버전·기기·OS에 의존하는 동작은 **확인 필요**다.

- AOSP ADB 구현 자료: https://android.googlesource.com/platform/packages/modules/adb/+/refs/heads/main/README.md
