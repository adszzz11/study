# Dify 심층 스터디

> 비주얼 캔버스로 LLM 워크플로우·에이전트·RAG를 만드는 셀프호스팅 플랫폼 — 142k★

## 한 줄 정의

**Dify**는 **노드 기반 비주얼 워크플로우 + RAG + 에이전트 + LLMOps**를 통합 제공하는 셀프호스팅 가능 플랫폼. 비기술자도 캔버스에서 LLM 앱을 만들 수 있고, 개발자에겐 API+SDK로 통합 가능하다.

## 3줄 요약

1. **비주얼 캔버스** + **API**의 결합 — 노코드와 코드 양쪽.
2. **RAG 풀스택**: 문서 ingestion·청킹·임베딩·재정렬·평가까지.
3. **셀프호스팅 OK**: Docker Compose 한 줄. 데이터 주권 + 무제한.

## 핵심 키워드

`#dify` `#visual-workflow` `#rag` `#agent` `#llmops` `#self-hosted` `#docker` `#apache-2.0+` `#python` `#nextjs`

## ⚡ Quick Start

```bash
git clone https://github.com/langgenius/dify.git
cd dify/docker
cp .env.example .env
docker compose up -d
# UI: http://localhost:80
```

요구사항: CPU 2+ core, RAM 4+ GiB, Docker.

## 📑 목차

| 파일 | 내용 |
|------|------|
| [01-overview.md](01-overview.md) | 컨셉 + 5대 빌딩블록 |
| [02-ecosystem.md](02-ecosystem.md) | n8n/Flowise/LangFlow와 차이 |
| [03-references.md](03-references.md) | 공식·자료 |
| [04-learning/01-self-host.md](04-learning/01-self-host.md) | Docker Compose 셋업 |
| [04-learning/02-workflow.md](04-learning/02-workflow.md) | 비주얼 워크플로우 |
| [04-learning/03-rag.md](04-learning/03-rag.md) | RAG 파이프라인 |
| [04-learning/04-agents-and-api.md](04-learning/04-agents-and-api.md) | 에이전트 + API 통합 |
| [05-projects.md](05-projects.md) | 실전 |
| [cheatsheet.md](cheatsheet.md) | 빠른 참조 |
