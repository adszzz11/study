---
date: 2025-01-18
tags:
  - tech
  - core
  - jenkins
  - pipeline
  - plugins
parent: "[[README]]"
---

# Jenkins - 핵심

> ⬅️ [[01-basics|이전: 기초]] | ➡️ [[03-practice|다음: 실무]]

---

## 1. Pipeline 문법

### Declarative vs Scripted

| 구분 | Declarative | Scripted |
|------|-------------|----------|
| 시작 | `pipeline {}` | `node {}` |
| 가독성 | 높음 | 낮음 |
| 유연성 | 제한적 | 완전한 Groovy |
| 권장 | ✅ 대부분 상황 | 복잡한 로직 |

### Declarative Pipeline 구조

```groovy
pipeline {
    agent any                    // 실행 환경

    options {                    // 파이프라인 옵션
        timeout(time: 1, unit: 'HOURS')
        buildDiscarder(logRotator(numToKeepStr: '10'))
    }

    environment {               // 환경 변수
        DEPLOY_ENV = 'production'
    }

    parameters {                // 빌드 파라미터
        string(name: 'VERSION', defaultValue: '1.0.0')
        booleanParam(name: 'DEPLOY', defaultValue: false)
    }

    stages {                    // 실행 단계들
        stage('Build') {
            steps {
                sh 'mvn clean package'
            }
        }
    }

    post {                      // 후처리
        always { /* 항상 실행 */ }
        success { /* 성공 시 */ }
        failure { /* 실패 시 */ }
    }
}
```

### Agent 옵션

```groovy
// 모든 에이전트
agent any

// 특정 에이전트 없음 (stage에서 지정)
agent none

// 레이블로 선택
agent { label 'linux' }

// Docker 컨테이너
agent {
    docker {
        image 'maven:3.8-openjdk-17'
        args '-v $HOME/.m2:/root/.m2'
    }
}

// Kubernetes Pod
agent {
    kubernetes {
        yaml '''
apiVersion: v1
kind: Pod
spec:
  containers:
  - name: maven
    image: maven:3.8-openjdk-17
'''
    }
}
```

---

## 2. Steps 상세

### 기본 Steps

```groovy
steps {
    // 셸 명령
    sh 'echo Hello'
    sh '''
        echo "Multi-line"
        ls -la
    '''

    // 디렉토리 이동
    dir('subdir') {
        sh 'pwd'
    }

    // 파일 작업
    writeFile file: 'output.txt', text: 'Hello'
    def content = readFile 'output.txt'

    // 환경 변수
    withEnv(['MY_VAR=value']) {
        sh 'echo $MY_VAR'
    }

    // 시간 제한
    timeout(time: 5, unit: 'MINUTES') {
        sh 'long-running-task'
    }
}
```

### 조건부 실행

```groovy
stages {
    stage('Deploy') {
        when {
            branch 'main'
            environment name: 'DEPLOY', value: 'true'
        }
        steps {
            sh 'deploy.sh'
        }
    }

    stage('Release') {
        when {
            allOf {
                branch 'main'
                tag pattern: "v\\d+\\.\\d+\\.\\d+", comparator: "REGEXP"
            }
        }
        steps {
            sh 'release.sh'
        }
    }
}
```

### 병렬 실행

```groovy
stage('Test') {
    parallel {
        stage('Unit Test') {
            steps {
                sh 'mvn test'
            }
        }
        stage('Integration Test') {
            steps {
                sh 'mvn verify'
            }
        }
        stage('E2E Test') {
            agent { label 'e2e-runner' }
            steps {
                sh 'npm run e2e'
            }
        }
    }
}
```

---

## 3. 자격 증명 (Credentials)

### Credentials 종류

| 유형 | 용도 | 예시 |
|------|------|------|
| **Username/Password** | 로그인 정보 | Docker Registry |
| **SSH Key** | 서버 접속 | Git, 배포 서버 |
| **Secret Text** | API 키 | Slack Token |
| **Secret File** | 파일 형태 | kubeconfig |

### 사용 방법

```groovy
pipeline {
    agent any

    environment {
        // 환경 변수로 주입
        DOCKER_CREDS = credentials('docker-hub-creds')
        // DOCKER_CREDS_USR, DOCKER_CREDS_PSW 자동 생성
    }

    stages {
        stage('Build') {
            steps {
                // withCredentials 블록
                withCredentials([
                    usernamePassword(
                        credentialsId: 'docker-hub-creds',
                        usernameVariable: 'DOCKER_USER',
                        passwordVariable: 'DOCKER_PASS'
                    )
                ]) {
                    sh 'docker login -u $DOCKER_USER -p $DOCKER_PASS'
                }

                // SSH Key
                withCredentials([
                    sshUserPrivateKey(
                        credentialsId: 'deploy-key',
                        keyFileVariable: 'SSH_KEY'
                    )
                ]) {
                    sh 'ssh -i $SSH_KEY user@server'
                }
            }
        }
    }
}
```

---

## 4. 핵심 플러그인

### Pipeline 관련

| 플러그인 | 용도 |
|---------|------|
| **Pipeline** | Jenkinsfile 지원 |
| **Pipeline: Stage View** | 시각적 파이프라인 |
| **Blue Ocean** | 현대적 UI |
| **Pipeline Utility Steps** | 파일 처리 유틸리티 |

### 빌드 도구 연동

```groovy
// Maven
stage('Maven Build') {
    tools {
        maven 'Maven-3.8'
        jdk 'JDK-17'
    }
    steps {
        sh 'mvn clean package'
    }
}

// Gradle
stage('Gradle Build') {
    steps {
        sh './gradlew build'
    }
}

// Node.js
stage('Node Build') {
    tools {
        nodejs 'Node-18'
    }
    steps {
        sh 'npm ci && npm run build'
    }
}
```

### Docker 연동

```groovy
pipeline {
    agent any

    stages {
        stage('Build Image') {
            steps {
                script {
                    def image = docker.build("myapp:${BUILD_NUMBER}")
                    docker.withRegistry('https://registry.hub.docker.com', 'docker-creds') {
                        image.push()
                        image.push('latest')
                    }
                }
            }
        }
    }
}
```

---

## 5. 알림 설정

### Slack 알림

```groovy
post {
    success {
        slackSend(
            channel: '#builds',
            color: 'good',
            message: "✅ 빌드 성공: ${env.JOB_NAME} #${env.BUILD_NUMBER}"
        )
    }
    failure {
        slackSend(
            channel: '#builds',
            color: 'danger',
            message: "❌ 빌드 실패: ${env.JOB_NAME} #${env.BUILD_NUMBER}"
        )
    }
}
```

### 이메일 알림

```groovy
post {
    failure {
        emailext(
            subject: "빌드 실패: ${env.JOB_NAME}",
            body: """
                빌드 #${env.BUILD_NUMBER} 실패
                로그: ${env.BUILD_URL}console
            """,
            to: 'team@example.com'
        )
    }
}
```

---

## 6. Shared Libraries

### 구조

```
(root)
├── vars/
│   ├── buildPipeline.groovy    # 전역 함수
│   └── deploy.groovy
├── src/
│   └── org/company/Utils.groovy # 클래스
└── resources/
    └── config.yaml
```

### 사용 예시

```groovy
// vars/buildPipeline.groovy
def call(Map config) {
    pipeline {
        agent any
        stages {
            stage('Build') {
                steps {
                    sh "mvn clean package -P${config.profile}"
                }
            }
        }
    }
}

// Jenkinsfile
@Library('my-shared-lib') _
buildPipeline(profile: 'production')
```

---

## 7. 체크리스트

### 이해도 확인

- [ ] Declarative Pipeline 구조 이해
- [ ] Agent 옵션 (docker, kubernetes) 사용 가능
- [ ] Credentials 안전하게 사용 가능
- [ ] 병렬 실행 (parallel) 구현 가능
- [ ] post 블록으로 후처리 설정 가능
- [ ] Shared Library 개념 이해

---

## 다음 단계

> [!tip] 다음으로
> 핵심 문법을 익혔다면 [[03-practice|실무 적용]]에서 실전 파이프라인을 학습하세요.

---

## References

- [Pipeline Syntax](https://www.jenkins.io/doc/book/pipeline/syntax/)
- [Pipeline Steps Reference](https://www.jenkins.io/doc/pipeline/steps/)
- [Shared Libraries](https://www.jenkins.io/doc/book/pipeline/shared-libraries/)
