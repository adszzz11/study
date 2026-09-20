---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# taste — Ecosystem과 비교

> [[01-overview|이전: Overview]] | [[README|목차로 돌아가기]] | [[03-references|다음: References]]

## 포지션

`taste`는 생성 model, design system, linter가 아니라 **artifact judgment를 위한 procedural knowledge layer**다. Agent Skills 표준을 통해 compatible client에서 재사용되며, 실제 품질보증 도구와 함께 쓸 때 역할이 선명하다.

## 선택지 비교

| 선택지 | 범위·방식 | 강점 | 한계 | 적합한 경우 |
|---|---|---|---|---|
| **Hmbown/taste** | code·UI·document·data·system용 범용 judgment Skill | 작고 portable하며 실제 exemplar, invention 억제, finish 조절에 집중 | model·입력 품질 의존, benchmark 부족 | 다양한 artifact의 “generated tell”을 줄일 때 |
| Project `AGENTS.md` / rules | repository별 상시 instruction | 조직 규칙과 명령을 구체적으로 고정 | 범용 재사용이 어렵고 길어지면 context 비용 증가 | naming, test, release 같은 project convention |
| Design system / component library | token과 구현 component로 UI 제약 | 일관성과 재사용성이 높음 | 문서·code critique까지 포괄하지 않음 | production UI 구현 |
| Linter·formatter·type checker | deterministic static validation | 반복 가능하고 CI gate로 사용 가능 | 목적, hierarchy, 독자 판단은 평가하지 못함 | 문법·style·type 품질보증 |
| Evaluation rubric / LLM judge | 기준별 비교·score | 실험과 후보 비교에 유용 | rubric 설계와 judge bias에 의존 | 여러 안의 체계적 평가 |
| Domain-specific Skill | 특정 workflow와 조직 지식 | 깊고 구체적인 절차 제공 가능 | 다른 domain으로 이동하기 어려움 | 보안 review, frontend 등 좁은 업무 |
| Manual expert review | practitioner의 맥락적 판단 | 암묵지와 책임소재가 분명함 | 비용·시간·일관성 문제 | high-stakes 최종 승인 |

## 함께 쓰는 구조

```text
Project rules + real artifacts
             ↓
       taste workflow
             ↓
      draft / critique
             ↓
test · lint · a11y audit · human review
```

- `taste`는 project rule을 대체하지 않고 우선순위와 근거 사용법을 보완한다.
- deterministic tool은 정답을 검사하고, `taste`는 무엇을 만들고 무엇을 뺄지 판단한다.
- high-stakes 결과의 최종 책임은 human reviewer에게 남는다.

## Client와 배포

| 대상 | 배치 방식 | 주의점 |
|---|---|---|
| Codex | repository를 `~/.codex/skills/taste`에 symlink | `agents/openai.yaml`이 implicit invocation metadata 제공 |
| Claude Code | 일부 directory를 제외하고 `~/.claude/skills/taste`에 복사 | 복사본 update 방식 확인 필요 |
| Project-local | `.agents/skills/taste` 또는 `.claude/skills/taste` | repository별 pin과 review에 유리 |
| Copilot CLI / Gemini CLI | Agent Skills compatible client의 discovery 규칙 사용 | client별 지원 범위 확인 필요 |

공개 Releases에는 조사 시점에 `v0.1.0`만 보이지만 repository metadata는 `1.0.0`이다. production에서는 `main`을 무기한 추적하기보다 검토한 commit이나 tag를 pin한다.

## 선택 가이드

- **judgment 문제**면 `taste`를 고려한다.
- **repository 규칙 문제**면 `AGENTS.md`나 project-local instruction을 먼저 쓴다.
- **기계적으로 판별 가능한 문제**면 linter, compiler, test를 우선한다.
- **조직 UI 일관성 문제**면 design system을 먼저 연결한다.
- **되돌리기 어려운 결정**이면 expert review와 평가 실험을 추가한다.

## Sources

- [Hmbown/taste SKILL.md](https://raw.githubusercontent.com/Hmbown/taste/main/SKILL.md)
- [Codex adapter metadata](https://raw.githubusercontent.com/Hmbown/taste/main/agents/openai.yaml)
- [Installer](https://raw.githubusercontent.com/Hmbown/taste/main/scripts/install.sh)
- [GitHub Releases](https://github.com/Hmbown/taste/releases)
- [Agent Skills specification](https://agentskills.io/)

