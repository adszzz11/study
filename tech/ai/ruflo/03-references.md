---
date: 2026-09-08
tags: [tech]
type: tech-tool-study
status: draft
---

# Ruflo References

> [[02-ecosystem|이전: 생태계]] · [[README|목차]] · [[04-learning/01-getting-started|다음: 시작하기]]

## 먼저 읽을 자료

| 우선순위 | 자료 | 확인할 내용 |
|---|---|---|
| 1 | [Official README](https://github.com/ruvnet/ruflo/blob/main/README.md) | 현재 설치 경로, CLI surface, plugin 목록 |
| 2 | [npm versions](https://www.npmjs.com/package/ruflo?activeTab=versions) | 실제 `latest`, release cadence |
| 3 | [Changelog](https://github.com/ruvnet/ruflo/blob/main/CHANGELOG.md) | breaking change, Claude Flow → Ruflo rebranding |
| 4 | [Configuration](https://github.com/ruvnet/ruflo/blob/main/v3/implementation/init/CONFIGURATION.md) | topology, max agents, backend, profile |
| 5 | [Ruflo SKILL.md](https://github.com/ruvnet/ruflo/blob/main/SKILL.md) | lifecycle hook와 intelligence pipeline |

## Subsystem 자료

| 영역 | 자료 | 읽을 때 주의할 점 |
|---|---|---|
| MCP/core | [ruflo-core](https://github.com/ruvnet/ruflo/blob/main/plugins/ruflo-core/README.md) | 314 tools는 해당 문서 snapshot; 필요한 namespace를 식별 |
| Memory | [AgentDB plugin](https://github.com/ruvnet/ruflo/blob/main/plugins/ruflo-agentdb/README.md) | 자체 benchmark claim과 일반 성능을 구분 |
| Guidance | [Architecture overview](https://github.com/ruvnet/ruflo/blob/main/v3/%40claude-flow/guidance/docs/guides/architecture-overview.md) | 설계 component가 실제 release에서 어느 정도 구현됐는지 확인 |
| Dependency | [Root package.json](https://github.com/ruvnet/ruflo/blob/main/package.json) | stable top-level version과 내부 alpha dependency를 별도 평가 |

## Version 검증

```bash
# registry의 실제 latest
npm view ruflo version

# 배포 tag와 전체 version 목록
npm view ruflo dist-tags --json
npm view ruflo versions --json

# 실행할 binary가 제공하는 실제 command surface
npx ruflo@latest --help
```

> [!note] 조사 snapshot
> 2026-09-08 기준 dossier의 npm `latest`는 `3.38.23`이다. 문서에 남은 `3.31.0`, `3.5.0` 예시는 현재 package version으로 간주하지 않는다.

## 출처 평가 원칙

- README의 feature count는 release마다 바뀌는 inventory이지 stable contract가 아니다.
- benchmark 수치는 dataset, hardware, baseline, metric이 제시된 경우에만 재현 가능하다고 판단한다.
- architecture 문서의 component 이름과 설치된 package export/CLI help를 대조한다.
- `main` branch 문서와 npm 배포 artifact가 다를 수 있으므로 production 검증은 pin한 version에서 한다.
- community tutorial보다 repository, npm metadata, package manifest를 우선한다.

## Related Notes

- [[tech/ai/model-context-protocol-mcp/README|Model Context Protocol (MCP)]]
- [[tech/ai/agent-orchestration/cli-agents|CLI Agents]]
- [[tech/ai/litellm/README|LiteLLM]]

## Sources

- https://github.com/ruvnet/ruflo/blob/main/README.md
- https://www.npmjs.com/package/ruflo?activeTab=versions
- https://github.com/ruvnet/ruflo/blob/main/CHANGELOG.md
- https://github.com/ruvnet/ruflo/blob/main/v3/implementation/init/CONFIGURATION.md
- https://github.com/ruvnet/ruflo/blob/main/SKILL.md
- https://github.com/ruvnet/ruflo/blob/main/plugins/ruflo-core/README.md
- https://github.com/ruvnet/ruflo/blob/main/plugins/ruflo-agentdb/README.md
- https://github.com/ruvnet/ruflo/blob/main/v3/%40claude-flow/guidance/docs/guides/architecture-overview.md
- https://github.com/ruvnet/ruflo/blob/main/package.json
