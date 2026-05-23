# Part 5. AutoGen 실전 프로젝트

## 🟢 P1. 코드 작성 + 리뷰 두 명 (★)

```
user_proxy ⇄ coder ⇄ reviewer
```

coder가 코드 작성 → reviewer가 비판 → coder 수정 → reviewer가 APPROVED 출력 → 종료.

대표적인 AutoGen 패턴. v0.2/AG2 GroupChat이 적합.

## 🟡 P2. 디베이트로 의사결정 (★★)

3명의 에이전트가 "이 PR 머지해야 하나" 두고 토론 후 voter가 결정.

- pro: 머지 찬성 입장만 주장
- con: 머지 반대 입장만 주장
- judge: 양측 듣고 결론

GroupChat의 진가가 발휘되는 케이스.

## 🟡 P3. AutoGen Studio로 가족 워크플로우 시연 (★)

비기술 가족에게 "이렇게 일이 흘러갑니다"를 보여줄 때 Studio 캔버스가 효과적.

## 🔴 P4. MagenticOne 패턴 시도 (★★★★)

Microsoft가 공개한 multi-agent 벤치마크 환경. 웹 브라우저 + 파일 + 코드 실행이 결합된 복합 작업 해결.

## ⚠️ Best Practices

- `max_round` 항상 명시 (무한 토론 방지)
- code execution은 Docker
- termination 조건 명시 (TextMention, MaxMessage, Timeout)
- 비용 모니터링: 매 라운드 LLM 호출 로깅
- 프로덕션 가려면 LangGraph로 마이그레이션 검토
