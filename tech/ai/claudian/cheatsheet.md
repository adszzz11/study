---
date: 2026-09-27
tags: [tech]
type: tech-tool-study
status: draft
---

# Claudian — Cheatsheet

> [[README|목차로 돌아가기]] · [[05-projects|이전: Projects]]

## Mental model

```text
Claudian = Obsidian UI + provider adapter
native CLI = model · tools · MCP · Skills · approval · history
vault = agent workspace (not merely chat context)
```

## UI 빠른 참조

| 표현 | 용도 | 기본 안전 원칙 |
|---|---|---|
| `@file.md` / `@folder` | 파일·폴더 context 지정 | 필요한 최소 범위만 명시 |
| `/` command | prompt template 실행 | 입력·출력 형식을 고정 |
| `$` Skill | 재사용 workflow | destructive step을 숨기지 않기 |
| `/side`, `/btw` | 임시 side conversation | 본 task의 결정은 main thread에 남기기 |
| inline diff | 변경 제안 검토·적용 | 적용 전 의미·삭제·frontmatter 확인 |

## 권장 prompt 패턴

### Read-first 조사

```text
@folder/ 이 폴더를 읽고 중복된 주제와 누락된 wikilink 후보를 찾아라.
파일은 수정하지 말고, 후보마다 근거가 된 노트 링크를 제시해 줘.
```

### 제한된 수정 제안

```text
@note.md 이 노트의 frontmatter를 아래 schema에 맞춰 제안해 줘.
다른 파일은 건드리지 말고, 사실을 추정하거나 추가하지 마.
변경은 inline diff로만 보여 줘.
```

### 검증 중심 문서 정비

```text
@docs/ @repo/ 문서와 구현의 불일치 후보를 찾아라.
각 후보에 source file, 근거, 확신도, 권장 수정안을 적고
확인하지 못한 내용은 TODO로 남겨라.
```

## 설치·문제 해결

| 증상 | 먼저 확인할 것 |
|---|---|
| provider가 목록에 없거나 실행 실패 | CLI 설치·로그인, executable path, Obsidian GUI의 `PATH` |
| 예상보다 넓은 파일을 언급 | `@mention` scope, vault instruction, search tool 권한 |
| tool이 승인 없이 동작할까 걱정 | native CLI approval policy와 MCP server 권한 |
| OpenCode 연결 문제 | v2 사용 여부와 v1 migration 안내 |
| 수정 결과가 이상함 | inline diff, Markdown rendering, link checker, `git diff`/backup |

## Run 전 30초 점검

- [ ] 이 prompt와 attachment가 provider로 전송돼도 되는가?
- [ ] target vault가 개인/비밀 vault와 분리됐는가?
- [ ] task scope와 금지 경로를 명시했는가?
- [ ] read-only로 먼저 확인할 수 있는가?
- [ ] 외부 write, Bash, delete에 native approval이 남아 있는가?
- [ ] 적용 전 diff, 적용 후 link/rendering을 검토할 것인가?

## Sources

- [Claudian README — Features, usage, troubleshooting](https://github.com/YishenTu/claudian)
- [Claudian README — Privacy & data use](https://github.com/YishenTu/claudian#privacy--data-use)
- [OpenCode v2 migration guide](https://opencode.ai/v2/docs/migrate-v1)
