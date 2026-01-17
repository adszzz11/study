# Jenkins Pipeline과 GitHub Actions 비교 시 장단점은?

## 답변

[여기에 답변 작성]

## 핵심 키워드

- Jenkins Pipeline
- GitHub Actions
- Self-hosted Runner
- Declarative vs Scripting
- Marketplace
- 플러그인 생태계

## Jenkins Pipeline 장단점

### 장점
-

### 단점
-

## GitHub Actions 장단점

### 장점
-

### 단점
-

## 선택 기준

-

## 설정 예시

### Jenkins Pipeline (Declarative)
```groovy
pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                // 빌드 스크립트
            }
        }
    }
}
```

### GitHub Actions
```yaml
name: CI
on: [push]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Build
        run: |
          # 빌드 스크립트
```

## 참고 자료

-
