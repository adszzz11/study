---
date: 2026-10-24
tags: [tech]
type: tech-tool-study
status: draft
---

# The Pragmatic Engineer — Deep dive

[[tech/devtools/the-pragramitic-engineer/README|학습 진입점]] · 다음: [[tech/devtools/the-pragramitic-engineer/05-projects|Projects]]

## AI coding 도입을 시스템으로 읽기

AI coding agent의 가치는 생성한 code 양이 아니라 팀이 안전하게 받아들이는 변화의 throughput으로 판단한다. Cursor 사례를 읽으며 `context management`, latency, indexing, database migration, feature flag를 분리해 architecture note를 만든다. 각각은 서로 다른 failure mode와 owner를 가진다.

| 층 | 질문 | 확인할 failure mode |
|---|---|---|
| Context | agent가 올바른 repo·문서를 보나? | 오래된 context, 권한 밖 정보 노출 |
| Indexing | 대규모 repo를 최신 상태로 찾나? | stale index, 긴 초기화 시간 |
| Generation | 제안 code가 실행 가능한가? | hallucination, API 오용 |
| Review | 사람이 위험을 이해하고 승인하나? | reviewer overload, ownership 공백 |
| Release | 작은 범위에서 되돌릴 수 있나? | feature flag 부재, 느린 rollback |

## baseline과 실험 설계

도입 전 최소 2~4주 baseline을 잡고, 한 team·한 repository에서 small-batch rollout을 한다. 도구의 dashboard만으로 성공을 선언하지 않고 아래 지표를 같은 정의로 비교한다.

```text
review throughput = 완료 PR 수 / reviewer 투입 시간
test pass rate = CI 통과 PR / 전체 PR
incident rate = 배포 후 incident / 배포 횟수
rollback time = incident 감지부터 안전 상태 복구까지의 시간
```

지표가 좋아도 security scan 결과, human owner 명시, change size, 운영 피로도를 함께 검토한다. 상관관계만으로 agent가 원인이라고 결론 내리지 않는다.

## governance checklist

- [ ] AI 생성 PR에도 human owner와 reviewer를 지정한다.
- [ ] test/eval과 security scan을 merge 전 필수 경로에 둔다.
- [ ] feature flag 또는 동등한 small-batch rollout·rollback 방법을 준비한다.
- [ ] privacy, context window, repo indexing, CI integration, 비용의 변경을 기록한다.
- [ ] threshold를 넘는 incident 또는 품질 저하 시 rollout을 멈출 조건을 합의한다.

## Sources

- [Building Cursor](https://newsletter.pragmaticengineer.com/p/cursor)
- [How AI-assisted coding will change software engineering](https://newsletter.pragmaticengineer.com/p/how-ai-will-change-software-engineering)
- [When AI writes almost all code](https://newsletter.pragmaticengineer.com/p/when-ai-writes-almost-all-code-what)
- [What is happening with code reviews](https://newsletter.pragmaticengineer.com/p/what-is-happening-with-code-reviews)
