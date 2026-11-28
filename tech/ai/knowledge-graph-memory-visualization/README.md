---
date: 2026-11-27
tags: [tech]
type: tech-tool-study
status: draft
---

# 지식 그래프 기반 AI 메모리 시각화와 에이전트 운영

> **한 줄 정의**: 지식 그래프 기반 AI 메모리 시각화는 파일·출력물·엔터티를 노드와 관계로 표현해, 에이전트가 다루는 정보의 연결 구조를 사람이 탐색하도록 하는 방식이다.

## Overview

Orbit Agents가 제시하는 방향은 **메모리 탐색과 에이전트 운영의 통합**이다. Claude·Codex 등 여러 AI 클라이언트가 하나의 메모리에 연결되고, 파일·출력물·엔터티의 관계를 knowledge graph 화면으로 탐색하는 구상이다. CRM, 성과 대시보드, 부서별 조직도도 등장한다.

- 학습 초점: 관계의 의미, 출처 추적, 공유 메모리의 변경, 업무 기록과의 연결.
- 배경 문제: 자료·출력물의 분산과 정보 맥락·운영 맥락의 분리. 이는 영상 구성에서 도출한 해석이다.
- 근거 수준: 홍보 영상의 요약. 화면이 등장한 것과 실제 연동·실행이 검증된 것은 구분한다.
- 미확인: graph database, API·protocol, 검색, 동기화, 권한, 비용 및 성과.

## Learning Path

- [ ] [[tech/ai/knowledge-graph-memory-visualization/01-overview|Overview]] — What/Why와 관찰·구상·미확인을 구분한다.
- [ ] [[tech/ai/knowledge-graph-memory-visualization/02-ecosystem|Ecosystem]] — Obsidian과의 비교 범위 및 판단 한계를 읽는다.
- [ ] [[tech/ai/knowledge-graph-memory-visualization/03-references|References]] — 자료의 출처와 검증 수준을 확인한다.
- [ ] [[tech/ai/knowledge-graph-memory-visualization/04-learning/01-getting-started|시작하기]] — 6개 노드로 관계와 근거 추적을 연습한다.
- [ ] [[tech/ai/knowledge-graph-memory-visualization/04-learning/02-deep-dive|Deep Dive]] — 충돌·버전·운영 연결의 검증을 설계한다.
- [ ] [[tech/ai/knowledge-graph-memory-visualization/05-projects|Projects]] — Research·Outreach·공유 메모리 과제를 수행한다.
- [ ] [[tech/ai/knowledge-graph-memory-visualization/cheatsheet|Cheatsheet]] — 평가 질문과 오해 방지 항목을 복습한다.

## When To Use

- 여러 에이전트의 자료와 출력물이 어떻게 연결되는지 사람이 검토할 때.
- 요약의 근거 파일을 추적하거나 에이전트 실행 기록과 연결하는 구조를 설계할 때.
- 공유 메모리 도입 전 검색·버전·충돌 처리를 검증할 때.

## When Not To Use

- 홍보 화면만으로 검증된 장기 기억·호환성·성과 개선을 보장해야 할 때.
- 관계의 의미나 출처 없이 노드 수와 연결 밀도만으로 신뢰성을 판단할 때.
- 단순 목록으로 충분한 작업에 그래프 관리 비용을 추가할 때.

## Related Notes

- [[MOCs/Index]]
- [[MOCs/AI]]
- [[tech/ai/knowledge-graph-memory-visualization/01-overview|AI 메모리 시각화의 개념과 아키텍처]]

위 MOC 경로는 요청된 vault 연결점이다. 현재 빈 작업 폴더에서는 대상 존재를 확인하지 못했으며 관리 파일은 생성하지 않았다.

## Sources

- 사용자 제공 dossier: Orbit Agents 홍보 영상 요약. 원본 영상·제품 URL 미제공으로 직접 확인 불가.
- Obsidian 공식 사이트: https://obsidian.md/ — 비교 대상의 공식 진입점인 보조 자료이며 Orbit Agents 기능의 근거가 아니다.
- Obsidian Help: https://help.obsidian.md/ — 노트 작성·그래프 탐색을 추가 학습하기 위한 보조 자료. 본 노트의 제품 비교는 dossier 범위로 제한한다.
