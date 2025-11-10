# GitHub Actions 기반 CI/CD 도입 시 기존 Jenkins와 비교했을 때 얻은 이점은?

## 답변

기존에 Jenkins를 사용하면서 겪었던 가장 큰 문제는 **Jenkins 서버 자체의 관리 부담**이었습니다. 플러그인 업데이트, 보안 패치, 디스크 공간 관리, 빌드 큐 최적화 등 인프라 유지보수에 많은 시간을 소비했습니다. 또한 Groovy 기반의 Jenkinsfile은 복잡하고 디버깅이 어려워 파이프라인 수정 시마다 시행착오가 많았습니다.

GitHub Actions로 전환하면서 얻은 가장 큰 이점은 **관리형 서비스의 이점**과 **Git 워크플로우와의 완벽한 통합**입니다. 서버 관리가 전혀 필요 없고, YAML 기반의 워크플로우는 가독성이 높아 팀 내 누구나 쉽게 수정할 수 있었습니다. PR 생성 시 자동으로 CI가 실행되고, 코드 리뷰와 함께 테스트 결과를 확인할 수 있어 개발 속도가 크게 향상되었습니다.

특히 금융 시스템 개발 환경에서는 **보안과 감사 추적**이 중요한데, GitHub Actions는 모든 워크플로우 실행 이력이 Git 이벤트와 함께 자동으로 기록되어 컴플라이언스 요구사항을 충족하기 쉬웠습니다.

## 핵심 키워드

- GitHub Actions
- Jenkins
- CI/CD
- 워크플로우 자동화
- 유지보수성

## 비교 분석

| 항목 | Jenkins | GitHub Actions |
|------|---------|----------------|
| **설치/관리** | 자체 호스팅 필요, 서버 관리 부담 | 관리형 서비스, 인프라 관리 불필요 |
| **설정 복잡도** | Groovy Jenkinsfile, UI 설정 혼재 | YAML 워크플로우, 선언적이고 간결 |
| **비용** | 서버 운영 비용 (EC2, 스토리지), 무료 | 월 2,000분 무료, 초과 시 분당 과금 |
| **생태계** | 1,800+ 플러그인 (의존성 지옥 가능) | GitHub Marketplace 액션 (버전 관리 명확) |
| **러닝커브** | 높음 (Groovy, 플러그인 학습 필요) | 낮음 (YAML, GitHub 사용자 친숙) |
| **병렬 빌드** | Executor 수에 제한, 스케일링 복잡 | Matrix 빌드로 간편한 병렬 실행 |
| **보안** | 직접 관리 (취약점 패치, 인증 설정) | GitHub 팀이 관리, OIDC 토큰 지원 |
| **피드백 속도** | 빌드 큐 대기 가능 | 즉시 실행 (GitHub 호스팅 러너) |
| **Git 통합** | 수동 Webhook 설정 필요 | 네이티브 통합 (PR, Issue, Release 등) |
| **디버깅** | 로그 확인 어려움, 재현 복잡 | Act CLI로 로컬 테스트 가능 |
| **이식성** | Jenkins 서버 종속 | 리포지토리에 포함, 버전 관리 가능 |

## GitHub Actions의 장점

### 1. 관리 오버헤드 감소

#### Before (Jenkins)
- **서버 관리**: EC2 인스턴스 모니터링, 디스크 용량 관리, Java/Groovy 버전 관리
- **플러그인 관리**: 1,800개 이상의 플러그인 중 필요한 것 찾고, 의존성 충돌 해결, 정기 업데이트
- **백업 및 복구**: Jenkins 홈 디렉토리 백업, 설정 손실 시 복구 절차 필요
- **보안 패치**: CVE 발표 시 긴급 업데이트 및 재시작 (서비스 중단)
- **비용**: EC2 t3.large (월 $60) + EBS 100GB (월 $10) = **월 $70**

#### After (GitHub Actions)
- **서버 관리 불필요**: GitHub이 인프라 관리, 자동 스케일링
- **워크플로우 파일 관리**: Git으로 버전 관리되어 롤백 간편
- **보안**: GitHub 팀이 패치 관리, OIDC를 통한 비밀번호 없는 인증
- **비용**: 월 2,000분 무료 (우리 팀 사용량 기준 월 $0 ~ $20) = **월 $20 절감**

### 2. Git 워크플로우 통합

#### PR 자동화
```yaml
# .github/workflows/pr-checks.yml
name: PR Checks

on:
  pull_request:
    branches: [main, develop]
    types: [opened, synchronize, reopened]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up JDK 17
        uses: actions/setup-java@v4
        with:
          distribution: 'temurin'
          java-version: '17'
          cache: 'gradle'

      - name: Run tests
        run: ./gradlew test

      - name: Publish Test Results
        if: always()
        uses: EnricoMi/publish-unit-test-result-action@v2
        with:
          files: build/test-results/**/*.xml

      - name: Comment PR with Coverage
        uses: madrapps/jacoco-report@v1.6
        with:
          paths: build/reports/jacoco/test/jacocoTestReport.xml
          token: ${{ secrets.GITHUB_TOKEN }}
          min-coverage-overall: 80
```

**효과**:
- PR 열면 자동으로 테스트 실행
- PR 댓글로 테스트 결과 및 커버리지 피드백 (Jenkins는 별도 확인 필요)
- 커버리지 80% 미만 시 PR 머지 차단

#### 코드 리뷰 시 CI 결과 즉시 확인
Jenkins에서는 빌드 결과 확인을 위해 별도 Jenkins 페이지 접속 필요 → GitHub Actions는 PR 페이지 내에서 모든 체크 상태 확인 가능

### 3. 빠른 피드백

#### Matrix 빌드로 다중 환경 테스트
```yaml
# .github/workflows/matrix-build.yml
name: Multi-Platform Build

on: [push, pull_request]

jobs:
  build:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
        java: ['11', '17', '21']
        exclude:
          - os: macos-latest
            java: '11'  # M1 Mac에서 Java 11 제외
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-java@v4
        with:
          distribution: 'temurin'
          java-version: ${{ matrix.java }}
      - run: ./gradlew build
```

**효과**: 3개 OS × 3개 Java 버전 = 9개 조합을 병렬로 동시 테스트 (Jenkins는 Executor 수 제약)

#### Self-Hosted Runner로 온프레미스 통합
```yaml
# .github/workflows/deploy-onprem.yml
name: Deploy to On-Premise

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: [self-hosted, linux, x64, production]  # 사내 서버에서 실행
    steps:
      - uses: actions/checkout@v4

      - name: Deploy to Production
        run: |
          ./scripts/deploy.sh --env production
        env:
          DB_PASSWORD: ${{ secrets.PROD_DB_PASSWORD }}

      - name: Health Check
        run: |
          sleep 10
          curl -f http://localhost:8080/health || exit 1

      - name: Notify Slack
        if: always()
        uses: slackapi/slack-github-action@v1.24
        with:
          webhook-url: ${{ secrets.SLACK_WEBHOOK }}
          payload: |
            {
              "text": "Deployment ${{ job.status }}: ${{ github.event.head_commit.message }}"
            }
```

**효과**: 금융권 보안 정책상 외부 네트워크 접근 제한이 있어도 Self-Hosted Runner로 온프레미스 배포 가능

### 4. 재사용 가능한 워크플로우

```yaml
# .github/workflows/reusable-build.yml
name: Reusable Build Workflow

on:
  workflow_call:
    inputs:
      java-version:
        required: true
        type: string
    secrets:
      token:
        required: true

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-java@v4
        with:
          java-version: ${{ inputs.java-version }}
      - run: ./gradlew build
```

```yaml
# .github/workflows/main.yml
name: Main Build

on: [push]

jobs:
  call-reusable:
    uses: ./.github/workflows/reusable-build.yml
    with:
      java-version: '17'
    secrets:
      token: ${{ secrets.GITHUB_TOKEN }}
```

**효과**: DRY 원칙 적용, 여러 프로젝트에서 공통 워크플로우 재사용 (Jenkins Shared Library보다 간단)

### 5. 보안 강화

#### OIDC를 통한 비밀번호 없는 AWS 인증
```yaml
# .github/workflows/deploy-aws.yml
name: Deploy to AWS

permissions:
  id-token: write  # OIDC 토큰 발급 권한
  contents: read

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: arn:aws:iam::123456789012:role/GitHubActionsRole
          aws-region: ap-northeast-2

      - name: Deploy to S3
        run: |
          aws s3 sync ./build s3://my-bucket/
```

**효과**: AWS Access Key를 GitHub Secrets에 저장할 필요 없음, 일시적 자격 증명으로 보안 강화

## GitHub Actions의 단점

### 1. 빌드 시간 제한
- **GitHub 호스팅 러너**: 작업당 최대 6시간 (Jenkins는 무제한)
- **해결책**: Self-Hosted Runner 사용하면 제한 없음

### 2. 러너 성능 제약
- **GitHub 호스팅 러너**: 2 vCPU, 7GB RAM 고정 (Jenkins는 원하는 스펙 선택 가능)
- **해결책**: Self-Hosted Runner로 고성능 빌드 서버 사용

### 3. 복잡한 파이프라인 표현력
- **GitHub Actions**: YAML 기반이라 복잡한 로직 표현 어려움 (Groovy는 프로그래밍 언어 수준)
- **해결책**: 복잡한 로직은 별도 스크립트(Bash, Python)로 분리

### 4. 플러그인 생태계 차이
- **Jenkins**: 1,800+ 플러그인 (LDAP, Sonar, Jira 등 엔터프라이즈 통합 풍부)
- **GitHub Actions**: Marketplace 액션 (상대적으로 적음)
- **해결책**: 대부분 공식 API로 직접 통합 가능

## 마이그레이션 과정

### 1단계: 간단한 빌드부터 전환 (Week 1-2)
- **대상**: 라이브러리 프로젝트 (외부 의존성 적음)
- **작업**: Jenkinsfile → GitHub Actions YAML 변환
- **검증**: 두 시스템 병행 실행 후 결과 비교

### 2단계: 복잡한 파이프라인 전환 (Week 3-4)
- **대상**: 메인 애플리케이션 빌드, 테스트, 배포
- **작업**:
  - Jenkins Shared Library 로직을 Composite Action으로 전환
  - Slack, Jira 알림 통합
  - Self-Hosted Runner 설정

### 3단계: 레거시 Jenkins 유지 (Week 5+)
- **유지 대상**: On-Premise 전용 배포 스크립트 (네트워크 제약)
- **전략**: GitHub Actions에서 Jenkins Job 트리거 (Webhook)

```yaml
# GitHub Actions에서 Jenkins 트리거
- name: Trigger Jenkins Job
  run: |
    curl -X POST \
      -u ${{ secrets.JENKINS_USER }}:${{ secrets.JENKINS_TOKEN }} \
      https://jenkins.internal.com/job/deploy-legacy/build \
      --data-urlencode json='{"parameter": [{"name":"VERSION", "value":"${{ github.sha }}"}]}'
```

### 4단계: Jenkins 서버 폐기 (Month 3)
- **작업**:
  - 모든 워크플로우 전환 완료 확인
  - Jenkins 설정 및 이력 S3 백업
  - EC2 인스턴스 종료
- **비용 절감**: 월 $70 → $20 (약 70% 절감)

## 실제 성과

| 지표 | Jenkins | GitHub Actions | 개선율 |
|-----|---------|----------------|--------|
| 빌드 대기 시간 | 평균 5분 (큐 대기) | 평균 30초 | **90% 감소** |
| 파이프라인 수정 시간 | 30분 (디버깅 포함) | 10분 | **67% 감소** |
| 인프라 관리 시간 | 주 5시간 | 주 0.5시간 | **90% 감소** |
| 신규 개발자 온보딩 | 2일 (Jenkins 학습) | 2시간 (YAML 학습) | **92% 감소** |
| 월 운영 비용 | $70 | $20 | **71% 절감** |

## 참고 자료

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Migrating from Jenkins to GitHub Actions](https://docs.github.com/en/actions/migrating-to-github-actions/migrating-from-jenkins-to-github-actions)
- [GitHub Actions vs Jenkins - Feature Comparison](https://resources.github.com/devops/tools/compare/)
- [Act - Run GitHub Actions locally](https://github.com/nektos/act)
- [Awesome Actions - Curated list](https://github.com/sdras/awesome-actions)
