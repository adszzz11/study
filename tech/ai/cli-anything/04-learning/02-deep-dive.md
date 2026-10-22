---
date: 2026-10-22
tags: [tech]
type: tech-tool-study
status: draft
---

# Deep dive

## Command와 state를 먼저 설계하기

좋은 harness는 GUI menu를 그대로 복제하지 않는다. agent가 수행할 domain action을 command group으로 정의하고, 각 command의 input, state transition, success artifact, JSON schema를 명시한다.

```json
{
  "ok": true,
  "artifact_path": "output/report.pdf",
  "operation": "export_pdf",
  "warnings": []
}
```

schema는 성공 경로만이 아니라 validation error, backend failure, partial result에서도 일관되게 설계한다. 사람이 보는 progress log는 stderr 등 별도 channel으로 분리할지 결정한다.

## E2E는 artifact로 판정하기

command exit code만으로는 실제 작업을 보장하지 못한다. 다음 순서로 검증한다.

1. 실제 backend로 native artifact를 생성한다.
2. artifact가 존재하고 예상 metadata/contents를 가지는지 검사한다.
3. 대상 software로 artifact를 재오픈 또는 재처리한다.
4. state snapshot과 JSON response를 assertion한다.

이 검증은 agent evaluation에도 유용하다. command, state snapshot, artifact assertion을 고정하면 task 성공을 deterministic하게 측정할 수 있다.

## Security boundary

generated harness는 신뢰 경계다. 특히 shell invocation, file path, network/API credential을 노출하면 아래 항목을 설계와 review에 넣는다.

- untrusted input validation과 path traversal 방지
- 허용된 executable·directory·endpoint의 allowlist
- 최소 권한(least privilege) credential과 분리된 secret 관리
- destructive action의 명시적 confirmation 및 dry-run
- command, caller, artifact를 남기는 audit log

MCP로 감싸더라도 이 경계는 사라지지 않는다. tool metadata와 user-facing description도 실제 권한과 부작용을 정확히 표현해야 한다.

## Sources

- https://github.com/HKUDS/CLI-Anything#-how-cli-anything-works
- https://github.com/HKUDS/CLI-Anything#limitations
- https://modelcontextprotocol.io/specification/2025-11-25/server/tools#security-considerations
