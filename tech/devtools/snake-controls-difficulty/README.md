---
date: 2026-11-27
tags: [tech]
type: tech-tool-study
status: draft
---

# Snake 게임의 방향키 조작·성장·속도 기반 난이도 규칙

> **한 줄 정의**: 방향키로 Snake를 조작하고 먹이 섭취 후 성장하며, 속도 증가 조건으로 난이도를 조절하는 게임 제작 요구사항이다.

## Overview

Craft Anything의 Game 제작 요청 예시를 바탕으로 Input, Growth, Difficulty를 검증 가능한 규칙으로 분해한다. 실제 요청 전문과 구현 결과는 제공되지 않았다. 구현 언어·Engine·Framework도 알 수 없다.

| 구분 | 내용 |
|---|---|
| 확인됨 | 방향키 조작, 먹이 섭취 후 성장, 속도 증가 조건 존재 |
| 설계 결정 필요 | 방향 전환 정책, 성장량, 초기 속도, 증가 Trigger·폭·상한 |
| 추가 요구사항 | 충돌, 종료, 재시작, 점수, 먹이 생성 정책 |

먹이 섭취 → 성장은 확인되지만, 먹이 섭취 → 속도 증가는 확인되지 않는다. Browse → Build → Check → Complete는 제작 흐름이며 게임 상태 전이 규칙이 아니다.

## Learning Path

- [ ] [[tech/devtools/snake-controls-difficulty/README|학습 진입점과 전체 경로]]
- [ ] [[tech/devtools/snake-controls-difficulty/01-overview|Overview]]
- [ ] [[tech/devtools/snake-controls-difficulty/02-ecosystem|설계 대안 비교]]
- [ ] [[tech/devtools/snake-controls-difficulty/03-references|References]]
- [ ] [[tech/devtools/snake-controls-difficulty/04-learning/01-getting-started|시작하기]]
- [ ] [[tech/devtools/snake-controls-difficulty/04-learning/02-deep-dive|심화 학습]]
- [ ] [[tech/devtools/snake-controls-difficulty/05-projects|실전 프로젝트]]
- [ ] [[tech/devtools/snake-controls-difficulty/cheatsheet|Cheatsheet]]

## When To Use

- 짧은 Snake 제작 요청을 명세와 Acceptance criteria로 바꿀 때.
- 입력, 성장, 속도 변화가 실제 동작으로 연결되는지 검사할 때.
- 단계별·연속 Difficulty curve를 비교하는 Prototype을 설계할 때.

## When Not To Use

- Craft Anything의 내부 아키텍처나 특정 Engine 사용법을 확인할 때.
- 원본 Snake의 충돌·점수·속도 수치가 확정된 사양이 필요할 때.
- 웹사이트 유사도 90% 또는 최대 6라운드를 게임 합격 기준으로 적용하려 할 때. 이 조건은 별도의 웹사이트 제작·검사 맥락이다.

## Related Notes

- [[MOCs/Index]]
- [[MOCs/Devtools]]
- [[tech/devtools/snake-controls-difficulty/04-learning/02-deep-dive|관련 tech 노트: Input·Growth·Difficulty 심화]]
- Craft Anything 관련 tech 노트: 현재 작업 폴더에서 존재 여부를 확인할 수 없어 링크하지 않는다.

## Sources

- 사용자 제공 dossier: Craft Anything의 Snake Game 제작 요청 예시에 관한 수집 요약. 원문·영상 URL은 제공되지 않아 기재할 수 없다.
- 아래 설계안과 실습 수치는 학습용 제안이며, 원자료의 구현 사실이 아니다.
