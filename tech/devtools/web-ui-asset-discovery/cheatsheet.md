---
date: 2026-11-26
tags: [tech]
type: tech-tool-study
status: draft
---

# Cheatsheet · 탐색에서 구현까지

## 기본 흐름

```text
예시 탐색 → 시각적 요구사항 기록 → 전달 형식·사용 조건 확인
→ 작은 범위 구현 → 외형·동작·실행 검증 → 적용 판단
```

위 흐름은 실습 절차다. 자료에서 확인된 흐름은 후보 선택 후 불명확한 형식의 내용을 Codex·Claude Code에 전달하는 활용 안내까지다.

## 확인 사실과 미확인 사항

| 구분 | 요약 |
|---|---|
| 확인 | 다양한 디자인 예시, 버튼·책 형태 카드, 애니메이션 배경 언급 |
| 안내 | Codex·Claude Code에 붙여넣기 |
| 미확인 | 복사 형식, 상세 preview, 검색·필터, 통합 결과 |
| 도입 전 확인 | framework, dependencies, license, 성능, 실행 조건 |

## 형식별 다음 행동

| 실제 확보한 내용 | 다음 확인 |
|---|---|
| source code | 파일 구성, imports, dependencies, 실행 조건 |
| prompt | 구체적 요구사항, 프로젝트 맥락, 생성 결과 |
| 기타·불명확 | 형식과 처리 방법 확인 후 진행 |

어느 형식도 threeui의 제공 형식으로 확정된 것은 아니다.

## 검증 체크리스트

- [ ] 형태·색상·배치와 interaction·animation을 구분했는가?
- [ ] 정지 화면 관찰과 실제 동작 확인을 나눴는가?
- [ ] 전달 형식과 사용 조건을 확인했는가?
- [ ] 외형·동작을 각각 검증했는가?
- [ ] 실행 성공·console error·dependency 변경을 확인했는가?
- [ ] 동적 배경의 가독성·입력 반응·화면 크기·motion 감소 대응을 확인했는가?

## 피해야 할 단정

- 디자인 예시가 곧 production component라는 단정.
- 꽃·타일 구체 외형만으로 WebGL·3D rendering·특정 library를 추론.
- 붙여넣기 안내만으로 자동 통합을 보장한다고 해석.
- 동일 조건의 실험 없이 Codex·Claude Code의 우열을 결론.


## Related Notes

- [[tech/devtools/web-ui-asset-discovery/README|학습 경로로 돌아가기]]

## Sources

- https://threeui.com/browse — dossier에 제시된 탐색 화면 URL. 아래 내용은 제공된 영상 요약에 근거하며, 사이트의 현재 기능을 직접 검증한 결과는 아니다.
