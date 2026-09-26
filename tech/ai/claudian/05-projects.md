---
date: 2026-09-27
tags: [tech]
type: tech-tool-study
status: draft
---

# Claudian — Projects

> [[README|목차로 돌아가기]] · [[04-learning/02-deep-dive|이전: Deep Dive]] · [[cheatsheet|다음: Cheatsheet]]

## 1. Research vault curator

논문·조사 노트의 frontmatter를 통일하고, 중복 claim과 관련 wikilink 후보를 찾은 뒤 인용 확인 TODO를 남긴다.

**Workflow**

1. sample 폴더 10개 이하를 `@mention`하고 schema를 명시한다.
2. agent에게 읽기 전용 inventory와 수정 계획을 요청한다.
3. frontmatter diff를 묶음이 아닌 작은 batch로 검토한다.
4. claim마다 source URL, 확인 필요, 추론을 구분하게 한다.

**완료 기준**: 원본 인용을 새로 만들지 않았고, 변경 파일 목록·diff·broken link 검사 결과가 남아 있다.

## 2. Meeting-to-knowledge pipeline

회의록을 action item, 결정, 미해결 질문으로 분해하고 프로젝트 note에 반영할 변경안을 제안한다.

```text
meeting note → extract (decision / action / question)
             → match project notes
             → propose per-file diff
             → reviewer accepts selected changes
```

**Guardrail**: 참석자, 고객명, 약속처럼 민감하거나 사실 확인이 필요한 항목은 “추정”으로 채우지 않는다. 프로젝트 note에 직접 적용하기 전에 source meeting note 링크를 보존한다.

## 3. Documentation maintenance

개발 repository와 docs vault를 함께 context로 두고 README/API 문서가 코드와 불일치하는 지점을 찾는다.

- repository는 read-only search로 시작한다.
- “불일치 후보 → 근거 file/line → 제안 diff” 순서로 출력하게 한다.
- API 계약, 버전, breaking change는 test 또는 source code evidence로 확인한다.
- 문서 변경은 code review와 별개로 reviewer가 승인한다.

**완료 기준**: 수정안의 각 claim이 code/source evidence에 연결되고, agent의 요약만으로 사실을 확정하지 않는다.

## 4. Personal CRM / project review

사람·프로젝트 노트에서 최근 활동, 막힌 일, 다음 행동을 집계해 weekly review 초안을 만든다.

**안전한 prompt 예시**

```text
@projects/ @people/ 최근 7일의 기록에서
1) 완료, 2) 막힌 일, 3) 다음 행동 후보를 표로 요약해 줘.
노트는 수정하지 말고, 날짜와 원본 노트 링크를 각 행에 붙여 줘.
```

민감한 vault에서는 provider 전송 범위와 attachment를 특히 제한한다. CRM의 요약은 기억의 대체물이 아니므로 원본 link를 포함해 사람이 맥락을 검토하게 한다.

## 5. Small-team knowledge project

Claudian Collab를 전용 Project 폴더에 사용해 Git-backed 변경 제안을 운영한다. `Publish → Change Request → Manager Accept` 흐름과 accepted `main` 보호를 이해한 뒤, 실제 팀 저장소가 아닌 pilot repository에서 시험한다.

**완료 기준**: 변경 제안의 작성자·검토자·accept 책임이 분명하고, conflict·rollback·LAN Host 장애 시의 작업 절차가 문서화돼 있다.

## 공통 회고 질문

- agent가 어떤 파일을 읽고 수정했는가?
- human review가 실제로 잡아낸 오류는 무엇인가?
- prompt/Skill/MCP 중 어느 부분이 가장 큰 권한을 가졌는가?
- 다음 run에서 read-only 또는 좁은 scope로 줄일 수 있는 권한은 무엇인가?

## Sources

- [Claudian README](https://github.com/YishenTu/claudian)
- [Claudian Collab — How it works](https://claudian.md/docs/collab-mode/how-it-works/)
- [Obsidian Community Plugins](https://help.obsidian.md/community-plugins)
