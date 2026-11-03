---
date: 2026-11-03
tags: [tech]
type: tech-tool-study
status: draft
---

# AI 기반 Paper Trading 및 불변 Risk Guard 시스템

> **한 줄 정의**: AI가 전략 가설·분석·개선안을 만들되, 독립된 불변 `Risk Guard`가 주문·손실·중단 한도를 강제하는 Paper Trading 시스템이다.

## Overview

LLM이 만든 전략과 코드가 그럴듯해도 과적합, look-ahead bias, 체결 가정, API 재시도 오류 때문에 안전한 매매 시스템이 되는 것은 아니다. 이 학습 노트는 AI를 `research / proposal / code generation`에 한정하고, 주문 권한과 손실 제한은 AI가 바꿀 수 없는 별도 경계로 분리하는 방법을 다룬다.

핵심 흐름은 `backtest → walk-forward / out-of-sample → paper trading → human approval`이다. Paper Trading은 검증 단계이지 live trading의 증명이 아니며, 실제 유동성·슬리피지·체결 품질과 차이가 난다.

## Learning Path

- [ ] [[tech/ai/ai-paper-trading-system/01-overview|Overview]] — 문제, 역할 분리, 핵심 구성요소
- [ ] [[tech/ai/ai-paper-trading-system/02-ecosystem|Ecosystem]] — Alpaca, LEAN, Freqtrade, FinRL 비교
- [ ] [[tech/ai/ai-paper-trading-system/04-learning/01-getting-started|시작하기]] — EMA backtest와 Paper 환경의 첫 안전장치
- [ ] [[tech/ai/ai-paper-trading-system/04-learning/02-deep-dive|Deep Dive]] — Immutable Guard, ledger, promotion gate 설계
- [ ] [[tech/ai/ai-paper-trading-system/05-projects|Projects]] — 단계별 구현 과제
- [ ] [[tech/ai/ai-paper-trading-system/03-references|References]] — 공식 문서와 검증 출처
- [ ] [[tech/ai/ai-paper-trading-system/cheatsheet|Cheatsheet]] — 운영 전·중 점검표

## When To Use

- AI가 전략 후보나 분석 요약을 제안하지만, 주문은 검증된 경로로만 보내야 할 때
- Paper broker에서 전략의 운영 관측성, 손실 제한, 장애 대응을 먼저 검증할 때
- 전략 버전·데이터·prompt·실패 원인을 재현 가능한 실험 기록으로 남겨야 할 때

## When Not To Use

- Paper 결과만으로 live 자본 투입 결정을 자동화하려 할 때
- AI process가 broker credential, risk limit, 배포 권한까지 직접 가져야 하는 구조일 때
- 규제·컴플라이언스·세무 검토가 필요한 실제 투자 자문 또는 고객 자산 운용을 대체하려 할 때

## Related Notes

- [[MOCs/Index]]
- [[MOCs/AI]]
- [[tech/ai/model-context-protocol-mcp/README|Model Context Protocol (MCP)]] — AI tool 권한을 최소화하는 경계 설계 참고

## Sources

- https://www.instagram.com/reel/DfPDCU-Ma2R/
- https://docs.alpaca.markets/us/v1.4.2/docs/paper-trading
- https://docs.alpaca.markets/us/docs/authentication
- https://mlflow.org/docs/latest/ml/tracking/
