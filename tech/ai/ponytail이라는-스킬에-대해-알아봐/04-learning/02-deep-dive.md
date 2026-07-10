---
date: 2026-06-24
tags:
  - tech
  - ai
  - agent-skills
  - deep-dive
  - ponytail
type: tech-tool-study
parent: "[[../README]]"
---

# ponytail skill - 심화

> [[01-getting-started|이전: 시작하기]] | [[../README|목차]] | [[../05-projects|다음: 프로젝트]]

---

## 1. Skill을 작게 유지하기

`SKILL.md`는 agent가 활성화 시 바로 읽는 파일이다. 모든 지식을 여기에 넣으면 progressive disclosure의 장점이 사라진다.

| 내용 | 위치 |
|------|------|
| activation 기준 | `SKILL.md` frontmatter `description` |
| 핵심 절차 | `SKILL.md` 본문 |
| 긴 정책 문서 | `references/` |
| 반복 계산/검증 | `scripts/` |
| template/sample | `assets/` 또는 `references/examples.md` |

권장 구조:

```text
ponytail/
├── SKILL.md
├── scripts/
│   └── validate_output.py
├── references/
│   ├── acceptance-criteria.md
│   └── examples.md
└── assets/
    └── report-template.md
```

## 2. references 설계

긴 문서는 topic별로 나눈다. `SKILL.md`에는 “언제 어떤 reference를 읽을지”만 적는다.

```markdown
## References

- Read `references/acceptance-criteria.md` when validating final output.
- Read `references/examples.md` only when the user asks for examples or the output format is unclear.
```

이 방식은 [[study/tech/ai/thin-harness-fat-skills]]의 관점과 잘 맞는다. harness는 얇게 유지하고, 업무 지식은 skill package에 두는 식이다.

## 3. scripts 설계

자연어 agent에게 맡기면 흔들리는 부분은 script로 뺀다.

```python
#!/usr/bin/env python3
import json
import sys

def validate(payload):
    required = ["summary", "steps", "validation"]
    missing = [key for key in required if key not in payload]
    return {"ok": not missing, "missing": missing}

if __name__ == "__main__":
    payload = json.load(sys.stdin)
    print(json.dumps(validate(payload), ensure_ascii=False, indent=2))
```

| script 후보 | 이유 |
|-------------|------|
| schema validation | 사람이 읽는 기준보다 재현성이 높음 |
| CSV/JSON 변환 | deterministic processing에 적합 |
| citation format check | 반복 규칙 검사에 적합 |
| report lint | 누락 section 확인에 적합 |

## 4. Activation 평가

Skill 품질은 “좋은 문장”보다 activation 정확도가 더 중요하다.

| 테스트 유형 | 예시 | 기대 |
|-------------|------|------|
| true positive | "Use the Ponytail workflow..." | 활성화 |
| false positive | "ponytail hairstyle trend 요약" | 비활성화 |
| ambiguous | "ponytail 해줘" | clarification |
| boundary | "PR review checklist를 ponytail 방식으로" | 목적에 따라 활성화 |

테스트 기록 예시:

```markdown
| Case | Prompt | Expected | Actual | Fix |
|------|--------|----------|--------|-----|
| TP-1 | Use the Ponytail workflow... | activate | activate | none |
| FP-1 | Summarize ponytail hairstyles | skip | activate | add negative case to description |
```

## 5. 보안 리뷰

third-party `ponytail` skill을 받았다면 먼저 코드를 읽는다.

| 체크 | 확인 방법 |
|------|-----------|
| shell 실행 | `scripts/`에서 `curl`, `rm`, `ssh`, `chmod`, `eval` 검색 |
| secret 접근 | env var, token, credential file 접근 검색 |
| network | 외부 URL 호출 여부 확인 |
| filesystem | workspace 밖 경로 접근 여부 확인 |
| prompt injection | reference가 external content를 instruction처럼 취급하는지 확인 |

```bash
rg -n "curl|wget|rm -rf|ssh|eval|TOKEN|SECRET|HOME|\\.ssh" ponytail/
```

## 6. 운영 패턴

| 단계 | 할 일 |
|------|-------|
| v0 | `SKILL.md`만 둔 최소 skill |
| v1 | 3-5개 실제 task로 activation 평가 |
| v2 | 반복 검증을 `scripts/`로 분리 |
| v3 | 긴 기준과 예제를 `references/`로 분리 |
| v4 | plugin 또는 shared repository로 배포 |

## 관련 노트

- [[study/tech/ai/model-context-protocol-mcp]] - external tool/data 연결이 필요할 때
- [[study/tech/ai/lazy-codex]] - 검증 루프와 false completion 대응
- [[study/tech/ai/claude/05-skills]] - Claude skill 구조

