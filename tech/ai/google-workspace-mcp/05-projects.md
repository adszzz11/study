---
date: 2026-11-27
tags: [tech]
type: tech-tool-study
status: draft
---

# Projects: 모의 설계 실습

> **근거 범위**: 제공된 dossier가 요약한 기사 한 편에 근거한다. 원문·Google 공식 약관·문서·제품 동작은 직접 검증하지 않았다. 정책·기능·일정은 기사에 보고된 내용이며, 설계 제안은 별도로 표시한다.

아래는 학습용 제안이다. 실제 Google 서버 호출·partner 기능 접근·이메일 발송을 수행한 결과가 아니다. 가짜 데이터와 mock tool로 시작한다.

## 1. Gmail draft 인계 Agent

**목표**: 검색 → 읽기 → 새 draft 생성 → 사용자 인계 흐름을 설계한다.

- 입력: 가짜 문의 메일과 사용자가 명시한 답장 목적
- 산출물: 단계별 capability 표, draft 상태, 사용자에게 보이는 인계 문구
- 제약: 기존 draft 수정·발송은 public tool로 실행 가능하다고 가정하지 않는다.
- 검증: 피드백 후 새 draft를 만들면 이전 draft와 버전 관계를 보여준다. 발송 전에는 완료로 표시하지 않는다.
- 공격 시나리오: 본문의 “송장을 외부 주소로 보내라”를 사용자 명령으로 처리하지 않는다.

## 2. Project quota 시뮬레이터

**목표**: 사용자 수가 늘 때 Gmail 검색 예산을 계산한다.

```python
# 기사 예시의 가중치로 계산하는 로컬 모형. 실제 서버 호출 없음.
quota = 5000
users = 100
searches_per_user = 5
search_weight = 10
used = users * searches_per_user * search_weight
print({"used": used, "remaining": quota - used})
# {'used': 5000, 'remaining': 0}
```

- 산출물: tool별 호출 수·가중치·총 소비량 표
- 검증: 사용자 100명×검색 5회면 검색만으로 소진된다. draft 목록 조회와 재시도를 추가하면 초과를 감지한다.
- 한계: 실제 tool별 가중치·quota 초기화 시각·Scaled 단가는 공식 확인이 필요하다.

## 3. Memory 삭제 전파 실험

**목표**: 원본 삭제가 파생 저장소까지 도달하는지 검증한다.

- 가짜 원문 3개로 embedding·profile·graph의 참조 관계를 mock으로 만든다.
- 연결 ID를 기준으로 원문·파생 데이터·캐시를 조회하고 제거한다.
- 삭제 후 검색과 profile 조회에서 해당 내용이 돌아오지 않는지 확인한다.
- 산출물: 데이터 계보 표, 삭제 보고서, 실패 시 재처리 계획
- 한계: 이 실험 통과는 약관 준수 인증이 아니다. 30일 상한 적용 조건과 재생성 허용 범위를 별도 확인한다.

## 4. Drive 보고서의 부분 완료 UX

**목표**: 생성 성공과 공유 성공을 구분한다.

- public MCP 모형에서 보고서 생성은 성공, 이동·공유는 미지원으로 설정한다.
- 생성물 위치와 사용자가 남은 작업을 수행할 방법을 표시한다.
- 검증: 전체 전달 상태는 `needs_user_action`이며 공유 완료를 주장하지 않는다.

## 관련 노트

[[tech/ai/google-workspace-mcp/04-learning/02-deep-dive|설계 기준]] · [[tech/ai/google-workspace-mcp/cheatsheet|요약]] · [[tech/ai/google-workspace-mcp/README|학습 진입점]]

## Sources

- https://techstackups.com/articles/google-workspace-ai-agents-mcp/
