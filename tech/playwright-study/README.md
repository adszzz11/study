---
date: 2026-02-02
tags:
  - tech
  - series
  - playwright
  - e2e-testing
  - automation
status: learning
type: tech-series
---

# Playwright 학습 가이드

> **한 줄 정의**: Microsoft가 개발한 크로스 브라우저 E2E 테스트 및 웹 자동화 프레임워크

## 개요

```mermaid
graph LR
    A[기초 개념] --> B[핵심 API]
    B --> C[실전 테스트]
    C --> D[고급 활용]

    style A fill:#e1f5ff
    style D fill:#ffe1e1
```

Playwright는 Chromium, Firefox, WebKit 등 모든 주요 브라우저에서 안정적인 E2E 테스트를 작성할 수 있게 해주는 현대적인 테스트 프레임워크입니다.

---

## Quick Start

### 설치 (Node.js)

```bash
# 새 프로젝트 초기화 (권장)
npm init playwright@latest

# 기존 프로젝트에 추가
npm install -D @playwright/test
npx playwright install
```

### 설치 (Python)

```bash
pip install playwright
playwright install
```

### 첫 테스트 작성

```typescript
// tests/example.spec.ts
import { test, expect } from '@playwright/test';

test('홈페이지 제목 확인', async ({ page }) => {
  await page.goto('https://playwright.dev');
  await expect(page).toHaveTitle(/Playwright/);
});
```

### 테스트 실행

```bash
# 모든 테스트 실행
npx playwright test

# UI 모드로 실행 (디버깅에 유용)
npx playwright test --ui

# 특정 브라우저로 실행
npx playwright test --project=chromium
```

---

## 학습 플랜

### 1단계: 기초 이해 (1시간)
- [ ] [[01-overview|개요]] - Playwright가 무엇인지 이해
- [ ] [[02-ecosystem|생태계]] - 관련 도구와 비교

### 2단계: 핵심 API 학습 (3시간)
- [ ] [[04-learning/01-page-control|페이지 조작]] - 기본 페이지 제어
- [ ] [[04-learning/02-locators|Locator]] - 요소 선택 전략
- [ ] [[04-learning/03-assertions|Assertions]] - 검증 방법

### 3단계: 실전 활용 (2시간)
- [ ] [[04-learning/04-network|네트워크]] - API 모킹과 가로채기
- [ ] [[04-learning/05-config|설정]] - 테스트 구성
- [ ] [[04-learning/06-debugging|디버깅]] - Codegen과 트러블슈팅

### 4단계: 프로젝트 적용 (선택)
- [ ] [[05-projects|실전 프로젝트]] - Best Practices

---

## 파일 구조

```
playwright-study/
├── README.md              ← 여기 (목차 + Quick Start)
├── 01-overview.md         ← 개요 (핵심 개념, 장단점)
├── 02-ecosystem.md        ← 생태계 (비교, 트렌드)
├── 03-references.md       ← 참고 자료
├── 04-learning/           ← 핵심 학습
│   ├── 01-page-control.md ← 페이지 조작
│   ├── 02-locators.md     ← Locator 전략
│   ├── 03-assertions.md   ← Assertions
│   ├── 04-network.md      ← 네트워크 가로채기
│   ├── 05-config.md       ← 테스트 설정
│   └── 06-debugging.md    ← 디버깅
├── 05-projects.md         ← 실전 프로젝트
└── cheatsheet.md          ← 빠른 참조
```

## 바로가기

| 단계 | 파일 | 설명 |
|------|------|------|
| 기초 | [[01-overview]] | 핵심 개념, 장단점, 사용 사례 |
| 생태계 | [[02-ecosystem]] | 관련 기술, Cypress/Selenium 비교 |
| 참조 | [[03-references]] | 공식 문서, 학습 자료 |
| 핵심 | [[04-learning/]] | 상세 API 학습 |
| 실전 | [[05-projects]] | 프로젝트 적용, Best Practices |
| 치트시트 | [[cheatsheet]] | 빠른 참조 |

---

## 관련 노트

- [[selenium-study]] (있다면)
- [[cypress-study]] (있다면)
- [[e2e-testing]]

---

**생성일**: 2026-02-02
**상태**: 학습 중
