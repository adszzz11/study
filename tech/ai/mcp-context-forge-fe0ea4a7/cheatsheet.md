---
date: 2026-11-29
tags: [tech]
type: tech-tool-study
status: draft
---

# ContextForge Cheatsheet

## 개념 빠른 참조

| 용어 | 기억할 점 |
|---|---|
| Registry | Tools·Prompts·Resources 중앙 관리 |
| Virtual Server | 선택한 tool들의 논리적 MCP server |
| `associated_tools` | Catalog에서 얻은 실제 tool ID 목록 |
| `/servers/<UUID>/mcp` | Virtual Server의 client 접속 경로 예시 |
| API adaptation | REST/gRPC를 MCP tool로 표현 |
| Transport bridging | stdio MCP를 SSE·Streamable HTTP로 노출 |
| Protocol version | Transport와 별도 호환성 설정; 자료 예시 `2025-11-25` |
| Federation | 여러 Gateway 연계; consistency·failover 세부 미확인 |

## 시작 전 체크

- [ ] 선택 release/tag 또는 commit SHA 기록
- [ ] Python ≥ 3.11 및 architecture 지원 확인
- [ ] `JWT_SECRET_KEY`, `AUTH_ENCRYPTION_SECRET` 준비 및 안전한 보관
- [ ] Client → Gateway와 Gateway → upstream 인증 분리
- [ ] 실제 tool ID·server UUID 확인
- [ ] 읽기 전용 정상·오류 호출 검증

## 문제를 좁히는 순서

| 증상 | 확인할 경계 |
|---|---|
| Gateway 시작 실패 | 필수 secret 및 선택 버전 설정 |
| Tool 목록이 예상과 다름 | Registry 등록과 `associated_tools` 구성 |
| Client 연결 실패 | Endpoint, transport, protocol version, Gateway 인증 |
| Upstream 인증 실패 | Backend credential과 `X-Upstream-Authorization` 적용 규칙 |
| gRPC discovery 실패 | Reflection 지원·접근 가능 여부 |
| 호출 지연·오류 | Gateway·adapter·upstream trace와 timeout/retry 정책 |

## 단정하지 말 것

- Virtual Server 구성만으로 권한 격리 보장
- Schema 자동 추출만으로 tool 설명 품질 보장
- Guardrails 소개만으로 prompt-injection 방어·DLP 보장
- Test 수만으로 성능·보안·장애 복구 보장
- TOON 압축률, routing 정책, federation failover의 미확인 세부

[[tech/ai/mcp-context-forge-fe0ea4a7/04-learning/01-getting-started|시작하기]] · [[tech/ai/mcp-context-forge-fe0ea4a7/03-references|출처와 미확인 사항]] · [[tech/ai/mcp-context-forge-fe0ea4a7/README|학습경로]]

## Sources

- https://github.com/IBM/mcp-context-forge — 제공된 repository 발췌 dossier의 원 출처.
- https://github.com/IBM/mcp-context-forge/blob/main/README.md — 설치·기능·배포 설명의 확인 지점. `main`은 변경될 수 있다.

> 근거는 제공된 dossier다. 저장소의 현재 상태, 명령 실행, 성능 및 보안은 직접 검증하지 않았다. 버전·수치·지원 범위는 발췌 시점의 프로젝트 설명이다.
