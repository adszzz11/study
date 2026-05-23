# Part 5. 실전 프로젝트 5종

> 셋업이 끝났다면, 진짜 "쓸모"를 만들어볼 차례. 난이도 🟢→🔴 순으로 정리.

## 🟢 P1. 매일 아침 일일 브리핑 봇 (난이도 ★)

**목표**: 매일 오전 7시, 텔레그램으로 날씨/뉴스/캘린더/이메일 요약을 받는다.

### 구성

```yaml
# config.yaml
agents:
  briefing:
    model: claude-sonnet-4-6  # 요약 정도엔 충분
    tools: [browser, calendar_read, gmail_read]
    skills: [news_aggregator]

cron:
  - id: morning-briefing
    schedule: "0 7 * * *"   # 매일 7시
    agent: briefing
    channel: telegram
    prompt: |
      오늘의 브리핑을 만들어줘:
      1) 서울 날씨 (현재·최고·최저, 비 예보)
      2) 오늘 캘린더 일정
      3) 새 이메일 중요한 것 3건 요약
      4) 한국·해외 헤드라인 5건
```

### 구현 단계

1. `gmail_read`, `calendar_read` 도구를 OAuth 연결
2. `news_aggregator` skill 설치 (또는 직접 RSS 도구로 대체)
3. cron 추가 후 `docker compose restart`
4. 다음날 아침 텔레그램 확인

### 발전 방향

- 휴일/주말 다른 브리핑 (운동 추천, 영화 등)
- 일정이 빡빡한 날엔 자동으로 "오늘 빡빡함" 알림 톤 강화

## 🟢 P2. 노션/Obsidian 노트 검색 봇 (난이도 ★★)

**목표**: 텔레그램에서 "지난주 회의록 뭐 있었지?" → 본 vault에서 검색해 답함.

### 구성

```yaml
agents:
  notes:
    model: ollama/qwen2.5:14b   # 로컬 우선 (프라이버시)
    tools: [files_read, vector_search]
    workspace: /Users/sm/code/leetangle/Note  # vault 마운트
```

### 구현 단계

1. docker-compose에 vault 마운트: `- ~/code/leetangle/Note:/workspace/vault:ro`
2. 임베딩 도구 추가: `ollama pull mxbai-embed-large`
3. 벡터 인덱스 빌드 (OpenClaw의 vector_search skill 또는 Khoj 연동)
4. 텔레그램 봇에 `/note <query>` 명령 추가

### 흔한 실수

- vault를 `rw`로 마운트하지 말 것 (LLM이 노트 변형 위험)
- 인덱스 빌드는 cron으로 일 1회 (실시간 안 해도 충분)

### 발전 방향

- 노트 작성 모드: "오늘 회의 정리해줘" → 새 노트 초안 (단, write는 confirmation 필수)
- Letta 연결: 사용자가 어떤 주제를 자주 묻는지 학습

## 🟡 P3. GitHub 알림 다이제스트 봇 (난이도 ★★)

**목표**: 매 4시간마다 GitHub 알림 중 중요한 것만 슬랙으로 요약 발송.

### 구성

```yaml
agents:
  gh-digest:
    model: claude-haiku-4-5     # 빠르고 저렴
    tools: [github_api, http_get]
    skills: [github_notifications]

channels:
  slack-personal:
    enabled: true
    agent: gh-digest

cron:
  - schedule: "0 */4 * * *"
    agent: gh-digest
    channel: slack-personal
    prompt: |
      최근 4시간 GitHub 알림 점검:
      - 내가 멘션된 PR/이슈
      - 내가 리뷰어로 지정된 PR
      - 내가 만든 PR의 새 코멘트
      각각 1줄 요약 + 링크. 무관한 알림 무시.
```

### 발전 방향

- 긴급도 자동 분류 (`status: blocked` 라벨이면 빨간색 이모지)
- 야간엔 알림 끄기

## 🟡 P4. 가족용 홈 모니터링 봇 (난이도 ★★★)

**목표**: 집의 도어센서/온도/카메라 상태를 가족 텔레그램 그룹에 보고.

### 구성

```yaml
agents:
  home:
    model: ollama/llama3.2:8b   # 로컬 강제 (집안 데이터)
    tools: [http_get, mqtt_subscribe]
    skills: [home_assistant_bridge]
```

### 구현 단계

1. Home Assistant 또는 Homebridge 인스턴스 동작 중 가정
2. OpenClaw에 HA REST API 도구 등록 (Long-Lived Access Token)
3. 가족 텔레그램 그룹에 봇 초대 + 페어링
4. 이벤트 후크: 외출 모드일 때 도어 열림 → 자동 알림

### 보안 고려

- 카메라 영상은 절대 클라우드 LLM에 보내지 말 것 (Ollama만)
- 가족 봇 권한은 `read-only` (자동으로 잠금/장치 제어 X — 사용자 확인 필요)

## 🔴 P5. 멀티 에이전트 연구 어시스턴트 (난이도 ★★★★)

**목표**: "최근 LangChain vs Mastra 비교 정리해줘" 한 마디로 리서치 → 마크다운 결과물 산출.

### 구성

```yaml
agents:
  research-coordinator:
    model: claude-opus-4-7
    tools: [agent_delegate]    # 다른 에이전트 호출
    subagents: [scraper, summarizer, writer]

  scraper:
    model: claude-haiku-4-5
    tools: [browser, http_get]
    workspace: /workspace/research

  summarizer:
    model: ollama/qwen2.5:14b
    tools: [files_read]

  writer:
    model: claude-opus-4-7
    tools: [files_write]
    workspace: /workspace/research/output
```

### 워크플로우

1. 사용자 텔레그램: `/research LangChain vs Mastra`
2. coordinator → scraper에게 "관련 공식 문서/블로그 10건 가져와"
3. scraper가 파일로 저장 → summarizer가 각 1단락 요약
4. writer가 비교표 + 결론 작성 → 마크다운 파일로 저장
5. coordinator가 텔레그램에 결과 URL/요약 전송

### 발전 방향

- 본 vault 자동 추가: 결과물을 `study/tech/ai/comparisons/` 디렉터리에 자동 작성
- 인간 in-the-loop: writer 결과를 사용자 확인 후 vault에 commit

## 🧭 Best Practices 체크리스트

프로젝트 시작 전 점검:

- [ ] 에이전트가 처리할 데이터의 **민감도**는? → 로컬/클라우드 모델 결정
- [ ] 외부 통신(이메일·메시지) 권한이 필요한가? → confirmation 또는 dry-run 모드
- [ ] 비용 한도는? → API 사용량 알람 미리
- [ ] **재현 가능성**: config.yaml과 docker-compose.yml은 git 관리 (`.env`만 제외)
- [ ] **롤백 계획**: `docker compose down && git checkout HEAD~1 && docker compose up -d`
- [ ] **로그**: 30일치 보관 + 시크릿 마스킹
- [ ] **테스트 채널**: 가족 그룹·운영 채널 건드리기 전에 별도 채널에서 동작 확인

## 📈 KPI 예시

OpenClaw를 잘 쓰고 있는지 측정하는 지표:

| 지표 | 목표 |
|------|------|
| 응답 시간 (TTFT) | < 3초 |
| 일 메시지 수 | 사용 빈도 측정 |
| 에이전트 실패율 | < 5% |
| 월 LLM 비용 | 본인 한도 내 |
| 보안 패치 적용 | 권고 후 7일 내 |
| 메모리/CPU peak | RAM 80% 미만 |

## 🔗 다음

→ [cheatsheet.md](cheatsheet.md) 자주 쓰는 명령어 빠른 참조
