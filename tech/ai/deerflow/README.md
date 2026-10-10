---
date: 2026-10-11
tags: [tech]
type: tech-tool-study
status: draft
---

# DeerFlow

> **한 줄 정의**: DeerFlow는 ByteDance가 공개한, subagent·memory·sandbox·skills·tools를 묶어 장시간 research, coding, artifact 생성 작업을 수행하는 오픈소스 SuperAgent harness다.

## Overview

일반 LLM chat은 단발성 질의에는 충분하지만 조사→계획→웹 탐색→파일·코드 작업→검증→결과물 생성처럼 긴 작업에서는 context 누적, tool 권한, 실행 격리, 실패 복구, 병렬화가 문제가 된다. DeerFlow는 이 long-horizon agent 문제를 위해 workflow graph를 매번 직접 조립하는 대신, 조합된 runtime과 reference App을 제공한다.

v2.0은 1.x Deep Research 구현을 단순히 갱신한 것이 아니라 코드 공유 없이 재작성한 SuperAgent harness다. 현재 활성 개발의 중심은 2.x 계열이다. Harness는 SDK/runtime 층이고, App은 deployment·운영·end-user workflow를 제공하는 reference application이다.

## Learning Path

- [ ] [[01-overview|개요]] — What/Why, 핵심 구조와 안전 경계 이해
- [ ] [[02-ecosystem|생태계]] — LangGraph, OpenAI Agents SDK, Google ADK, CrewAI 비교
- [ ] [[03-references|참고자료]] — 공식 문서와 release note 확인
- [ ] [[04-learning/01-getting-started|시작하기]] — repository 기반 설치와 최소 research task 실행
- [ ] [[04-learning/02-deep-dive|심화]] — middleware, subagent, memory, sandbox 설계
- [ ] [[05-projects|프로젝트]] — intelligence, analyst copilot, engineering agent 적용
- [ ] [[cheatsheet|치트시트]] — 구성요소·보안·도입 점검 빠른 참조

## When To Use

- research·coding·analysis처럼 여러 tool 호출, 파일 산출물, 긴 작업 상태가 필요한 경우
- isolated subagent로 탐색을 병렬화하고 lead agent의 context pollution을 줄이고 싶은 경우
- self-hosted runtime과 함께 바로 쓸 수 있는 web App 운영층도 필요한 경우
- sandbox, skill allowlist, approval boundary를 갖춘 agent workflow를 실험·구축할 때

## When Not To Use

- 단일 모델 호출이나 짧은 deterministic workflow만 필요한 경우
- node별 상태 전이와 retry/HITL을 매우 세밀하게 직접 설계해야 하는 경우에는 LangGraph가 더 적합할 수 있다.
- sandbox 없이 host shell·filesystem을 광범위하게 노출해야 한다고 생각하는 경우
- production에서 multi-user isolation, authorization, backup·rollback을 검증하지 않은 상태

## Related Notes

- [[MOCs/Index]]
- [[MOCs/AI]]
- [[tech/ai/model-context-protocol-mcp/README|Model Context Protocol (MCP)]] — 외부 tool 연결과 최소 권한 경계

## Sources

- https://github.com/bytedance/deer-flow
- https://deerflow.tech/en/docs
- https://github.com/bytedance/deer-flow/releases/tag/v2.0.0
- https://github.com/bytedance/deer-flow/releases
