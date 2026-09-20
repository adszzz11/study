---
date: 2026-09-09
tags: [tech]
type: tech-tool-study
status: draft
---

# Getting started — 작은 Baseline과 Static Profile

[학습 진입점](../README.md) · 다음: [Deep dive](02-deep-dive.md)

## 학습 목표

동일한 task·tool·verifier를 유지하고, **tool 결과 해석만 바꾼 profile**을 비교한다. NVIDIA는 파일 첫 페이지를 전체로 오인하는 문제에 middleware를 추가해 읽기 테스트 **0/3 → 3/3**, 전체 평가 평균 **94/127 → 96/127**을 보고했다. 아래 예제는 그 문제에서 착안한 교육용 simulation이며 논문의 재현이나 실제 모델 성능 측정은 아니다. [NVIDIA 사례](https://developer.nvidia.com/blog/?p=119638)

## 1. Task Contract 고정

| 항목 | 실습 조건 |
|---|---|
| 목표 | 두 페이지로 나뉜 자료에서 모든 key-value를 수집 |
| Tool | `read_page(cursor)` 하나 |
| 공통 예산 | tool 호출 최대 3회 |
| 완료 기준 | 정답 dictionary와 정확히 일치 |
| 비교 변수 | continuation 안내를 해석하는 static profile |
| 기록 | 완료 여부·tool 호출 수 |

실제 서비스에서는 입력 자료, tool schema, 시간·비용 상한과 verifier 버전도 고정한다. 모델의 “완료했다”는 문장과 acceptance criteria 통과는 구분한다.

## 2. API 없이 실행해 구조 확인

Python 3 표준 라이브러리만 사용한다. 아래 코드 전체를 `python3`로 실행할 수 있다. `simulated_model`은 의도적으로 단순화한 결정적 정책이며 실제 LLM을 호출하지 않는다. adapted profile의 안내 문구를 읽으면 다음 페이지를 요청하도록 만들어 **차이가 생기는 위치**를 관찰하는 예제다.

```python
from dataclasses import dataclass


PAGES = ({"alpha": 1}, {"omega": 9})
EXPECTED = {"alpha": 1, "omega": 9}
MAX_TOOL_CALLS = 3


def read_page(cursor):
    return {
        "data": dict(PAGES[cursor]),
        "next_cursor": cursor + 1 if cursor + 1 < len(PAGES) else None,
    }


@dataclass(frozen=True)
class Profile:
    name: str
    explain_continuation: bool


def present_result(raw, profile):
    # Keep the original tool result; add guidance in the presentation layer.
    view = dict(raw)
    if profile.explain_continuation and raw["next_cursor"] is not None:
        view["guidance"] = "More pages remain; request next_cursor."
    return view


def simulated_model(view):
    # Deliberately models a reader that stops without explicit guidance.
    if view.get("guidance"):
        return view["next_cursor"]
    return None


def run(profile):
    cursor, calls, answer = 0, 0, {}
    while cursor is not None and calls < MAX_TOOL_CALLS:
        raw = read_page(cursor)
        calls += 1
        answer.update(raw["data"])
        cursor = simulated_model(present_result(raw, profile))
    return {
        "profile": profile.name,
        "passed": answer == EXPECTED,
        "tool_calls": calls,
    }


for profile in (Profile("baseline", False), Profile("adapted", True)):
    print(run(profile))
```

예상 출력:

```text
{'profile': 'baseline', 'passed': False, 'tool_calls': 1}
{'profile': 'adapted', 'passed': True, 'tool_calls': 2}
```

두 조건의 원본 tool·예산·verifier는 같고 presentation만 달라진다. 호출 수 증가가 성공률에 기여하므로 실제 평가에서는 비용과 지연도 함께 봐야 한다. 결정적 페이지 순회만 필요한 제품이라면 LLM 없이 일반 코드로 처리하는 편이 간단하다.

## 3. 실제 모델 실험으로 확장

1. 사용할 provider·API·model/version과 SDK·harness 버전을 기록한다.
2. 원본 response blocks/items를 보존하는 adapter를 준비한다.
3. 실제 모델에는 정답 `EXPECTED`를 제공하지 않고 tool 결과로 답하게 한다.
4. 같은 모델에서 baseline과 안내를 추가한 profile을 비교한다.
5. 정답이 첫 페이지·중간·끝에 있는 여러 과제와 짧은 파일을 포함한다.
6. 설정을 고치는 개발 과제와 최종 확인용 holdout 과제를 분리한다.
7. 동일 조건으로 반복 실행해 성공률, tool 호출 수, 실제 비용, 지연을 함께 기록한다.

Deep Agents를 쓴다면 행동 조정은 `HarnessProfile`, 모델 생성 설정은 `ProviderProfile` 책임으로 나눈다. Profiles는 Beta이므로 위 simulation을 그대로 SDK API 예제로 해석하지 않는다. [공식 설정 문서](https://docs.langchain.com/oss/python/deepagents/profiles)

## 완료 체크

- [ ] 공통 core와 profile이 각각 무엇을 바꿨는지 설명할 수 있다.
- [ ] baseline 실패를 verifier로 확인했다.
- [ ] simulation의 성공을 실제 LLM 성능 향상으로 오해하지 않는다.
- [ ] profile 개선을 평가할 별도 과제와 비용·지연 기록 항목을 정했다.

## Sources

- [NVIDIA Harness Profile 사례](https://developer.nvidia.com/blog/?p=119638)
- [Deep Agents Profiles](https://docs.langchain.com/oss/python/deepagents/profiles)
- [LangChain: Harness engineering](https://www.langchain.com/blog/improving-deep-agents-with-harness-engineering)
