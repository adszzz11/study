# Prefect Cloud vs Self-hosted

## 📌 핵심 개념

| 기능 | Prefect Cloud | Self-hosted Server |
|------|--------------|-------------------|
| 설치 | 없음 (SaaS) | `prefect server start` |
| 비용 | 유료 플랜 | 무료 |
| 인증 | 내장 | 직접 구현 |
| 자동화 | 전체 기능 | 일부 제한 |
| 지원 | 공식 지원 | 커뮤니티 |

---

## 💻 Self-hosted 서버 시작

```bash
# 1. Prefect 서버 시작
prefect server start

# 2. 다른 터미널에서 API URL 설정
prefect config set PREFECT_API_URL="http://localhost:4200/api"

# 3. Flow 실행 - 자동으로 서버에 기록됨
python my_flow.py
```

---

## 💻 Prefect Cloud 연결

```bash
# API 키 설정
prefect cloud login --key YOUR_API_KEY

# 또는 환경 변수
export PREFECT_API_KEY="YOUR_API_KEY"
export PREFECT_API_URL="https://api.prefect.cloud/api/accounts/..."
```

---

## 언제 무엇을 선택?

| 상황 | 추천 |
|------|------|
| 빠른 시작, 팀 협업 | **Prefect Cloud** |
| 데이터 주권, 비용 절감 | **Self-hosted** |
| 엔터프라이즈 보안 요구 | Prefect Cloud Enterprise |
| 개인 프로젝트/학습 | Self-hosted |

---

## ✅ 체크포인트

- [ ] 언제 Cloud vs Self-hosted를 선택해야 하는지 판단할 수 있는가?
- [ ] Self-hosted 서버를 시작하고 연결할 수 있는가?

---

## 🔗 더 알아보기

- [Prefect Cloud](https://docs.prefect.io/cloud/)
