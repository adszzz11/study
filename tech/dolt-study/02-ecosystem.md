# Dolt 에코시스템

## 관련 기술 및 도구

### Dolt 패밀리

| 도구 | 설명 | 용도 |
|------|------|------|
| **Dolt** | 핵심 데이터베이스 | 로컬 개발, 서버 운영 |
| **DoltHub** | 데이터 호스팅 플랫폼 | 협업, 공유, 발견 |
| **DoltLab** | 셀프 호스팅 DoltHub | 기업 내부 운영 |
| **Hosted Dolt** | 관리형 Dolt 서비스 | 클라우드 운영 |
| **doltpy** | Python 라이브러리 | Python 통합 |
| **dolt-workbench** | 웹 UI | 시각적 데이터 관리 |

### DoltHub

```
DoltHub = GitHub for Data
```

- 공개/비공개 데이터 저장소
- 데이터 Pull Request
- 데이터 이슈 트래킹
- 온라인 SQL 쿼리 편집기
- 데이터 발견 및 검색

**인기 공개 데이터셋:**
- 미국 병원 가격 데이터
- 스포츠 통계 데이터
- 지리 데이터
- 공공 API 데이터

### DoltLab

```
DoltLab = GitHub Enterprise for Data
```

- 온프레미스 설치
- 기업 내부 데이터 협업
- SSO/LDAP 통합
- 접근 권한 관리

---

## 경쟁 및 유사 기술 비교

### 데이터 버전 관리 도구

| 도구 | 접근 방식 | 쿼리 | 저장소 |
|------|----------|------|--------|
| **Dolt** | 네이티브 DB | SQL | 로컬/DoltHub |
| **DVC** | 파일 기반 | 없음 | Git + 원격 스토리지 |
| **LakeFS** | 객체 스토리지 | Spark/Trino | S3/GCS |
| **Pachyderm** | 파이프라인 중심 | 없음 | Kubernetes |
| **Delta Lake** | 레이크하우스 | Spark SQL | 클라우드 스토리지 |

### 상세 비교

#### Dolt vs DVC

```
DVC:
- Git + 외부 스토리지 (S3, GCS)
- 파일 단위 버전 관리
- ML 파이프라인에 최적화
- 쿼리 기능 없음

Dolt:
- 네이티브 SQL 데이터베이스
- 행(Row) 단위 diff
- SQL 쿼리 지원
- 실시간 데이터 서빙 가능
```

**선택 기준:**
- 정형 데이터 + SQL 쿼리 필요 -> **Dolt**
- 대용량 파일 (이미지, 모델) 중심 -> **DVC**

#### Dolt vs LakeFS

```
LakeFS:
- 기존 데이터 레이크 위에 Git 레이어
- Spark, Presto, Trino와 통합
- 객체 스토리지 기반

Dolt:
- 독립 SQL 데이터베이스
- MySQL 호환
- 단일 노드 최적화
```

**선택 기준:**
- 대규모 분석 클러스터 -> **LakeFS**
- 애플리케이션 데이터베이스 -> **Dolt**

#### Dolt vs 일반 RDBMS + 감사 테이블

| 항목 | Dolt | RDBMS + 감사 |
|------|------|-------------|
| 설정 복잡도 | 낮음 (내장) | 높음 (직접 구현) |
| 브랜칭 | 지원 | 불가 |
| 시점 쿼리 | AS OF 구문 | 복잡한 조인 |
| 저장 효율 | 구조적 공유 | 전체 복사 |
| 머지/충돌 해결 | 지원 | 불가 |

---

## 통합 가능한 도구

### 데이터베이스 클라이언트

```
MySQL 호환 클라이언트 모두 사용 가능:
- MySQL Workbench
- DBeaver
- DataGrip
- TablePlus
- HeidiSQL
```

### 프로그래밍 언어

```python
# Python - doltpy
from doltpy.core import Dolt

db = Dolt.clone("dolthub/museum-collections")
```

```go
// Go - go-dolt
import "github.com/dolthub/go-mysql-server/sql"
```

```javascript
// Node.js - mysql2
const mysql = require('mysql2');
const conn = mysql.createConnection({
  host: 'localhost',
  port: 3306,
  database: 'my_dolt_db'
});
```

### BI 도구

- Metabase
- Apache Superset
- Grafana
- Tableau (MySQL 커넥터)

### ETL 도구

- dbt
- Airbyte
- Apache Airflow
- Prefect

---

## 기술 트렌드

### 1. DataOps 부상

```
DevOps가 소프트웨어 개발을 변화시켰듯,
DataOps는 데이터 작업을 변화시키고 있음

Dolt는 DataOps의 핵심 도구가 될 수 있음:
- 데이터 버전 관리
- 데이터 CI/CD
- 데이터 코드 리뷰
```

### 2. ML/AI 데이터 관리 중요성 증가

```
Model-Centric AI -> Data-Centric AI

데이터 품질과 버전 관리가 핵심:
- 학습 데이터 추적
- 실험 재현성
- 데이터 계보 (Lineage)
```

### 3. 데이터 민주화

```
더 많은 이해관계자가 데이터에 접근:
- 비개발자도 데이터 기여
- 데이터 변경 검토 프로세스
- 협업 중심 데이터 관리
```

### 4. 규제 준수 강화

```
GDPR, CCPA 등 데이터 규제:
- 데이터 변경 감사
- 시점별 데이터 스냅샷
- 데이터 삭제 추적
```

---

## 도입 고려사항

### 적합한 팀

- 데이터 엔지니어링 팀
- ML/AI 팀
- 분석 팀
- 데이터 협업이 필요한 조직

### 도입 단계

```
1단계: 파일럿
   - 비핵심 데이터로 시작
   - 소규모 팀 테스트

2단계: 확장
   - 주요 데이터셋 마이그레이션
   - 워크플로우 정립

3단계: 표준화
   - 조직 전체 적용
   - 거버넌스 정책 수립
```

### 성공 요인

1. **명확한 사용 사례 정의**
2. **팀 교육 투자**
3. **Git 경험 활용**
4. **점진적 도입**

---

## 커뮤니티 및 지원

### 공식 채널

- [Discord](https://discord.gg/gqr7K4VNKe) - 가장 활발
- [GitHub Issues](https://github.com/dolthub/dolt/issues)
- [DoltHub Blog](https://www.dolthub.com/blog)

### 학습 리소스

- [공식 문서](https://docs.dolthub.com)
- [YouTube 채널](https://www.youtube.com/c/DoltHub)
- [블로그 튜토리얼](https://www.dolthub.com/blog)

---

## 다음 단계

- [[03-references|참고 자료]] - 학습 자료 모음
- [[04-learning/01-installation|설치 가이드]] - 실습 시작
