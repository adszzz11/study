# ELK Stack 스터디 가이드

> 최종 업데이트: 2025-10-06
>
> 이 문서는 ELK Stack (Elasticsearch, Logstash, Kibana)의 최신 정보를 바탕으로 작성되었습니다.

## 📚 목차

### [01. Client 관점](./01-Client/)
클라이언트 애플리케이션에서 ELK로 로그를 전송하는 방법

- [웹 브라우저 로깅](./01-Client/01-웹-브라우저-로깅.md) - React, Vue, Angular
- [모바일 애플리케이션 로깅](./01-Client/02-모바일-애플리케이션-로깅.md) - iOS, Android
- [Client Best Practices](./01-Client/03-Client-Best-Practices.md) - 보안, 성능, 데이터 품질

### [02. Server 관점](./02-Server/)
서버 측에서 로그를 수집, 처리, 저장하는 방법

- [Beats 설치 및 구성](./02-Server/01-Beats-설치-및-구성.md) - Filebeat, Metricbeat
- [Logstash 파이프라인](./02-Server/02-Logstash-파이프라인.md) - Input, Filter, Output
- [Elasticsearch 설치 및 구성](./02-Server/03-Elasticsearch-설치-및-구성.md) - 클러스터 구성
- [Kibana 시각화](./02-Server/04-Kibana-시각화.md) - 대시보드, 시각화

### [03. Components 상세](./03-Components/)
각 구성 요소의 동작 원리와 고급 기능

- [Elasticsearch 아키텍처](./03-Components/01-Elasticsearch-아키텍처.md) - 클러스터, 노드, 샤드
- [Logstash 상세](./03-Components/02-Logstash-상세.md) - 파이프라인 심화
- [Kibana 고급 기능](./03-Components/03-Kibana-고급-기능.md) - KQL, 고급 시각화
- [ILM 정책](./03-Components/04-ILM-정책.md) - 데이터 수명 주기 관리
- [보안 및 인증](./03-Components/05-보안-및-인증.md) - TLS, RBAC, API Keys
- [성능 튜닝](./03-Components/06-성능-튜닝.md) - 최적화 가이드

## 🎯 개요

### ELK Stack이란?

ELK Stack은 **Elasticsearch**, **Logstash**, **Kibana**의 세 가지 오픈소스 프로젝트로 구성된 강력한 로그 관리 및 분석 플랫폼입니다. 현재는 **Beats**를 포함하여 **Elastic Stack**으로 불리고 있습니다.

#### 핵심 구성 요소

- **Elasticsearch**: 분산형 검색 및 분석 엔진
- **Logstash**: 서버 측 데이터 처리 파이프라인
- **Kibana**: 데이터 시각화 및 탐색 도구
- **Beats**: 경량 데이터 수집기 (Filebeat, Metricbeat 등)

## 📊 최신 버전 정보 (2025-10-06 기준)

### 현재 버전

- **최신 안정 버전**: 9.1.4 (2025년 9월 18일 릴리스)
- **지원 버전**: 8.x, 9.x

### Elasticsearch 9.x 주요 신기능

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

**출처**:
- [Elasticsearch 9.1 Release Notes](https://www.elastic.co/blog/whats-new-elastic-9-1-0)
- [Elasticsearch 9.0 Release Notes](https://www.elastic.co/blog/whats-new-elastic-search-9-0-0)

## 🗺️ 학습 로드맵

```
1단계: 기초 개념 이해 (README 읽기)
   ↓
2단계: Client 관점 학습
   - 웹 브라우저 로깅
   - 모바일 앱 로깅
   - Best Practices
   ↓
3단계: Server 관점 학습
   - Elasticsearch 설치
   - Kibana 설정
   - Beats 구성
   - Logstash 파이프라인
   ↓
4단계: Components 심화 학습
   - Elasticsearch 아키텍처
   - ILM 정책
   - 보안 및 인증
   - 성능 튜닝
   ↓
5단계: 프로덕션 환경 구성
```

## 🚀 빠른 시작

### 초보자를 위한 추천 경로

1. **Client 관점** 먼저 학습
   - [웹 브라우저 로깅](./01-Client/01-웹-브라우저-로깅.md)에서 로그가 어떻게 생성되고 전송되는지 이해

2. **Server 관점** 구성
   - [Elasticsearch 설치 및 구성](./02-Server/03-Elasticsearch-설치-및-구성.md)으로 시작
   - [Kibana 시각화](./02-Server/04-Kibana-시각화.md)로 UI 설정
   - [Beats 설치 및 구성](./02-Server/01-Beats-설치-및-구성.md)으로 로그 수집

3. **심화 학습**
   - [Components 상세](./03-Components/)에서 각 구성 요소 깊이 이해

### 개발자를 위한 추천 경로

```
Client 개발자 → 01-Client → 02-Server (Elasticsearch, Kibana)
Backend 개발자 → 02-Server → 03-Components
DevOps 엔지니어 → 02-Server → 03-Components (전체)
```

## 📁 디렉터리 구조

```
study/ELK/
├── README.md                          # 이 파일 (시작점)
│
├── 01-Client/                         # 클라이언트 관점
│   ├── README.md
│   ├── 01-웹-브라우저-로깅.md
│   ├── 02-모바일-애플리케이션-로깅.md
│   └── 03-Client-Best-Practices.md
│
├── 02-Server/                         # 서버 관점
│   ├── README.md
│   ├── 01-Beats-설치-및-구성.md
│   ├── 02-Logstash-파이프라인.md
│   ├── 03-Elasticsearch-설치-및-구성.md
│   └── 04-Kibana-시각화.md
│
└── 03-Components/                     # 컴포넌트 상세
    ├── README.md
    ├── 01-Elasticsearch-아키텍처.md
    ├── 02-Logstash-상세.md
    ├── 03-Kibana-고급-기능.md
    ├── 04-ILM-정책.md
    ├── 05-보안-및-인증.md
    └── 06-성능-튜닝.md
```

## 🔑 핵심 개념

### Client vs Server 로깅

| 구분 | Client | Server |
|-----|--------|--------|
| **연결** | 백엔드 API를 통해서만 | 직접 ELK 연결 가능 |
| **네트워크** | 불안정 | 안정적 |
| **보안** | 민감 정보 필터링 필수 | 내부 네트워크 |
| **오프라인** | 로컬 버퍼링 필요 | 불필요 |

### ELK Stack 데이터 흐름

```
[Client App] → [Backend API] → [Logstash] → [Elasticsearch] → [Kibana]
                                    ↑
                                [Filebeat]
                                    ↑
                            [서버 로그 파일]
```

## 📚 주요 참고 자료

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
- [Elasticsearch Architecture | Coralogix](https://coralogix.com/guides/elasticsearch/elasticsearch-architecture-8-key-components-and-putting-them-to-work/)

## ✨ 이 가이드의 특징

✅ **2025-10-06 기준 최신 정보**
- Elasticsearch 9.1.4 버전 정보
- 최신 기능 및 Best Practices
- 2025년 블로그 및 공식 문서 참조

✅ **모든 자료에 출처 명시**
- 공식 Elastic 문서
- Stack Overflow, Medium 등 커뮤니티
- 최신 튜토리얼 및 가이드

✅ **Client/Server 관점으로 체계적 분류**
- Client: 로그 생성 및 전송
- Server: 수집, 처리, 저장, 시각화

✅ **실전 예시 코드 포함**
- React, Vue, Angular 로깅 구현
- iOS, Android 로깅 구현
- Filebeat, Logstash 설정
- Docker Compose 구성
- Elasticsearch 쿼리

✅ **가독성 중심의 구조**
- 주제별로 파일 분리
- 명확한 목차 구조
- 단계별 학습 가이드

## 💡 학습 팁

1. **순서대로 학습**: README → Client → Server → Components
2. **실습 중심**: 예제 코드를 직접 실행해보기
3. **출처 확인**: 더 깊은 학습을 위해 참고 자료 링크 활용
4. **프로덕션 준비**: Best Practices와 보안 섹션 필독

## 🔗 바로가기

### 처음 시작하는 분
1. [웹 브라우저 로깅](./01-Client/01-웹-브라우저-로깅.md) - 클라이언트에서 로그 전송하기
2. [Elasticsearch 설치](./02-Server/03-Elasticsearch-설치-및-구성.md) - ELK Stack 설치
3. [Kibana 시각화](./02-Server/04-Kibana-시각화.md) - 대시보드 만들기

### 특정 주제 찾기
- **보안이 궁금하다면**: [Client Best Practices](./01-Client/03-Client-Best-Practices.md), [보안 및 인증](./03-Components/05-보안-및-인증.md)
- **성능 최적화**: [성능 튜닝](./03-Components/06-성능-튜닝.md)
- **데이터 관리**: [ILM 정책](./03-Components/04-ILM-정책.md)
- **모바일 로깅**: [모바일 애플리케이션 로깅](./01-Client/02-모바일-애플리케이션-로깅.md)

---

**작성 일자**: 2025-10-06
**버전**: 2.0 (가독성 개선 - 파일 분리)
**다음 업데이트 예정**: Elasticsearch 10.x 릴리스 시
