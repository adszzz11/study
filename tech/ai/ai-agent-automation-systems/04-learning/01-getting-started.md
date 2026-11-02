---
date: 2026-11-03
tags: [tech]
type: tech-tool-study
status: draft
---

# AI Agent·MCP·콘텐츠 자동화 시스템: 시작하기

[[tech/ai/ai-agent-automation-systems/README|README]] · 다음: [[tech/ai/ai-agent-automation-systems/04-learning/02-deep-dive|심화]]

## 목표

“매주 경쟁사 AI 뉴스 조사 후 출처가 있는 5개 요약을 초안으로 저장”처럼 작고 되돌릴 수 있는 반복 업무 하나를 완성한다. 첫 버전은 자동 발행하지 않는다.

## 1. 업무를 분해한다

```text
입력: 주제, 기간, 신뢰할 출처
판단: 중복 제거, 중요도 평가, 요약
실행: 검색 결과와 초안 저장
검수: 출처·사실·형식 점검
발행: 사람 승인 후에만 수행
```

## 2. Agent contract를 쓴다

```yaml
role: research editor
allowed_sources: 공식 문서와 공개 웹 페이지
output: [{title, summary, source_url, confidence}]
prohibited_actions: [send_email, publish_post, purchase]
done_when: source_url이 있는 5개 항목과 누락 사유를 반환
```

## 3. 최소 권한으로 연결한다

- search와 문서 읽기 같은 read-only tool부터 쓴다.
- 저장 위치는 draft folder 또는 database의 draft 상태로 한정한다.
- write action을 필요로 하면 workflow에서 approval token을 확인한다.

## 4. workflow로 고정한다

schedule → source fetch → Agent 요약 → schema validation → draft 저장 → reviewer 알림 순서로 둔다. API 실패는 retry하되, 중복 실행에도 같은 초안이 여러 번 생기지 않도록 idempotency key를 둔다.

## 완료 기준

- 5개 항목에 URL이 있고 원문 없이도 검토할 수 있다.
- Agent가 호출한 tool과 실패가 run log에 남는다.
- 자동 공개·발송 없이 사람이 초안을 승인할 수 있다.

## Sources

- https://n8n.io/ai-agents/
- https://docs.n8n.io/advanced-ai/ai-agents/
- https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/prompt-templates-and-variables

