---
date: 2026-11-28
tags: [tech]
type: tech-tool-study
status: draft
---

# Ecosystem: 제품 대신 구현 대안 비교

## 비교 범위

제공 자료에는 경쟁 backend 제품의 가격·기능·보안 비교가 없다. 아래는 이슈의 제안과 구현 선택지 비교다.

| 방식 | 장점 | 한계·주의점 | 사례와의 관계 |
|---|---|---|---|
| Remote fetch 후 즉시 실행 | 중앙 로직 갱신 용이 | 실행 시점마다 코드가 달라질 수 있음 | `add` 구조 |
| 다운로드와 실행만 분리 | 검토 지점 마련 가능 | 검토·검증이 없으면 신뢰 문제 유지 | 분리 자체는 보증 아님 |
| Plugin에 script 포함 | 배포물과 실행 코드 함께 검토 | 업데이트마다 재검토 | 작성자 제안 |
| Hash pinning | 승인한 bytes와 동일성 확인 | Hash 신뢰 경로 필요; 안전성 보증 아님 | 작성자 제안 |
| 전송 고지와 선택권 | 데이터 이동 판단 가능 | 거절 시 기본 경로 필요 | 작성자 제안 |
| 원격 실행 명시, harness 판단 수용 | 실행 의도와 정책 일치 | 환경에 따라 승인 또는 거절 | 회피 지시 제거 |

## Marketplace와 신뢰

작성자는 plugin이 Anthropic의 `claude-plugins-official` marketplace에 있다고 설명한다. 이는 제공 이슈의 진술이며 현재 등록 상태나 심사 범위를 별도로 확인한 결과가 아니다. 배포 채널의 신뢰는 개별 skill의 payload와 실행 코드 검토를 대체하지 않는다.

후속 댓글의 대안 제품 검토 반응은 신뢰에 대한 정성적 신호다. 고객 이탈 규모나 취약점 재현을 입증하지 않는다. 제공 댓글에는 maintainer의 해명이나 수정 완료를 확인할 내용도 없다.

## 적용 기준

- 데이터 전송과 코드 실행을 각각 명시하고 선택 가능하게 한다.
- 검토한 코드와 실행한 코드가 같은지 확인할 수 있게 한다.
- Tool call을 나누더라도 전체 실행 효과를 harness에 드러낸다.

[[tech/devtools/convex-skill-trust-boundary/05-projects|대안 설계 프로젝트]] · [[tech/devtools/convex-skill-trust-boundary/README|학습 경로]]

## Sources

- https://github.com/convex/convex-backend-skill/issues/64
