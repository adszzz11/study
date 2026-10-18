---
date: 2026-10-18
tags: [tech]
type: tech-tool-study
status: draft
---

# Humanizer — 시작하기

> [[../README|목차로 돌아가기]] | [[02-deep-dive|다음: 심화]]

## Goal

detector 판정이 아니라 **명확성, 독자 적합성, 사실 보존, 고유 voice**를 측정하는 작은 rewrite workflow를 만든다. 첫 실습은 production 문서가 아닌 사용 권한이 있는 초안으로 한다.

## Prepare an Evaluation Set

1. 원문 20개와 사람이 승인한 최종본 20개를 모은다.
2. 각 쌍에서 tone, 문장 길이, 직접성, 선호·금지 어휘, locale을 찾아 brand style spec으로 기록한다.
3. 각 원문에 고유명사, 수치, 인용, URL, 법률·의학·제품 용어를 `preserve list`로 붙인다.
4. 결과를 승인할 editor와 사실을 확인할 domain reviewer를 정한다.

## Minimal Rewrite Contract

```text
Task: Rewrite for <audience> in <channel>.
Voice: <style-spec>.
Preserve exactly: <names, numbers, quotations, URLs, terminology>.
Do not add claims or sources. If a sentence cannot be safely rewritten,
return it unchanged and flag the reason.
Return: rewritten text, change rationale, and uncertainty flags.
```

`preserve list`는 prompt에만 넣지 말고, 출력 검사에도 같은 값을 사용한다. LLM이 따르지 못할 수 있다는 전제로 설계해야 한다.

## Review Loop

| 단계 | 자동 검사 | 사람의 판단 |
|---|---|---|
| 입력 | PII·비밀값 redaction, URL/인용 추출 | 외부 전송 가능 여부 |
| rewrite | style 조건과 preserve list 전달 | 불확실성 flag 확인 |
| quality gate | diff, glossary, URL, 수치, semantic similarity | 사실·의도·tone 검토 |
| 승인 | version history 저장 | publish, 수정 요청, 거절 |

## Checklist

- [ ] 원문과 승인본이 짝지어진 20개 이상의 evaluation set을 만들었다.
- [ ] style guide와 preserve list를 분리해 기록했다.
- [ ] 모든 결과에 원문 대비 diff와 변경 이유를 남겼다.
- [ ] factuality와 citation preservation을 사람이 승인했다.
- [ ] PII, retention, authorship 공개 규칙을 조직 정책과 맞췄다.

## Sources

- https://support.grammarly.com/hc/en-us/articles/38552339652109-Humanizer-user-guide
- https://guides.turnitin.com/hc/en-us/articles/22774058814093-Using-the-AI-Writing-Report
- https://quillbot.com/ai-humanizer
