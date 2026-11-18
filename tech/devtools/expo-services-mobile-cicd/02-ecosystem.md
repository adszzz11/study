---
date: 2026-11-18
tags: [tech, devtools, expo, mobile, cicd]
type: tech-tool-study
status: researched
---

# 적용 범위와 선택 기준

Expo SDK는 앱 개발 프레임워크이고 Expo Services는 빌드·배포를 지원하는 서비스다. Expo Build는 기존 React Native 프로젝트도 지원하며 반드시 새 Expo 프로젝트로 다시 시작해야 하는 것은 아니다. [Build 지원 범위](https://docs.expo.dev/build/introduction/)

## 팀별 검토 질문

| 선택 | 기대 효과 | 검증할 부담 |
|---|---|---|
| Expo Services 중심 | 빌드와 업데이트 설정을 일관되게 관리 | 호스팅 비용, 서비스 장애 시 대응, 서명 관리 |
| 기존 CI에서 EAS CLI 호출 | 현재 승인 체계를 유지하면서 필요한 기능 사용 | CI 토큰 보관, 환경 선택, 작업 중복 |
| 기존 네이티브 배포 체계 유지 | 이미 검증한 도구·운영 지식 활용 | macOS 빌드 환경, 서명 갱신, OTA 별도 설계 |

위 표는 설계 판단 기준이며 경쟁 제품의 성능 비교 결과가 아니다. 도구 이름보다 누가 서명 정보를 관리하고, 어느 단계에서 배포를 승인하며, 실패했을 때 무엇을 복구할 수 있는지 먼저 정한다.

Workflows는 `.eas/workflows/`의 YAML로 작업을 구성한다. 공식 시작 안내에는 실패한 작업부터 재실행하는 흐름이 있으며, deploy 템플릿은 호환 빌드 여부에 따라 OTA를 게시할 수 있다. 따라서 템플릿 생성과 실행을 단순한 문서 미리보기로 취급하면 안 된다. [Workflows 시작](https://docs.expo.dev/eas/workflows/get-started/)

## 관련 노트

- [[tech/devtools/expo-services-mobile-cicd/README|연구 목차]]
