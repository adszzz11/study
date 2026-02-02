---
date: 2026-02-02
tags:
  - tech
  - modal
  - references
parent: "[[README]]"
---

# Modal - 참고자료

> [[02-ecosystem|이전: 생태계]] | [[README|목차]] | [[04-learning/01-setup|다음: 설치 가이드]]

---

## 1. 공식 문서

### 필수 문서

| 문서 | URL | 설명 |
|------|-----|------|
| 공식 사이트 | [modal.com](https://modal.com) | 메인 페이지, 가격 정보 |
| 공식 문서 | [modal.com/docs](https://modal.com/docs) | 전체 가이드 |
| API Reference | [modal.com/docs/reference](https://modal.com/docs/reference) | 상세 API 문서 |
| Examples | [modal.com/docs/examples](https://modal.com/docs/examples) | 공식 예제 |

### 핵심 가이드

| 주제 | URL | 설명 |
|------|-----|------|
| Getting Started | [modal.com/docs/guide](https://modal.com/docs/guide) | 시작하기 |
| Functions | [modal.com/docs/guide/functions](https://modal.com/docs/guide/functions) | 함수 정의 |
| GPU | [modal.com/docs/guide/gpu](https://modal.com/docs/guide/gpu) | GPU 사용 |
| Web Endpoints | [modal.com/docs/guide/webhooks](https://modal.com/docs/guide/webhooks) | 웹 API |
| Volumes | [modal.com/docs/guide/volumes](https://modal.com/docs/guide/volumes) | 저장소 |
| Scheduling | [modal.com/docs/guide/cron](https://modal.com/docs/guide/cron) | Cron 작업 |

---

## 2. GitHub 저장소

### 공식 저장소

```
github.com/modal-labs/
├── modal-client      # Python 클라이언트 (pip install modal)
├── modal-examples    # 공식 예제 모음
└── modal-docs        # 문서 소스
```

### 유용한 예제

| 예제 | 링크 | 설명 |
|------|------|------|
| LLM 서빙 | [vLLM 예제](https://github.com/modal-labs/modal-examples/tree/main/06_gpu_and_ml/llm-serving) | vLLM으로 LLM 서빙 |
| Stable Diffusion | [SD 예제](https://github.com/modal-labs/modal-examples/tree/main/06_gpu_and_ml/stable_diffusion) | 이미지 생성 |
| 파인튜닝 | [Fine-tuning](https://github.com/modal-labs/modal-examples/tree/main/06_gpu_and_ml/finetuning) | 모델 학습 |
| 웹 스크래핑 | [Playwright](https://github.com/modal-labs/modal-examples/tree/main/10_integrations/playwright) | 브라우저 자동화 |

---

## 3. 튜토리얼 및 블로그

### Modal 공식 블로그

- [modal.com/blog](https://modal.com/blog)
  - 새 기능 발표
  - 사용 사례 소개
  - 기술 심층 분석

### 추천 글

| 제목 | 링크 | 내용 |
|------|------|------|
| Intro to Modal | 공식 문서 | 기본 개념 소개 |
| Running LLMs | 공식 블로그 | LLM 서빙 가이드 |
| GPU Computing | 공식 블로그 | GPU 활용법 |

---

## 4. 영상 자료

### YouTube

| 채널/영상 | 내용 |
|----------|------|
| Modal 공식 채널 | 튜토리얼, 데모 |
| 컨퍼런스 발표 | PyCon, MLOps 컨퍼런스 등 |

### 추천 영상

- Modal 시작하기 튜토리얼
- LLM 서빙 워크숍
- GPU 컴퓨팅 심층 분석

---

## 5. 커뮤니티

### 공식 커뮤니티

| 플랫폼 | 링크 | 용도 |
|--------|------|------|
| Discord | [discord.gg/modal](https://discord.gg/modal) | 질문, 토론 |
| Twitter/X | [@modal_labs](https://twitter.com/modal_labs) | 업데이트, 소식 |
| GitHub Issues | modal-client repo | 버그 리포트 |

### 활용 팁

- Discord에서 #help 채널 활용
- GitHub Issues에서 유사 문제 검색
- 공식 예제 먼저 참고

---

## 6. 학습 로드맵

### 입문자 (1주)

```
Day 1: 설치 및 첫 실행
├── modal setup
├── Hello World 실행
└── 기본 개념 이해

Day 2-3: 함수와 이미지
├── @app.function 이해
├── 커스텀 이미지 만들기
└── 의존성 설치

Day 4-5: GPU와 웹
├── GPU 함수 작성
├── 웹 엔드포인트 만들기
└── FastAPI 통합

Day 6-7: 실전 프로젝트
├── 간단한 API 만들기
├── 배포 및 테스트
└── 문서 정리
```

### 중급자 (2주)

```
Week 1: 심화 기능
├── Volume 사용
├── Secret 관리
├── Cron 스케줄링
└── 병렬 처리 (map)

Week 2: 실전 적용
├── LLM 서빙
├── 모델 학습
├── 프로덕션 배포
└── 모니터링
```

---

## 7. 빠른 참조 링크

### 자주 찾는 문서

```
# 설치
https://modal.com/docs/guide/install

# 함수 정의
https://modal.com/docs/guide/functions

# GPU 사용
https://modal.com/docs/guide/gpu

# 이미지 설정
https://modal.com/docs/guide/custom-container

# 웹 엔드포인트
https://modal.com/docs/guide/webhooks

# Volume
https://modal.com/docs/guide/volumes

# Secret
https://modal.com/docs/guide/secrets

# 가격
https://modal.com/pricing
```

---

## 다음 단계

> [!tip] 다음으로
> 참고자료를 확인했다면 [[04-learning/01-setup|실습을 시작]]하세요!

---

## References

- [Modal 공식 문서](https://modal.com/docs)
- [Modal GitHub](https://github.com/modal-labs)
- [Modal Discord](https://discord.gg/modal)
