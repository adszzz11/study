# Part 3: References & 커뮤니티 반응

## 원문 자료

| 자료 | 링크 | 설명 |
|------|------|------|
| 원문 블로그 | [My AI Adoption Journey](https://mitchellh.com/writing/my-ai-adoption-journey) | 2026.02.05 게시, 6단계 AI 도입 여정 |
| 실전 사례 | [Vibing a Non-Trivial Ghostty Feature](https://mitchellh.com/writing/non-trivial-vibing) | Ghostty 자동 업데이트 기능을 AI로 구현한 16세션 기록 |
| AI 공개 정책 | [Ghostty PR #8289](https://github.com/ghostty-org/ghostty/pull/8289) | Ghostty 기여 시 AI 사용 공개 의무 정책 |
| Ghostty 프로젝트 | [ghostty.org](https://ghostty.org) | Hashimoto의 현재 주력 프로젝트 |

## 2차 분석 자료

| 자료 | 링크 |
|------|------|
| Pragmatic Engineer 분석 | [Mitchell Hashimoto's new way of writing code](https://newsletter.pragmaticengineer.com/p/mitchell-hashimoto) |
| Serenities AI 정리 | [Mitchell Hashimoto's AI Workflow](https://serenitiesai.com/articles/mitchell-hashimoto-ai-workflow) |
| Simon Willison 소개 | [Mitchell Hashimoto: My AI Adoption Journey](https://simonwillison.net/2026/Feb/5/ai-adoption-journey/) |
| Xiumu AI 분석 | [The Practitioner's Roadmap](https://xiumu.com/the-practitioners-roadmap-to-ai-assisted-development-lessons-from-mitchell-hashimoto/) |
| Catalin's Tech | [How Experts Use AI: Mitchell Hashimoto](https://catalins.tech/how-experts-use-ai-mitchell-hashimoto/) |

## 커뮤니티 반응

### Hacker News ([링크](https://news.ycombinator.com/item?id=46903558))

**긍정적 반응:**

- **libraryofbabel**: "Such a lovely balanced thoughtful refreshingly hype-free post." 2025년이 회의론자들도 AI 도구의 실용적 가치를 인정하기 시작한 시점이라 평가
- **keyle**: 건축가가 손 제도에서 CAD로 전환한 것에 비유. "vibe coding"이라는 용어가 기술을 과소평가한다고 비판
- **saghm**: Claude Code로 100~200줄 범위의 제한된 작업을 실시간으로 감시하며 사용하는 방식 공유. 위임이 아닌 자동화로 접근

**비판적 반응:**

- **atomicnumber3**: "Compilers will produce working output given working input literally 100% of the time." LLM과 컴파일러의 본질적 차이를 지적
- **grey-area**: "LLMs are non-deterministic and unpredictable and fuzzy by _design_." 정확한 출력이 필요한 코드 작성에 비결정적 도구의 한계 강조
- **dns_snek**: 에이전트 주변에 복잡한 제어 장치를 구축하는 것을 "벽돌을 무작위로 던지는 기계 주변에 비계를 세우는 것"에 비유

**실무 관점:**

- **datsci_est_2015**: 솔로 개발 너머에서의 확장성 문제 제기. 생성된 코드의 보안 책임은 여전히 개발자에게 귀속
- **tptacek**: (간결하게) "So read the code."
- **kaibee**: 코드 작성이 조직의 병목이 아닌 경우가 많다고 지적. 의사결정, 컨텍스트 엔지니어링, 벤더 의존성이 진짜 병목

**미래 전망:**

- **wtetzner**: "LLM에 명확한 형식 언어를 입력할 거면, 그 언어의 컴파일러를 작성하면 되지 않나?"
- **senko**: "50년쯤 뒤에 LLM이 얼마나 (비)신뢰할 수 있는지 보자." 컴파일러도 성숙하는 데 수십 년이 걸렸다

### Lobsters ([링크](https://lobste.rs/s/87rudf/my_ai_adoption_journey))

**핵심 토론:**

- **Aloys**: "I interrupt the agent, not the other way around"라는 원칙을 특히 높이 평가. 생산성 향상이 "혁명적"이 아닌 "나쁘지 않은 추가"라는 솔직함에 공감
- **Edk-**: "균형 잡힌" 프레이밍에 의문. AI 혜택을 논하는 것 자체가 암묵적 홍보라는 비판
- **Osa1**: 수동 커밋을 AI로 재현하는 훈련 방식에 의문. AI가 독자적 접근법을 취하도록 허용하는 게 더 나을 수 있다는 대안 제시
- **Hwayne**: AI의 다른 해법을 이해하면 AI를 신뢰할 시점을 판단하는 데 도움이 된다고 반론

**비용 토론:**

- Hashimoto의 월간 AI 비용($400~600)이 예상보다 높다/낮다는 양쪽 반응
- 시간 절약 대비 비용 효율성에 대한 논쟁

**안정성 우려:**

- **Abnercoimbre**: 모델이 업데이트될 때마다 워크플로우를 다시 배워야 하는 문제. 한 개발자가 3세대 모델에 걸쳐 "AI 특성을 재학습"해야 했던 경험 공유

## Ghostty AI 공개 정책

Hashimoto는 Ghostty 프로젝트에 **AI 사용 공개 의무 정책**을 도입했다 (2025.08):

### 규칙 요약

| 항목 | 정책 |
|------|------|
| AI 사용 공개 | PR에 반드시 AI 사용 여부와 범위를 명시 |
| 예외 | 단일 키워드/짧은 구문의 자동완성은 공개 불필요 |
| PR 응답 | AI로 생성한 PR 응답도 공개 필수 |
| 근거 | 공개하지 않으면 "first and foremost rude to the human operators" |

### 공개 예시

- 간단: "This PR was written primarily by Claude Code."
- 상세: "I consulted ChatGPT to understand the codebase but the solution was fully authored manually by myself."

## 관련 읽을거리

- [[01-overview|이전: 저자 소개와 맥락]]
- [[04-learning/01-adoption-stages|다음: AI 도입 단계별 여정]]
- Anthropic의 [AI와 기술 형성 연구](https://www.anthropic.com/research/skill-formation) - Hashimoto가 직접 언급
