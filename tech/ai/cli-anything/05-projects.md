---
date: 2026-10-22
tags: [tech]
type: tech-tool-study
status: draft
---

# CLI-Anything projects

## Creative production agent

Blender, GIMP, FFmpeg workflow를 domain command로 정리한다. batch rendering, asset export, 검수 artifact 생성을 자동화하고, output을 실제 tool로 재오픈해 검증한다.

## Office automation

LibreOffice 기반 spreadsheet, report, PDF 변환을 job queue와 CI artifact로 운영한다. 입력 fixture, 변환 결과, 재열기 test를 versioned fixture로 관리한다.

## Internal legacy app bridge

source가 있는 사내 desktop tool에서 핵심 업무를 command group으로 추출한다. human GUI는 fallback으로 남기고, agent에는 승인된 workflow와 최소 권한만 노출한다.

## API consolidation CLI

여러 SaaS endpoint를 업무 단위의 stateful CLI로 묶는다. raw endpoint를 모두 노출하기보다 `customer sync`, `invoice export`처럼 의도를 드러낸 command를 만들면 tool 선택과 token 부담을 줄일 수 있다.

## Benchmark/evaluation harness

CLI command, state snapshot, artifact assertion을 fixture와 함께 제공한다. 동일한 input에서 native artifact와 JSON schema가 안정적인지 검사해 agent task의 성공 여부를 deterministic하게 평가한다.

## 공통 acceptance criteria

- `--help`만으로 안전한 command를 발견할 수 있다.
- machine-readable JSON이 stable schema를 따른다.
- 실제 backend가 native artifact를 생성하고 재오픈된다.
- 권한, path, network access가 allowlist와 audit log로 통제된다.

## Sources

- https://github.com/HKUDS/CLI-Anything
- https://arxiv.org/abs/2606.03854
