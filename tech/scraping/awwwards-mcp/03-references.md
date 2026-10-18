---
date: 2026-10-18
tags: [tech]
type: tech-tool-study
status: draft
---

# References

## Primary sources

1. [awwwards-mcp repository / README](https://github.com/INSANE0777/Awwwards-mcp) — 설치, tool surface, 운영 안내
2. [GitHub Releases](https://github.com/INSANE0777/Awwwards-mcp/releases) — version pinning과 변경 이력
3. [npm: awwwards-mcp](https://www.npmjs.com/package/awwwards-mcp) — package 배포 정보
4. [package.json](https://github.com/INSANE0777/Awwwards-mcp/blob/main/package.json) — Node requirement와 dependency 확인
5. [TypeScript server source](https://github.com/INSANE0777/Awwwards-mcp/tree/main/src) — 실제 구현과 tool 동작 검토
6. [bundled agent skills](https://github.com/INSANE0777/Awwwards-mcp/tree/main/skills) — agent workflow 예시

## Protocol / 대상

7. [MCP TypeScript SDK v2](https://ts.sdk.modelcontextprotocol.io/v2/)
8. [MCP stdio serving](https://ts.sdk.modelcontextprotocol.io/v2/serving/stdio) — stdout channel 제약
9. [Awwwards](https://www.awwwards.com/) — reference의 원 출처

## 읽는 순서

repository README로 기능과 install을 확인하고, release와 `package.json`으로 실행 조건을 고정한다. 이후 source에서 cache·capture의 동작을 검토한 뒤, MCP stdio 문서로 host integration의 stdout/stderr 규칙을 확인한다.
