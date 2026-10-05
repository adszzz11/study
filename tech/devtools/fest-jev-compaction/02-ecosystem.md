---
date: 2026-10-05
tags: [tech]
type: tech-tool-study
status: draft
---

# fast-jev-compaction: Ecosystem

| 방식 | 처리 방식 | 원문 보존 | 강점 | 주요 trade-off |
|---|---|---:|---|---|
| fast-jev-compaction | Jev의 per-tool keep/truncate/drop | 유지 항목만 | log/path/error 보존에 유리 | 외부 API, 판정 오류, rewrite 비용 |
| Claude Code native compaction | built-in summary/auto-compaction | 보장 안 됨 | 별도 plugin 의존이 작음 | 세부 evidence 탈락 가능 |
| Fresh context + filesystem state | 새 session에서 repo/progress file 재발견 | 파일에는 가능 | history 재작성 회피 | 문서화 discipline·재탐색 필요 |
| RAG/retrieval memory | 필요 시 외부 index retrieval | index 품질 의존 | 대규모 장기 memory | indexing/retrieval 오류, 실시간 history와 분리 |
| Pi community adapter | Pi lifecycle에 extractive compaction | 유지 항목만 | Pi workflow에 맞춤 | upstream과 별개인 third-party 구현 |
| Codex port/PoC | Codex lifecycle 주위 Jev pruning | 유지 항목만 | 개념 검증 | 작성자도 experimental, 실작업은 기본 compaction 권고 |

## 선택 기준

1. **증거 재사용성**: 다음 turn이 이전 stack trace/path를 정확히 참조해야 하면 extractive pruning 후보가 된다.
2. **데이터 경계**: 외부 endpoint 전송이 불가하면 native compaction 또는 fresh context를 택한다.
3. **작업 지속성**: 장기 작업은 compaction 여부와 무관하게 filesystem에 progress/state를 남긴다.
4. **검증 가능성**: 동일 trajectory에서 task success, 재실행 수, evidence 재발견 시간까지 비교한다.

## Claude Code와의 관계

Claude Code는 `DISABLE_AUTO_COMPACT`, `DISABLE_COMPACT`, `CLAUDE_CODE_AUTO_COMPACT_WINDOW` 등의 native compaction 제어 환경 변수를 제공한다. plugin은 이를 대체하는 보편 표준이 아니라 function-hook 기반의 선택적 실험으로 취급한다.

## 관련 링크

- [Claude Code environment variables](https://code.claude.com/docs/ko/env-vars)
- [Pi adapter example](https://github.com/QuentinDanblon/pi-fast-jev-compaction)
- [Codex PoC](https://github.com/leonaaardob/fast-dev-compaction)
