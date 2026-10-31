---
date: 2026-06-20
tags:
  - tech
  - ai
  - claude
  - projects
  - prompt-governance
type: tech-tool-study
parent: "[[README]]"
---

# Claude System Prompts Release Notes - 실전 프로젝트

> [[04-learning/02-deep-dive|이전: 심화]] | [[README|목차로 돌아가기]] | [[cheatsheet|다음: 치트시트]]

---

## 프로젝트 1. System prompt changelog tracker

Claude System Prompts release notes를 주기적으로 snapshot하고 diff를 남기는 작은 tracker를 만든다.

| 항목 | 내용 |
|------|------|
| 목표 | prompt release note 변화와 최신 항목을 기록 |
| 입력 | official docs URL, checked_at |
| 출력 | Markdown changelog, YAML metadata |
| 핵심 포인트 | "latest"를 날짜와 함께 저장 |

```yaml
snapshot:
  url: https://platform.claude.com/docs/en/release-notes/system-prompts
  checked_at: 2026-06-20
  latest_entry:
    model: Claude Fable 5
    date: 2026-06-09
  scope: claude.ai web/mobile
  api_applies: false
```

확장:

- release note diff를 PR로 생성
- 변경 항목별 "formatting", "safety", "tool", "date/context" tag 부여
- [[study/tech/ai/ai-ecosystem/01-overview]] provider watchlist와 연결

## 프로젝트 2. API prompt governance template

내 application의 production prompt를 code-managed artifact로 관리하는 template를 만든다.

| 구성요소 | 설명 |
|----------|------|
| `prompt.md` | 사람이 review하는 source prompt |
| `metadata.yaml` | owner, version, target model, eval suite |
| `evals/` | golden input/output, refusal cases |
| `CHANGELOG.md` | prompt 변경 이유와 영향 |

```text
prompts/
└── study-note-writer/
    ├── prompt.md
    ├── metadata.yaml
    ├── CHANGELOG.md
    └── evals/
        ├── basic.yaml
        └── refusal.yaml
```

성공 기준:

- prompt 변경 PR에 eval 결과가 붙는다.
- model ID, prompt version, checked_at이 로그에 남는다.
- secret이나 proprietary detail이 prompt에 들어가지 않는다.

## 프로젝트 3. Web Claude vs API behavior lab

같은 user prompt를 `claude.ai`, API no-system, API custom-system에서 비교한다.

| Surface | 목적 |
|---------|------|
| `claude.ai` | app-level core system prompt의 영향 관찰 |
| API no-system | explicit system 없이 base behavior 관찰 |
| API custom-system | application prompt의 영향 관찰 |

기록 schema:

```yaml
case:
  id: claude-system-prompt-001
  user_prompt: "Write a concise Korean explanation of prompt governance."
  surfaces:
    - name: claude_ai
      observed_at: 2026-06-20
    - name: anthropic_api_no_system
      model_id: claude-sonnet-4-6
    - name: anthropic_api_custom_system
      model_id: claude-sonnet-4-6
      system_prompt_version: study-v1
  observations:
    - formatting
    - refusal_behavior
    - citation_style
```

주의:

- 차이를 전부 model quality로 해석하지 않는다.
- web surface의 hidden prompt와 product state를 별도 변수로 둔다.
- API에서는 temperature/sampling 설정을 기록한다.

## 프로젝트 4. Prompt leak audit

production system prompt를 leak-resilient하게 점검한다.

| 점검 | 질문 |
|------|------|
| Secret | prompt 안에 API key, internal URL, private policy가 있는가? |
| Proprietary detail | 공개되면 곤란한 ranking rule이나 business logic이 있는가? |
| Separation | user context/query와 system instruction이 분리되는가? |
| Post-processing | 민감 필드 redaction이 있는가? |
| Audit | prompt extraction 시도와 결과를 기록하는가? |

간단한 audit prompt:

```text
Review this system prompt as if it could be leaked.
List proprietary details, unnecessary internal implementation notes,
and instructions that should move into code or policy config.
```

## 프로젝트 5. Multi-provider instruction adapter

Claude, OpenAI, Gemini의 instruction primitive 차이를 adapter로 추상화한다.

| Provider | Field |
|----------|-------|
| Anthropic | `system` |
| OpenAI | `instructions` 또는 `developer` message |
| Gemini | `system_instruction` |

```python
def build_instruction(provider: str, instruction: str) -> dict:
    if provider == "anthropic":
        return {"system": instruction}
    if provider == "openai":
        return {"instructions": instruction}
    if provider == "gemini":
        return {"system_instruction": instruction}
    raise ValueError(f"unsupported provider: {provider}")
```

이 프로젝트는 [[study/tech/ai/litellm]] 같은 gateway와 함께 쓰기 좋다.

---

## 관련 노트

- [[study/tech/ai/litellm]] - multi-provider routing 위에 instruction adapter를 얹는 프로젝트
- [[study/tech/ai/model-context-protocol-mcp]] - prompt governance와 tool/resource governance를 같이 설계
- [[study/tech/ai/agent-orchestration/cli-agents]] - agent runtime prompt audit 대상으로 확장
