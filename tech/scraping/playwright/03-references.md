---
date: 2026-02-02
tags:
  - tech
  - playwright
  - references
parent: "[[README]]"
---

# Playwright - 참고 자료

> [[02-ecosystem|이전: 생태계]] | [[README|목차]] | [[04-learning/01-page-control|다음: 페이지 조작]]

---

## 1. 공식 문서

### 필수 문서

| 문서 | URL | 설명 |
|------|-----|------|
| 공식 홈페이지 | [playwright.dev](https://playwright.dev) | 메인 문서 |
| Getting Started | [playwright.dev/docs/intro](https://playwright.dev/docs/intro) | 시작 가이드 |
| API Reference | [playwright.dev/docs/api/class-playwright](https://playwright.dev/docs/api/class-playwright) | API 레퍼런스 |
| Best Practices | [playwright.dev/docs/best-practices](https://playwright.dev/docs/best-practices) | 권장 사례 |

### 주요 가이드

| 주제 | URL |
|------|-----|
| Locators | [playwright.dev/docs/locators](https://playwright.dev/docs/locators) |
| Assertions | [playwright.dev/docs/test-assertions](https://playwright.dev/docs/test-assertions) |
| Auto-waiting | [playwright.dev/docs/actionability](https://playwright.dev/docs/actionability) |
| Network | [playwright.dev/docs/network](https://playwright.dev/docs/network) |
| Authentication | [playwright.dev/docs/auth](https://playwright.dev/docs/auth) |
| Test Configuration | [playwright.dev/docs/test-configuration](https://playwright.dev/docs/test-configuration) |
| Debugging | [playwright.dev/docs/debug](https://playwright.dev/docs/debug) |

---

## 2. GitHub 리소스

### 공식 저장소

| 저장소 | 설명 |
|--------|------|
| [microsoft/playwright](https://github.com/microsoft/playwright) | 메인 저장소 |
| [microsoft/playwright-python](https://github.com/microsoft/playwright-python) | Python 바인딩 |
| [microsoft/playwright-java](https://github.com/microsoft/playwright-java) | Java 바인딩 |
| [microsoft/playwright-dotnet](https://github.com/microsoft/playwright-dotnet) | .NET 바인딩 |

### 유용한 저장소

| 저장소 | 설명 |
|--------|------|
| [playwright-community](https://github.com/playwright-community) | 커뮤니티 플러그인 |
| [Awesome Playwright](https://github.com/mxschmitt/awesome-playwright) | 리소스 모음 |

---

## 3. 학습 자료

### 무료 강좌

| 강좌명 | 플랫폼 | 언어 |
|--------|--------|------|
| Learn Playwright | [playwright.dev/docs/intro](https://playwright.dev/docs/intro) | 영어 |
| Playwright Tutorial | YouTube (여러 채널) | 영어 |
| Test Automation University - Playwright | [testautomationu.applitools.com](https://testautomationu.applitools.com) | 영어 |

### 추천 블로그/아티클

| 제목 | 출처 |
|------|------|
| Playwright 공식 블로그 | [playwright.dev/blog](https://playwright.dev/community/welcome) |
| Microsoft DevBlogs | [devblogs.microsoft.com](https://devblogs.microsoft.com) |
| Testing JavaScript | [testingjavascript.com](https://testingjavascript.com) |

### 책

| 제목 | 저자 | 비고 |
|------|------|------|
| End-to-End Web Testing with Playwright | Debbie O'Brien | 입문용 |
| Playwright: Up and Running | TBD | 실무 중심 |

---

## 4. 커뮤니티

### 공식 채널

| 채널 | URL | 용도 |
|------|-----|------|
| Discord | [aka.ms/playwright/discord](https://aka.ms/playwright/discord) | 실시간 Q&A |
| GitHub Discussions | [github.com/microsoft/playwright/discussions](https://github.com/microsoft/playwright/discussions) | 질문/토론 |
| Stack Overflow | [stackoverflow.com/questions/tagged/playwright](https://stackoverflow.com/questions/tagged/playwright) | Q&A |
| Twitter/X | [@plaaborwrightweb](https://twitter.com/playwrightweb) | 업데이트 소식 |

### 한국어 커뮤니티

| 채널 | 설명 |
|------|------|
| OKKY | 한국 개발자 커뮤니티 Q&A |
| Velog/티스토리 | 한국어 블로그 포스팅 |

---

## 5. 도구 및 확장

### VS Code 확장

| 확장 | 설명 |
|------|------|
| [Playwright Test for VS Code](https://marketplace.visualstudio.com/items?itemName=ms-playwright.playwright) | 공식 확장 (필수) |

### 리포팅 도구

| 도구 | 설명 |
|------|------|
| HTML Reporter | 기본 제공 |
| Allure | [allure-playwright](https://www.npmjs.com/package/allure-playwright) |
| ReportPortal | 엔터프라이즈급 리포팅 |

### 시각적 테스트

| 도구 | 설명 |
|------|------|
| Playwright 내장 | `toHaveScreenshot()` |
| Percy | 시각적 리뷰 플랫폼 |
| Chromatic | Storybook 통합 |
| Argos | 오픈소스 시각적 테스트 |

---

## 6. 버전 및 릴리스

### 릴리스 주기

- **주기**: 약 월 1회 마이너 버전 릴리스
- **LTS**: 별도 LTS 없음 (항상 최신 버전 권장)

### 버전 확인

```bash
# 설치된 버전 확인
npx playwright --version

# 최신 버전 확인
npm view @playwright/test version
```

### 업그레이드

```bash
# 최신 버전으로 업그레이드
npm install -D @playwright/test@latest

# 브라우저도 함께 업데이트
npx playwright install
```

### Changelog

- [GitHub Releases](https://github.com/microsoft/playwright/releases)
- [playwright.dev/docs/release-notes](https://playwright.dev/docs/release-notes)

---

## 7. 학습 로드맵

### 입문자 (1주)

1. [ ] 공식 Getting Started 완료
2. [ ] 첫 테스트 작성 및 실행
3. [ ] Codegen으로 코드 생성 체험
4. [ ] Locator 기본 사용법

### 중급자 (2주)

1. [ ] 모든 Locator 전략 학습
2. [ ] Assertions 완전 이해
3. [ ] 네트워크 가로채기 실습
4. [ ] CI/CD 통합

### 고급자 (지속)

1. [ ] 커스텀 Fixture 작성
2. [ ] 리포팅 커스터마이징
3. [ ] 성능 테스트 통합
4. [ ] 팀 테스트 전략 수립

---

## 다음 단계

> [!tip] 다음으로
> 참고 자료를 북마크했다면 [[04-learning/01-page-control|페이지 조작]]부터 실습을 시작하세요.

---

## References

- [Playwright 공식 문서](https://playwright.dev)
- [Awesome Playwright](https://github.com/mxschmitt/awesome-playwright)
