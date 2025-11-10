# Nginx에서 Rate Limiting 구현 방법은?

## 답변

[여기에 답변 작성]

## 핵심 키워드

- Rate Limiting
- limit_req
- limit_conn
- Leaky Bucket
- Token Bucket
- burst
- nodelay

## Rate Limiting 방식

### limit_req (요청 수 제한)
-

### limit_conn (연결 수 제한)
-

## Leaky Bucket vs Token Bucket

-

## burst와 nodelay 옵션

### burst
-

### nodelay
-

## Zone 설정

-

## 응용 사례

### API Rate Limiting
-

### DDoS 방어
-

## 설정 예시

### 기본 Rate Limiting
```nginx
http {
    # IP별 요청 수 제한 (초당 10개)
    limit_req_zone $binary_remote_addr zone=req_limit:10m rate=10r/s;

    # IP별 동시 연결 수 제한
    limit_conn_zone $binary_remote_addr zone=conn_limit:10m;

    server {
        listen 80;

        location /api/ {
            # burst 허용 (최대 20개 대기)
            limit_req zone=req_limit burst=20 nodelay;

            # 동시 연결 10개까지
            limit_conn conn_limit 10;

            # 429 에러 시 커스텀 응답
            limit_req_status 429;
            limit_conn_status 429;

            proxy_pass http://backend;
        }
    }
}
```

### 사용자별 Rate Limiting
```nginx
http {
    # 사용자 ID 기반 제한
    map $http_authorization $user_id {
        ~*Bearer\s+(?<token>.+) $token;
        default "anonymous";
    }

    limit_req_zone $user_id zone=user_limit:10m rate=100r/m;

    server {
        location /api/ {
            limit_req zone=user_limit burst=10;
            proxy_pass http://backend;
        }
    }
}
```

### 경로별 차등 적용
```nginx
http {
    limit_req_zone $binary_remote_addr zone=general:10m rate=10r/s;
    limit_req_zone $binary_remote_addr zone=strict:10m rate=1r/s;

    server {
        # 일반 요청
        location / {
            limit_req zone=general burst=20 nodelay;
            proxy_pass http://backend;
        }

        # 민감한 작업 (로그인, 회원가입 등)
        location /auth/ {
            limit_req zone=strict burst=5;
            proxy_pass http://backend;
        }
    }
}
```

### 화이트리스트 적용
```nginx
http {
    geo $limit {
        default 1;
        10.0.0.0/8 0;  # 내부 네트워크 제외
        192.168.0.0/16 0;
    }

    map $limit $limit_key {
        0 "";
        1 $binary_remote_addr;
    }

    limit_req_zone $limit_key zone=api_limit:10m rate=10r/s;

    server {
        location /api/ {
            limit_req zone=api_limit burst=20 nodelay;
            proxy_pass http://backend;
        }
    }
}
```

## 모니터링

```nginx
# 상태 페이지 설정
location /nginx_status {
    stub_status on;
    access_log off;
    allow 127.0.0.1;
    deny all;
}
```

## 참고 자료

-
