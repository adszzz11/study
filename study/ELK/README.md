# ELK Stack 스터디 가이드

> 최종 업데이트: 2025-10-06
>
> 이 문서는 ELK Stack (Elasticsearch, Logstash, Kibana)의 최신 정보를 바탕으로 작성되었습니다.

## 목차

1. [개요](#개요)
2. [최신 버전 정보](#최신-버전-정보)
3. [학습 로드맵](#학습-로드맵)
4. [문서 구조](#문서-구조)

## 개요

ELK Stack은 Elasticsearch, Logstash, Kibana의 세 가지 오픈소스 프로젝트로 구성된 강력한 로그 관리 및 분석 플랫폼입니다. 현재는 Beats를 포함하여 **Elastic Stack**으로 불리고 있습니다.

### 핵심 구성 요소

- **Elasticsearch**: 분산형 검색 및 분석 엔진
- **Logstash**: 서버 측 데이터 처리 파이프라인
- **Kibana**: 데이터 시각화 및 탐색 도구
- **Beats**: 경량 데이터 수집기 (Filebeat, Metricbeat 등)

## 최신 버전 정보

### 현재 버전 (2025년 10월 기준)

- **최신 안정 버전**: 9.1.4 (2025년 9월 18일 릴리스)
- **지원 버전**: 8.x, 9.x

### 주요 신기능 (Elasticsearch 9.x)

#### 1. Better Binary Quantization (BBQ)
- OpenSearch 대비 **5배 빠른 성능**
- 메모리 사용량 **95% 이상 감소**
- 버전 9.1부터 기본 활성화

#### 2. AI 및 시맨틱 검색
- `semantic_text` 필드 타입 GA (Generally Available)
- ColPali, ColBERT 등 멀티스테이지 모델 지원
- `rank_vectors` 새 필드 타입 (실험적 기능)

#### 3. ES|QL 개선사항
- LOOKUP JOIN 기술 프리뷰
- 점수 매기기 및 시맨틱 검색 지원
- KQL 함수 추가

#### 4. ACORN 알고리즘
- 필터링된 벡터 검색 최적화
- 기존 대비 **최대 5배 빠른** 필터링 검색

#### 5. 보안 기능
- 버전 8.0부터 **기본적으로 보안 활성화**
- TLS, RBAC 필수 설정

## 학습 로드맵

```
1단계: 기초 개념 이해
   ↓
2단계: Client 관점 학습 (로그 생성 및 전송)
   ↓
3단계: Server 관점 학습 (수집, 저장, 분석)
   ↓
4단계: 컴포넌트별 심화 학습
   ↓
5단계: 프로덕션 환경 구성
```

## 문서 구조

### 1. [Client 관점](./01-Client-관점.md)
클라이언트 애플리케이션에서 ELK로 로그를 전송하는 방법

- 웹 브라우저 (JavaScript, React, Vue, Angular)
- 모바일 애플리케이션 (iOS, Android)
- 데스크톱 애플리케이션
- 로그 전송 아키텍처 및 Best Practices

### 2. [Server 관점](./02-Server-관점.md)
서버 측에서 로그를 수집, 처리, 저장하는 방법

- Beats를 통한 로그 수집
- Logstash 파이프라인 구성
- Elasticsearch 클러스터 아키텍처
- Kibana 대시보드 및 시각화

### 3. [컴포넌트별 상세 프로세스](./03-컴포넌트별-상세-프로세스.md)
각 구성 요소의 동작 원리와 상세 설정

- Elasticsearch 아키텍처 (노드, 클러스터, 샤드)
- Logstash 파이프라인 (Input, Filter, Output)
- Beats 종류별 설정
- Kibana 고급 기능
- Index Lifecycle Management (ILM)
- 보안 및 성능 최적화

## 주요 참고 자료

### 공식 문서
- [Elastic Stack 공식 사이트](https://www.elastic.co/elastic-stack)
- [Elasticsearch 공식 문서](https://www.elastic.co/guide/en/elasticsearch/reference/current/index.html)
- [Logstash 공식 문서](https://www.elastic.co/guide/en/logstash/current/index.html)
- [Kibana 공식 문서](https://www.elastic.co/guide/en/kibana/current/index.html)
- [Beats 공식 문서](https://www.elastic.co/guide/en/beats/libbeat/current/index.html)

### 릴리스 정보
- [Elasticsearch 9.1 릴리스 노트](https://www.elastic.co/blog/whats-new-elastic-9-1-0)
- [Elasticsearch 9.0 릴리스 노트](https://www.elastic.co/blog/whats-new-elastic-search-9-0-0)
- [Past Releases](https://www.elastic.co/downloads/past-releases)

### 커뮤니티 및 튜토리얼
- [The Complete Guide to the ELK Stack | Logz.io](https://logz.io/learn/complete-guide-elk-stack/)
- [The Definitive Guide to the ELK Stack in 2025](https://prepare.sh/articles/the-definitive-guide-to-the-elk-stack-in-2025-from-zero-to-production-ready-observability)
- [AWS - What is the ELK stack?](https://aws.amazon.com/what-is/elk-stack/)

## 시작하기

1. **먼저 읽기**: [Client 관점](./01-Client-관점.md) 문서를 읽고 로그가 어떻게 생성되고 전송되는지 이해합니다.
2. **서버 구성**: [Server 관점](./02-Server-관점.md) 문서를 읽고 ELK Stack을 설치하고 구성합니다.
3. **심화 학습**: [컴포넌트별 상세 프로세스](./03-컴포넌트별-상세-프로세스.md)를 통해 각 구성 요소를 깊이 이해합니다.

---

**작성 일자**: 2025-10-06
**작성자**: Claude Code
**버전**: 1.0
