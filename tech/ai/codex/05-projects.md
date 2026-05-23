---
date: 2026-05-20
tags:
  - tech
  - Codex
  - projects
parent: "[[README]]"
---

# Codex - 실전 프로젝트

> [[README|목차로 돌아가기]]

---

## 1. 프로젝트 아이디어

| 프로젝트 | 난이도 | 학습 포인트 |
|----------|--------|------------|
| AGENTS.md 셋업 | ⭐ | 스택형 컨텍스트, 컨벤션 코드화 |
| `codex exec`로 CI 자동 lint 수정 | ⭐⭐ | 비대화형 실행, GitHub Actions 통합 |
| 자체 Skill 작성 (릴리스 노트) | ⭐⭐ | SKILL.md 구조, 입력/출력 명세 |
| MCP 서버 연결 (Linear/Sentry) | ⭐⭐⭐ | MCP 표준, 인증, 외부 시스템 |
| `codex remote-control` 멀티 에이전트 | ⭐⭐⭐ | v0.130 헤드리스, cmux 결합 |
| GitHub Cloud PR 자동 리뷰 | ⭐⭐⭐ | code_review.md, 팀 표준화 |
| AGENTS.md + Skill + MCP 풀세트 | ⭐⭐⭐⭐ | 신입 온보딩 1시간 → 5분 |

---

## 2. Best Practices

### Codex를 "팀원처럼" 다뤄라

> "Codex works best when you treat it less like a one-off assistant and more like a teammate you configure and improve over time."
> — OpenAI 공식

- 매번 새 컨텍스트 주지 말고 **AGENTS.md / Skills**에 영구화
- 반복 교정은 즉시 Skill로 승격
- 환경 설정(작업 디렉토리, 권한, 모델)을 초기에 제대로

### AGENTS.md 작성 패턴

```markdown
# AGENTS.md

## 빌드 & 테스트
- 셋업: pnpm install
- 테스트: pnpm test
- 린트: pnpm lint:fix

## 컨벤션
- TypeScript strict
- 모든 PR은 changeset 포함
- 한국어 커밋 메시지 (gitmoji 포함)

## 아키텍처
- src/api: HTTP 핸들러
- src/core: 도메인
- src/infra: DB/외부 어댑터

## 제약
- src/legacy/는 수정 금지 (마이그레이션 중)
- secrets는 환경변수만, 코드 하드코딩 금지

## 검증
- 변경 후 항상 pnpm test 실행
- 빌드 통과 후에만 커밋
```

### Skills로 반복 워크플로우 패키징

좋은 Skill 후보:
- 로그 트리아지
- 릴리스 노트 생성
- PR 리뷰 체크리스트
- 디버깅 플레이북
- 마이그레이션 시나리오

원칙:
- 하나의 잡(job)에만 집중
- 입력/출력 명시
- 5문단 이상이면 분리

### MCP는 "수동 루프"가 있을 때만

> "Add tools only when they unlock a real workflow."

먼저 1-2개로 시작:
- 자주 ssh로 prod log 보기? → SSH/Tail MCP
- Linear 이슈 자주 옮김? → Linear MCP

도구 많이 깐다고 능력 늘지 않음 — 컨텍스트만 늘어남.

### 권한 점진 완화

- 처음엔 `approval = untrusted` + `sandbox = read-only`
- 신뢰가 쌓이고 워크플로우가 명확해지면 단계적 완화
- **신뢰 못 하는 저장소에서는 절대 완화 금지**

---

## 3. 실무 적용 시 고려사항

### 성능

- 기본 reasoning은 Medium 유지, 어려울 때만 High
- `/compact`로 긴 세션 압축
- MCP는 정말 필요한 1-2개만
- 모델 캐시 활용 (반복 패턴은 캐시 히트율↑)

### 보안

- secrets는 절대 AGENTS.md에 하드코딩 금지
- `approval = trusted`는 신뢰 저장소만
- `sandbox = danger-full-access`는 거의 쓰지 말 것
- MCP 인증은 환경변수 (`auth_token_env`) 사용
- 회사 정책 위반 가능한 명령은 Hook으로 차단

### 모니터링

- `codex exec --json` 출력 로깅
- CI에서 Codex 토큰 사용량 추적 (예산 알람)
- 자동 PR 리뷰 결과 별도 라벨로 표시
- 회귀 발생 시 즉시 이전 버전으로 롤백 (`@0.129.0` 등)

---

## 4. 실전 워크플로우 예시

### Workflow 1: CI/CD 자동 수정

`.github/workflows/codex-fix.yml`:
```yaml
name: Codex Auto-fix
on:
  pull_request:
    types: [labeled]

jobs:
  fix:
    if: github.event.label.name == 'codex-fix'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm install -g @openai/codex@0.130.0
      - name: Auto-fix
        run: |
          codex exec --effort high \
            "Fix all lint errors in src/. Don't break tests. Commit changes."
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
      - run: git push
```

### Workflow 2: 멀티 에이전트 (v0.130 remote-control)

```bash
# Terminal A: 오케스트레이터
codex remote-control --port 8080

# Terminal B: 워커 발사
curl -X POST localhost:8080/sessions \
  -d '{"prompt": "Refactor src/auth/"}'
```

cmux와 결합:
```bash
cmux new-workspace --name "Codex: refactor" --cwd /repo
cmux send --workspace workspace:N 'codex exec "..."'
```

### Workflow 3: 사내 MCP 통합

```toml
# ~/.codex/config.toml
[mcp_servers.internal-billing]
url = "https://mcp.internal/billing"
auth_token_env = "BILLING_TOKEN"
```

```markdown
# AGENTS.md
## Internal Tools
- billing MCP: 청구 데이터 조회 (read-only)
- 예: "지난주 매출 추세 보고서 만들어줘"
```

### Workflow 4: PR 리뷰 표준화

`.codex/code-review.md`:
```markdown
# Code Review Standards
## 필수
- [ ] 테스트 추가
- [ ] CHANGELOG 업데이트
- [ ] 마이그레이션 시 다운 스크립트
- [ ] 외부 API 변경 시 OpenAPI 갱신

## 거부 조건
- 미사용 import 남김
- console.log 남김
- TODO 주석에 담당자/이슈 미기재
```

### Workflow 5: 신입 온보딩

```bash
codex exec --effort high \
  "Read AGENTS.md and CONTRIBUTING.md. Set up local dev environment. \
   Run all tests. Report any failures with possible causes."
```

AGENTS.md만 잘 작성해두면 셋업이 1시간 → 5분.

---

## 5. 프로젝트 구조 예시

```
my-project/
├── AGENTS.md                       ← 저장소 표준 컨텍스트
├── .codex/
│   ├── config.toml                 ← 저장소 설정
│   └── code-review.md              ← PR 리뷰 가이드
├── .agents/skills/                 ← 팀 공유 스킬
│   ├── release-notes/SKILL.md
│   └── debug-flow/SKILL.md
├── src/
│   ├── api/
│   ├── core/
│   ├── infra/
│   └── legacy/                     ← AGENTS.md에서 수정 금지 명시
└── .github/workflows/
    └── codex-fix.yml               ← CI 자동 수정
```

---

## 6. 함정 / 안티패턴

| 안티패턴 | 문제 | 대안 |
|---------|------|------|
| AGENTS.md를 너무 짧게 | 매번 같은 컨텍스트 반복 입력 | 빌드/테스트/컨벤션/제약 명시 |
| 모든 도구 MCP에 등록 | 컨텍스트 폭주, 속도↓ | 자주 쓰는 1-2개만 |
| `approval = trusted` 즉시 | 사고 위험 | `on-failure`로 시작 |
| 매번 Extra High effort | 응답 느림, 토큰 폭증 | 기본 Medium, 어려울 때만 High |
| Skill 없이 반복 프롬프트 | 일관성↓ | 3번 이상 반복하면 Skill화 |
| 1M 컨텍스트 갈망 | Codex 미지원 | 대형 컨텍스트는 Claude Opus 4.7 |
| 회귀 즉시 적용 | 사고 위험 | 1-2 패치 지난 안정 버전 사용 |

---

## 관련 노트

- [[README]]
- [[01-overview]]
- [[02-ecosystem]]
- [[cheatsheet]]
- [[../claude/13-2026-05-latest]]
