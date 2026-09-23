---
date: 2026-09-23
tags: [tech]
type: tech-tool-study
status: draft
---

# OpenCut — References

[[tech/devtools/opencut/README|학습 진입점]]

## 공식 OpenCut 자료

| 자료 | 확인할 내용 |
|---|---|
| [Main repository](https://github.com/OpenCut-app/OpenCut) | 현재 status, license, 개발 명령, classic/rewrite의 endpoint |
| [Rewrite tracking #811](https://github.com/OpenCut-app/OpenCut/issues/811) | Rust core 구조, plugin·MCP·headless·scripting roadmap과 progress checklist |
| [Releases](https://github.com/OpenCut-app/OpenCut/releases) | classic 기능 변화와 release note |
| [v0.3.0](https://github.com/OpenCut-app/OpenCut/releases/tag/v0.3.0) | masks, graph editor, captions, ripple-editing 관련 상세 |
| [Classic repository](https://github.com/OpenCut-app/opencut-classic) | 현재 사용할 classic source와 archived 상태 |
| [Classic architecture guidance](https://github.com/OpenCut-app/opencut-classic/blob/main/AGENTS.md) | Next.js와 Rust/WASM compositor·effects·masks·bindings 방향 |
| [Desktop README](https://github.com/OpenCut-app/OpenCut/blob/main/apps/desktop/README.md) | desktop build 및 platform requirements |
| [Classic editor](https://opencut.app/) | 학습용 UI 실습 endpoint |
| [Rewrite preview](https://new.opencut.app/) | rewrite의 개발 preview endpoint |

## 읽는 순서

1. main repository의 **Status**에서 classic과 rewrite를 먼저 구분한다.
2. `v0.3.0` release로 classic에서 실제 사용할 수 있는 기능을 확인한다.
3. #811의 architecture와 progress checklist로 automation 기능의 완료 여부를 재확인한다.
4. 개발 참여 전에는 desktop README와 repository의 `proto use`, Moon task를 함께 읽는다.

## 상태를 재검증해야 하는 항목

- `opencut.app`과 `new.opencut.app`이 어떤 version을 가리키는가
- rewrite의 public beta, plugin host, Editor API, MCP, headless mode의 완료 여부
- classic의 archive/maintenance 상태와 최신 release
- desktop의 실제 buildability와 지원 platform

## Sources

- [OpenCut main repository](https://github.com/OpenCut-app/OpenCut)
- [Rewrite tracking](https://github.com/OpenCut-app/OpenCut/issues/811)
- [OpenCut releases](https://github.com/OpenCut-app/OpenCut/releases)
- [Desktop README](https://github.com/OpenCut-app/OpenCut/blob/main/apps/desktop/README.md)
