---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# Refero MCP — Deep Dive

> [[01-getting-started|이전: Getting Started]] · [[../README|목차]] · [[../05-projects|다음: Projects]]

## Research Is Not Copying

좋은 output은 “어느 회사 UI를 쓸까”가 아니라 “목표에 맞는 trait 조합은 무엇인가”를 답한다. 최소 두 개 이상의 reference를 비교하고 trait가 user goal에 어떻게 기여하는지 적는다.

| 관찰 | 나쁜 결론 | 더 나은 synthesis |
|---|---|---|
| 빈 화면에 illustration이 있다 | illustration을 복제한다 | 불안을 줄이는 설명과 다음 CTA가 필요하다 |
| invite에 modal을 쓴다 | 같은 modal을 만든다 | current context를 유지하면서 permission을 설명해야 한다 |
| table가 compact하다 | 행 높이를 베낀다 | power user가 빠르게 scan할 density가 필요하다 |

## From Traits to Semantic Tokens

raw 값 대신 role을 만든 뒤 자사 brand token으로 검증한다.

```yaml
semantic_roles:
  surface/subtle: empty state 또는 secondary panel 배경
  text/primary: heading과 중요 값
  text/secondary: helper copy와 metadata
  action/primary: primary CTA
  border/default: section과 interactive control 경계
```

reference의 hex color나 font size를 그대로 token으로 승격하지 않는다. contrast, existing system, locale, platform을 함께 검토한다.

## Flow Coverage Matrix

screen이 아니라 journey를 평가하려면 happy path 밖을 기록한다.

| 단계 | 사용자 의도 | 필요한 상태 | 검증 질문 |
|---|---|---|---|
| entry | teammate 초대 | empty / existing member | 왜 초대해야 하는가? |
| input | email과 role 선택 | validation / permission limit | 오류를 즉시 고칠 수 있는가? |
| submit | invitation 전송 | loading / success / failure | 중복 전송을 막는가? |
| pending | 수락 대기 | resend / cancel / expiry | 다음 행동이 분명한가? |
| completion | member 합류 | confirmation / handoff | workspace의 다음 가치로 연결되는가? |

## Visual QA Loop

```text
reference lock
  → implementation screenshot (desktop + mobile)
  → compare: hierarchy / density / spacing / color role / imagery
  → inspect: keyboard, focus, contrast, error states
  → revise one hypothesis at a time
```

QA는 pixel-perfect copy가 아니라 intended hierarchy와 interaction clarity의 검증이다. screenshot comparison은 accessibility test를 대체하지 않으므로 keyboard path, focus visibility, semantic labels, contrast를 별도로 확인한다.

## Operational Boundaries

- MCP는 read-only research access다. code change 권한으로 오해하지 않는다.
- 결과에 포함된 content를 brand, license, privacy 정책과 별개로 검토한다.
- public Skill의 tool name은 drift할 수 있다. client discovery와 현재 vendor docs를 기준으로 automation을 갱신한다.
- corpus count는 vendor snapshot이지 design quality metric이 아니다.

## Sources

- https://github.com/referodesign/refero_skill/blob/master/skills/refero-design/SKILL.md
- https://github.com/referodesign/refero_skill/blob/master/skills/refero-design/references/visual-workflow.md
- https://github.com/referodesign/refero_skill/issues/1
