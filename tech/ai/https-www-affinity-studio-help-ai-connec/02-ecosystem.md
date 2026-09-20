---
date: 2026-09-01
tags: [tech]
type: tech-tool-study
status: draft
---

# Ecosystem과 대안 비교

## 비교표

| 방식 | 실행 대상 | 강점 | 제약·비용 | 적합한 경우 |
|---|---|---|---|---|
| **Affinity AI Connector for Claude** | 실행 중인 Affinity 문서와 Scripting workflow | 자연어 자동화, custom dialog/tool 생성, script 재사용 | Claude Desktop 의존, beta, 결과 검수 필요 | Affinity 중심 반복 production workflow |
| **Affinity Macro / Batch Job** | 기록 가능한 고정 편집·여러 파일 | 빠르고 deterministic하며 LLM 불필요 | 조건 분기, 문서 의미 해석, custom UI에 약함 | 같은 resize, filter, export의 반복 |
| **직접 Affinity scripting** | Affinity document model | 정밀 제어, version control과 test 가능, AI 불필요 | API와 coding 학습 필요, 문서화 성숙도 제약 | 팀 표준 automation, 장기 운영 도구 |
| **Canva AI Studio in Affinity** | 이미지/vector 생성과 AI-assisted edit | Generative Fill/Expand, Remove Background, Super Resolve 등 | Canva premium 필요, 범용 scripting 도구가 아님 | 콘텐츠 생성, 보정, selection 작업 |

## 선택 기준

```text
작업이 콘텐츠 생성·보정인가?
├─ Yes → Canva AI Studio 검토
└─ No
   └─ 동일한 고정 절차인가?
      ├─ Yes → Macro / Batch Job 검토
      └─ No
         └─ 문맥 해석·빠른 탐색이 중요한가?
            ├─ Yes → AI Connector로 prototype
            └─ No → 직접 scripting

검증된 Connector workflow가 장기 운영 대상인가?
└─ Yes → source review + test + version control을 거쳐 직접 관리
```

## 상호 배타적이지 않은 조합

- **Connector → Scripting panel**: 자연어로 초안을 만든 후 reusable tool로 저장한다.
- **Connector → 직접 scripting**: prototype을 source review, refactor, regression test를 거쳐 팀 도구로 승격한다.
- **AI Studio + Connector**: AI Studio로 asset을 생성·보정하고 Connector로 layer naming, layout, export를 자동화한다.
- **Macro + Connector**: 단순 고정 작업은 Macro로 유지하고 문서별 조건이 필요한 부분만 Connector에 맡긴다.

## 비교 시 주의

Adobe 등 다른 vendor의 Claude integration은 지원 application, 허용 action, 데이터 흐름이 다를 수 있다. 이름이 비슷하다는 이유만으로 Affinity Connector와 capability parity를 가정하지 말고 각 제품의 현재 공식 문서를 기준으로 비교해야 한다.

## Sources

- [Affinity integrations](https://www.affinity.studio/integrations)
- [Automate design tasks in Affinity with Claude](https://www.affinity.studio/blog/automate-design-tasks-affinity-claude)
- [Canva AI integrations in Affinity](https://www.affinity.studio/canva-integrations)

