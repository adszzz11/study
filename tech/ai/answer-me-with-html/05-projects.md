---
date: 2026-10-05
tags: [tech]
type: tech-tool-study
status: draft
---

# Answer me with HTML — Projects

> [[README|목차로 돌아가기]] | [[cheatsheet|다음: 치트시트]]

## 1. Architecture Onboarding Page

**목표:** 새 팀원이 repository/module map, request lifecycle, dependency tree를 한 페이지에서 탐색하게 한다.

- `sheet` template에 system context, module ownership, request `flow`, dependency `tree`, local-run checklist를 배치한다.
- diagram은 구조를, prose는 책임·예외·운영 규칙을 설명하게 분리한다.
- 완료 기준: 신규 독자가 10분 안에 entry point와 첫 디버깅 경로를 말할 수 있다.

## 2. ADR / Technology Comparison

**목표:** Redis vs Memcached, queue, cloud service 선택의 trade-off를 검토 가능한 artifact로 남긴다.

- conclusion을 첫 panel에 두고, workload assumptions와 비용·운영 제약을 표로 분리한다.
- unknown과 결정 보류 조건을 `callout`으로 명시한다.
- 완료 기준: reviewer가 recommendation과 반대 선택이 더 나은 조건을 모두 찾을 수 있다.

## 3. Incident or Postmortem Brief

**목표:** impact, timeline, root cause hypothesis, remediation을 읽는 순서대로 정리한다.

- `timeline`으로 사건을, `limits`로 영향 범위를, `flow`로 remediation ownership을 표시한다.
- 개인 식별 정보, credential, 고객 민감 데이터는 draft에 넣지 않는다.
- 완료 기준: incident commander가 next action과 owner를 빠르게 확인할 수 있다.

## 4. Security Review

**목표:** trust boundary, data flow, threat/mitigation matrix를 review-ready로 만든다.

- data flow와 trust boundary는 diagram으로, risk acceptance와 control evidence는 표로 쓴다.
- threat model이 아닌 renderer가 security correctness를 보장한다고 오해하지 않는다.
- 완료 기준: 각 mitigation에 owner, 검증 방법, residual risk가 연결된다.

## 5. Developer Education Explainer

**목표:** TCP/TLS/OAuth/Kubernetes lifecycle을 개념-순서-예외 순으로 교육한다.

- `sequence`와 state `flow`를 중심으로 짧은 panel을 구성한다.
- narration을 추가한 video는 보조 산출물로 두고, text-only HTML만으로도 핵심 내용을 읽을 수 있게 한다.
- 완료 기준: 학습자가 오류 사례를 순서도에서 추적하고 다음 확인 지점을 설명한다.

## Delivery Checklist

- [ ] source의 주장·수치·인용을 공식/1차 출처와 대조했다.
- [ ] target 독자가 page를 열 수 있는 offline 환경에서 HTML을 확인했다.
- [ ] diagram이 text 대안 없이 유일한 정보 전달 수단이 되지 않게 했다.
- [ ] lint 경고를 검토했고, 고유명사·용어의 false positive를 구분했다.
- [ ] source Markdown과 생성 artifact의 보관·수정 정책을 정했다.

## Sources

- https://github.com/QingYunA/answer-me-with-html
- https://raw.githubusercontent.com/QingYunA/answer-me-with-html/main/skills/answer-me-with-html/SKILL.md
