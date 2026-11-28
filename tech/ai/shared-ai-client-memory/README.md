---
date: 2026-11-27
tags: [tech]
type: tech-tool-study
status: draft
---

# 여러 AI 클라이언트의 공유 메모리와 에이전트 운영 아키텍처

> **한 줄 정의**: Claude·Codex 등 여러 AI 클라이언트가 공통 지식과 작업 맥락을 참조하도록 연결하는 메모리 구조이며, Orbit Agents는 이를 지식 그래프와 에이전트 운영 화면에 결합하는 구상으로 소개된다.

## Overview

클라이언트가 바뀔 때마다 정보를 다시 전달하는 부담을 줄이려는 접근이다. 공통 메모리는 파일·출력물·엔터티의 관계를 보존하고 다음 작업의 접점이 될 수 있다. 다만 반복 입력 감소나 작업 인계의 성공은 제공 자료에서 측정되지 않았다.

Orbit Agents 소개에는 지식 그래프, Lead Finder·Email Outreach Agent, CRM, 성과 대시보드와 부서별 조직도가 등장한다. **화면 소개는 확인되지만 Claude와 Codex의 실제 연결·읽기·쓰기·작업 인계는 미검증**이다. 저장 DB, 검색 기술, MCP·API·파일 동기화 사용 여부도 알 수 없다.

| 관점 | 학습 질문 |
|---|---|
| 공유 메모리 | 누가 어떤 정보를 읽고 쓰며 최신 상태를 공유하는가? |
| 지식 그래프 | 정보 사이 관계의 의미와 근거를 어떻게 표현하는가? |
| 에이전트 운영 | 실행 증거·권한·성과를 어떻게 확인하는가? |

## Learning Path

- [ ] [[tech/ai/shared-ai-client-memory/01-overview|Overview]] — 정의, 구성, 확인 범위 구분
- [ ] [[tech/ai/shared-ai-client-memory/02-ecosystem|Ecosystem]] — 제품·클라이언트·설계 접근 비교
- [ ] [[tech/ai/shared-ai-client-memory/03-references|References]] — 근거 수준과 누락된 원문 확인
- [ ] [[tech/ai/shared-ai-client-memory/04-learning/01-getting-started|시작하기]] — 작은 Research 인계 실험 설계
- [ ] [[tech/ai/shared-ai-client-memory/04-learning/02-deep-dive|Deep Dive]] — 최신성·충돌·권한·실행 증거 평가
- [ ] [[tech/ai/shared-ai-client-memory/05-projects|Projects]] — 검증 단계를 적용 프로젝트로 확장
- [ ] [[tech/ai/shared-ai-client-memory/cheatsheet|Cheatsheet]] — 평가 질문과 판정 기준 재확인

## When To Use

- 여러 AI 클라이언트가 같은 조사 자료를 재사용해야 할 때
- 원본과 파생 출력물의 계보·출처를 추적하려 할 때
- 메모리와 에이전트 운영을 함께 평가할 기준이 필요할 때

## When Not To Use

- 단일 클라이언트의 작은 작업으로 공통 저장소 운영 부담을 감당할 이유가 없을 때
- 검증 없이 제품의 호환성·보안·성능을 보장해야 하는 상황
- 그래프 화면이나 조직도만으로 동기화·접근 통제를 판단하려 할 때

## Related Notes

- [[MOCs/Index]]
- [[MOCs/AI]]
- [[tech/ai/shared-ai-client-memory/01-overview|공유 메모리의 개념과 아키텍처]]
- [[tech/ai/shared-ai-client-memory/04-learning/02-deep-dive|메모리 신뢰성과 운영 검증]]

현재 작업 폴더에는 기존 vault 파일이 없어 MOC 두 항목의 존재를 확인하지 못했다. 위 MOC 링크는 요청된 연결 지점이며, 관리 파일은 생성하거나 수정하지 않았다.

## Sources

- 사용자 제공 dossier: Orbit Agents 소개 영상의 수집 요약. 원본 URL·게시일·제품 버전은 제공되지 않았다.
- 출처 URL: 미제공. 제품 이름만으로 공식 사이트나 영상을 추정해 기재하지 않는다.
- 아래 실습·평가 기준은 dossier에서 도출한 학습 제안이며, 제품의 검증된 기능이나 공식 사용법이 아니다.
