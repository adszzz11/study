---
date: 2026-09-27
tags: [tech]
type: tech-tool-study
status: draft
---

# Claudian — Getting Started

> [[../README|목차로 돌아가기]] · [[../03-references|이전: References]] · [[02-deep-dive|다음: Deep Dive]]

## 목표

개인 vault가 아닌 disposable test vault에서 한 provider를 연결하고, context 지정 → 변경 제안 → diff 검토 → wikilink 제안까지의 짧은 loop를 안전하게 실행한다.

## 1. 설치 전 신뢰 경계 정하기

Community Plugin은 third-party code를 실행한다. 다음을 먼저 결정한다.

- 테스트용 vault에는 secret, 개인 일기, credential을 넣지 않는다.
- 외부 provider로 전송해도 되는 노트만 context로 사용한다.
- 첫 실습에서는 read-only 조사와 inline diff 제안만 허용한다.
- 외부 write MCP와 위험한 Bash command는 사용하지 않는다.

## 2. plugin과 CLI 준비

1. Obsidian **Desktop**에서 Community Plugins를 활성화하고 `Claudian`을 설치·활성화한다.
2. Claude Code 또는 Codex 등 **하나의** supported CLI만 먼저 설치하고 로그인한다.
3. Claudian Settings에서 provider와 executable path를 확인한다.
4. provider가 발견되지 않으면 GUI app의 `PATH`와 CLI 절대 경로를 확인한다.

> [!tip]
> 처음부터 여러 provider를 연결하지 않는다. UI 문제인지 CLI 인증 문제인지 구분하려면 하나의 provider와 하나의 test vault가 가장 빠르다.

## 3. 첫 agent loop

`note.md`와 관련 노트 2~3개를 만든 뒤 sidebar에서 `@note.md`로 context를 지정한다.

```text
@note.md 이 노트를 세 문단으로 재구성해 줘.
사실을 추가하지 말고, 먼저 변경 계획을 짧게 말한 뒤
inline diff로만 제안해 줘.
```

다음 순서로 검토한다.

1. agent가 언급한 파일 범위가 의도한 노트인지 확인한다.
2. inline diff에서 의미 변경, 삭제, frontmatter 손상을 확인한다.
3. 적용 후 Obsidian link와 Markdown rendering을 확인한다.
4. 필요하면 version control 또는 backup에서 되돌릴 수 있는지 확인한다.

두 번째 연습 prompt:

```text
이 노트와 같은 주제의 노트를 vault에서 찾아라.
파일을 수정하지 말고, 추가할 wikilink 후보와 근거를 목록으로 제안해 줘.
```

## 4. 반복 작업으로 확장하기

| 다음 단계 | 안전한 시작 |
|---|---|
| `/` prompt template | “회의록을 결정·action item·질문으로 분해”처럼 출력 형식을 고정 |
| `$` Skill | frontmatter 정규화나 broken link 검사처럼 반복되는 read-first workflow 정의 |
| MCP | 검색·조회 중심의 read-only server부터 추가 |
| vault instruction | 금지 경로, 파일 삭제 금지, 적용 전 diff 제시를 명시 |

## 완료 점검

- [ ] plugin이 Obsidian Desktop에서 활성화됐다.
- [ ] 하나의 provider CLI가 Settings에서 발견되고 인증됐다.
- [ ] `@mention`으로 파일 context를 지정했다.
- [ ] 첫 변경을 inline diff로 검토했다.
- [ ] 수정 없는 link 후보 제안을 받아 사람이 선택했다.
- [ ] Bash와 외부 write MCP의 approval을 유지했다.

## Sources

- [Claudian README — Troubleshooting](https://github.com/YishenTu/claudian#troubleshooting)
- [Claudian README — Features & usage](https://github.com/YishenTu/claudian#features--usage)
- [Obsidian — Community plugins](https://help.obsidian.md/community-plugins)
