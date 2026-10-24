---
date: 2026-10-24
tags: [tech]
type: tech-tool-study
status: draft
---

# Mercurial Cheatsheet

## 매일 쓰는 명령

| 목적 | 명령 |
| --- | --- |
| 상태 확인 | `hg status` |
| 변경 확인 | `hg diff` |
| commit | `hg commit -m "message"` |
| DAG log | `hg log -G` |
| remote 복제 | `hg clone <url>` |
| 동기화 | `hg pull`, `hg push` |

## Bookmark와 named branch

```sh
hg book feature/login       # bookmark 생성 또는 현재 위치에 지정
hg bookmarks                # bookmark 목록
hg update feature/login     # bookmark/changeset으로 이동
hg branch stable            # 다음 commit부터 named branch 지정
hg commit -m "Start stable line"
```

`bookmark`는 feature work, `hg branch NAME`은 release처럼 영속할 계통에 쓴다. named branch 이름은 commit history에 들어간다.

## Merge와 충돌

```sh
hg update <target>
hg merge <source>
hg resolve --list
hg resolve --mark <file>
hg commit -m "Merge <source>"
```

## Phase와 history 정리

```sh
hg phase
hg log -r . -T '{phase}\n'
hg rebase -s <source-rev> -d <destination-rev>
hg histedit <base-rev>
```

`draft`인지 확인한 뒤 rewrite한다. `public` changeset은 공유 history이므로 rewrite하지 않는다. `secret` changeset은 push/pull/clone되지 않는다.

## Extension

```ini
[extensions]
evolve =
convert =
```

```sh
hg help evolve
hg evolve --list
hg help convert
```

## Sources

- https://www.mercurial-scm.org/help/commands/bookmarks
- https://www.mercurial-scm.org/help/topics/phases
- https://www.mercurial-scm.org/help/extensions
