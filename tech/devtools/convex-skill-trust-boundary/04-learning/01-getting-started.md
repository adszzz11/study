---
date: 2026-11-28
tags: [tech]
type: tech-tool-study
status: draft
---

# 시작하기: 네트워크 없는 Data-flow tracing

## 목표와 준비

제공 dossier의 발췌 흐름을 종이에 표시하거나 로컬 dummy JSON으로 확인한다. 실제 Convex endpoint, 비밀정보, 다운로드 script는 필요 없다. 아래 코드는 Python 표준 라이브러리만 사용하고 네트워크 요청을 하지 않는다.

## 1. 입력과 응답 분리

```python
import json

idea = "공개 예제: 독서 목록 앱"
request_body = json.dumps({"idea": idea, "template": "nextjs-shadcn"},
                          ensure_ascii=False)
response_body = '{"id": "demo-local-run"}'  # 가짜 응답
slug = json.loads(response_body)["id"]
print(request_body)
print(slug)
```

예상 결과는 `idea`, `template`을 담은 JSON과 `demo-local-run`이다. 이는 원본 shell 명령의 재현이 아니라 payload와 response id의 구분을 위한 모델이다.

## 2. 정보 분류

| 항목 | 방향 | 판정 |
|---|---|---|
| `idea`, `template` | 로컬 → 외부 요청 | 발췌에 포함 |
| 응답 `id` | 외부 → 로컬 | 다음 call에서 재사용 |
| `/tmp/convex-qb-slug` | 로컬 call 간 전달 | id 저장 경로 |
| 아이디어 원문 보관 | 서버 내부 | 미확인 |

## 3. 주석과 실제 효과 대조

- `[telemetry 1/3]`라는 명칭보다 JSON의 필드를 먼저 읽는다.
- `"a run started"`라는 주석이 원문 저장 여부를 설명하는지 따져 본다.
- 요청 제한 시간과 실패 무시는 각각 가용성과 오류 처리에 관한 설정으로 분류한다.
- 나머지 telemetry 단계는 자료에 없다고 표시한다.

## 완료 기준

- [ ] 전송된 데이터와 응답 데이터를 구분했다.
- [ ] 전송과 저장을 다른 주장으로 적었다.
- [ ] 실제 endpoint 요청 없이 흐름을 설명할 수 있다.

[[tech/devtools/convex-skill-trust-boundary/04-learning/02-deep-dive|다음: Deep Dive]] · [[tech/devtools/convex-skill-trust-boundary/README|학습 경로]]

## Sources

- https://github.com/convex/convex-backend-skill/issues/64 — 실습의 근거; Python 예제는 학습용 재구성
