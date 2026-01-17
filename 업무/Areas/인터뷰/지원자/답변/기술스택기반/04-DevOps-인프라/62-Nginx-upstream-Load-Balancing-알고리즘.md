# upstream 모듈의 Load Balancing 알고리즘 선택 기준은?

## 답변

[여기에 답변 작성]

## 핵심 키워드

- upstream
- Round Robin
- Least Connections
- IP Hash
- Weight
- Health Check
- Sticky Session

## Load Balancing 알고리즘

### Round Robin (기본)
-

### Least Connections
-

### IP Hash
-

### Hash
-

### Random
-

## Weight 설정

-

## Health Check

### Passive Health Check
-

### Active Health Check (Commercial)
-

## Sticky Session

-

## 알고리즘 선택 기준

-

## 설정 예시

### Round Robin with Weight
```nginx
upstream backend {
    # 가중치 기반 라운드 로빈
    server backend1.example.com:8080 weight=3;
    server backend2.example.com:8080 weight=2;
    server backend3.example.com:8080 weight=1;

    # Keepalive 연결 유지
    keepalive 32;
}
```

### Least Connections
```nginx
upstream backend {
    least_conn;

    server backend1.example.com:8080;
    server backend2.example.com:8080;
    server backend3.example.com:8080;
}
```

### IP Hash (Session Persistence)
```nginx
upstream backend {
    ip_hash;

    server backend1.example.com:8080;
    server backend2.example.com:8080;
    server backend3.example.com:8080;
}
```

### Generic Hash
```nginx
upstream backend {
    # URL 기반 해싱
    hash $request_uri consistent;

    server backend1.example.com:8080;
    server backend2.example.com:8080;
    server backend3.example.com:8080;
}
```

### Health Check 및 백업 서버
```nginx
upstream backend {
    server backend1.example.com:8080 max_fails=3 fail_timeout=30s;
    server backend2.example.com:8080 max_fails=3 fail_timeout=30s;
    server backend3.example.com:8080 backup;  # 백업 서버

    # 다운된 서버 표시 (수동)
    # server backend4.example.com:8080 down;
}
```

### 고급 설정
```nginx
upstream backend {
    least_conn;

    server backend1.example.com:8080 weight=2 max_fails=2 fail_timeout=30s;
    server backend2.example.com:8080 weight=1 max_fails=2 fail_timeout=30s;
    server backend3.example.com:8080 backup;

    # slow start (Commercial)
    # server backend4.example.com:8080 slow_start=30s;

    keepalive 32;
    keepalive_requests 100;
    keepalive_timeout 60s;
}

server {
    listen 80;

    location / {
        proxy_pass http://backend;
        proxy_http_version 1.1;
        proxy_set_header Connection "";

        # 에러 발생 시 다음 서버로
        proxy_next_upstream error timeout http_500 http_502 http_503;
        proxy_next_upstream_tries 3;
    }
}
```

### Cookie 기반 Sticky Session
```nginx
upstream backend {
    server backend1.example.com:8080;
    server backend2.example.com:8080;
    server backend3.example.com:8080;
}

server {
    location / {
        proxy_pass http://backend;

        # Cookie 기반 세션 유지 (Commercial)
        # sticky cookie srv_id expires=1h domain=.example.com path=/;
    }
}
```

## 참고 자료

-
