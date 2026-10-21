---
date: 2026-10-21
tags: [tech]
type: tech-tool-study
status: draft
---

# Deep dive: quality tiers and MCP boundary

## Quality tier를 단계적으로 올리기

| 단계 | 적용 대상 | 확인할 점 |
|---|---|---|
| 기본 converter | digital PDF, Office, 웹 문서 | 구조 보존, 속도, 비용 0의 local path |
| OCR plugin | 이미지가 포함된 문서 | Vision client 출력의 정확도·비용·개인정보 경계 |
| Azure Document Intelligence | 스캔본과 layout OCR | 페이지 layout과 OCR 오류 감소 여부 |
| Azure Content Understanding | 정형 field가 필요한 업무 문서 | analyzer 결과, confidence, 호출 비용 |

동일한 스캔 PDF와 복잡한 표를 각 단계로 변환해 Markdown 품질과 retrieval 성능을 비교한다. cloud tier는 기본 path가 부족하다는 측정 결과가 있을 때만 도입한다.

## Plugin 원칙

third-party plugin은 기본 비활성화다. 사용 전 plugin의 유지보수 상태, 추가 네트워크 호출, 입력 데이터 처리 위치를 확인하고 필요한 경우에만 `--use-plugins`로 활성화한다.

## MCP 배포와 보안

`markitdown-mcp`는 STDIO, Streamable HTTP, SSE transport와 `convert_to_markdown(uri)` tool을 제공한다. `file:`, `data:`, `http(s):` URI를 읽을 수 있으므로, 변환 권한은 실행 process의 I/O 권한과 같다.

- untrusted input은 가능한 한 `convert_local()` 또는 `convert_stream()`처럼 좁은 API로 처리한다.
- HTTP/SSE server는 localhost에 bind하거나 container sandbox에 격리한다.
- container에는 필요한 directory만 최소·read-only mount한다.
- 외부 interface 공개와 무제한 `file:` URI 접근을 피한다.
- 허용 URI scheme, 경로 allowlist, 크기·시간 제한, 변환 audit log를 운영 경계에 둔다.

## Sources

- https://github.com/microsoft/markitdown/blob/main/packages/markitdown-mcp/README.md
- https://github.com/microsoft/markitdown
- https://learn.microsoft.com/en-us/azure/ai-services/content-understanding/overview
