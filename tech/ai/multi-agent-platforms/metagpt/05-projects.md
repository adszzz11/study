# Part 5. MetaGPT 실전

## 🟢 P1. Side Project MVP (★)

`metagpt "Twitter 클론 MVP. Next.js + Postgres + tRPC"`

20분 안에 PRD + 설계 + 코드 생성. 그대로 안 돌아가도 좋은 시작점.

## 🟢 P2. Data Interpreter로 분석 자동화 (★)

`metagpt "data/sales_2025.csv 의 카테고리별 분기 트렌드"`

Jupyter 없이도 차트 + 인사이트 보고서.

## 🟡 P3. 점진적 풀스택 앱 (★★)

```
1. MVP
2. 인증 추가
3. 결제 (Stripe)
4. 이메일 알림
5. 관리자 대시보드
```

각 단계마다 `--inc`로 누적. 한 달짜리 토이 프로젝트.

## 🟡 P4. Custom Role 추가 (★★)

기본 5개 Role에 **DevOps**, **Security Reviewer** 추가:
```python
class SecurityReviewer(Role):
    actions = [ScanCode, SuggestFixes]
    _watch = [WriteCode]
```

## 🔴 P5. MetaGPT를 Paperclip 직원으로 (★★★)

Paperclip이 "프로젝트 생성" 티켓을 MetaGPT 직원에게 위임:
```yaml
agent: project-bootstrapper
runtime: python
command: "metagpt '{ticket.description}'"
budget: $5
```

## ⚠️ Best Practices
- **invest 한도 항상**: $2-5 시작
- Docker 모드 권장 (`--use_docker`)
- 결과 코드는 항상 사람 검토 — 그대로 prod 금지
- 한국어 요구사항도 OK지만 영어가 안정적 결과
- 큰 프로젝트는 `--inc` 단계적으로
