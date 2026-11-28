---
date: 2026-11-26
tags: [tech]
type: tech-tool-study
status: draft
---

# References — 근거와 검증 대기 항목

## 근거 상태

> **검증 범위:** EAS = Expo Application Services라는 잠정 해석이다. ‘Eas’의 정확한 의미와 현재 기능·요금·정책·명령어는 확인이 필요하다. 제공된 자료·URL은 없으며 웹 검색이나 URL 열기는 수행하지 않았다.

제공 dossier는 개념 설명의 기반이다. 직접 수집한 제품 문서나 실측 결과는 없으므로 현재 사양을 확인한 것으로 읽지 않는다.

## 확인 순서

| 우선순위 | 확인할 질문 | 확인 후 남길 기록 |
|---|---|---|
| 1 | ‘Eas’가 Expo Application Services인가? | 주제 확인 근거 |
| 2 | Build·Submit·Update의 현재 지원 범위는? | 문서 URL, 확인일, 지원 조건 |
| 3 | Runtime과 배포 대상은 어떻게 연결되는가? | 설정 의미와 호환성 사례 |
| 4 | Credential·Secret은 어디에 저장·노출되는가? | 권한, 보관, 교체 절차 |
| 5 | CLI·설정 문법과 버전 요구는? | 검증한 버전과 최소 재현 예 |
| 6 | 요금·동시 실행·대기·복구 정책은? | 현재 요금표와 실험 결과 |

## 후속 조사 기록 양식

```text
확인일:
문서 URL / 제목:
대상 CLI·SDK·Toolchain 버전:
확인한 사실:
재현 조건 / 결과:
미확인 사항:
영향받는 노트:
```

URL 후보를 기재했다는 사실은 해당 페이지의 내용이나 최신성을 검증했다는 뜻이 아니다. 검증된 문법이 없으므로 실행용 CLI 명령은 이 노트 묶음에 제시하지 않는다.

## 연결

[[tech/devtools/expo-application-services/README|학습 진입점]] · [[tech/devtools/expo-application-services/04-learning/02-deep-dive|심화 검증]]

## Sources

제공 dossier를 기반으로 작성했다. 아래 URL은 후속 확인용 공식 문서 후보이며, 본문을 직접 열어 확인한 근거는 아니다.

- Expo EAS 문서: https://docs.expo.dev/eas/
- EAS Build: https://docs.expo.dev/build/introduction/
- EAS Submit: https://docs.expo.dev/submit/introduction/
- EAS Update: https://docs.expo.dev/eas-update/introduction/
