# Reverse Proxy와 Forward Proxy 구성 시 주의사항은?

## 답변

[여기에 답변 작성]

## 핵심 키워드

- Reverse Proxy
- Forward Proxy
- X-Forwarded-For
- X-Real-IP
- Proxy Protocol
- 버퍼링
- 타임아웃

## Reverse Proxy vs Forward Proxy

### Reverse Proxy
-

### Forward Proxy
-

## Reverse Proxy 주의사항

### 헤더 전달
-

### 버퍼링
-

### 타임아웃
-

### SSL/TLS
-

## Forward Proxy 주의사항

### 접근 제어
-

### 캐싱
-

## 보안 고려사항

-

## 설정 예시

### Reverse Proxy 기본 설정
```nginx
upstream backend {
    server backend1.example.com:8080;
    server backend2.example.com:8080;
    keepalive 32;
}

server {
    listen 80;
    server_name example.com;

    location / {
        proxy_pass http://backend;

        # 클라이언트 IP 정보 전달
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header Host $host;

        # 버퍼링 설정
        proxy_buffering on;
        proxy_buffer_size 4k;
        proxy_buffers 8 4k;
        proxy_busy_buffers_size 8k;

        # 타임아웃 설정
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;

        # Keepalive
        proxy_http_version 1.1;
        proxy_set_header Connection "";
    }
}
```

### Forward Proxy 설정
```nginx
server {
    listen 8080;

    # DNS resolver 설정
    resolver 8.8.8.8;

    location / {
        proxy_pass http://$http_host$uri$is_args$args;

        # 접근 제어
        allow 10.0.0.0/8;
        deny all;

        # 캐싱 설정
        proxy_cache_path /var/cache/nginx levels=1:2 keys_zone=proxy_cache:10m;
        proxy_cache proxy_cache;
        proxy_cache_valid 200 1h;
    }
}
```

### WebSocket Proxy
```nginx
location /ws {
    proxy_pass http://backend;

    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";

    proxy_read_timeout 86400;
}
```

## 참고 자료

-
