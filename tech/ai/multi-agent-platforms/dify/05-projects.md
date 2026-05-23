# Part 5. Dify 실전 프로젝트

## 🟢 P1. Vault RAG 챗봇 (★)

본 Obsidian vault 전체를 KB로 인덱싱 → 텔레그램 봇으로 검색·요약.

- KB: vault 마크다운 파일 자동 동기화 (cron)
- Workflow: Retrieval → LLM → 한국어 응답
- Telegram API 외부 통합

## 🟢 P2. 일일 브리핑 (★)

Scheduled API 호출 (외부 cron) → Workflow가 날씨·뉴스·캘린더 조합 → 텔레그램/이메일.

## 🟡 P3. 멀티 단계 코드 리뷰 (★★)

```
[Start: PR URL] → [HTTP: GitHub API로 diff] → [LLM: 보안] → [LLM: 스타일] → [LLM: 통합] → [End]
```

## 🟡 P4. 가족용 사진 검색 (★★)

이미지 임베딩 + 캡션 → KB → 자연어 검색.

## 🔴 P5. Paperclip + Dify 통합 (★★★)

Paperclip에 Dify 워크플로우를 webhook 직원으로 등록. 비기술자(가족 등)가 Dify 캔버스에서 비서 흐름 편집 → Paperclip이 호출.

## ⚠️ Best Practices

- DSL을 git에 commit (워크플로우 버전 관리)
- Eval 데이터셋 만들고 변경 시 회귀 측정
- API key 환경별 분리 (dev/staging/prod)
- Workflow에 cost 알람 (LLM 노드 가격 합산)
- 정기 백업 (Postgres + Weaviate)
- Tailscale 외 노출 절대 금지
