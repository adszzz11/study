---
date: 2026-10-04
tags: [tech]
type: tech-tool-study
status: draft
---

# Claude Code Extension Ecosystem

## 기능 비교

| 대상 | 주 역할 | 실행/결정성 | Claude Mod와의 차이 |
| --- | --- | --- | --- |
| Claude Mod | runtime 행동·UI 확장 | event마다 code로 강제 | event rewrite/replace와 UI rendering까지 다룬다. 권한과 supply-chain 위험도 크다. |
| Classic Hook | lint, notification, policy check | lifecycle event마다 | shell/HTTP/prompt 자동화에 좋지만 event rewrite·persistent UI에는 맞지 않는다. |
| Skill | 재사용 knowledge/workflow | on-demand | instruction이므로 enforcement가 아니다. |
| MCP | 외부 tool/data 접속 | tool invocation | capability를 제공할 뿐 Claude Code runtime/UI를 수정하지 않는다. |
| Plugin | 여러 extension의 package | install/enable | Mod는 plugin 안에 들어가는 고급 구현 형태다. |
| `CLAUDE.md` | 프로젝트 상시 규칙·context | session context | 지시문이며 hard enforcement가 아니다. |

## 선택 규칙

```text
외부 데이터 또는 서비스가 필요한가? ── 예 → MCP
아니오 ┬ 매번 강제할 규칙인가? ── 예 → Classic Hook 또는 Mod
       │  UI / event rewrite / session state가 필요한가? ── 예 → Mod
       └ 지식·절차를 안내하면 되는가? ── 예 → Skill 또는 CLAUDE.md
```

공식 가이드도 Hook을 deterministic automation, Skill을 on-demand instruction으로 구분한다. “반드시 매번 지켜야 하는 규칙”은 `PreToolUse` Hook 같은 enforcement layer에 두는 것이 기본 선택이다. UI가 필요하거나 Hook의 input/output contract를 넘어 event pipeline을 다뤄야 할 때 Mod로 올라간다.

## Plugin과 Marketplace

Plugin은 commands, subagents, MCP servers, Hooks, Mods 등을 배포 가능한 단위로 묶는다. Claude Mod는 별도 package format이 아니라 그 plugin 안의 function-hooks module이다. 따라서 install source, manifest, dependency, update channel까지 plugin supply chain 관점에서 관리한다.

## 실무 판단 예시

| 요구 | 우선 선택 | 이유 |
| --- | --- | --- |
| API 문서를 읽어 배포 상태를 조회 | MCP | 외부 capability 연결 문제 |
| 모든 deploy 전 branch 명명 검사 | PreToolUse Hook | UI/rewrite 없이 deterministic enforcement |
| deploy command를 수정하고 승인 pane 표시 | Mod | event rewrite + custom UI 필요 |
| 팀의 coding convention 설명 | `CLAUDE.md` 또는 Skill | context/knowledge 주입 문제 |
| 매 turn context 사용량을 시각화 | Mod | stateful UI rendering 필요 |

## Sources

- https://code.claude.com/docs/en/features-overview
- https://claude.com/blog/claude-code-plugins
- https://claude.com/marketplace/plugins
- https://claude.com/blog/claude-code-mods
