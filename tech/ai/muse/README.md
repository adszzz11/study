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

## 추가 조사: 학습 대상 정정 — Meta Muse

> 정정일: 2026-09-09. 사용자 의견 “다시 학습해 이거 meta의 muse야”를 반영한다. **이 study의 대상은 Meta Muse다.** 위 Microsoft Research/WHAM 설명과 기존 학습 경로는 대상을 잘못 선택한 기록이며, Meta Muse의 정의·사양·설치법으로 사용하지 않는다. append 요청에 따라 기존 본문은 보존한다.

- **Muse:** Meta가 2026-09-08 발표한 개인 AI 에이전트(personal AI agent).
- **Muse Spark:** 에이전트의 추론을 담당하는 기반 모델 계열. 제품 Muse와 모델 Muse Spark를 구분한다.
- 새 학습 순서: 각 파일의 `추가 조사` 섹션을 **개요 → 생태계 → 참고자료 → 시작하기 → 심화 → 프로젝트 → cheatsheet** 순서로 읽는다.
- 연구 질문: “어떤 게임 프레임을 생성하는가?”에서 “사용자 목표를 어떻게 실행하고, 기억하며, 검증 가능한 결과로 남기는가?”로 전환한다.

출처: [Meta Muse 공식 발표](https://about.fb.com/news/2026/09/introducing-muse-personal-ai-agent/).
