---
date: 2026-06-23
tags:
  - tech
  - ai
  - fugu
  - sakana-ai
  - references
type: tech-tool-study
parent: "[[README]]"
---

# Sakana Fugu - 참고자료

> [[02-ecosystem|이전: 생태계]] | [[README|목차로 돌아가기]] | [[04-learning/01-getting-started|다음: 시작하기]]

---

## 1. 공식 자료

| 자료 | URL | 읽을 포인트 |
|------|-----|-------------|
| Sakana Fugu 공식 페이지 | https://sakana.ai/fugu/ | 제품 정의, Fugu/Fugu Ultra 차이, OpenAI-compatible API, opt-out, benchmark claim |
| Sakana Fugu Technical Report | https://arxiv.org/abs/2606.21228 | "orchestrator models" 관점, Fugu/Fugu-Ultra 공개, benchmark method |

---

## 2. 기반 연구

| 자료 | URL | Fugu 학습에서의 의미 |
|------|-----|----------------------|
| TRINITY: An Evolved LLM Coordinator | https://ar5iv.labs.arxiv.org/html/2512.04695 | compact coordinator가 Thinker, Worker, Verifier 역할을 배정하는 방식 |
| Learning to Orchestrate Agents in Natural Language with the Conductor | https://ar5iv.labs.arxiv.org/html/2512.04388 | 7B Conductor가 RL/GRPO로 workflow, subtask, topology를 생성 |
| AI Scientist-v2 | https://arxiv.org/abs/2504.08066 | autonomous scientific discovery/research workflow 맥락 |

---

## 3. 비교 연구와 대안

| 자료 | URL | 비교 포인트 |
|------|-----|-------------|
| Mixture-of-Agents | https://arxiv.org/abs/2406.04692 | 여러 LLM 출력을 layer로 결합하는 multi-agent composition |
| MASRouter | https://arxiv.org/abs/2502.11133 | collaboration mode, role, LLM routing 학습 |
| RouteLLM | https://arxiv.org/abs/2406.18665 | strong/weak model routing으로 비용 절감 |
| AutoGen | https://arxiv.org/abs/2308.08155 | 개발자가 직접 multi-agent conversation framework를 구성 |
| LangGraph | https://arxiv.org/abs/2605.19743 | graph-based agent workflow와 stateful orchestration |

---

## 4. 읽는 순서

1. **Sakana Fugu 공식 페이지**
   - 제품이 무엇을 약속하는지 먼저 확인한다.
   - `Fugu`, `Fugu Ultra`, provider/model opt-out, pricing, benchmark chart를 기록한다.

2. **Fugu Technical Report**
   - Fugu가 단순 router인지, learned orchestrator model인지 구분한다.
   - benchmark별 평가 방식과 baseline 출처를 확인한다.

3. **TRINITY**
   - Thinker/Worker/Verifier role assignment를 중심으로 읽는다.
   - 작은 coordinator와 큰 expert model의 결합 방식에 주목한다.

4. **Conductor**
   - natural-language workflow generation, randomized agent pool, recursive topology를 확인한다.
   - test-time scaling이 cost/latency에 미치는 영향을 정리한다.

5. **RouteLLM, Mixture-of-Agents, MASRouter**
   - Fugu와 비슷해 보이는 연구들이 실제로는 어떤 범위까지만 다루는지 비교한다.

---

## 5. 검증 체크리스트

| 질문 | 확인 방법 |
|------|-----------|
| benchmark score가 provider-reported인가? | 공식 페이지와 technical report의 baseline 설명 확인 |
| 내부 route/model 사용 내역이 공개되는가? | API response metadata와 docs 확인 |
| cost가 token 기준인지 subscription 포함인지? | pricing docs와 invoice/usage export 확인 |
| opt-out이 어떤 provider/model 단위로 가능한가? | account setting 또는 API parameter 확인 |
| Ultra에서도 opt-out이 가능한가? | 공식 문서 확인. dossier 기준 Ultra는 full agent pool 고정 |

---

## 관련 노트

- [[study/tech/ai/agent-orchestration/conductor]] - Conductor 기반 orchestration 이해
- [[study/tech/ai/autoresearch-study]] - research automation 적용 맥락
- [[study/tech/ai/litellm]] - routing/gateway 비교 기준
