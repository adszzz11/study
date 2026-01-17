# SSL/TLS Termination 위치 결정 기준은?

## 답변

[여기에 답변 작성]

## 핵심 키워드

- SSL/TLS Termination
- Edge Termination
- Re-encryption
- End-to-End Encryption
- Performance
- Security
- Compliance

## SSL/TLS Termination 옵션

### Edge Termination (엣지 종료)
-

### Re-encryption (재암호화)
-

### End-to-End Encryption (종단간 암호화)
-

### Passthrough (통과)
-

## 각 방식의 장단점

### Edge Termination
#### 장점
-

#### 단점
-

### Re-encryption
#### 장점
-

#### 단점
-

### End-to-End
#### 장점
-

#### 단점
-

## 선택 기준

### Performance 우선
-

### Security 우선
-

### Compliance 요구사항
-

## 설정 예시

### Edge Termination (Nginx)
```nginx
server {
    listen 443 ssl http2;
    server_name example.com;

    # SSL 인증서
    ssl_certificate /etc/nginx/ssl/cert.pem;
    ssl_certificate_key /etc/nginx/ssl/key.pem;

    # SSL 프로토콜 및 암호화 방식
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;

    # SSL 세션 캐시
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;

    # HSTS
    add_header Strict-Transport-Security "max-age=31536000" always;

    location / {
        # 백엔드는 HTTP
        proxy_pass http://backend:8080;

        # 클라이언트가 HTTPS로 접속했음을 전달
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

### Re-encryption (Nginx)
```nginx
upstream backend {
    server backend1.example.com:8443;
    server backend2.example.com:8443;
}

server {
    listen 443 ssl http2;
    server_name example.com;

    # 프론트엔드 SSL
    ssl_certificate /etc/nginx/ssl/frontend-cert.pem;
    ssl_certificate_key /etc/nginx/ssl/frontend-key.pem;
    ssl_protocols TLSv1.2 TLSv1.3;

    location / {
        # 백엔드도 HTTPS
        proxy_pass https://backend;

        # 백엔드 인증서 검증
        proxy_ssl_verify on;
        proxy_ssl_trusted_certificate /etc/nginx/ssl/backend-ca.pem;
        proxy_ssl_verify_depth 2;

        # 또는 자체 서명 인증서 허용
        # proxy_ssl_verify off;

        proxy_ssl_protocols TLSv1.2 TLSv1.3;
        proxy_ssl_ciphers HIGH:!aNULL:!MD5;
    }
}
```

### Kubernetes Ingress - Edge Termination
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: myapp-ingress
  annotations:
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
spec:
  tls:
  - hosts:
    - example.com
    secretName: example-tls
  rules:
  - host: example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: myapp-service
            port:
              number: 8080  # HTTP
```

### Kubernetes Ingress - Re-encryption
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: myapp-ingress
  annotations:
    nginx.ingress.kubernetes.io/backend-protocol: "HTTPS"
    nginx.ingress.kubernetes.io/proxy-ssl-verify: "true"
spec:
  tls:
  - hosts:
    - example.com
    secretName: example-tls
  rules:
  - host: example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: myapp-service
            port:
              number: 8443  # HTTPS
```

### Let's Encrypt with Certbot
```bash
# Certbot 설치
apt-get install certbot python3-certbot-nginx

# 인증서 발급
certbot --nginx -d example.com -d www.example.com

# 자동 갱신 설정
certbot renew --dry-run

# Crontab에 자동 갱신 추가
0 0 * * * certbot renew --quiet
```

## 참고 자료

-
