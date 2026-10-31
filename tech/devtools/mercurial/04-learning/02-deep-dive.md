---
date: 2026-10-24
tags: [tech]
type: tech-tool-study
status: draft
---

# 심화: phase, rewrite, evolution

## 1. Phase를 먼저 확인한다

```sh
hg log -r . -T '{rev}:{node|short} {phase} {bookmarks}\n'
hg phase
```

`draft`는 local history 정리에 쓸 수 있지만, `public`은 공유된 history라는 신호다. server가 publishing mode인지에 따라 push 뒤의 phase 전환이 달라질 수 있으므로 설정과 결과를 함께 확인한다. `secret`은 network operation에 포함되지 않는다.

## 2. Draft changeset만 rewrite한다

```sh
# extension이 설치·활성화된 환경에서 실행
hg rebase -s <source-rev> -d <destination-rev>
hg histedit <base-rev>
```

실습 전 `hg phase`를 실행하고 대상이 `draft`임을 확인한다. `public` changeset rewrite가 거부되는지 확인하는 것은 안전장치의 의미를 배우는 좋은 방법이지만, 실제 공유 repository에서는 시도하지 않는다.

## 3. Evolve로 troubled changeset 관찰

설정 파일의 `[extensions]`에 `evolve =`를 활성화한 뒤 사본에서 history mutation을 만든다.

```ini
[extensions]
evolve =
```

```sh
hg evolve --list
hg evolve
```

`evolve`는 obsolete, orphan, content-divergent state를 식별하고 후속 changeset을 안정화하는 데 쓴다. 자동 해결 결과는 `hg log -G`와 diff로 검토한다.

## 4. Git migration은 검증 가능한 사본에서

```ini
[extensions]
convert =
```

```sh
hg convert /path/to/git-project /path/to/hg-project
cd /path/to/hg-project
hg log -G
hg bookmarks
```

변환 후 reachable branch와 remote ref가 bookmark로 어떻게 매핑됐는지, author/committer metadata가 기대와 같은지 확인한다. 이 기능은 일회성 migration을 위한 것이며 Git remote와 일상적으로 동기화하는 bridge가 아니다.

## Sources

- https://www.mercurial-scm.org/help/topics/phases
- https://www.mercurial-scm.org/help/commands/rebase
- https://www.mercurial-scm.org/help/commands/histedit
- https://www.mercurial-scm.org/help/commands/evolve
- https://www.mercurial-scm.org/help/commands/convert
