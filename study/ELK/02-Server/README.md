# Server 관점 - 개요

> 최종 업데이트: 2025-10-06

서버 측에서 로그를 수집, 처리, 저장, 시각화하는 전체 ELK Stack 아키텍처와 구성 방법을 다룹니다.

## 📚 목차

1. [Beats 설치 및 구성](./01-Beats-설치-및-구성.md)
   - Filebeat: 로그 파일 수집
   - Metricbeat: 시스템 메트릭 수집

2. [Logstash 파이프라인](./02-Logstash-파이프라인.md)
   - Input, Filter, Output 플러그인
   - 파이프라인 설정 및 최적화

3. [Elasticsearch 설치 및 구성](./03-Elasticsearch-설치-및-구성.md)
   - 클러스터 아키텍처
   - 인덱스 관리
   - ILM 정책

4. [Kibana 시각화](./04-Kibana-시각화.md)
   - 대시보드 생성
   - 시각화 도구
   - 알림 설정

## 전체 아키텍처

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

### 프로덕션 아키텍처

```
┌─────────────────────────────────────┐
│         로그 소스 (서버들)            │
│  Web, App, DB, Backend Servers     │
└────────────┬────────────────────────┘
             ▼
   ┌──────────────────┐
   │   Beats Layer    │
   │ Filebeat/Metric  │
   └────────┬─────────┘
            ▼
   ┌──────────────────┐
   │    Logstash      │ (선택적)
   │  Parsing/Filter  │
   └────────┬─────────┘
            ▼
   ┌──────────────────┐
   │  Elasticsearch   │
   │     Cluster      │
   └────────┬─────────┘
            ▼
   ┌──────────────────┐
   │     Kibana       │
   │  Visualization   │
   └──────────────────┘
```

## 최신 아키텍처 트렌드 (2025)

### 1. Beats → Elasticsearch 직접 전송

단순한 로그의 경우 Logstash를 생략하고 Beats에서 Elasticsearch로 직접 전송:

```
Filebeat → Elasticsearch → Kibana
```

**장점**:
- 단순한 아키텍처
- 낮은 리소스 사용
- 빠른 구성

**단점**:
- 복잡한 파싱 불가
- 변환 기능 제한

### 2. Logstash 대체

Fluentd, Vector 등 경량 대안 사용:

```
Filebeat → Fluentd → Elasticsearch → Kibana
```

**출처**: [The Complete Guide to the ELK Stack | Logz.io](https://logz.io/learn/complete-guide-elk-stack/)

## 구성 요소별 역할

### Beats
- **역할**: 로그 및 메트릭 수집
- **특징**: 경량, 낮은 리소스 사용
- **종류**: Filebeat, Metricbeat, Packetbeat 등

### Logstash
- **역할**: 데이터 파싱, 변환, 필터링
- **특징**: 강력한 파싱 기능, 다양한 플러그인
- **용도**: 복잡한 로그 처리

### Elasticsearch
- **역할**: 데이터 저장, 검색, 집계
- **특징**: 분산 아키텍처, 실시간 검색
- **핵심**: ELK Stack의 중심

### Kibana
- **역할**: 데이터 시각화, 대시보드
- **특징**: 직관적 UI, 다양한 시각화 도구
- **용도**: 로그 분석, 모니터링

## 설치 순서

### 권장 설치 순서

1. **Elasticsearch** (먼저)
   - 데이터 저장소이므로 먼저 구성
   - 클러스터 설정 및 보안 구성

2. **Kibana**
   - Elasticsearch 연결
   - 대시보드 및 인덱스 패턴 설정

3. **Logstash** (선택적)
   - 복잡한 파싱이 필요한 경우
   - Elasticsearch 연결 테스트

4. **Beats** (마지막)
   - 각 서버에 설치
   - Elasticsearch 또는 Logstash로 전송

## 빠른 시작

### Docker Compose로 시작하기

```bash
# ELK Stack 전체를 Docker로 실행
git clone https://github.com/deviantony/docker-elk.git
cd docker-elk
docker-compose up -d
```

### 개별 설치

각 컴포넌트별 상세 가이드:

1. [Beats 설치 및 구성](./01-Beats-설치-및-구성.md)
2. [Logstash 파이프라인](./02-Logstash-파이프라인.md)
3. [Elasticsearch 설치 및 구성](./03-Elasticsearch-설치-및-구성.md)
4. [Kibana 시각화](./04-Kibana-시각화.md)

## 다음 단계

- 먼저 [Elasticsearch 설치 및 구성](./03-Elasticsearch-설치-및-구성.md)부터 시작하는 것을 권장합니다
- 그 다음 [Kibana 시각화](./04-Kibana-시각화.md)를 설정합니다
- 로그 수집을 위해 [Beats 설치 및 구성](./01-Beats-설치-및-구성.md)을 참조하세요
- 복잡한 파싱이 필요하면 [Logstash 파이프라인](./02-Logstash-파이프라인.md)을 확인하세요

---

**다음**: [Components 상세](../03-Components/README.md)에서 각 구성 요소의 심화 내용 학습
