# Docker와 Podman의 차이점과 선택 이유

## Keywords
`Container Runtime`, `Daemonless`, `Rootless`, `OCI 표준`, `보안`, `Docker`, `Podman`

## 핵심 답변
Docker와 Podman은 모두 컨테이너 런타임이지만, 아키텍처와 보안 측면에서 중요한 차이가 있습니다. Docker는 중앙 데몬(dockerd)이 root 권한으로 실행되는 구조이며, Podman은 데몬 없이 각 컨테이너를 독립적인 프로세스로 실행하는 daemonless 구조입니다.

**주요 차이점:**
1. **아키텍처**: Docker는 Client-Server 구조, Podman은 Fork-Exec 모델
2. **보안**: Podman은 rootless 컨테이너를 기본 지원
3. **시스템 통합**: Podman은 systemd와 긴밀하게 통합
4. **호환성**: Podman은 Docker CLI와 호환 가능 (별칭 설정 가능)

**Podman 선택 이유:**
- 보안 강화: 데몬 없이 실행되어 단일 장애 지점 제거
- Rootless 컨테이너: 권한 분리로 보안 향상
- Kubernetes 호환: Pod 개념을 네이티브 지원
- 시스템 리소스: 데몬이 없어 메모리 사용량 감소

## 상세 설명

### Docker 아키텍처
```
Client (docker CLI)
    ↓ REST API
Docker Daemon (dockerd) - root 권한 필요
    ↓
containerd
    ↓
runc (OCI Runtime)
```

### Podman 아키텍처
```
Client (podman CLI)
    ↓ 직접 호출
conmon (Container Monitor)
    ↓
runc/crun (OCI Runtime)
```

### 보안 비교

**Docker의 보안 이슈:**
```bash
# Docker 데몬은 항상 root로 실행
$ ps aux | grep dockerd
root  1234  ... /usr/bin/dockerd

# 데몬 소켓도 root 소유
$ ls -l /var/run/docker.sock
srw-rw---- 1 root docker ... /var/run/docker.sock
```

**Podman의 Rootless 모드:**
```bash
# Rootless 컨테이너 실행
$ podman run --rm -it nginx

# 사용자 권한으로 실행 확인
$ ps aux | grep conmon
user  5678  ... /usr/bin/conmon

# 사용자별 소켓
$ ls -l $XDG_RUNTIME_DIR/podman/podman.sock
srw------- 1 user user ... podman.sock
```

### 기능 비교

| 기능 | Docker | Podman |
|------|--------|--------|
| 데몬 필요 | ✓ (dockerd) | ✗ (daemonless) |
| Rootless 모드 | 실험적 지원 | 기본 지원 |
| Systemd 통합 | 제한적 | 네이티브 지원 |
| Pod 관리 | ✗ | ✓ |
| Compose | docker-compose | podman-compose |
| Swarm | ✓ | ✗ |

### Podman 실전 사용 예시

**1. Docker 명령어와 동일한 사용:**
```bash
# Docker 별칭 설정
alias docker=podman

# 동일한 명령어 사용 가능
podman run -d --name web -p 8080:80 nginx
podman ps
podman logs web
podman stop web
```

**2. Pod 관리 (Kubernetes 유사):**
```bash
# Pod 생성
podman pod create --name myapp -p 8080:80

# Pod에 컨테이너 추가
podman run -d --pod myapp --name web nginx
podman run -d --pod myapp --name cache redis

# Pod 단위 관리
podman pod ps
podman pod stop myapp
```

**3. Systemd 통합:**
```bash
# Systemd 유닛 파일 생성
podman generate systemd --new --files --name web

# Systemd 서비스로 등록
mv container-web.service ~/.config/systemd/user/
systemctl --user enable --now container-web.service

# 서비스 상태 확인
systemctl --user status container-web
```

**4. Rootless 컨테이너 실행:**
```bash
# 일반 사용자로 실행 (root 불필요)
podman run --rm -it \
  --security-opt label=disable \
  -v $HOME/data:/data:Z \
  alpine sh

# 포트 매핑 (1024 이상)
podman run -d -p 8080:80 nginx

# 권한이 필요한 포트는 slirp4netns 사용
podman run -d -p 80:80 --network slirp4netns:port_handler=slirp4netns nginx
```

## 예시 코드

### Podman으로 마이그레이션

**docker-compose.yml을 Podman으로 실행:**
```yaml
# docker-compose.yml
version: '3'
services:
  web:
    image: nginx:latest
    ports:
      - "8080:80"
    volumes:
      - ./html:/usr/share/nginx/html:ro

  app:
    image: myapp:latest
    depends_on:
      - db
    environment:
      DATABASE_URL: postgresql://db:5432/mydb

  db:
    image: postgres:15
    environment:
      POSTGRES_PASSWORD: secret
    volumes:
      - pgdata:/var/lib/postgresql/data

volumes:
  pgdata:
```

```bash
# Podman으로 실행
podman-compose up -d

# 또는 Kubernetes YAML 생성
podman generate kube myapp > myapp-pod.yaml
```

### Podman을 사용한 CI/CD 파이프라인

**Jenkinsfile:**
```groovy
pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                script {
                    // Podman으로 이미지 빌드
                    sh 'podman build -t myapp:${BUILD_NUMBER} .'
                }
            }
        }

        stage('Test') {
            steps {
                script {
                    // Rootless 컨테이너로 테스트 실행
                    sh '''
                        podman run --rm \
                          --security-opt label=disable \
                          myapp:${BUILD_NUMBER} \
                          npm test
                    '''
                }
            }
        }

        stage('Push') {
            steps {
                script {
                    // Registry에 푸시
                    sh '''
                        podman tag myapp:${BUILD_NUMBER} registry.example.com/myapp:${BUILD_NUMBER}
                        podman push registry.example.com/myapp:${BUILD_NUMBER}
                    '''
                }
            }
        }
    }
}
```

### 보안 강화 설정

**Rootless 컨테이너 보안 설정:**
```bash
# SELinux 레이블 적용
podman run -d --security-opt label=type:container_runtime_t nginx

# Capability 제한
podman run -d \
  --cap-drop=ALL \
  --cap-add=NET_BIND_SERVICE \
  nginx

# Read-only 루트 파일시스템
podman run -d \
  --read-only \
  --tmpfs /tmp \
  --tmpfs /run \
  nginx

# User namespace 매핑
podman run -d \
  --userns=auto \
  --uidmap 0:100000:65536 \
  nginx
```

## 실무 적용 팁

### 마이그레이션 전략
1. **호환성 확인**: Docker CLI 명령어 대부분 호환
2. **점진적 전환**: 개발 환경부터 시작
3. **Systemd 활용**: 운영 환경에서 서비스 관리
4. **네트워크 설정**: Rootless 모드의 포트 제약 고려

### 주의사항
- Rootless 모드에서 1024 이하 포트 직접 바인딩 불가
- Docker Swarm 기능은 Podman에서 미지원
- 일부 Docker 전용 도구와 호환성 문제 가능
- Volume 마운트 시 SELinux 컨텍스트 설정 필요

## 참고 자료
- [Podman Official Documentation](https://docs.podman.io/)
- [Docker vs Podman](https://www.redhat.com/en/topics/containers/what-is-podman)
- [Rootless Containers](https://rootlesscontaine.rs/)
- [Podman Compose](https://github.com/containers/podman-compose)
