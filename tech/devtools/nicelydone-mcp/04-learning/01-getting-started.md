---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# Getting Started

## 목표

첫 세션에서는 UI를 생성하지 않는다. B2B analytics SaaS의 data table 문제를 사례 기반으로 조사하고, 구현 전에 design brief를 만든다.

## 준비

1. Nicelydone Pro 계정으로 로그인한다.
2. [MCP 페이지](https://nicelydone.club/mcp)에서 사용할 client의 config를 복사한다.
3. Codex에서는 공식 안내의 `config.toml` 또는 CLI 등록 절차를 따른 뒤 client를 재시작한다.
4. endpoint·header·key를 추측해 작성하지 않는다. 공개 페이지에 실제 연결값이 보이지 않을 수 있으므로 계정 화면의 값을 쓴다.

## Research-only prompt

```text
B2B analytics SaaS의 data table + filter + empty state 사례를 8개 찾고,
공통 UX pattern과 차이점을 표로 요약해줘.
각 사례에서 관찰한 사실과 해석을 분리하고, 원본 copy·branding·asset은 인용하지 마.
```

요청 결과는 다음 표로 압축한다.

| 관찰 항목 | 사례 간 pattern | 우리 제품의 판단 |
| --- | --- | --- |
| Filter | 적용 상태를 chip 또는 summary로 노출 | 복수 filter와 clear-all이 필요한가? |
| Empty state | 원인과 다음 action을 함께 제시 | 권한 없음·검색 결과 없음·초기 상태를 분리할 것인가? |
| Table | density와 column control을 상태별로 조정 | mobile에서 priority column을 어떻게 둘 것인가? |

## Brief로 전환

reference 2~3개를 고른 뒤 아래 세 묶음을 분리한다.

- **채택할 구조:** 예: filter summary, column visibility, empty-state CTA
- **피할 요소:** 예: 지나친 density, 맥락 없는 icon-only control
- **제품 제약:** 자사 token, 권한 모델, API latency, mobile breakpoint, 번역 길이

그 다음에만 original code를 요청한다. 구현 요청에는 `reference를 복제하지 말고 brief와 design system에 맞춰 구현`이라는 제약을 포함한다.

## 완료 기준

- 8개 사례의 관찰과 해석이 구분되어 있다.
- 채택/배제/제약이 있는 brief가 있다.
- 구현 전에 empty, loading, error state가 정의되어 있다.

## Sources

- [Nicelydone MCP](https://nicelydone.club/mcp)
- [Nicelydone Screens](https://nicelydone.club/pages)
- [Nicelydone Components](https://nicelydone.club/components)
