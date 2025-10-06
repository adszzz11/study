# ELK Stack - Server 관점

> 최종 업데이트: 2025-10-06

서버 측에서 로그를 수집, 처리, 저장, 시각화하는 전체 ELK Stack 아키텍처와 구성 방법을 다룹니다.

## 목차

1. [개요](#개요)
2. [전체 아키텍처](#전체-아키텍처)
3. [Beats - 로그 수집](#beats---로그-수집)
4. [Logstash - 로그 처리](#logstash---로그-처리)
5. [Elasticsearch - 로그 저장 및 검색](#elasticsearch---로그-저장-및-검색)
6. [Kibana - 시각화 및 분석](#kibana---시각화-및-분석)
7. [실전 구성 예시](#실전-구성-예시)
8. [Best Practices](#best-practices)

## 개요

ELK Stack의 서버 측 구성은 로그의 수집부터 저장, 분석, 시각화까지 전체 라이프사이클을 담당합니다.

### 데이터 흐름

```
[로그 소스]
    ↓
[Beats/Filebeat] ← 로그 수집
    ↓
[Logstash] ← 파싱, 변환, 필터링 (선택적)
    ↓
[Elasticsearch] ← 인덱싱, 저장, 검색
    ↓
[Kibana] ← 시각화, 대시보드
```

### 최신 아키텍처 트렌드 (2025)

현대적인 ELK 구성에서는 다음과 같은 변화가 있습니다:

1. **Beats → Elasticsearch 직접 전송**
   - 단순한 로그는 Logstash 생략
   - Filebeat → Elasticsearch → Kibana

2. **Logstash 대체**
   - Fluentd, Vector 등 경량 대안 사용
   - 복잡한 파싱이 필요한 경우에만 Logstash 사용

3. **Elastic Agent**
   - Beats를 통합한 단일 에이전트
   - Fleet을 통한 중앙 관리

**출처**: [The Complete Guide to the ELK Stack | Logz.io](https://logz.io/learn/complete-guide-elk-stack/)

## 전체 아키텍처

### 프로덕션 아키텍처

```
┌─────────────────────────────────────────────────────────────┐
│                        로그 소스                              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │Web Server│  │App Server│  │   DB     │  │ Backend  │   │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘   │
└───────┼────────────┼─────────────┼─────────────┼──────────┘
        │            │             │             │
        ▼            ▼             ▼             ▼
   ┌────────────────────────────────────────────────┐
   │              Beats Layer                       │
   │  ┌──────────┐  ┌──────────┐  ┌──────────┐    │
   │  │ Filebeat │  │Metricbeat│  │Packetbeat│    │
   │  └────┬─────┘  └────┬─────┘  └────┬─────┘    │
   └───────┼────────────┼─────────────┼────────────┘
           │            │             │
           └────────────┼─────────────┘
                        ▼
              ┌──────────────────┐
              │    Logstash      │ (선택적)
              │  - Input         │
              │  - Filter        │
              │  - Output        │
              └─────────┬────────┘
                        ▼
        ┌───────────────────────────────┐
        │     Elasticsearch Cluster     │
        │  ┌─────────┐  ┌─────────┐    │
        │  │ Master  │  │  Data   │    │
        │  │  Node   │  │  Node   │    │
        │  └─────────┘  └─────────┘    │
        └──────────────┬────────────────┘
                       ▼
              ┌─────────────────┐
              │     Kibana      │
              │  - Dashboard    │
              │  - Visualization│
              └─────────────────┘
```

**출처**: [Elastic Stack Architecture | Medium](https://medium.com/orion-innovation-techclub/elastic-stack-architecture-c2a04f90c6f1)

### 단순화된 아키텍처 (소규모)

```
[애플리케이션] → [Filebeat] → [Elasticsearch] → [Kibana]
```

## Beats - 로그 수집

Beats는 경량 데이터 수집기로, 다양한 종류의 데이터를 수집합니다.

### Beats 종류

| Beat | 용도 | 수집 데이터 |
|------|------|-----------|
| **Filebeat** | 로그 파일 | 애플리케이션 로그, 시스템 로그 |
| **Metricbeat** | 메트릭 | CPU, 메모리, 디스크, 네트워크 |
| **Packetbeat** | 네트워크 | 네트워크 패킷, 프로토콜 분석 |
| **Winlogbeat** | Windows 이벤트 | Windows Event Log |
| **Heartbeat** | 가동시간 모니터링 | 서비스 헬스체크 |
| **Auditbeat** | 감사 데이터 | 시스템 감사 로그 |
| **Functionbeat** | 클라우드 | AWS Lambda, CloudWatch |

### Filebeat 설치 및 구성

#### 1. 설치 (Ubuntu/Debian 예시)

```bash
# 최신 버전 9.1.4 설치
wget https://artifacts.elastic.co/downloads/beats/filebeat/filebeat-9.1.4-amd64.deb
sudo dpkg -i filebeat-9.1.4-amd64.deb
```

**출처**: [Filebeat Installation | Elastic Docs](https://www.elastic.co/docs/reference/beats/filebeat/filebeat-installation-configuration)

#### 2. 기본 설정 (filebeat.yml)

```yaml
# Filebeat 설정 파일: /etc/filebeat/filebeat.yml

# ========== Filebeat Inputs ==========
filebeat.inputs:
  # 애플리케이션 로그
  - type: log
    enabled: true
    paths:
      - /var/log/myapp/*.log
    fields:
      service: myapp
      environment: production
    fields_under_root: true

    # 멀티라인 로그 처리 (스택 트레이스)
    multiline.type: pattern
    multiline.pattern: '^[0-9]{4}-[0-9]{2}-[0-9]{2}'
    multiline.negate: true
    multiline.match: after

  # Nginx 액세스 로그
  - type: log
    enabled: true
    paths:
      - /var/log/nginx/access.log
    fields:
      service: nginx
      log_type: access

  # 시스템 로그
  - type: syslog
    enabled: true

# ========== Filebeat Modules ==========
filebeat.config.modules:
  path: ${path.config}/modules.d/*.yml
  reload.enabled: false

# ========== Elasticsearch Output ==========
output.elasticsearch:
  hosts: ["localhost:9200"]

  # 인덱스 설정
  index: "filebeat-%{[agent.version]}-%{+yyyy.MM.dd}"

  # 보안 설정 (Elasticsearch 8.x부터 필수)
  username: "elastic"
  password: "your-password"
  ssl.enabled: true
  ssl.certificate_authorities: ["/etc/filebeat/certs/ca.crt"]

# ========== Kibana 설정 ==========
setup.kibana:
  host: "localhost:5601"

# ========== 프로세서 ==========
processors:
  - add_host_metadata:
      when.not.contains.tags: forwarded
  - add_cloud_metadata: ~
  - add_docker_metadata: ~
  - add_kubernetes_metadata: ~

# ========== 로깅 ==========
logging.level: info
logging.to_files: true
logging.files:
  path: /var/log/filebeat
  name: filebeat
  keepfiles: 7
  permissions: 0644
```

#### 3. Filebeat 모듈 활성화

```bash
# Nginx 모듈 활성화
sudo filebeat modules enable nginx

# Apache 모듈 활성화
sudo filebeat modules enable apache

# MySQL 모듈 활성화
sudo filebeat modules enable mysql

# 활성화된 모듈 확인
sudo filebeat modules list
```

#### 4. 인덱스 템플릿 및 대시보드 로드

```bash
# Elasticsearch에 인덱스 템플릿 로드
sudo filebeat setup --index-management

# Kibana에 대시보드 로드
sudo filebeat setup --dashboards

# 전체 설정 (권장)
sudo filebeat setup -e
```

#### 5. Filebeat 시작

```bash
# 설정 파일 테스트
sudo filebeat test config

# Elasticsearch 연결 테스트
sudo filebeat test output

# Filebeat 시작
sudo systemctl start filebeat

# 부팅시 자동 시작
sudo systemctl enable filebeat

# 상태 확인
sudo systemctl status filebeat
```

**출처**: [Filebeat quick start | Elastic Docs](https://www.elastic.co/docs/reference/beats/filebeat/filebeat-installation-configuration)

### Metricbeat 설치 및 구성

#### 1. 설치

```bash
wget https://artifacts.elastic.co/downloads/beats/metricbeat/metricbeat-9.1.4-amd64.deb
sudo dpkg -i metricbeat-9.1.4-amd64.deb
```

#### 2. 기본 설정 (metricbeat.yml)

```yaml
# Metricbeat 설정: /etc/metricbeat/metricbeat.yml

# ========== Metricbeat Modules ==========
metricbeat.config.modules:
  path: ${path.config}/modules.d/*.yml
  reload.enabled: false

metricbeat.modules:
  # 시스템 메트릭
  - module: system
    period: 10s
    metricsets:
      - cpu
      - load
      - memory
      - network
      - process
      - process_summary
      - socket_summary
      - filesystem
      - fsstat
    process.include_top_n:
      by_cpu: 5
      by_memory: 5

  # Docker 메트릭
  - module: docker
    period: 10s
    hosts: ["unix:///var/run/docker.sock"]
    metricsets:
      - container
      - cpu
      - diskio
      - healthcheck
      - info
      - memory
      - network

# ========== Elasticsearch Output ==========
output.elasticsearch:
  hosts: ["localhost:9200"]
  username: "elastic"
  password: "your-password"

# ========== Kibana ==========
setup.kibana:
  host: "localhost:5601"

# ========== 프로세서 ==========
processors:
  - add_host_metadata: ~
  - add_cloud_metadata: ~
  - add_docker_metadata: ~
```

#### 3. Metricbeat 모듈 및 시작

```bash
# 시스템 모듈 활성화
sudo metricbeat modules enable system

# Docker 모듈 활성화
sudo metricbeat modules enable docker

# Setup 및 시작
sudo metricbeat setup -e
sudo systemctl start metricbeat
sudo systemctl enable metricbeat
```

**출처**:
- [Metricbeat Installation | Elastic Docs](https://www.elastic.co/docs/reference/beats/metricbeat/metricbeat-installation-configuration)
- [How to Configure Metricbeat | Packt](https://www.packtpub.com/en-us/learning/how-to-tutorials/how-to-configure-metricbeat-for-application-and-server-infrastructure)

### Beats 모니터링

Beats 자체의 상태를 모니터링하는 방법:

```bash
# Filebeat 로그 확인
sudo tail -f /var/log/filebeat/filebeat

# Metricbeat 메트릭 확인
curl -X GET "localhost:5066/stats"

# Beats 모니터링 활성화 (metricbeat.yml)
monitoring.enabled: true
monitoring.elasticsearch:
  hosts: ["localhost:9200"]
```

## Logstash - 로그 처리

Logstash는 데이터 수집, 변환, 전달을 위한 서버 측 파이프라인입니다.

### Logstash 파이프라인 구조

```
Input → Filter → Output
```

### 1. Input Plugins

데이터 소스로부터 이벤트를 받아옵니다.

**주요 Input 플러그인**:
- `beats`: Filebeat, Metricbeat 등으로부터 수신
- `file`: 파일에서 직접 읽기
- `http`: HTTP/HTTPS 엔드포인트
- `tcp/udp`: TCP/UDP 소켓
- `syslog`: Syslog 메시지
- `kafka`: Kafka 토픽
- `jdbc`: 데이터베이스

### 2. Filter Plugins

이벤트를 파싱, 변환, 보강합니다.

**주요 Filter 플러그인**:
- `grok`: 비구조화 로그를 구조화
- `mutate`: 필드 조작 (rename, remove, replace)
- `date`: 날짜 파싱
- `geoip`: IP 주소 지리 정보 추가
- `useragent`: User-Agent 파싱
- `json`: JSON 파싱
- `csv`: CSV 파싱

### 3. Output Plugins

처리된 이벤트를 목적지로 전송합니다.

**주요 Output 플러그인**:
- `elasticsearch`: Elasticsearch로 전송
- `file`: 파일로 저장
- `kafka`: Kafka로 전송
- `stdout`: 콘솔 출력 (디버깅용)

### Logstash 설치 및 구성

#### 설치

```bash
# Ubuntu/Debian
wget https://artifacts.elastic.co/downloads/logstash/logstash-9.1.4-amd64.deb
sudo dpkg -i logstash-9.1.4-amd64.deb
```

#### 기본 파이프라인 예시

**Apache 로그 처리 파이프라인** (`/etc/logstash/conf.d/apache.conf`):

```ruby
# ========== Input ==========
input {
  beats {
    port => 5044
    type => "apache"
  }
}

# ========== Filter ==========
filter {
  if [type] == "apache" {
    grok {
      match => {
        "message" => "%{COMBINEDAPACHELOG}"
      }
    }

    # 날짜 파싱
    date {
      match => [ "timestamp", "dd/MMM/yyyy:HH:mm:ss Z" ]
      target => "@timestamp"
    }

    # GeoIP 정보 추가
    geoip {
      source => "clientip"
      target => "geoip"
    }

    # User-Agent 파싱
    useragent {
      source => "agent"
      target => "useragent"
    }

    # 불필요한 필드 제거
    mutate {
      remove_field => [ "message", "agent" ]
    }
  }
}

# ========== Output ==========
output {
  elasticsearch {
    hosts => ["localhost:9200"]
    index => "apache-logs-%{+YYYY.MM.dd}"
    user => "elastic"
    password => "your-password"
  }

  # 디버깅용 (개발 환경)
  stdout {
    codec => rubydebug
  }
}
```

**JSON 로그 처리 파이프라인** (`/etc/logstash/conf.d/app.conf`):

```ruby
input {
  http {
    port => 8080
    codec => json
  }
}

filter {
  # JSON 필드 파싱
  json {
    source => "message"
    target => "parsed"
  }

  # 타임스탬프 변환
  date {
    match => [ "[parsed][timestamp]", "ISO8601" ]
  }

  # 조건부 필터링
  if [parsed][level] == "ERROR" {
    mutate {
      add_tag => [ "error" ]
    }
  }

  # 필드 재구성
  mutate {
    rename => {
      "[parsed][userId]" => "user_id"
      "[parsed][sessionId]" => "session_id"
    }
    add_field => {
      "service" => "backend-api"
      "environment" => "production"
    }
  }
}

output {
  elasticsearch {
    hosts => ["localhost:9200"]
    index => "app-logs-%{+YYYY.MM.dd}"
    user => "elastic"
    password => "your-password"
  }
}
```

**출처**:
- [Logstash Configuration Examples | Elastic Docs](https://www.elastic.co/guide/en/logstash/current/config-examples.html)
- [How Logstash Works | Elastic Docs](https://www.elastic.co/guide/en/logstash/current/pipeline.html)

#### Logstash 시작

```bash
# 설정 파일 테스트
sudo /usr/share/logstash/bin/logstash -f /etc/logstash/conf.d/apache.conf --config.test_and_exit

# Logstash 시작
sudo systemctl start logstash
sudo systemctl enable logstash

# 상태 확인
sudo systemctl status logstash

# 로그 확인
sudo tail -f /var/log/logstash/logstash-plain.log
```

### 멀티 파이프라인 구성

`/etc/logstash/pipelines.yml`:

```yaml
# 여러 파이프라인 동시 실행
- pipeline.id: apache-pipeline
  path.config: "/etc/logstash/conf.d/apache.conf"
  pipeline.workers: 2

- pipeline.id: app-pipeline
  path.config: "/etc/logstash/conf.d/app.conf"
  pipeline.workers: 4
```

**출처**: [Logstash Multiple Pipeline Configuration | Medium](https://medium.com/@0ccupi3R/logstash-multiple-pipeline-configuration-8bf9eef587ee)

## Elasticsearch - 로그 저장 및 검색

Elasticsearch는 분산형 검색 및 분석 엔진으로, ELK Stack의 핵심입니다.

### 클러스터 아키텍처

#### 노드 역할

| 노드 유형 | 역할 | 설정 |
|----------|------|------|
| **Master Node** | 클러스터 관리, 메타데이터 관리 | `node.master: true`<br>`node.data: false` |
| **Data Node** | 데이터 저장, 검색, 집계 | `node.master: false`<br>`node.data: true` |
| **Coordinating Node** | 요청 라우팅, 결과 집계 | `node.master: false`<br>`node.data: false` |
| **Ingest Node** | 데이터 전처리 | `node.ingest: true` |

**출처**:
- [Node roles | Elastic Docs](https://www.elastic.co/docs/deploy-manage/distributed-architecture/clusters-nodes-shards/node-roles)
- [Understanding Elasticsearch Node Types | Instaclustr](https://www.instaclustr.com/blog/understanding-and-configuring-elasticsearch-node-types/)

#### 데이터 티어 아키텍처

```
Hot Tier (최근 1개월) → Warm Tier (1-6개월) → Cold Tier (6-12개월) → Frozen Tier (아카이브)
```

- **Hot**: 활발한 읽기/쓰기, SSD
- **Warm**: 읽기 전용, SSD/HDD
- **Cold**: 드문 검색, HDD
- **Frozen**: 장기 보관, 저렴한 스토리지

### Elasticsearch 설치 및 구성

#### 설치

```bash
# Ubuntu/Debian
wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-9.1.4-amd64.deb
sudo dpkg -i elasticsearch-9.1.4-amd64.deb
```

#### 기본 설정 (/etc/elasticsearch/elasticsearch.yml)

```yaml
# ========== Cluster ==========
cluster.name: production-elk
node.name: node-1

# ========== Paths ==========
path.data: /var/lib/elasticsearch
path.logs: /var/log/elasticsearch

# ========== Network ==========
network.host: 0.0.0.0
http.port: 9200

# ========== Discovery ==========
discovery.type: single-node  # 단일 노드 (개발용)

# 프로덕션 클러스터 (3개 마스터 노드)
# discovery.seed_hosts: ["node-1:9300", "node-2:9300", "node-3:9300"]
# cluster.initial_master_nodes: ["node-1", "node-2", "node-3"]

# ========== Security (8.x부터 필수) ==========
xpack.security.enabled: true
xpack.security.enrollment.enabled: true

xpack.security.http.ssl:
  enabled: true
  keystore.path: certs/http.p12

xpack.security.transport.ssl:
  enabled: true
  verification_mode: certificate
  keystore.path: certs/transport.p12
  truststore.path: certs/transport.p12

# ========== JVM Heap 설정 ==========
# /etc/elasticsearch/jvm.options
# -Xms4g  # 최소 힙: 물리 메모리의 50%
# -Xms4g  # 최대 힙: 최소와 동일하게 설정
```

#### Elasticsearch 시작

```bash
# Elasticsearch 시작
sudo systemctl start elasticsearch
sudo systemctl enable elasticsearch

# 상태 확인
sudo systemctl status elasticsearch

# 클러스터 상태 확인
curl -X GET "localhost:9200/_cluster/health?pretty"

# 노드 정보 확인
curl -X GET "localhost:9200/_cat/nodes?v"
```

### Index Lifecycle Management (ILM)

로그 데이터의 수명 주기를 자동 관리합니다.

#### ILM 정책 생성

```json
PUT _ilm/policy/logs-policy
{
  "policy": {
    "phases": {
      "hot": {
        "min_age": "0ms",
        "actions": {
          "rollover": {
            "max_size": "50GB",
            "max_age": "1d",
            "max_docs": 10000000
          },
          "set_priority": {
            "priority": 100
          }
        }
      },
      "warm": {
        "min_age": "7d",
        "actions": {
          "shrink": {
            "number_of_shards": 1
          },
          "forcemerge": {
            "max_num_segments": 1
          },
          "set_priority": {
            "priority": 50
          }
        }
      },
      "cold": {
        "min_age": "30d",
        "actions": {
          "set_priority": {
            "priority": 0
          }
        }
      },
      "delete": {
        "min_age": "90d",
        "actions": {
          "delete": {}
        }
      }
    }
  }
}
```

**출처**: [Index lifecycle management | Elastic Docs](https://www.elastic.co/docs/manage-data/lifecycle/index-lifecycle-management)

## Kibana - 시각화 및 분석

Kibana는 Elasticsearch 데이터를 시각화하고 탐색하는 UI를 제공합니다.

### Kibana 설치 및 구성

#### 설치

```bash
wget https://artifacts.elastic.co/downloads/kibana/kibana-9.1.4-amd64.deb
sudo dpkg -i kibana-9.1.4-amd64.deb
```

#### 기본 설정 (/etc/kibana/kibana.yml)

```yaml
# ========== Server ==========
server.port: 5601
server.host: "0.0.0.0"
server.name: "kibana-server"

# ========== Elasticsearch ==========
elasticsearch.hosts: ["https://localhost:9200"]
elasticsearch.username: "kibana_system"
elasticsearch.password: "your-password"
elasticsearch.ssl.certificateAuthorities: ["/etc/kibana/certs/ca.crt"]

# ========== Security ==========
xpack.security.enabled: true
xpack.security.encryptionKey: "something_at_least_32_characters_long"

# ========== Monitoring ==========
monitoring.enabled: true
```

#### Kibana 시작

```bash
sudo systemctl start kibana
sudo systemctl enable kibana

# 상태 확인
sudo systemctl status kibana

# 웹 접속
# http://your-server:5601
```

### Kibana 주요 기능

#### 1. Discover - 로그 검색

- 실시간 로그 검색
- KQL (Kibana Query Language) 사용
- 시간 범위 필터링

**KQL 예시**:
```
# 에러 로그만 검색
level: "ERROR"

# 특정 사용자 로그
user_id: "user-123" AND status: 500

# 범위 검색
response_time > 1000

# 와일드카드
message: *timeout*
```

#### 2. Visualizations - 시각화

**주요 시각화 타입**:
- Line Chart: 시간별 트렌드
- Bar Chart: 카테고리별 비교
- Pie Chart: 비율 표시
- Heat Map: 패턴 분석
- Data Table: 집계 데이터
- Metric: 단일 숫자 표시
- Tag Cloud: 키워드 빈도

#### 3. Dashboard - 대시보드

여러 시각화를 조합하여 종합적인 뷰 생성

**대시보드 생성 단계**:
1. Navigate to Dashboard → Create dashboard
2. Add 버튼 클릭하여 기존 시각화 추가
3. 시각화 배치 및 크기 조정
4. 저장

**출처**:
- [How To Use Kibana Dashboards and Visualizations | DigitalOcean](https://www.digitalocean.com/community/tutorials/how-to-use-kibana-dashboards-and-visualizations)
- [Kibana Dashboard Tutorial | DevOpsCube](https://devopscube.com/kibana-dashboard-tutorial/)

#### 4. Alerting - 알림

특정 조건에서 알림 발송

```json
{
  "name": "High Error Rate Alert",
  "schedule": {
    "interval": "5m"
  },
  "conditions": [
    {
      "type": "query",
      "query": "level:ERROR",
      "timeWindow": "5m",
      "threshold": 100
    }
  ],
  "actions": [
    {
      "type": "email",
      "to": ["ops@example.com"],
      "subject": "High error rate detected"
    }
  ]
}
```

## 실전 구성 예시

### Docker Compose를 사용한 ELK Stack 구성

```yaml
version: '3.8'

services:
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:9.1.4
    container_name: elasticsearch
    environment:
      - node.name=es01
      - cluster.name=elk-cluster
      - discovery.type=single-node
      - "ES_JAVA_OPTS=-Xms2g -Xmx2g"
      - xpack.security.enabled=true
      - ELASTIC_PASSWORD=changeme
    volumes:
      - esdata:/usr/share/elasticsearch/data
    ports:
      - "9200:9200"
    networks:
      - elk

  logstash:
    image: docker.elastic.co/logstash/logstash:9.1.4
    container_name: logstash
    volumes:
      - ./logstash/pipeline:/usr/share/logstash/pipeline
      - ./logstash/config/logstash.yml:/usr/share/logstash/config/logstash.yml
    ports:
      - "5044:5044"
      - "9600:9600"
    environment:
      - "LS_JAVA_OPTS=-Xms1g -Xmx1g"
    networks:
      - elk
    depends_on:
      - elasticsearch

  kibana:
    image: docker.elastic.co/kibana/kibana:9.1.4
    container_name: kibana
    ports:
      - "5601:5601"
    environment:
      - ELASTICSEARCH_HOSTS=http://elasticsearch:9200
      - ELASTICSEARCH_USERNAME=elastic
      - ELASTICSEARCH_PASSWORD=changeme
    networks:
      - elk
    depends_on:
      - elasticsearch

  filebeat:
    image: docker.elastic.co/beats/filebeat:9.1.4
    container_name: filebeat
    user: root
    volumes:
      - ./filebeat/filebeat.yml:/usr/share/filebeat/filebeat.yml:ro
      - /var/lib/docker/containers:/var/lib/docker/containers:ro
      - /var/run/docker.sock:/var/run/docker.sock:ro
    command: filebeat -e -strict.perms=false
    networks:
      - elk
    depends_on:
      - elasticsearch

volumes:
  esdata:
    driver: local

networks:
  elk:
    driver: bridge
```

**출처**: [Deploying ELK Stack with Docker Compose 2025 | IPNET](https://ipnet.xyz/2025/06/deploying-elk-stack-with-docker-compose-2025-edition/)

## Best Practices

### 1. 아키텍처 설계

✅ **Do:**
- 프로덕션에서 최소 3개의 마스터 노드 사용
- 데이터 노드와 마스터 노드 분리
- 로드 밸런서 뒤에 Coordinating 노드 배치
- 데이터 티어 아키텍처 구현 (Hot/Warm/Cold)

### 2. 보안

✅ **Do:**
- TLS/SSL 필수 활성화 (Elasticsearch 8.x부터 기본)
- RBAC (Role-Based Access Control) 구현
- 최소 권한 원칙 적용
- API 키 사용
- 정기적인 보안 업데이트

**출처**: [Building a Scalable & Secure ELK Stack Infrastructure | DEV](https://dev.to/chaira/building-a-scalable-secure-elk-stack-infrastructure-a-practical-guide-37hb)

### 3. 성능 최적화

✅ **Do:**
- JVM 힙 크기를 물리 메모리의 50%로 설정 (최대 31GB)
- ILM 정책으로 오래된 데이터 자동 관리
- 샤드 크기 10-50GB 유지
- 불필요한 필드 인덱싱 비활성화
- Bulk API 사용 (개별 요청 대신)

**출처**: [7 Ways to Optimize Elastic Stack | Better Stack](https://betterstack.com/community/guides/scaling-elastic-stack/optimize-elastic-stack/)

### 4. 모니터링

✅ **Do:**
- ELK Stack 자체 모니터링 (별도 모니터링 시스템)
- Metricbeat으로 클러스터 메트릭 수집
- JVM 힙 사용률 모니터링
- 디스크 공간 경고 설정
- 인덱싱 및 검색 레이턴시 추적

### 5. 데이터 관리

✅ **Do:**
- 인덱스 명명 규칙 일관성 유지
- ILM으로 자동 롤오버 및 삭제
- 백업 정책 수립 (스냅샷)
- 복제본(replica) 설정 (최소 1개)

```json
PUT /logs-2025.10.06
{
  "settings": {
    "number_of_shards": 3,
    "number_of_replicas": 1,
    "index.lifecycle.name": "logs-policy",
    "index.lifecycle.rollover_alias": "logs"
  }
}
```

## 다음 단계

- [컴포넌트별 상세 프로세스](./03-컴포넌트별-상세-프로세스.md)에서 각 구성 요소를 더 깊이 학습

---

**주요 참고 자료**:
- [The Complete Guide to the ELK Stack | Logz.io](https://logz.io/learn/complete-guide-elk-stack/)
- [The Definitive Guide to the ELK Stack in 2025](https://prepare.sh/articles/the-definitive-guide-to-the-elk-stack-in-2025-from-zero-to-production-ready-observability)
- [Elastic Stack Official Documentation](https://www.elastic.co/elastic-stack)
- [Filebeat Installation | Elastic Docs](https://www.elastic.co/docs/reference/beats/filebeat/filebeat-installation-configuration)
- [Metricbeat Installation | Elastic Docs](https://www.elastic.co/docs/reference/beats/metricbeat/metricbeat-installation-configuration)

**최종 업데이트**: 2025-10-06
