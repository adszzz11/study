# Nginx의 Worker Process 동작 원리는?

## 답변

[여기에 답변 작성]

## 핵심 키워드

- Master Process
- Worker Process
- Event-driven
- Non-blocking I/O
- epoll/kqueue
- Connection Pool
- Worker Connections

## Master Process 역할

-

## Worker Process 역할

-

## Event-driven 아키텍처

### epoll (Linux)
-

### kqueue (BSD/macOS)
-

## Non-blocking I/O 처리

-

## Worker Process 개수 설정

-

## Connection 처리 과정

-

## 설정 예시

### nginx.conf
```nginx
# Master process는 root로 실행
user nginx;

# Worker process 개수 (보통 CPU 코어 수와 동일)
worker_processes auto;

# Worker process당 최대 연결 수
events {
    worker_connections 1024;
    # Linux에서 효율적인 이벤트 처리
    use epoll;
    # 가능한 많은 연결 수락
    multi_accept on;
}

http {
    # Keepalive 설정
    keepalive_timeout 65;
    keepalive_requests 100;

    # 버퍼 설정
    client_body_buffer_size 128k;
    client_max_body_size 10m;

    server {
        listen 80;
        server_name example.com;

        location / {
            proxy_pass http://backend;
        }
    }
}
```

### Worker Process 튜닝
```nginx
worker_processes 4;
worker_cpu_affinity 0001 0010 0100 1000;
worker_priority -10;
worker_rlimit_nofile 65535;

events {
    worker_connections 4096;
    use epoll;
    multi_accept on;
}
```

## 성능 모니터링

```bash
# Worker process 상태 확인
ps aux | grep nginx

# 연결 상태 확인
netstat -an | grep :80 | wc -l

# Nginx 상태 페이지
curl http://localhost/nginx_status
```

## 참고 자료

-
