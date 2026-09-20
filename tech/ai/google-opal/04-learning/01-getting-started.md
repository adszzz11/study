---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# Google Opal Getting Started

> [[../README|목차로 돌아가기]] · [[02-deep-dive|다음: Deep Dive]]

## 목표

주제를 받아 조사·요약한 webpage를 만드는 최소 workflow를 완성하고, Console에서 각 step을 검증한다.

## 1. Gallery에서 구조를 먼저 읽기

1. [Opal Gallery](https://opal.google/)에서 demo Opal을 연다.
2. `Remix`로 복제한다.
3. Input, Generate, Output이 각각 어떤 값과 결과를 갖는지 기록한다.
4. 처음에는 prompt를 바꾸지 말고 Preview를 한 번 실행한다.

## 2. 첫 mini-app 만들기

```text
User Input: topic
  ↓
Generate: @Search로 조사하고, 주장마다 출처 URL을 붙여 5개 bullet로 요약
  ↓
Output: 제목 · 핵심 요약 · 출처 목록을 가진 webpage
```

Generate prompt 예시:

```text
주제: @topic
@Search를 사용해 최근 정보를 조사하라.
사실과 추론을 분리하고, 각 핵심 주장에 source URL을 붙여라.
확인할 수 없는 내용은 단정하지 말고 “검증 필요”로 표시하라.
```

## 3. Console로 검증하기

- [ ] `User Input` 값이 예상대로 전달되는가?
- [ ] Generate step을 개별 실행했을 때 search result와 요약이 대응하는가?
- [ ] Output이 source URL을 실제로 표시하는가?
- [ ] 빈 입력, 모호한 입력에서도 안전하게 재질문하거나 제한을 말하는가?
- [ ] 실행 시간과 오류가 특정 step에 집중되지 않는가?

## 4. asset context 실습

reference document를 업로드하고 `@` reference로 주입한다. “문서 형식을 지켜 결과를 생성하라”처럼 format constraint를 명시하고, 원문에 없는 사실을 만들지 않도록 지시한다. static file·YouTube link도 context asset으로 쓸 수 있지만, 민감한 파일은 공유 전에 제거한다.

## 5. Publish 전 최소 점검

- output의 hallucination과 attribution을 사람이 확인한다.
- prompt·asset에 API key, 개인 정보, 내부 전략이 없는지 확인한다.
- Drive 공유 권한과 Opal editor/remix 권한을 별도로 확인한다.

## Sources

- https://developers.google.com/opal/quickstart
- https://developers.google.com/opal/overview
- https://developers.google.com/opal/faq
