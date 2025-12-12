# ZonAgent MVP - 빠른 시작 가이드

> Cherokee County 회의 문서 스크래퍼 MVP

## 🚀 5분 만에 시작하기

### 1단계: 환경 설정 (2분)

```bash
# mvp 디렉터리로 이동
cd /Users/leetangle/code/Note/assignment/zonagent/mvp

# 가상환경 생성
python3 -m venv venv

# 가상환경 활성화 (macOS/Linux)
source venv/bin/activate

# Windows의 경우:
# venv\Scripts\activate

# 패키지 설치
pip install -r requirements.txt
```

**예상 시간**: 1-2분 (인터넷 속도에 따라)

### 2단계: 첫 스크래핑 실행 (1분)

```bash
# Cherokee County 데이터 수집 (최근 10개)
python -m src.main backfill --jurisdiction cherokee --limit 10
```

**예상 출력**:
```
============================================================
ZonAgent MVP - Backfill Mode
============================================================
지자체: Cherokee County
최대 수집: 10
데이터베이스: /Users/leetangle/code/Note/assignment/zonagent/mvp/data/documents.db
============================================================

🚀 스크래핑 시작...

2025-12-12 ... - scraper.cherokee - INFO - Fetching page: https://cherokeega.granicus.com/ViewPublisher.php?view_id=1
2025-12-12 ... - scraper.cherokee - INFO - Received 123,456 bytes of HTML
2025-12-12 ... - scraper.cherokee - INFO - Found 48 meeting rows
2025-12-12 ... - scraper.cherokee - INFO - Successfully parsed 20 documents

💾 데이터베이스 저장 중...

============================================================
📊 Cherokee County 스크래핑 결과
   발견: 20개
   신규: 20개
   스킵: 0개
   에러: 0개
   소요 시간: 2.3초
============================================================
```

### 3단계: 결과 확인 (1분)

```bash
# 통계 조회
python -m src.main stats
```

**예상 출력**:
```
📊 데이터베이스 통계
============================================================

전체:
  총 문서: 20개
  지자체: 1개
  회의: 10개
  기간: 2024-11-01 ~ 2025-12-05

지자체별:
  cherokee            :   20개  (2024-11-01 ~ 2025-12-05)

문서 타입별:
  agenda    :   10개
  minutes   :   10개
============================================================
```

```bash
# 문서 목록 보기
python -m src.main list --limit 5
```

**예상 출력**:
```
📋 문서 목록 (최근 5개)

================================================================================
2025-12-05 | cherokee        | agenda     | Planning Commission Meeting - Agenda
2025-12-05 | cherokee        | minutes    | Planning Commission Meeting - Minutes
2025-11-18 | cherokee        | agenda     | Planning Commission Meeting - Agenda
2025-11-18 | cherokee        | minutes    | Planning Commission Meeting - Minutes
2025-11-01 | cherokee        | agenda     | Planning Commission Meeting - Agenda
================================================================================
총 5개
```

## ✅ 성공!

축하합니다! MVP가 정상적으로 작동합니다.

---

## 📖 추가 사용법

### 전체 데이터 수집

```bash
# limit 없이 실행 (모든 과거 데이터 수집)
python -m src.main backfill --jurisdiction cherokee
```

**주의**: 전체 수집 시 5-10분 소요될 수 있습니다.

### 상세 로그 보기

```bash
# --verbose 플래그 추가
python -m src.main backfill --jurisdiction cherokee --limit 10 --verbose
```

또는:

```bash
# DEBUG 레벨 로그
python -m src.main backfill --jurisdiction cherokee --limit 10 --log-level DEBUG
```

### 도움말 보기

```bash
# 전체 도움말
python -m src.main --help

# 명령어별 도움말
python -m src.main backfill --help
python -m src.main stats --help
python -m src.main list --help
```

---

## 🐛 문제 해결

### 문제 1: `No module named 'src'`

**원인**: 가상환경이 활성화되지 않았거나 잘못된 디렉터리에서 실행

**해결**:
```bash
# mvp 디렉터리에 있는지 확인
pwd
# 출력: /Users/leetangle/code/Note/assignment/zonagent/mvp

# 가상환경 활성화 확인
which python
# 출력: /Users/leetangle/code/Note/assignment/zonagent/mvp/venv/bin/python
```

### 문제 2: `ModuleNotFoundError: No module named 'httpx'`

**원인**: 패키지가 설치되지 않음

**해결**:
```bash
# requirements.txt 재설치
pip install -r requirements.txt
```

### 문제 3: `HTTPError: ... 403 Forbidden`

**원인**: 너무 빠른 요청으로 서버에서 차단

**해결**:
- 잠시 대기 후 재시도
- `--limit`을 작게 설정 (예: 5)

### 문제 4: 데이터베이스 파일 위치를 모르겠어요

```bash
# 데이터베이스 위치 확인
ls -lh data/
# 출력: documents.db

# SQLite로 직접 확인 (선택)
sqlite3 data/documents.db "SELECT COUNT(*) FROM documents;"
```

---

## 📁 생성된 파일

성공적으로 실행하면 다음 파일들이 생성됩니다:

```
mvp/
├── data/
│   └── documents.db        # SQLite 데이터베이스
└── src/
    └── __pycache__/        # Python 캐시 (자동 생성)
```

---

## 🎯 다음 단계

MVP가 작동하는 것을 확인했다면:

1. **전체 데이터 수집**
   ```bash
   python -m src.main backfill --jurisdiction cherokee
   ```

2. **데이터 분석**
   - `data/documents.db`를 SQLite 클라이언트로 열기
   - 또는 Python으로 추가 분석

3. **Phase 2 준비**
   - Marietta (CivicEngage) 추가
   - Continuous 모드 구현

---

**작성일**: 2025-12-12
**Phase**: 1 (MVP)
**예상 소요 시간**: 5분
