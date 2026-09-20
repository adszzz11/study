---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# taste — References

> [[02-ecosystem|이전: Ecosystem]] | [[README|목차로 돌아가기]] | [[04-learning/01-getting-started|다음: Getting started]]

## Sources

### 프로젝트 원문

| 자료 | 읽을 이유 |
|---|---|
| [README](https://github.com/Hmbown/taste#readme) | 문제 정의, v1.0 재설계 배경, 사용 예시 |
| [SKILL.md](https://raw.githubusercontent.com/Hmbown/taste/main/SKILL.md) | activation metadata와 핵심 Create/Critique workflow |
| [DOMAINS.md](https://raw.githubusercontent.com/Hmbown/taste/main/references/DOMAINS.md) | code, UI, document, data, system별 판단 기준 |
| [REVIEW.md](https://raw.githubusercontent.com/Hmbown/taste/main/references/REVIEW.md) | verdict 중심 critique와 비교 절차 |
| [openai.yaml](https://raw.githubusercontent.com/Hmbown/taste/main/agents/openai.yaml) | Codex UI metadata와 implicit invocation 설정 |
| [install.sh](https://raw.githubusercontent.com/Hmbown/taste/main/scripts/install.sh) | client별 실제 설치 동작과 filesystem 변경 |
| [Releases](https://github.com/Hmbown/taste/releases) | packaged artifact와 source version 차이 확인 |

### Agent Skills 배경

- [Agent Skills specification](https://agentskills.io/)
- [Agent Skills GitHub](https://github.com/agentskills/agentskills)
- [Anthropic Engineering — Equipping agents for the real world with Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)
- [OpenAI Academy — Skills](https://openai.com/academy/skills/)
- [OpenAI skill-creator](https://github.com/openai/skills/blob/main/skills/.system/skill-creator/SKILL.md)

## 설치 전 보안 검토

Third-party Skill은 instruction뿐 아니라 executable script를 포함할 수 있다. 다음을 먼저 확인한다.

- [ ] `SKILL.md`의 activation 범위와 지시가 과도하지 않은가?
- [ ] `references/`가 민감정보를 외부로 보내도록 지시하지 않는가?
- [ ] `scripts/`가 수정·삭제·network access를 수행하는가?
- [ ] symlink와 copy 대상 path가 예상한 client directory인가?
- [ ] 검토한 commit 또는 tag를 pin했는가?
- [ ] update와 rollback 방법을 기록했는가?

```bash
# 실행하지 않고 먼저 읽는다.
git show <commit>:SKILL.md
git show <commit>:scripts/install.sh
git diff <old-commit>..<new-commit> -- SKILL.md references scripts
```

## 조사 메모

- 조사 기준일: **2026-09-20**
- 분석 대상: **Hmbown/taste**, repository metadata `version: "1.0.0"`
- 제외 대상: Taste Labs, TasteCode, TASTE benchmark, frontend 전용 Taste Skill
- 유의점: 공개 Releases의 최신 표시와 repository 내부 version 사이에 distribution lag가 있을 수 있다.
