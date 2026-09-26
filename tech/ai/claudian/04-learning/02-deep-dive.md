---
date: 2026-09-27
tags: [tech]
type: tech-tool-study
status: draft
---

# Claudian — Deep Dive

> [[01-getting-started|이전: Getting Started]] · [[../README|목차로 돌아가기]] · [[../05-projects|다음: Projects]]

## 1. provider-neutral UI와 native CLI의 경계

Claudian의 `core`는 execution, registry, session lifecycle, approval을 provider 중립적으로 조정한다. 그러나 각 provider adapter의 transport와 state model은 다르다.

| Adapter | 연결 방식 | 확인할 운영 항목 |
|---|---|---|
| Claude | SDK | CLI 인증, tool approval, session 규칙 |
| Codex | app-server / JSON-RPC | executable discovery, app-server protocol, approval |
| Grok | ACP | ACP 호환성과 provider capability |
| OpenCode | RPC | v2 사용 여부와 migration 상태 |
| Pi | native JSONL history | history 저장 위치와 retention |

따라서 “multi-provider”는 같은 model behavior를 보장한다는 뜻이 아니다. 지원 여부, tool capability, approval dialog, session persistence를 provider별로 작은 test task로 확인한다.

## 2. context는 최소 권한으로 구성하기

`@mention`은 중요한 노트를 명시적으로 context에 넣는 좋은 출발점이지만, agent가 vault search를 수행하면 추가 파일을 발견할 수 있다. context는 다음처럼 계층화한다.

```text
task instruction
  + named files (@note.md, @folder)
  + vault-local instruction / Skill
  + agent search results
  + MCP tool output
```

- named file: 사용자가 의도한 자료
- search/tool output: 유용하지만 prompt injection과 stale information을 포함할 수 있는 자료
- instruction: 권한을 넓히기보다 금지 경로·수정 규칙·출력 형식을 명확히 하는 계약

예시 instruction:

```text
- `private/`, `.obsidian/`, `archive/`는 읽거나 수정하지 않는다.
- 파일 변경 전 대상 파일과 변경 이유를 요약한다.
- 삭제·이동·외부 전송은 실행하지 않고 제안만 한다.
- claim을 추가할 때는 source URL 또는 확인 TODO를 남긴다.
```

## 3. MCP와 Skills: 재사용하되 별도 위협 모델로 본다

Claudian은 별도 MCP marketplace를 만들어 권한을 추상화하기보다 native CLI의 MCP config와 Skills를 재사용한다. 이 방식은 기존 workflow를 UI로 가져오는 장점이 있지만, MCP server가 가진 network·filesystem·write 권한도 함께 가져온다.

권장 rollout:

1. built-in file context와 provider 기본 tool부터 검증한다.
2. 조회만 하는 MCP server 하나를 test vault에 연결한다.
3. tool description과 output을 untrusted input으로 취급한다.
4. write MCP는 action별 approval, allowlist, audit 가능성이 갖춰진 뒤 추가한다.
5. 반복 prompt는 `$` Skill로 만들되, destructive action을 Skill 내부의 자동 단계로 숨기지 않는다.

## 4. 변경 workflow: propose → review → apply → verify

```text
Scope files → read/search → proposal → inline diff → human review → apply → verification
```

| 단계 | 확인 질문 |
|---|---|
| Scope | agent가 접근한 파일과 폴더가 task에 필요한 최소 범위인가? |
| Proposal | 새 사실·인용·해석을 분리해 설명했는가? |
| Review | frontmatter, wikilink, 삭제, 의미 변화가 의도한 것인가? |
| Apply | 실제 적용 대상이 검토한 diff와 같은가? |
| Verify | link, Markdown rendering, search result, `git diff`로 결과를 확인했는가? |

agent의 완료 선언은 검증이 아니다. 특히 bulk rename, frontmatter migration, link repair에서는 변경 파일 수·broken link 수·diff를 독립적으로 점검한다.

## 5. prompt injection과 data egress

노트 본문, 웹에서 가져온 자료, MCP output에는 “다른 파일을 읽어라”, “approval을 무시하라” 같은 간접 지시가 섞일 수 있다. 해당 텍스트는 task instruction이 아니라 data다.

- 개인 vault와 project vault를 분리한다.
- provider로 전송될 수 있는 prompt, attachment, tool output을 사전에 분류한다.
- shell/network/write tool은 native CLI approval을 해제하지 않는다.
- external write, publish, delete는 explicit human approval 뒤에만 실행한다.
- trace나 공유한 chat export에서 secret·PII를 제거한다.

## Production readiness checklist

- [ ] provider별 executable, authentication, capability를 test vault에서 검증했다.
- [ ] vault instruction에 금지 경로와 변경 전 검토 규칙이 있다.
- [ ] read-only MCP부터 도입했고 write 권한은 분리했다.
- [ ] inline diff와 version control/backup으로 rollback 경로가 있다.
- [ ] prompt injection을 포함한 자료를 untrusted로 취급한다.
- [ ] provider data-use policy와 local approval policy를 모두 확인했다.

## Sources

- [Claudian README — Architecture](https://github.com/YishenTu/claudian#architecture)
- [Claudian README — Privacy & data use](https://github.com/YishenTu/claudian#privacy--data-use)
- [Claudian README — Features & usage](https://github.com/YishenTu/claudian#features--usage)
- [Model Context Protocol](https://modelcontextprotocol.io/)
