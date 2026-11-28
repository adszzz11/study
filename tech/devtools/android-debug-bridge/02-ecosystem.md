---
date: 2026-11-25
tags: [tech]
type: tech-tool-study
status: draft
---

# ADB Ecosystem — 비교와 선택

## 도구별 역할

| 도구 | 주된 역할 | ADB와의 관계 | 선택 기준 |
|---|---|---|---|
| ADB | 연결·명령·배포·진단 | 기반 도구 | CLI 자동화와 상태 조사 |
| Android Studio | 개발·빌드·디버깅 UI | 기기 작업에 ADB 활용 | 코드와 디버거를 함께 다룸 |
| Fastboot | Bootloader 작업·image flashing | 별도 단계와 protocol | OS 실행 전 작업, unlock·지원 확인 필요 |
| scrcpy | 화면 표시·입력 제어 | 일반적으로 ADB 연결 활용 | 화면을 보며 수동 재현 |
| Appium / UI Automator | UI 시나리오·검증 | 상위 테스트 계층 | 사용자 흐름 반복 검증 |
| SSH | 원격 shell·파일 전송 | 별도 서버와 환경 필요 | 관리 가능한 Linux 환경, Android 기본 제공 확인 필요 |

## 조합 판단

- ADB만으로 좌표 입력과 대기를 연결하면 UI 변화와 타이밍에 취약하다.
- UI 테스트 도구만으로는 연결 장애와 시스템 상태를 충분히 설명하기 어렵다.
- 테스트 프레임워크가 시나리오·assertion을 담당하고, ADB가 대상 선택·배포·실패 자료 수집을 맡게 구성한다.
- Fastboot 명령은 ADB shell 명령의 연장이 아니다. 실행 단계와 데이터 변경 범위를 먼저 확인한다.

## 적용 예

수동 재현은 scrcpy + ADB logcat, 반복 회귀는 UI Automator/Appium + ADB 진단, 앱 코드 디버깅은 Android Studio + ADB 연결을 고려한다. 각 도구의 버전별 통합 범위는 **확인 필요**다.

## 관련 학습

[[tech/devtools/android-debug-bridge/05-projects|진단 보조 프로젝트]] · [[tech/devtools/android-debug-bridge/README|학습 경로]]
## Sources

- Android Developers — Android Debug Bridge: https://developer.android.com/tools/adb
- Android SDK Platform-Tools: https://developer.android.com/tools/releases/platform-tools
- Android Developers — Logcat CLI: https://developer.android.com/tools/logcat

> **검증 상태:** 제공된 dossier는 기존 기술 지식에 기반하며 외부 자료로 검증되지 않았다. 아래 URL은 추가 검증용 공식 문서이며 이번 작성에서 열람하지 않았다. 버전·기기·OS에 의존하는 동작은 **확인 필요**다.

- scrcpy: https://github.com/Genymobile/scrcpy
- UI Automator: https://developer.android.com/training/testing/other-components/ui-automator
- Appium: https://appium.io/docs/en/latest/
