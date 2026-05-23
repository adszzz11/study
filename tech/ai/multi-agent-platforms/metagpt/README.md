# MetaGPT 심층 스터디

> "한 줄 요구사항 → 완성된 소프트웨어 회사" — SOP(Standard Operating Procedure) 기반 LLM 조직

## 한 줄 정의

**MetaGPT**는 PM·Architect·PM·Engineer·QA 등 **소프트웨어 회사 직책**을 LLM 역할로 시뮬레이션. **"Code = SOP(Team)"** 원칙으로 자연어 요구사항을 자동 분해·구현한다.

## 3줄 요약

1. **소프트웨어 회사 메타포**: PM(기획) → Architect(설계) → Engineer(구현) → QA(검증).
2. **SOP 명문화**: 회사 SOP를 명시적으로 코드화 → LLM 협업의 일관성 ↑.
3. **결과물 풍부**: user story, 경쟁 분석, 요구사항, 데이터 구조, API spec, 소스 코드, 문서까지.

## 핵심 키워드

`#metagpt` `#sop` `#software-company` `#multi-agent` `#code-generation` `#python` `#mit` `#chatdev-similar`

## ⚡ Quick Start

```bash
pip install --upgrade metagpt
metagpt --init-config
# ~/.metagpt/config2.yaml 에 OPENAI/Anthropic 키 입력

metagpt "할 일 관리 웹앱을 만들어줘. React + FastAPI 스택"
# 결과: workspace/ 에 PRD, 설계 문서, 소스코드 생성
```

## 📑 목차
| 파일 | 내용 |
|------|------|
| [01-overview.md](01-overview.md) | SOP 모델·역할들 |
| [02-ecosystem.md](02-ecosystem.md) | ChatDev/AutoGen와 차이 |
| [03-references.md](03-references.md) | 논문·자료 |
| [04-learning/01-roles-and-actions.md](04-learning/01-roles-and-actions.md) | Role+Action 패턴 |
| [04-learning/02-environment-messaging.md](04-learning/02-environment-messaging.md) | 환경·메시지 publish/subscribe |
| [04-learning/03-data-interpreter.md](04-learning/03-data-interpreter.md) | Data Interpreter |
| [04-learning/04-incremental-dev.md](04-learning/04-incremental-dev.md) | 점진적 개발 |
| [05-projects.md](05-projects.md) | 실전 |
| [cheatsheet.md](cheatsheet.md) | 빠른 참조 |
