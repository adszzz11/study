---
date: 2026-11-29
tags: [tech]
type: tech-tool-study
status: draft
---

# References

## 1차 출처와 확인 범위

| 출처 | 활용한 정보 | 주의점 |
|---|---|---|
| GitHub 저장소 README | 목적, 명령, 설치·build, cache, section ID 경고 | 제공된 dossier를 통해 정리 |
| 수집 당시 저장소 화면 | 5 commits·0 stars·0 forks | 현재 상태·품질을 의미하지 않음 |
| README의 개발 명령 | format·lint·typecheck·test | 실행 결과·coverage 미확인 |

원문: https://github.com/miinhho/codewiki-cli

## 추가 확인할 항목

- RPC 오류와 upstream 변경에 대한 처리 방식.
- Cache TTL·손상 복구·동시 접근 정책.
- Wiki 미제공 저장소 및 잘못된 ID의 반환 동작.
- Chunk 최대 크기·token 기준·overlap·출력 schema.
- Skill 내부 상세 지침과 bundled CLI 갱신 상태.
- 일반 command 설치를 위한 배포 경로.

위 항목은 검토 과제다. 구현되어 있거나 test가 있다는 뜻은 아니다. 이 노트의 명령은 README 기반 학습 예시이며 실제 실행을 확인한 결과가 아니다.

관련: [[tech/devtools/codewiki-cli-analysis-9fbbd58a/04-learning/02-deep-dive|검증 실습]] · [[tech/devtools/codewiki-cli-analysis-9fbbd58a/README|학습 진입점]]


## Sources

- https://github.com/miinhho/codewiki-cli — 제공된 dossier의 README 기반 정리. 실습 및 성능 검증은 미실행.
