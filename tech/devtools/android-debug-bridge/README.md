---
date: 2026-11-25
tags: [tech]
type: tech-tool-study
status: draft
---

# ADB — Android 기기 제어와 디버깅 아키텍처

> **한 줄 정의**: ADB(Android Debug Bridge)는 개발 호스트와 Android 기기 또는 Emulator 사이에서 명령 실행, 앱 배포, 로그 수집, 파일 전송과 디버깅 연결을 제공하는 CLI 기반 통신 도구다.

## Overview

Android 앱은 빌드에 성공해도 설치·실행·권한·네트워크·기기별 동작이 보장되지 않는다. ADB는 개발 환경과 실제 기기 상태를 연결하여 관찰과 자동화를 돕는다.

- **분류:** Android 개발·테스트용 devtools, Android SDK Platform-Tools에 포함.
- **구조:** host의 adb client → adb server → USB/network transport → device의 adbd.
- **핵심:** 대상 Serial을 명시하고 연결 성공, OS 준비, 앱 성공을 각각 판단한다.
- **한계:** ADB는 명령 전달 수단이며 앱의 정확성이나 테스트 성공을 스스로 판정하지 않는다.

> **검증 상태:** 제공된 dossier는 기존 기술 지식에 기반하며 외부 자료로 검증되지 않았다. 아래 URL은 추가 검증용 공식 문서이며 이번 작성에서 열람하지 않았다. 버전·기기·OS에 의존하는 동작은 **확인 필요**다.

## Learning Path

- [ ] [[tech/devtools/android-debug-bridge/01-overview|Overview]] — What/Why, 구조와 권한 경계 이해
- [ ] [[tech/devtools/android-debug-bridge/02-ecosystem|Ecosystem]] — Android Studio·Fastboot·scrcpy·테스트 도구 비교
- [ ] [[tech/devtools/android-debug-bridge/04-learning/01-getting-started|시작하기]] — 연결 → 대상 지정 → 설치·로그·파일 전송 실습
- [ ] [[tech/devtools/android-debug-bridge/04-learning/02-deep-dive|Deep Dive]] — transport·준비 상태·권한·포트 매핑 진단
- [ ] [[tech/devtools/android-debug-bridge/05-projects|Projects]] — 수집 CLI와 smoke-test pipeline 설계
- [ ] [[tech/devtools/android-debug-bridge/cheatsheet|Cheatsheet]] — 자주 쓰는 명령과 정리 절차 확인
- [ ] [[tech/devtools/android-debug-bridge/03-references|References]] — 공식 문서로 버전별 지원 범위 검증

## When To Use

- APK 배포, device shell 접근, logcat 수집을 반복하거나 스크립트로 묶을 때.
- 실제 기기에서 설치·권한·네트워크 문제를 계층별로 조사할 때.
- CI 기기의 상태를 확인하고 테스트 실패 시 진단 자료를 수집할 때.

## When Not To Use

- UI 시나리오의 성공 조건과 안정적인 요소 탐색이 필요하면 Appium/UI Automator 같은 테스트 계층을 함께 사용한다.
- Bootloader 단계의 image flashing은 지원 기기에서 Fastboot 등 별도 도구를 검토한다.
- Production 앱의 sandbox를 우회하거나 모든 기기에서 root 권한을 얻는 수단으로 가정하지 않는다.

## Related Notes

- [[MOCs/Index]]
- [[MOCs/Devtools]]
- [[tech/devtools/android-debug-bridge/01-overview|ADB 아키텍처와 권한 경계]]
- [[tech/devtools/android-debug-bridge/02-ecosystem|Android 개발 도구 비교]]

필수 MOC 링크는 대상 vault에 존재한다는 전제로 기재했다. 이 작업 공간에는 MOCs가 없어 존재 여부는 확인 필요하며, 관리 파일은 생성하지 않는다.

## Sources

- Android Developers — Android Debug Bridge: https://developer.android.com/tools/adb
- Android SDK Platform-Tools: https://developer.android.com/tools/releases/platform-tools
- Android Developers — Logcat CLI: https://developer.android.com/tools/logcat

> **검증 상태:** 제공된 dossier는 기존 기술 지식에 기반하며 외부 자료로 검증되지 않았다. 아래 URL은 추가 검증용 공식 문서이며 이번 작성에서 열람하지 않았다. 버전·기기·OS에 의존하는 동작은 **확인 필요**다.
