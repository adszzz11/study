# Beats 설치 및 구성

> 최종 업데이트: 2025-10-06

Beats는 경량 데이터 수집기로, 서버에서 로그와 메트릭을 수집합니다.

## Beats 종류

| Beat | 용도 | 수집 데이터 |
|------|------|-----------|
| **Filebeat** | 로그 파일 | 애플리케이션 로그, 시스템 로그 |
| **Metricbeat** | 메트릭 | CPU, 메모리, 디스크, 네트워크 |
| **Packetbeat** | 네트워크 | 네트워크 패킷, 프로토콜 분석 |
| **Winlogbeat** | Windows 이벤트 | Windows Event Log |
| **Heartbeat** | 가동시간 | 서비스 헬스체크 |
| **Auditbeat** | 감사 | 시스템 감사 로그 |

## Filebeat 설치

### Ubuntu/Debian

```bash
# 최신 버전 9.1.4 다운로드
wget https://artifacts.elastic.co/downloads/beats/filebeat/filebeat-9.1.4-amd64.deb

# 설치
sudo dpkg -i filebeat-9.1.4-amd64.deb
```

**출처**: [Filebeat Installation | Elastic Docs](https://www.elastic.co/docs/reference/beats/filebeat/filebeat-installation-configuration)

### 기본 설정

`/etc/filebeat/filebeat.yml`:

```yaml
filebeat.inputs:
- type: log
  enabled: true
  paths:
    - /var/log/*.log

output.elasticsearch:
  hosts: ["localhost:9200"]
  username: "elastic"
  password: "changeme"

setup.kibana:
  host: "localhost:5601"
```

### Filebeat 시작

```bash
sudo systemctl start filebeat
sudo systemctl enable filebeat
sudo systemctl status filebeat
```

## Metricbeat 설치

```bash
wget https://artifacts.elastic.co/downloads/beats/metricbeat/metricbeat-9.1.4-amd64.deb
sudo dpkg -i metricbeat-9.1.4-amd64.deb
```

### 기본 설정

`/etc/metricbeat/metricbeat.yml`:

```yaml
metricbeat.modules:
- module: system
  period: 10s
  metricsets:
    - cpu
    - memory
    - network

output.elasticsearch:
  hosts: ["localhost:9200"]
```

**출처**: [Metricbeat Installation | Elastic Docs](https://www.elastic.co/docs/reference/beats/metricbeat/metricbeat-installation-configuration)

---

**다음**: [Logstash 파이프라인](./02-Logstash-파이프라인.md)
