### Use Helm to deploy Prometheus Operator


시스템에 관련된 정량적 수치를 수집, 처리, 집계, 보여주는 행위
서비스 관점(지연시간, 트래픽, 에러, 포화도)
시스템 관점(사용률, 포화도, 에러)
사용자에 따라



#### 모니터링의 구성요소
- Metrics
- Logging
- Tracing
- Alerting
- Visualization


Observability

Prometheus
Time-series based
Open-source
#CNCF?

Service Discovery
Alery
Visualization(Grafana)


Multi-dimensional data model
PromQL, flexible query language
Pull over HTTP
Push gateway
Service discovery or Static configuration
Multiple modes of graphing and dashboarding support

TSDB(Time Scale Database)
- 2hour memory


Exporter
서비스나 앱에서 데이터 수집
프로메테우스 형식으로 HTTP 통해 노출

AlertManager
생성 조건에 의해 트리거 알림(무료)

Visualization
API
- PromQL 쿼리를 통해 원시 데이터 제공

WEB-GUI(Prometheus console)
- 2종류의 내부 시각화 컴포넌트 제공
- PromQL 쿼리 시각화

GRAFANA
- 다양한 데이터소스 대상으로 시각화 가능
- 다양한 플러그인 지원
- Alert 무료
- Grafanalab을 통한 다양한 dashboard 탬플릿 제공

#키바나 ?

# Kubernetes

## Control Plain Components

### kube-apiserver
- 자체적인 DNS와 네트워크 구성으로 서비스 통신
- 로드밸런싱
### etcd
- cluster data
### kube-scheduler
### kube-controller-manager
### cloud-controller-manager


# EKS
AWS에서 제공하는 서비스
Control Plane 역할에 한해서 대신 해줌
- 무중단 보장
- ECR, ELB, IAM, VPC와의 유연한 연동
- Upgradable


# Helm
https://helm.sh
: 살짝 쿠버네티스.hub 느낌

Package Manager
특정 패키지를 다루는 작업을 편리하고 안전하게 수행하기 위한 툴
- 설치, 업데이트, 수정, 삭제 용이
- Dependency 관리 편리함


Helm
- CNCF GRADUATED
- Manage Complexity
- Easy Updates
- SImple SHaring
- Rollbacks

Yaml 형식의 chart 사용
- Chart.yaml, chars/
- Templates
- Values.yaml


# Prometheus Operator

## Operator
Kubernetes 에서 Prometheus의 관리 제공
간편한 스택 구성, 자동화 제공

CRDS를 손쉽게 적용할 수 있게 해줌

Kubernetes Custom Resources
Simplified Deployment Configuration
Prometheus Target Configuration


Promethus Operator
공식
kube-prometheus
클러스터링 목적
HA 지원
Prometheus operator포함됨
community helm chart
유저가 많이 쓰는 애들 적재


https://www.youtube.com/c/악분일상



