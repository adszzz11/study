# Part 5. 본 vault에 적용하는 실전 시나리오

## 🎯 사용자 컨텍스트

본 vault는 이미:
- `study/tech/ai/` — 풍부한 자료
- `study/tech/ai/multi-agent-platforms/` — 오늘 81 파일 추가
- `study/tech/ai/openclaw-study/` — Hermes/OpenClaw 자료
- `study/tech/ai/autoresearch-study/` — Karpathy 자율 패턴

→ **이미 wiki에 가까움**. 다만 LLM-maintained 영역과 사람-maintained 영역이 섞여있음. 점진 분리 + LLM Wiki 패턴 적용이 자연스러움.

## 🟢 P1. 본 study/ 자료를 wiki/ 컴파운딩 (★)

### 목표
지금까지 만든 study/tech/ai/* 자료를 LLM이 읽고 **개념 페이지·엔티티 페이지·비교 페이지로 통합**.

### 단계
```
1. /wiki init (이미 완료)
2. CLAUDE.md에 LLM Wiki 섹션 추가
3. 첫 ingest:
   /wiki ingest study/tech/ai/multi-agent-platforms/README.md
   → 다음 페이지들이 자동 생성/갱신:
      • wiki/concepts/multi-agent-orchestration.md
      • wiki/comparisons/paperclip-vs-crewai-vs-langgraph.md
      • wiki/entities/karpathy.md (autoresearch 언급 갱신)
      • wiki/concepts/employee-pattern.md
4. /wiki ingest study/tech/ai/openclaw-study/01-overview.md
5. /wiki ingest study/tech/ai/llm-wiki-study/01-overview.md (재귀!)
6. /wiki lint
```

### 기대 효과
- "Hermes vs OpenClaw" 같은 cross-도메인 질문에 1초 답변
- 본 vault의 모든 자료가 자동 cross-ref
- 새 study 추가 시 자동 통합

## 🟡 P2. 매주 자동 LLM Wiki 점검 (★★)

### 시나리오
매주 일요일 23:00 → 자동 `/wiki lint` + 보고서 텔레그램 전송.

### 구현 (옵션 A: cron)
```bash
# crontab -e
0 23 * * 0 cd /Users/sm/code/leetangle/Note && \
  obsidian search-content "TODO|확인 필요" --vault leetangle --json > /tmp/lint.json && \
  curl -s -X POST "https://api.telegram.org/bot${TG_TOKEN}/sendMessage" \
    -d "chat_id=${TG_CHAT}" \
    -d "text=주간 wiki 점검: $(jq length /tmp/lint.json) 항목 미해결"
```

### 구현 (옵션 B: Hermes 직원으로)
Phase 2에서 Paperclip 들어오면 wiki-lint 직원 채용:
```yaml
agent: wiki-lint
runtime: bash
schedule: "0 23 * * 0"
command: "/wiki lint --format markdown"
on_completion:
  notify_agent: chief
  message: "주간 wiki 점검 결과: {result_summary}"
```

## 🟡 P3. 매번 새 자료 작성 시 자동 ingest (★★)

### 시나리오
새 study 자료를 작성하면 자동으로 wiki에 통합.

### Git hook으로 트리거
```bash
# .git/hooks/post-commit
#!/bin/bash
NEW_FILES=$(git diff --name-only HEAD HEAD~1 | grep '^study/' | grep -v '^study/wiki/')
for f in $NEW_FILES; do
  echo "[ingest] $f" >> /tmp/wiki-queue.log
done
```

별도 cron이 큐를 처리 → ingest 실행 → wiki 갱신.

## 🟡 P4. Obsidian Canvas로 본 vault 지도 (★★)

### 시나리오
JSON Canvas Skill로 본 vault의 **카테고리·관계 지도** 자동 생성.

```
/json-canvas create "본 vault AI 카테고리 지도"
  --include "study/tech/ai/**/README.md"
  --layout force-directed
```

결과: study/wiki/canvas/ai-vault-map.canvas
- 노드: 각 study 폴더
- 엣지: cross-ref
- 색상: 카테고리 (orchestration, framework, tool, ...)

매월 자동 갱신.

## 🔴 P5. Hermes + LLM Wiki 통합 (★★★)

### 시나리오
텔레그램 비서 Hermes가 본 vault를 **장기 기억**으로 사용.

```
사용자: "지난 주에 우리가 LangGraph vs Mastra 비교한 거 다시 알려줘"
   ↓
Hermes → obsidian-mcp-server → wiki/comparisons/ 검색
   ↓
관련 페이지 합성 → 답변
   ↓
대화 자체도 raw/conversations/2026-05-30.md 로 저장
   ↓
다음 /wiki ingest 사이클에 다시 통합 (recursive!)
```

### 핵심 가치
- 비서가 "어제 우리가 뭐 정리했더라"를 정확히 기억
- 새 대화가 영구적 wiki로 통합 (Letta보다 강력한 메모리)

## 🔴 P6. raw/ 자동 수집 파이프라인 (★★★★)

### 시나리오
관심 자료를 자동으로 raw/에 떨어뜨림.

```
입력 채널:
├─ Twitter 북마크 → cron → raw/twitter/YYYY-MM-DD.md
├─ Obsidian Web Clipper + defuddle → raw/web/...
├─ Telegram "북마크 봇" → raw/telegram/...
├─ Gmail 라벨 "save-to-wiki" → cron → raw/email/...
└─ YouTube 트랜스크립트 → yt-dlp → raw/youtube/...
        ↓
주기적 /wiki ingest --batch
        ↓
wiki/ 통합 + Telegram 알림
```

→ **외부 정보가 거의 자동으로 본인의 second brain에 흡수**.

## 🧭 Best Practices

### 시작은 작게
- 첫 주 1개 자료 ingest → 결과 확인
- wiki/ 페이지 품질 검토 → CLAUDE.md 조정
- 마음에 들면 점진 확장

### 운영 KPI
| 지표 | 목표 |
|------|------|
| 월 ingest 수 | 10-50 |
| wiki 페이지 수 | 페이스대로, 100-1000 |
| orphan 비율 | < 10% |
| contradiction 미해결 | 0 |
| ingest 비용 | 월 $5-20 |

### 안티패턴
- 한 번에 너무 많은 자료 ingest (비용 + 품질 모두 망함)
- wiki/와 기존 study/ 노트를 강제 통합 시도 (둘 다 망함)
- 영문 slug 강제 (한국어 vault에 부자연스러움)
- LLM에게 너무 자유로운 권한 (raw/ 침범)

## 🔗 다음

→ [cheatsheet.md](cheatsheet.md) 명령어 빠른 참조
