---
date: 2026-09-23
tags: [tech]
type: tech-tool-study
status: draft
---

# References

## 공식 문서

| 자료 | 용도 |
| --- | --- |
| [Introduction](https://hyperframes.heygen.com/introduction) | 제품 정의와 agent-built/editable/reliable render 개요 |
| [GitHub repository](https://github.com/heygen-com/hyperframes) | source, license, issue, example 탐색 |
| [GitHub Releases](https://github.com/heygen-com/hyperframes/releases) | 최신 버전과 breaking change 확인 |
| [CLI](https://hyperframes.heygen.com/packages/cli) | `init`, `preview`, `lint`, `render`, `doctor` reference |
| [Engine](https://hyperframes.heygen.com/packages/engine) | browser/capture/encoding internals |
| [Frame Adapters](https://hyperframes.heygen.com/concepts/frame-adapters) | seekable runtime integration과 v0 API 주의사항 |
| [Deploy guide](https://hyperframes.heygen.com/guides/deploy) | preview와 render API 배포 |

## Package registry

- https://www.npmjs.com/package/hyperframes
- https://www.npmjs.com/package/@hyperframes/engine

## 읽는 순서

1. Introduction으로 authoring model과 deterministic rendering의 목적을 잡는다.
2. CLI의 `init`, `preview`, `lint`, `render`, `doctor` 항목을 실제 명령과 함께 읽는다.
3. Engine과 Frame Adapter 문서로 frame seek contract를 확인한다.
4. Deploy guide를 읽고 production에서는 environment pinning과 job orchestration을 별도 설계한다.

## Sources

- https://hyperframes.heygen.com/introduction
- https://hyperframes.heygen.com/packages/cli
- https://github.com/heygen-com/hyperframes/releases
