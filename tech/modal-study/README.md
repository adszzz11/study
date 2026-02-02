---
date: 2026-02-02
tags:
  - tech
  - series
  - modal
  - serverless
  - cloud
  - ai-ml
status: learning
type: tech-series
---

# Modal

> **한 줄 정의**: Python 코드를 클라우드에서 서버리스로 실행하는 AI/ML 특화 플랫폼

## 개요

Modal은 복잡한 인프라 설정 없이 Python 코드를 클라우드에서 바로 실행할 수 있게 해주는 서버리스 플랫폼입니다.
특히 AI/ML 워크로드에 최적화되어 있으며, GPU 접근이 매우 쉽습니다.

```mermaid
graph LR
    A[로컬 Python 코드] --> B[Modal 데코레이터]
    B --> C[클라우드 실행]
    C --> D[자동 스케일링]

    style A fill:#e1f5ff
    style D fill:#ffe1e1
```

### 핵심 특징

- **1초 만에 컨테이너 스핀업** - 빠른 cold start
- **Zero to Scale** - 사용하지 않으면 비용 0
- **GPU 지원** - T4부터 B200까지 다양한 GPU
- **No YAML** - 모든 설정이 Python 코드
- **매달 $30 무료 크레딧**

---

## Quick Start

```bash
# 1. 설치
pip install modal

# 2. 인증 설정
modal setup

# 3. 첫 번째 앱 실행
modal run hello.py
```

```python
# hello.py
import modal

app = modal.App("hello-modal")

@app.function()
def hello():
    return "Hello, Modal!"

@app.local_entrypoint()
def main():
    print(hello.remote())
```

---

## 학습 경로

### 1단계: 기초 이해 (30분)
- [ ] [[01-overview|개요]] 읽기 - 핵심 개념, 장단점
- [ ] [[02-ecosystem|생태계]] 파악 - 관련 기술, 비교

### 2단계: 환경 설정 (30분)
- [ ] [[04-learning/01-setup|설치 및 첫 배포]] - 개발 환경 구축

### 3단계: 핵심 기능 학습 (2시간)
- [ ] [[04-learning/02-functions|Function 정의]] - 데코레이터, 컨테이너 설정
- [ ] [[04-learning/03-gpu|GPU 사용하기]] - GPU 함수 작성
- [ ] [[04-learning/04-web-endpoints|웹 엔드포인트]] - API 만들기

### 4단계: 고급 기능 (1시간)
- [ ] [[04-learning/05-volumes|볼륨과 저장소]] - 데이터 영구 저장
- [ ] [[04-learning/06-scheduling|스케줄링]] - Cron 작업

### 5단계: 실전 적용
- [ ] [[05-projects|실전 프로젝트]] - Best Practices
- [ ] [[cheatsheet|치트시트]] - 빠른 참조

---

## 파일 구조

```
modal-study/
├── README.md              ← 여기 (개요 + 학습 로드맵)
├── 01-overview.md         ← 핵심 개념, 장단점, 사용 사례
├── 02-ecosystem.md        ← 관련 기술, 비교, 트렌드
├── 03-references.md       ← 공식 문서, 학습 자료
├── 04-learning/           ← 실습 가이드
│   ├── 01-setup.md        ← 설치 및 첫 배포
│   ├── 02-functions.md    ← Function 정의와 데코레이터
│   ├── 03-gpu.md          ← GPU 사용하기
│   ├── 04-web-endpoints.md← 웹 엔드포인트 만들기
│   ├── 05-volumes.md      ← 볼륨과 영구 저장소
│   └── 06-scheduling.md   ← 스케줄링과 Cron
├── 05-projects.md         ← 실전 프로젝트, Best Practices
└── cheatsheet.md          ← 빠른 참조
```

## 바로가기

| 단계 | 파일 | 설명 |
|------|------|------|
| 개요 | [[01-overview]] | 핵심 개념, 장단점, 사용 사례 |
| 생태계 | [[02-ecosystem]] | 관련 기술 비교, 트렌드 |
| 참고자료 | [[03-references]] | 공식 문서, 학습 자료 |
| 설치 | [[04-learning/01-setup]] | 개발 환경 설정 |
| 함수 | [[04-learning/02-functions]] | Function 데코레이터 |
| GPU | [[04-learning/03-gpu]] | GPU 활용 |
| 웹 | [[04-learning/04-web-endpoints]] | API 엔드포인트 |
| 저장소 | [[04-learning/05-volumes]] | Volume, 영구 저장 |
| 스케줄 | [[04-learning/06-scheduling]] | Cron 작업 |
| 프로젝트 | [[05-projects]] | 실전 예제 |
| 치트시트 | [[cheatsheet]] | 빠른 참조 |

---

## 관련 노트

- [[serverless]]
- [[aws-lambda]]
- [[kubernetes]]
- [[docker]]

---

**생성일**: 2026-02-02
**상태**: 학습 중
