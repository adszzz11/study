---
date: 2026-02-02
tags:
  - tech
  - stagehand
  - references
parent: "[[README]]"
---

# Stagehand - 참고자료

> [[02-ecosystem|이전: 생태계]] | [[README|목차]] | [[04-learning/01-setup|다음: 초기 설정]]

---

## 1. 공식 문서

### 핵심 링크

| 자료 | 링크 | 설명 |
|------|------|------|
| **공식 문서** | [docs.stagehand.dev](https://docs.stagehand.dev) | 메인 문서 사이트 |
| **GitHub** | [github.com/browserbase/stagehand](https://github.com/browserbase/stagehand) | 소스 코드, 이슈 |
| **npm** | [npmjs.com/package/@browserbasehq/stagehand](https://www.npmjs.com/package/@browserbasehq/stagehand) | 패키지 페이지 |
| **Browserbase** | [browserbase.com](https://browserbase.com) | 클라우드 브라우저 플랫폼 |

### 문서 구조

```
docs.stagehand.dev/
├── Getting Started      ← 설치 및 Quick Start
├── API Reference        ← act, extract, observe 상세
├── Agent               ← 자율 에이전트 가이드
├── Configuration       ← 설정 옵션
├── Examples            ← 예제 코드
└── FAQ                 ← 자주 묻는 질문
```

---

## 2. 학습 자료

### 공식 자료

| 유형 | 제목 | 링크 |
|------|------|------|
| 예제 | Stagehand Examples | [GitHub Examples](https://github.com/browserbase/stagehand/tree/main/examples) |
| 블로그 | Browserbase Blog | [browserbase.com/blog](https://browserbase.com/blog) |
| 데모 | 라이브 데모 | 공식 문서 참조 |

### 추천 학습 순서

1. **시작하기**
   - [ ] 공식 문서 Getting Started
   - [ ] GitHub README 읽기

2. **핵심 API**
   - [ ] `act()` 가이드 정독
   - [ ] `extract()` 가이드 정독
   - [ ] `observe()` 가이드 정독

3. **실습**
   - [ ] 공식 예제 따라하기
   - [ ] 간단한 스크래핑 프로젝트

4. **심화**
   - [ ] Agent 문서 학습
   - [ ] 캐싱 및 성능 최적화

---

## 3. 커뮤니티

### 공식 채널

| 채널 | 링크 | 용도 |
|------|------|------|
| **GitHub Issues** | [Issues](https://github.com/browserbase/stagehand/issues) | 버그 리포트, 기능 요청 |
| **GitHub Discussions** | [Discussions](https://github.com/browserbase/stagehand/discussions) | Q&A, 아이디어 공유 |
| **Discord** | Browserbase Discord | 실시간 채팅 (공식 문서에서 링크 확인) |
| **Twitter/X** | @browseraborbase | 업데이트 소식 |

### 활용 팁

- **이슈 검색**: 문제 발생 시 먼저 GitHub Issues 검색
- **예제 코드**: examples 폴더에서 유사 사례 찾기
- **버전 확인**: 문서와 설치된 버전 일치 확인

---

## 4. 관련 기술 문서

### 필수 참고

| 기술 | 문서 | 이유 |
|------|------|------|
| **Playwright** | [playwright.dev](https://playwright.dev) | 하위 엔진 이해 |
| **TypeScript** | [typescriptlang.org](https://www.typescriptlang.org) | 언어 기초 |
| **Zod** | [zod.dev](https://zod.dev) | 스키마 정의 |

### LLM API 문서

| 제공자 | 문서 |
|--------|------|
| OpenAI | [platform.openai.com/docs](https://platform.openai.com/docs) |
| Anthropic | [docs.anthropic.com](https://docs.anthropic.com) |

---

## 5. 유용한 도구

### 개발 도구

| 도구 | 용도 |
|------|------|
| **VS Code** | TypeScript 개발 |
| **Playwright Inspector** | 브라우저 디버깅 |
| **dotenv** | 환경 변수 관리 |

### 테스트 사이트

연습용 웹사이트:

| 사이트 | 용도 |
|--------|------|
| [books.toscrape.com](http://books.toscrape.com) | 스크래핑 연습 |
| [quotes.toscrape.com](http://quotes.toscrape.com) | 간단한 추출 연습 |
| [the-internet.herokuapp.com](https://the-internet.herokuapp.com) | 다양한 UI 패턴 |

---

## 6. 버전 및 변경 이력

### 버전 확인

```bash
# 설치된 버전 확인
npm list @browserbasehq/stagehand

# 최신 버전 확인
npm view @browserbasehq/stagehand version
```

### 변경 이력 확인

- [GitHub Releases](https://github.com/browserbase/stagehand/releases)
- [CHANGELOG.md](https://github.com/browserbase/stagehand/blob/main/CHANGELOG.md)

---

## 7. 트러블슈팅 참고

### 자주 발생하는 문제

| 문제 | 참고 |
|------|------|
| LLM API 오류 | API 키 확인, 요금제 한도 확인 |
| 브라우저 시작 실패 | Playwright 브라우저 설치 확인 |
| 타임아웃 | timeout 설정 조정 |
| 요소 못 찾음 | 자연어 명령 구체화 |

### 디버깅 자료

- Playwright 디버깅 가이드
- Stagehand verbose 모드 활용

---

## 다음 단계

> [!tip] 다음으로
> 참고자료를 북마크했다면 [[04-learning/01-setup|초기 설정]]에서 실습 환경을 구성하세요.

---

## References

- [Stagehand 공식 문서](https://docs.stagehand.dev)
- [GitHub 저장소](https://github.com/browserbase/stagehand)
