---
date:
event: AWS Network Service 톺아보기
speaker:
tags:
  - conference
  - aws
  - network
  - vpc
  - infrastructure
type: conference-note
---

# AWS Network Service 톺아보기

## 📋 이벤트 정보

- **이벤트명**: AWS Network Service 톺아보기 Conference
- **발표자**: (미기재)
- **일시**: (미기재)
- **장소**: (미기재)
- **발표 주제**: AWS 네트워크 서비스의 핵심 개념과 구성요소

---

## 🎯 핵심 내용

### AWS Region과 가용영역

**물리적 위치:**
- Region: 지리적으로 분리된 AWS 인프라의 묶음
- 가용영역(AZ): Region 내의 물리적으로 분리된 데이터센터

### AWS VPC, Subnet, Routing Table

#### VPC (Virtual Private Cloud)
- **사설망**: AWS 클라우드 내 논리적으로 격리된 네트워크
- 사용자가 정의한 가상 네트워크 환경

#### Subnet (서브넷)
- **부분망**: VPC 내의 IP 주소 범위
- Public/Private Subnet으로 구분
- 특정 가용영역에 속함

#### Routing Table
- **트래픽 경로**: 네트워크 트래픽이 향하는 위치 결정
- Subnet과 연결되어 트래픽 라우팅 규칙 정의

### 보안 및 트래픽 제어

#### NACL (Network Access Control List)
- **Subnet 단위 트래픽 제어**
- **Stateless**: 인바운드/아웃바운드 규칙을 각각 설정해야 함
- **단점**: Unknown Port를 열어야 함 (응답 트래픽 처리)
- ACL 방식으로 트래픽 허용/거부 설정

#### Security Group
- **Service 트래픽 제어**: 인스턴스 레벨의 가상 방화벽
- **Stateful**: 인바운드 허용 시 아웃바운드 응답 자동 허용
- 트래픽 **허용**만 가능 (거부 규칙 없음)
- 인바운드, 아웃바운드 트래픽 규칙 정의

### Gateway

#### Internet Gateway
- **VPC - Internet 간 통신** 담당
- Public Subnet의 인스턴스가 인터넷과 통신할 수 있게 함
- Routing Table의 목적지로 설정

#### NAT Gateway
- **Private 서브넷의 아웃바운드 통신**을 가능하게 함
- Private 서브넷의 인스턴스가 인터넷으로 나가는 트래픽 허용
- 인바운드 트래픽은 차단 (보안)
- Public Subnet에 배치됨

---

## 💡 인사이트 & 배운 점

- **NACL vs Security Group 차이**:
	- NACL은 Stateless, Security Group은 Stateful
	- NACL은 Subnet 레벨, Security Group은 인스턴스 레벨
- **NAT Gateway의 중요성**:
	- Private 서브넷이 외부 패키지를 다운로드하거나 업데이트할 때 필수
- **보안의 계층화**:
	- NACL과 Security Group을 함께 사용하여 다층 보안 구현 가능

---

## ❓ 질의응답 (Q&A)

(기록 없음)

---

## 🔗 참고 자료

- [AWS VPC 공식 문서](https://docs.aws.amazon.com/vpc/)
- [AWS Networking & Content Delivery](https://aws.amazon.com/products/networking/)

---

## 💭 개인 회고

### 인상 깊었던 점

- Stateful vs Stateless 개념이 보안 그룹과 NACL의 핵심 차이
- Private 서브넷의 아웃바운드 전용 통신을 위한 NAT Gateway 설계

### 적용해볼 점

- VPC 설계 시 Public/Private Subnet 분리 전략
- 보안 그룹과 NACL을 활용한 다층 방어 구성
- NAT Gateway를 활용한 Private 인스턴스의 안전한 인터넷 접근

### 추가 학습이 필요한 부분

- VPC Peering과 Transit Gateway
- VPC Endpoint (PrivateLink)
- Route 53과의 통합
- VPC Flow Logs를 활용한 네트워크 모니터링

---

## 📌 TODO

- [ ] AWS VPC 실습 환경 구성해보기
- [ ] Public/Private Subnet 분리한 3-tier 아키텍처 설계
- [ ] Security Group과 NACL 규칙 작성 연습
- [ ] NAT Gateway vs NAT Instance 비교 분석
