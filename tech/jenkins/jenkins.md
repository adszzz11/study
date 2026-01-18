---
date: 2025-01-18
tags:
  - tech
  - tool
  - devops
  - ci-cd
status: evaluating
type: tech-tool
---

# Jenkins

## 1. Overview

> **한 줄 소개**: 오픈소스 자동화 서버로, 1,800+ 플러그인을 통해 빌드, 테스트, 배포를 자동화하는 CI/CD 도구

| 항목 | 내용 |
|------|------|
| 공식 사이트 | https://www.jenkins.io |
| GitHub | https://github.com/jenkinsci/jenkins |
| 라이선스 | MIT License (오픈소스) |
| 최신 버전 | 2.x LTS |
| 사용 언어 | Java |

---

## 2. 도입 검토

### 해결하려는 문제

- 수동 빌드/배포로 인한 휴먼 에러
- 반복적인 테스트 실행 자동화
- 배포 파이프라인 표준화

### 도입 목적

- 코드 변경 시 자동 빌드 및 테스트
- 배포 프로세스 자동화 (Dev → Staging → Prod)
- 품질 게이트 (테스트 실패 시 배포 중단)

### 예상 효과

- 배포 시간 단축 (수동 30분 → 자동 5분)
- 휴먼 에러 감소
- 개발팀 생산성 향상

---

## 3. 핵심 기능

### 주요 기능

| 기능 | 설명 | 중요도 |
|------|------|--------|
| **Pipeline as Code** | Jenkinsfile로 파이프라인 정의 | ⭐⭐⭐ |
| **Plugin Ecosystem** | 1,800+ 플러그인 지원 | ⭐⭐⭐ |
| **Distributed Builds** | Master-Agent 분산 빌드 | ⭐⭐⭐ |
| **Blue Ocean UI** | 모던 파이프라인 시각화 | ⭐⭐ |
| **Credentials 관리** | 시크릿 안전 저장 | ⭐⭐ |

### 아키텍처

```
┌─────────────────────────────────────────────┐
│                 Jenkins Master              │
│  ┌─────────┐ ┌─────────┐ ┌─────────────┐   │
│  │  Job    │ │ Plugin  │ │ Credentials │   │
│  │ Config  │ │ Manager │ │   Store     │   │
│  └─────────┘ └─────────┘ └─────────────┘   │
└──────────────────┬──────────────────────────┘
                   │
       ┌───────────┼───────────┐
       ▼           ▼           ▼
  ┌─────────┐ ┌─────────┐ ┌─────────┐
  │ Agent 1 │ │ Agent 2 │ │ Agent 3 │
  │ (Linux) │ │(Windows)│ │ (Docker)│
  └─────────┘ └─────────┘ └─────────┘
```

---

## 4. 비교 분석

### vs 대안 도구

| 비교 항목 | Jenkins | GitHub Actions | GitLab CI |
|-----------|---------|----------------|-----------|
| **호스팅** | Self-hosted | Cloud (SaaS) | Cloud/Self-hosted |
| **설정 복잡도** | 높음 | 낮음 | 중간 |
| **플러그인** | 1,800+ | Marketplace | 내장 기능 |
| **러닝커브** | 높음 | 낮음 | 중간 |
| **비용** | 인프라 비용만 | 무료 + 사용량 | 무료 + 사용량 |
| **보안 스캔** | 플러그인 | 기본 제공 | 기본 제공 |
| **적합 규모** | 대기업/레거시 | 소규모~중규모 | 중규모~대규모 |

### 장단점 정리

**장점**
- ✅ 완전한 커스터마이징 가능
- ✅ 온프레미스/에어갭 환경 지원
- ✅ 레거시 시스템 통합 용이
- ✅ 무료 (인프라 비용 외)

**단점**
- ❌ 유지보수 부담 (직접 운영)
- ❌ 플러그인 호환성 이슈
- ❌ UI가 구식
- ❌ 초기 설정 복잡

### 선택 가이드

```
GitHub 사용 중?
├── Yes → 규모가 작고 빠른 설정 원함?
│         ├── Yes → GitHub Actions
│         └── No  → Jenkins (복잡한 워크플로우)
└── No  → GitLab 사용 중?
          ├── Yes → GitLab CI
          └── No  → Jenkins (범용)
```

---

## 5. Quick Start

### 설치 (Docker)

```bash
# Jenkins 이미지 다운로드
docker pull jenkins/jenkins:lts

# Jenkins 컨테이너 실행
docker run -d \
  -p 8080:8080 \
  -p 50000:50000 \
  -v jenkins_home:/var/jenkins_home \
  --name jenkins \
  jenkins/jenkins:lts

# 초기 비밀번호 확인
docker logs jenkins
```

### 기본 설정

1. `http://localhost:8080` 접속
2. 초기 비밀번호 입력 (logs에서 확인)
3. "Install suggested plugins" 선택
4. Admin 계정 생성

### Hello World Pipeline

```groovy
// Jenkinsfile
pipeline {
    agent any

    stages {
        stage('Hello') {
            steps {
                echo 'Hello, World!'
            }
        }

        stage('Build') {
            steps {
                sh 'echo "Building..."'
            }
        }

        stage('Test') {
            steps {
                sh 'echo "Testing..."'
            }
        }
    }

    post {
        success {
            echo 'Pipeline succeeded!'
        }
        failure {
            echo 'Pipeline failed!'
        }
    }
}
```

---

## 6. 실무 적용 가이드

### 프로젝트 구조

```
project/
├── Jenkinsfile           # 파이프라인 정의
├── src/
├── build.gradle
└── Dockerfile
```

### 실전 Pipeline 예시

```groovy
pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'myapp'
        DOCKER_TAG = "${env.BUILD_NUMBER}"
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/user/repo.git',
                    credentialsId: 'github-token'
            }
        }

        stage('Build') {
            steps {
                sh 'chmod +x ./gradlew'
                sh './gradlew build -x test'
            }
        }

        stage('Test') {
            steps {
                sh './gradlew test'
            }
            post {
                always {
                    junit '**/build/test-results/test/*.xml'
                }
            }
        }

        stage('Docker Build') {
            steps {
                sh "docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} ."
            }
        }

        stage('Deploy') {
            when {
                branch 'main'
            }
            steps {
                sh "docker stop ${DOCKER_IMAGE} || true"
                sh "docker rm ${DOCKER_IMAGE} || true"
                sh "docker run -d -p 8080:8080 --name ${DOCKER_IMAGE} ${DOCKER_IMAGE}:${DOCKER_TAG}"
            }
        }
    }
}
```

### 트러블슈팅

| 문제 | 원인 | 해결 |
|------|------|------|
| Permission denied | gradlew 실행 권한 | `chmod +x ./gradlew` |
| Plugin 충돌 | 버전 불일치 | 플러그인 업데이트/다운그레이드 |
| Agent 연결 실패 | 네트워크/방화벽 | 포트 50000 오픈 확인 |
| 메모리 부족 | 힙 설정 부족 | `JAVA_OPTS=-Xmx2g` |

---

## 7. 도입 체크리스트

### 기술 검토

- [x] 공식 문서 읽기
- [x] 로컬 환경에서 Docker로 테스트
- [ ] 기존 시스템과 호환성 확인
- [ ] 필요한 플러그인 목록 정리

### 도입 결정

- [ ] 팀 내 공유 및 논의
- [ ] PoC 프로젝트 진행
- [ ] GitHub Actions와 비교 검토
- [ ] 도입 여부 결정

### 도입 후

- [ ] 팀 가이드 문서 작성
- [ ] Jenkinsfile 템플릿 제작
- [ ] 모니터링 설정 (Prometheus + Grafana)

---

## 8. References

- [Jenkins 공식 문서](https://www.jenkins.io/doc/)
- [Jenkins vs GitHub Actions Comparison](https://northflank.com/blog/github-actions-vs-jenkins)
- [CI/CD Platform Guide](https://sanj.dev/post/github-actions-gitlab-ci-jenkins-comparison-2025)
- [Why Jenkins Still Relevant in 2024](https://community.lambdatest.com/t/why-is-jenkins-still-relevant-in-2024-over-github-actions-and-gitlab-ci-cd/36853)
- 관련 노트: [[Docker]], [[GitHub-Actions]], [[CI-CD]]

---

## 9. 학습 로그

### 2022-11-01

- Docker로 Jenkins 설치 완료
- GitHub Webhook 연동 (ngrok 사용)
- 기본 Pipeline 작성 및 테스트
- JUnit 테스트 결과 연동

### 2025-01-18

- 템플릿 기반으로 노트 재구성
- GitHub Actions, GitLab CI 비교 추가
- 선택 가이드 의사결정 트리 추가
