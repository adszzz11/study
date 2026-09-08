---
date: 2026-09-09
tags: [tech]
type: tech-tool-study
status: draft
---

# Muse — Microsoft Research

> **한 줄 정의**: Muse는 게임 화면과 controller actions를 함께 학습해 이후 화면·행동을 생성하는 Microsoft의 World and Human Action Model(WHAM) 연구 프로그램이다.

## Overview

짧은 gameplay prompt에서 여러 가능한 전개를 만들어 **gameplay ideation**을 탐색한다. Microsoft Research와 Ninja Theory가 협력했으며 초기 공개 WHAM은 **Bleeding Edge**에 특화됐다.

- **범위·기준일:** Microsoft Research Muse, 2026-09-09. Unity Muse와 Meta Muse Spark는 별개다.
- **초기 WHAM:** 200M·1.6B checkpoint, 화면·행동 공동 생성, 300×180 출력.
- **실시간 계열:** 현재 공식 명칭은 WHAM-RT. 2025년 기술 발표는 WHAMM이라는 이름을 사용한다.
- **학습 관점:** Consistency·Diversity·Persistency를 구분해 관찰한다. 생성 영상의 자연스러움만으로 게임 규칙의 정확성을 입증할 수 없다.
- **사용 조건:** Microsoft Research License가 적용된다. weights 공개가 자유로운 상업 이용을 뜻하지 않는다.

## Learning Path

- [ ] [[tech/ai/muse/01-overview|Overview]] — 목적, 입력과 출력, 주요 한계 이해
- [ ] [[tech/ai/muse/02-ecosystem|Ecosystem]] — world model과 제작 지원 도구 구분
- [ ] [[tech/ai/muse/03-references|References]] — 원문과 주장 연결
- [ ] [[tech/ai/muse/04-learning/01-getting-started|Getting started]] — 200M과 tiny-sample로 로컬 재현 준비
- [ ] [[tech/ai/muse/04-learning/02-deep-dive|Deep dive]] — tokenization·MaskGIT·평가 설계 학습
- [ ] [[tech/ai/muse/05-projects|Projects]] — 관찰 기록과 비교 실험 설계
- [ ] [[tech/ai/muse/cheatsheet|Cheatsheet]] — 명령·수치·주의점 복습

## When To Use

- gameplay 기록에서 환경 변화와 사람 행동을 함께 모델링하는 연구를 배울 때.
- 같은 출발점의 여러 rollout을 비교해 창의적 탐색 가능성을 평가할 때.
- autoregressive 생성과 MaskGIT의 지연·품질 절충을 공부할 때.

## When Not To Use

- 게임 엔진이나 emulator처럼 정확한 상태·규칙 실행이 필요할 때.
- 임의의 게임이나 자연어 prompt를 처리하는 범용 제작 도구가 필요할 때.
- 초기 공개 checkpoint로 실시간 플레이 또는 장기 객체 기억을 기대할 때.
- 공개 weights를 그대로 상업 서비스에 탑재하거나 재배포하려 할 때.

## Related Notes

- [[MOCs/Index]]
- [[MOCs/AI]]
- [[tech/ai/modal/README|Modal]] — GPU 실험 환경을 공부할 때 참고할 관련 노트. Muse와의 공식 통합을 뜻하지 않는다.

## Sources

- [Microsoft Research — WHAM 프로젝트](https://www.microsoft.com/en-us/research/project/wham/)
- [Muse 최초 발표 (2025-02-19)](https://www.microsoft.com/en-us/research/blog/introducing-muse-our-first-generative-ai-model-designed-for-gameplay-ideation/)
- [공식 Model Card·실행 코드·weights](https://huggingface.co/microsoft/wham)
- [WHAM-RT 현재 소개](https://www.microsoft.com/en-us/research/project/wham/wham-rt/)
- [Microsoft Research License](https://huggingface.co/microsoft/wham/blob/main/LICENSE.md)
