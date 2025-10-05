---
date:
event: Prometheus Operator 세미나
speaker:
tags:
  - conference
  - kubernetes
  - prometheus
  - monitoring
  - devops
  - helm
type: conference-note
---

# Use Helm to deploy Prometheus Operator

## 📋 이벤트 정보

- **이벤트명**: Prometheus Operator 세미나
- **발표자**: (미기재)
- **일시**: (미기재)
- **장소**: (미기재)
- **발표 주제**: Helm을 활용한 Prometheus Operator 배포 및 모니터링 시스템 구축

---

## 🎯 핵심 내용

### 모니터링(Monitoring)이란?

**정의:** 시스템에 관련된 정량적 수치를 수집, 처리, 집계, 보여주는 행위

**관점:**
- **서비스 관점**: 지연시간, 트래픽, 에러, 포화도
- **시스템 관점**: 사용률, 포화도, 에러
- 사용자에 따라 다양한 관점 존재

#### 모니터링의 구성요소
- **Metrics**: 수치 데이터
- **Logging**: 로그 데이터
- **Tracing**: 분산 추적
- **Alerting**: 경고 알림
- **Visualization**: 시각화

**Observability (관측 가능성)**: 모니터링을 통해 시스템 상태를 이해하고 파악하는 능력

---

### Prometheus

**특징:**
- **Time-series based**: 시계열 데이터베이스 기반
- **Open-source**: 오픈소스
- **CNCF Graduated Project**

**주요 기능:**
- **Service Discovery**: 자동 서비스 탐지
- **Alert**: AlertManager를 통한 알림
- **Visualization**: Grafana 연동

**핵심 컴포넌트:**
- **Multi-dimensional data model**: 다차원 데이터 모델
- **PromQL**: 유연한 쿼리 언어
- **Pull over HTTP**: HTTP를 통한 메트릭 수집 (Pull 방식)
- **Push Gateway**: Push 방식 지원 (선택적)
- **Service Discovery or Static configuration**: 동적/정적 설정 지원
- **Multiple modes of graphing and dashboarding support**: 다양한 시각화 지원

#### TSDB (Time Series Database)
- **2-hour Memory**: 2시간 동안 메모리에 데이터 보관
- 이후 디스크로 저장

---

### Prometheus 아키텍처

#### Exporter
- **서비스나 앱에서 데이터 수집**
- **Prometheus 형식으로 HTTP를 통해 노출**
- 다양한 Exporter 존재 (Node Exporter, MySQL Exporter 등)

#### AlertManager
- **생성 조건에 의해 트리거 알림** (무료)
- 알림 그룹화, 중복 제거, 라우팅 기능

#### Visualization

**API:**
- PromQL 쿼리를 통해 원시 데이터 제공

**WEB-GUI (Prometheus Console):**
- 2종류의 내부 시각화 컴포넌트 제공
- PromQL 쿼리 시각화

**Grafana:**
- 다양한 데이터소스 대상으로 시각화 가능
- 다양한 플러그인 지원
- Alert 무료
- **Grafana Labs를 통한 다양한 Dashboard 템플릿 제공**

---

## Kubernetes

### Control Plane Components

**주요 컴포넌트:**
- **kube-apiserver**
	- 자체적인 DNS와 네트워크 구성으로 서비스 통신
	- 로드밸런싱
- **etcd**
	- Cluster data 저장
- **kube-scheduler**
	- Pod 스케줄링
- **kube-controller-manager**
	- 컨트롤러 관리
- **cloud-controller-manager**
	- 클라우드 제공자와의 통합

---

## EKS (Elastic Kubernetes Service)

**정의:** AWS에서 제공하는 관리형 Kubernetes 서비스

**특징:**
- **Control Plane 역할을 AWS가 대신 관리**
- **무중단 보장**
- **ECR, ELB, IAM, VPC와의 유연한 연동**
- **Upgradable**: 쉬운 버전 업그레이드

---

## Helm

**공식 사이트:** https://helm.sh

**정의:** Kubernetes를 위한 Package Manager (쿠버네티스 허브 느낌)

### Package Manager란?
특정 패키지를 다루는 작업을 편리하고 안전하게 수행하기 위한 툴

**장점:**
- 설치, 업데이트, 수정, 삭제 용이
- Dependency 관리 편리함

### Helm의 장점
- **CNCF GRADUATED**
- **Manage Complexity**: 복잡성 관리
- **Easy Updates**: 쉬운 업데이트
- **Simple Sharing**: 간편한 공유
- **Rollbacks**: 롤백 지원

### Helm Chart 구조
YAML 형식의 Chart 사용
- **Chart.yaml**: Chart 메타데이터
- **charts/**: 의존성 Chart
- **Templates**: Kubernetes 리소스 템플릿
- **Values.yaml**: 설정 값

---

## Prometheus Operator

### Operator란?
**Kubernetes에서 Prometheus의 관리를 제공**
- 간편한 스택 구성
- 자동화 제공
- **CRDs(Custom Resource Definitions)를 손쉽게 적용**

### Prometheus Operator의 이점
- **Kubernetes Custom Resources**: 커스텀 리소스 활용
- **Simplified Deployment Configuration**: 간소화된 배포 설정
- **Prometheus Target Configuration**: 타겟 설정 간편화

### 배포 옵션

**1. Prometheus Operator (공식)**
- 기본 Operator만 제공

**2. kube-prometheus**
- 클러스터링 목적
- HA(High Availability) 지원
- Prometheus Operator 포함됨

**3. Community Helm Chart**
- 유저가 많이 쓰는 설정 적재
- Helm을 통한 쉬운 배포
- 가장 대중적

---

## 💡 인사이트 & 배운 점

- **Prometheus의 Pull 방식**:
	- 서비스가 메트릭을 노출하고, Prometheus가 주기적으로 수집
	- Push 방식보다 관리가 용이
- **Grafana의 강력함**:
	- 다양한 템플릿을 통해 빠른 대시보드 구성
	- 무료 Alert 기능
- **Helm의 필요성**:
	- Kubernetes 리소스 관리의 복잡성 해결
	- 버전 관리와 롤백이 쉬움

---

## ❓ 질의응답 (Q&A)

(기록 없음)

---

## 🔗 참고 자료

- [Prometheus 공식 문서](https://prometheus.io/docs/)
- [Helm 공식 사이트](https://helm.sh)
- [Prometheus Operator GitHub](https://github.com/prometheus-operator/prometheus-operator)
- [Grafana 공식 사이트](https://grafana.com/)
- [악분 일상 YouTube](https://www.youtube.com/c/악분일상)

---

## 💭 개인 회고

### 인상 깊었던 점

- Prometheus Operator가 CRDs를 통해 Kubernetes Native하게 동작
- Helm Chart를 통한 배포 자동화의 편리함
- Grafana Labs의 커뮤니티 대시보드 템플릿 활용

### 적용해볼 점

- EKS 환경에서 Helm으로 Prometheus Operator 배포
- Node Exporter, kube-state-metrics 등 기본 Exporter 설정
- Grafana 대시보드 구성 및 Alert 설정

### 추가 학습이 필요한 부분

- PromQL 쿼리 작성법
- ServiceMonitor, PodMonitor 설정
- AlertManager 알림 라우팅 설정
- Thanos를 활용한 장기 메트릭 저장
- Grafana Loki를 활용한 로그 통합

---

## 📌 TODO

- [ ] Prometheus Operator Helm Chart 설치 실습
- [ ] PromQL 기본 쿼리 학습
- [ ] Grafana Dashboard 템플릿 탐색 및 커스터마이징
- [ ] AlertManager 알림 설정 (Slack 연동)
- [ ] Custom Exporter 작성 (애플리케이션 메트릭)
