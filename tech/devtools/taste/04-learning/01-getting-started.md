---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# taste — Getting Started

> [[../03-references|이전: References]] | [[../README|목차로 돌아가기]] | [[02-deep-dive|다음: Deep dive]]

## 1. 설치 전에 source 검토

공식 installer를 바로 실행하지 말고 repository와 변경 대상을 먼저 확인한다.

```bash
git clone https://github.com/Hmbown/taste.git
cd taste
git log -1 --oneline
sed -n '1,240p' SKILL.md
sed -n '1,260p' scripts/install.sh
find references agents scripts -maxdepth 2 -type f -print
```

검토한 commit hash를 기록한다. 공개 release와 repository version이 다를 수 있으므로 production 사용은 commit 또는 tag pin을 권장한다.

## 2. 배치 방식 선택

| 범위 | 예시 path | 선택 기준 |
|---|---|---|
| Codex user-level | `~/.codex/skills/taste` | 여러 project에서 같은 검토본 사용 |
| Claude user-level | `~/.claude/skills/taste` | Claude Code 전체에서 사용 |
| Project-local | `.agents/skills/taste` | 팀 review와 version pin이 중요할 때 |
| Project-local Claude | `.claude/skills/taste` | Claude 전용 project 설정 |

공식 installer는 Codex에는 symlink, Claude Code에는 일부 directory를 제외한 copy를 사용한다. 실제 설치는 script를 검토하고 client 문서에서 discovery path를 확인한 뒤 수행한다.

## 3. 첫 작업에 적용

### Step 1 — The job

```text
Artifact: API deprecation memo
Audience: 이 API를 호출하는 application team
Action: 금요일까지 migration owner와 일정 확정
```

### Step 2 — Reader knowledge

```text
Known: 기존 API 이름과 현재 장애 증상
Needs verification: 영향 repository, 종료일, 대체 API readiness
```

### Step 3 — The exemplar

- 최근 승인된 migration memo
- 실제 call-site와 test
- 현재 API 문서와 incident record

### Step 4 — Create 요청

```text
Use the taste skill. Create one short deprecation memo grounded in the
attached call-sites and the latest approved migration memo. Do not invent
dates or owners; mark missing facts as [confirm: ...].
```

## 4. 결과 검토

- [ ] 첫 문장에 결론과 필요한 행동이 있는가?
- [ ] source에 없는 숫자, 일정, 기능, 정책을 만들지 않았는가?
- [ ] 중요한 결정에 가장 많은 공간을 썼는가?
- [ ] 관습적인 배경 설명과 반복 결론을 잘랐는가?
- [ ] 다음 한 시간의 polish가 독자 행동을 바꾸는가?
- [ ] compiler, test, linter 등 필요한 별도 검증을 실행했는가?

## 5. Rollback

- project-local 설치는 추가한 skill directory를 제거하고 repository 변경을 되돌린다.
- user-level symlink는 symlink target을 확인한 뒤 link만 제거한다.
- Claude copy 방식은 복사본과 원본을 구분해 대상 directory만 제거한다.
- 삭제 전에는 `ls -ld`와 `git status`로 정확한 path와 tracked 여부를 확인한다.

## Sources

- [Hmbown/taste README](https://github.com/Hmbown/taste#readme)
- [Installer](https://raw.githubusercontent.com/Hmbown/taste/main/scripts/install.sh)
- [SKILL.md](https://raw.githubusercontent.com/Hmbown/taste/main/SKILL.md)

