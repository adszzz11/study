---
date: 2026-11-01
tags: [tech]
type: tech-tool-study
status: draft
---

# 시작하기: 작은 skill과 private gateway

[[tech/devtools/github-ai-agent-toolkit/README|README]]의 첫 실습은 새 권한을 최소화하고, 결과와 위험을 함께 기록하는 것이다.

## 1. Ponytail로 작은 diff 만들기

1. own bug-fix repository와 test를 하나 고른다.
2. 변경 전 diff 크기와 test 결과를 기록한다.
3. Ponytail의 YAGNI 기준으로 요구사항 밖의 refactor를 제외한다.
4. 변경 후 diff, test, 제외한 변경을 비교한다.

## 2. Taste Skill 결과 비교

같은 frontend 요구사항을 기본 agent와 Taste Skill에 각각 실행한다. typography, spacing, motion, keyboard navigation, contrast를 screenshot과 함께 비교한다. browser inspection은 test profile에서만 한다.

## 3. FreeLLMAPI localhost 실습

Docker 배포는 documentation의 최신 명령을 확인한 후 localhost에만 bind한다. OpenAI-compatible client로 streaming과 provider fallback을 시험하되, production key를 공유하지 않는다.

```text
client -> http://127.0.0.1:<port>/v1 -> gateway -> provider A
                                           -> fallback provider B
```

외부 공개 전에는 auth, encrypted storage, backup, key rotation 정책을 준비한다.

## 완료 기준

- [ ] third-party source와 install script를 읽었다.
- [ ] 실행·파일·network·credential permission을 기록했다.
- [ ] localhost bind와 test key를 사용했다.
- [ ] rollback 또는 uninstall 방법을 확인했다.

심화: [[tech/devtools/github-ai-agent-toolkit/04-learning/02-deep-dive|Deep Dive]]

## Sources

- https://github.com/DietrichGebert/ponytail
- https://github.com/Leonxlnx/taste-skill
- https://github.com/tashfeenahmed/freellmapi/blob/main/docs/en/README.md

## 추가 조사: ECC — cross-harness agent 운영

- ECC는 Claude Code, Codex, OpenCode, Cursor 등 여러 harness에 skills, rules, hooks, MCP convention을 이식하는 agent harness 시스템이다.
- 첫 실습에서는 전체 설치 대신 빈 test repository와 한 harness만 택한다. 설치 전/후에 생성·변경되는 파일을 기록하고, 제거(uninstall) 후 원상 복구되는지 확인한다.
- 성공 기준은 “더 많은 automation”이 아니라, 동일 요구에서 규칙이 재현되고 hook 실패가 작업을 망가뜨리지 않는 것이다.

```text
새 test repo
  ├─ 설치 전: git status / config 백업
  ├─ ECC 최소 설치: 대상 harness 하나
  ├─ smoke task + test
  └─ uninstall → git diff로 잔여 설정 검토
```

## 추가 조사: Agent-Reach — 웹 research access

- Agent-Reach는 X/Twitter, Reddit, YouTube, GitHub 등 여러 채널을 하나의 CLI로 search/read하는 research access 도구다. 채널·백엔드에 따라 로그인 상태나 browser profile에 의존할 수 있다.
- 연구용 계정(secondary account)과 전용 browser profile을 사용하고 read-only로 시작한다. 개인 세션 cookie, production account, 결제 권한이 있는 profile은 연결하지 않는다.
- 결과물에는 원문 URL, 수집 시각, 채널, 요약과 직접 관찰한 사실을 분리해 적는다. 검색 결과는 인용 근거의 후보이지 자동으로 신뢰할 수 있는 근거가 아니다.

## 추가 조사: FreeLLMAPI — OpenAI-compatible gateway

- FreeLLMAPI는 여러 provider와 custom OpenAI-compatible endpoint를 하나의 `/v1` API 뒤에 두고 smart routing, automatic failover, encrypted key storage를 제공한다. 개인 실험(personal experimentation) 용도라는 프로젝트 경계를 유지한다.
- 최신 문서상 agent 호환 기능에는 gateway 상태·지원 모델·provider health를 살피는 MCP 경로도 있다. 이는 관측성(observability)을 높이지만 gateway 접근 토큰의 권한을 넓히므로 별도 test token으로 검증한다.

```bash
# 값은 문서의 현재 Docker/로컬 실행 절차로 대체한다.
export OPENAI_BASE_URL='http://127.0.0.1:<port>/v1'
export OPENAI_API_KEY='<test-gateway-token>'
# streaming, provider 장애, fallback 뒤의 응답/로그를 각각 확인한다.
```

- 운영 전 점검: 외부 bind 금지, bearer token 설정, provider key 암호화 backup, rotation 절차, 실패한 fallback의 비용·데이터 경로 기록.

## 추가 조사: DeepInfer — DeepSeek 대규모 추론(Serving)

- DeepInfer는 DeepSeek 모델의 고성능·대규모 inference framework다. 따라서 일반적인 작은 모델 localhost 실습보다 GPU cluster serving과 긴 context·높은 동시성 benchmark에 적합하다.
- 비교 대상(vLLM/SGLang 등)은 같은 model revision, quantization, prompt/output 길이, batch/concurrency, GPU·driver·network 조건을 고정한다.

| 구간 | 기록할 지표 | 해석 |
|---|---|---|
| Prefill | input tokens/s, time-to-first-token | 긴 입력 처리 병목 |
| Decode | output tokens/s, inter-token latency | 생성 체감 속도 |
| 운영 | error rate, retry, GPU memory/utilization | 안정성·비용 |
