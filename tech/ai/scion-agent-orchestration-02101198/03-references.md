---
date: 2026-11-29
tags: [tech]
type: tech-tool-study
status: draft
---

# Scion References

## 자료 읽기 지도

| 자료 | URL | 읽을 목적 |
|---|---|---|
| 공식 repository·README | https://github.com/GoogleCloudPlatform/scion | 정의·Quick Start·운영 모드·주의사항 |
| README 원문 | https://github.com/GoogleCloudPlatform/scion/blob/main/README.md | 설치와 명령 변경 확인 |
| 공식 문서 진입점 | https://googlecloudplatform.github.io/scion/ | 설치·architecture·configuration 문서 탐색 |
| License | https://github.com/GoogleCloudPlatform/scion/blob/main/LICENSE | Apache-2.0 조건 확인 |
| Release 목록 | https://github.com/GoogleCloudPlatform/scion/releases | 실습 버전과 변경사항 확인 |
| Issues | https://github.com/GoogleCloudPlatform/scion/issues | 제약·문제 보고 확인 |
| Scion Films | https://films.scion-ai.dev/ | 사람 피드백과 agent retrospective의 적용 사례 |

## 근거의 강도

- **기능 설명:** 제공 dossier를 주된 근거로 정리했다. 작성 시 repository README에서도 프로젝트 정의와 Quick Start 경로를 대조했다.
- **활용 사례:** Films, Relics of Athenaeum, Google 내부 실험은 가능성을 보여준다. 일반적인 성능 보장은 아니다.
- **설계적 해석:** Workspace 선택의 장단점, 협업 역할 계약, 평가 방법은 학습을 위한 해석·제안이다.
- **미확인:** 정량 생산성·비용 효과, metrics 상세, 감사 로그 보존, 상세 권한 모델, sandbox 수준, A2A 호환 범위.

Relics of Athenaeum은 README의 In Action에서 연결된 사례로 찾아간다. 확인되지 않은 별도 URL을 만들지 않는다. 제공 dossier 자체에는 독립적인 공개 URL이 없다.

## 버전 기록 요령

Pre-1.0에서는 문서와 설치 버전이 달라질 수 있다. 실습 기록에 날짜, release/tag 또는 commit, CLI help에서 확인한 명령 형식, harness·runtime 조합을 남긴다. 이 노트 작성 과정에서는 Scion을 설치하거나 실제 agent 실행을 검증하지 않았다.

## Navigation

- [[tech/ai/scion-agent-orchestration-02101198/README|Scion 학습 진입점]]

## Sources

- https://github.com/GoogleCloudPlatform/scion — README 및 제공된 dossier의 프로젝트 설명.
