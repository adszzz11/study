---
date: 2026-09-01
tags: [tech]
type: tech-tool-study
status: draft
---

# Getting Started

## 준비물

- macOS 또는 Windows의 최신 **Affinity by Canva desktop app**
- Affinity에서 사용할 Canva account
- 최신 **Claude Desktop**과 Claude account
- 원본이 아닌 테스트용 `.af` 문서
- undo/history 및 versioned backup을 사용할 수 있는 환경

Team·Enterprise Claude 환경에서는 조직 관리자가 Connector를 먼저 허용해야 할 수 있다.

## 설치와 연결

1. Affinity를 설치하고 Canva account로 로그인한다.
2. Claude Desktop에 로그인한다.
3. Claude Desktop의 `Customize/Settings → Connectors → Browse connectors`에서 **Affinity**를 선택해 설치한다.
4. Affinity에서 `Settings → Model Context Protocol`을 연다.
5. **Enable MCP server**를 활성화한다.
6. Affinity와 Claude Desktop을 모두 실행한 채 테스트 문서를 연다.
7. Claude에 연결 상태를 확인한다.

```text
Can you see the Affinity MCP server?
연결 상태와 현재 열려 있는 문서를 읽을 수 있는지만 확인해 줘.
문서는 수정하지 마.
```

UI label은 beta update나 OS에 따라 달라질 수 있으므로 보이지 않으면 공식 setup guide의 최신 화면을 확인한다.

## 안전한 첫 실행

읽기 전용 확인 → 작은 reversible change → 결과 검수 순서로 진행한다.

```text
현재 문서에서 선택된 artboard 하나만 대상으로 작업해 줘.
먼저 변경 예정인 layer 수와 rename 계획을 보여 주고 기다려.
승인 후 unnamed layer만 `section-role-index` 규칙으로 rename해 줘.
그 외 object, style, position, export setting은 변경하지 마.
```

실행 전 확인할 항목:

- 대상 document와 selection이 맞는가?
- 변경 범위가 layer 이름처럼 쉽게 되돌릴 수 있는가?
- 출력 경로와 overwrite 정책이 명시됐는가?
- 결과를 눈으로 비교하거나 count로 검증할 수 있는가?

## 첫 workflow 저장

1. 작은 sample document에서 prompt를 반복해 동작을 안정화한다.
2. generated script의 대상 범위와 file I/O를 검토한다.
3. 같은 sample에 두 번 실행해 idempotency 또는 중복 효과를 확인한다.
4. Affinity의 Scripting panel에 알아보기 쉬운 이름으로 저장한다.
5. Affinity version, script version, sample file, 예상 결과를 기록한다.

예시 이름:

```text
Export Social Artboards v1
Input: selected artboards
Output: ./exports/{artboard}-{width}x{height}.png
Affinity tested: <version>
```

## 문제 해결

| 증상 | 점검 |
|---|---|
| Claude가 Affinity를 찾지 못함 | 두 앱 실행 여부, Connector 설치, `Enable MCP server` 확인 |
| Connector가 목록에 없음 | Claude Desktop update, account/region/organization 정책 확인 |
| 잘못된 문서가 대상이 됨 | active document와 selection을 prompt에 명시하고 실행 전 preview 요청 |
| script가 일부 object에서 실패 | object type, locked layer, naming collision을 sample로 분리 |
| update 후 기존 script 실패 | version 기록 확인 후 regression sample로 재검증 |

## Sources

- [Affinity AI Connector 설정 가이드](https://www.affinity.studio/help/ai-connector-setup/)
- [Anthropic Connector 가이드](https://support.claude.com/en/articles/11176164-use-connectors-to-extend-claude-s-capabilities)
- [Affinity automation examples](https://www.affinity.studio/blog/automate-design-tasks-affinity-claude)

