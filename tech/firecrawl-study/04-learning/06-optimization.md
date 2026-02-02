# 캐싱과 비용 최적화

## 개요

Firecrawl은 사용량 기반 과금이므로, **효율적인 크레딧 관리와 캐싱 전략**이 중요하다. 이 문서에서는 비용을 절감하면서도 성능을 유지하는 방법을 다룬다.

---

## Firecrawl 요금 구조

### 크레딧 소비

| API | 크레딧 소비 |
|-----|------------|
| Scrape | 1 크레딧/페이지 |
| Crawl | 1 크레딧/페이지 |
| Map | 1 크레딧/요청 |
| Extract | 추가 크레딧 |
| Search | 1 크레딧/요청 |

### 요금제

```
Free:    500 크레딧/월, 10 req/min
Hobby:   $19/월, 3,000 크레딧
Starter: $99/월, 15,000 크레딧
Growth:  사용량 기반
```

---

## 캐싱 전략

### 1. 로컬 파일 캐싱

```python
import json
import hashlib
import os
from datetime import datetime, timedelta
from firecrawl import FirecrawlApp

class CachedFirecrawl:
    def __init__(self, api_key, cache_dir="./firecrawl_cache", ttl_hours=24):
        self.app = FirecrawlApp(api_key=api_key)
        self.cache_dir = cache_dir
        self.ttl = timedelta(hours=ttl_hours)
        os.makedirs(cache_dir, exist_ok=True)

    def _get_cache_path(self, url, options=None):
        """URL과 옵션으로 캐시 파일 경로 생성"""
        key = f"{url}:{json.dumps(options or {}, sort_keys=True)}"
        hash_key = hashlib.md5(key.encode()).hexdigest()
        return os.path.join(self.cache_dir, f"{hash_key}.json")

    def _is_cache_valid(self, cache_path):
        """캐시 유효성 검사"""
        if not os.path.exists(cache_path):
            return False

        with open(cache_path, "r") as f:
            data = json.load(f)

        cached_time = datetime.fromisoformat(data["cached_at"])
        return datetime.now() - cached_time < self.ttl

    def scrape_url(self, url, options=None):
        """캐시를 활용한 스크래핑"""
        cache_path = self._get_cache_path(url, options)

        # 캐시 확인
        if self._is_cache_valid(cache_path):
            with open(cache_path, "r") as f:
                data = json.load(f)
            print(f"[캐시 히트] {url}")
            return data["result"]

        # 실제 API 호출
        print(f"[API 호출] {url}")
        result = self.app.scrape_url(url, options or {})

        # 캐시 저장
        with open(cache_path, "w") as f:
            json.dump({
                "url": url,
                "options": options,
                "cached_at": datetime.now().isoformat(),
                "result": result
            }, f)

        return result

# 사용
cached_app = CachedFirecrawl(api_key="fc-YOUR_API_KEY", ttl_hours=48)
result = cached_app.scrape_url("https://example.com")
```

### 2. Redis 캐싱 (프로덕션용)

```python
import redis
import json
import hashlib
from firecrawl import FirecrawlApp

class RedisFirecrawlCache:
    def __init__(self, api_key, redis_url="redis://localhost:6379", ttl_seconds=86400):
        self.app = FirecrawlApp(api_key=api_key)
        self.redis = redis.from_url(redis_url)
        self.ttl = ttl_seconds

    def _cache_key(self, url, options=None):
        key = f"{url}:{json.dumps(options or {}, sort_keys=True)}"
        return f"firecrawl:{hashlib.md5(key.encode()).hexdigest()}"

    def scrape_url(self, url, options=None):
        cache_key = self._cache_key(url, options)

        # 캐시 확인
        cached = self.redis.get(cache_key)
        if cached:
            print(f"[Redis 캐시 히트] {url}")
            return json.loads(cached)

        # API 호출
        print(f"[API 호출] {url}")
        result = self.app.scrape_url(url, options or {})

        # 캐시 저장
        self.redis.setex(cache_key, self.ttl, json.dumps(result))

        return result

# 사용
cached_app = RedisFirecrawlCache(
    api_key="fc-YOUR_API_KEY",
    redis_url="redis://localhost:6379",
    ttl_seconds=86400  # 24시간
)
```

### 3. 데이터베이스 캐싱

```python
import sqlite3
import json
import hashlib
from datetime import datetime, timedelta
from firecrawl import FirecrawlApp

class SQLiteFirecrawlCache:
    def __init__(self, api_key, db_path="firecrawl_cache.db", ttl_hours=24):
        self.app = FirecrawlApp(api_key=api_key)
        self.db_path = db_path
        self.ttl_hours = ttl_hours
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS cache (
                url_hash TEXT PRIMARY KEY,
                url TEXT,
                options TEXT,
                result TEXT,
                cached_at TIMESTAMP
            )
        """)
        conn.commit()
        conn.close()

    def _url_hash(self, url, options):
        key = f"{url}:{json.dumps(options or {}, sort_keys=True)}"
        return hashlib.md5(key.encode()).hexdigest()

    def scrape_url(self, url, options=None):
        url_hash = self._url_hash(url, options)
        conn = sqlite3.connect(self.db_path)

        # 캐시 확인
        cursor = conn.execute(
            "SELECT result, cached_at FROM cache WHERE url_hash = ?",
            (url_hash,)
        )
        row = cursor.fetchone()

        if row:
            cached_at = datetime.fromisoformat(row[1])
            if datetime.now() - cached_at < timedelta(hours=self.ttl_hours):
                print(f"[DB 캐시 히트] {url}")
                conn.close()
                return json.loads(row[0])

        # API 호출
        print(f"[API 호출] {url}")
        result = self.app.scrape_url(url, options or {})

        # 캐시 저장 (upsert)
        conn.execute("""
            INSERT OR REPLACE INTO cache (url_hash, url, options, result, cached_at)
            VALUES (?, ?, ?, ?, ?)
        """, (url_hash, url, json.dumps(options), json.dumps(result), datetime.now().isoformat()))
        conn.commit()
        conn.close()

        return result
```

---

## 비용 최적화 전략

### 1. 필요한 데이터만 요청

```python
# 나쁜 예: 모든 포맷 요청
result = app.scrape_url(url, {
    "formats": ["markdown", "html", "screenshot", "links"]
})

# 좋은 예: 필요한 것만
result = app.scrape_url(url, {
    "formats": ["markdown"]
})
```

### 2. Map으로 사전 필터링

```python
def smart_crawl(base_url, target_pattern):
    """필요한 페이지만 크롤링"""
    # 1. Map으로 URL 목록 가져오기 (1 크레딧)
    map_result = app.map_url(base_url)
    all_urls = map_result["links"]

    # 2. 필터링
    target_urls = [url for url in all_urls if target_pattern in url]

    print(f"전체 {len(all_urls)}개 중 {len(target_urls)}개만 스크래핑")
    print(f"예상 크레딧: {len(target_urls)} (절약: {len(all_urls) - len(target_urls)})")

    # 3. 필요한 URL만 스크래핑
    results = []
    for url in target_urls:
        result = app.scrape_url(url, {"formats": ["markdown"]})
        results.append(result)

    return results

# 사용: /docs/ 경로만 크롤링
docs = smart_crawl("https://example.com", "/docs/")
```

### 3. 증분 크롤링

```python
import json
from datetime import datetime

class IncrementalCrawler:
    def __init__(self, api_key, state_file="crawl_state.json"):
        self.app = FirecrawlApp(api_key=api_key)
        self.state_file = state_file

    def _load_state(self):
        try:
            with open(self.state_file, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return {"crawled_urls": {}, "last_crawl": None}

    def _save_state(self, state):
        with open(self.state_file, "w") as f:
            json.dump(state, f, indent=2)

    def crawl_new_only(self, base_url, max_pages=100):
        """새로운/변경된 페이지만 크롤링"""
        state = self._load_state()
        crawled_urls = state["crawled_urls"]

        # 현재 URL 목록 가져오기
        map_result = self.app.map_url(base_url)
        current_urls = set(map_result["links"])

        # 이전에 없던 URL만 선택
        new_urls = [
            url for url in current_urls
            if url not in crawled_urls
        ][:max_pages]

        print(f"새 URL: {len(new_urls)}개 (기존: {len(crawled_urls)}개)")

        results = []
        for url in new_urls:
            try:
                result = self.app.scrape_url(url, {"formats": ["markdown"]})
                results.append(result)

                # 상태 업데이트
                crawled_urls[url] = datetime.now().isoformat()
            except Exception as e:
                print(f"실패: {url} - {e}")

        # 상태 저장
        state["crawled_urls"] = crawled_urls
        state["last_crawl"] = datetime.now().isoformat()
        self._save_state(state)

        return results

# 사용
crawler = IncrementalCrawler(api_key="fc-YOUR_API_KEY")
new_docs = crawler.crawl_new_only("https://docs.example.com")
```

### 4. 배치 처리 최적화

```python
def batch_scrape_with_rate_limit(urls, rate_limit=10, delay=1):
    """Rate limit을 고려한 배치 스크래핑"""
    import time

    results = []
    for i, url in enumerate(urls):
        result = app.scrape_url(url, {"formats": ["markdown"]})
        results.append(result)

        # Rate limit 준수
        if (i + 1) % rate_limit == 0:
            print(f"진행: {i + 1}/{len(urls)}, {delay}초 대기...")
            time.sleep(delay)

    return results
```

---

## 비용 모니터링

### 사용량 추적

```python
class UsageTracker:
    def __init__(self, api_key, monthly_budget=500):
        self.app = FirecrawlApp(api_key=api_key)
        self.monthly_budget = monthly_budget
        self.usage = {"scrape": 0, "crawl": 0, "map": 0}

    def scrape_url(self, url, options=None):
        if self._check_budget(1):
            result = self.app.scrape_url(url, options or {})
            self.usage["scrape"] += 1
            return result
        else:
            raise Exception("월간 크레딧 한도 초과")

    def crawl_url(self, url, options=None):
        # 예상 크레딧 계산
        estimated = options.get("limit", 100)
        if self._check_budget(estimated):
            result = self.app.crawl_url(url, options or {})
            actual = len(result.get("data", []))
            self.usage["crawl"] += actual
            return result
        else:
            raise Exception(f"예상 크레딧 {estimated}이 남은 한도 초과")

    def _check_budget(self, required):
        current = sum(self.usage.values())
        return current + required <= self.monthly_budget

    def get_usage_report(self):
        total = sum(self.usage.values())
        remaining = self.monthly_budget - total
        return {
            "usage": self.usage,
            "total": total,
            "remaining": remaining,
            "budget": self.monthly_budget,
            "utilization": f"{(total / self.monthly_budget) * 100:.1f}%"
        }

# 사용
tracker = UsageTracker(api_key="fc-YOUR_API_KEY", monthly_budget=500)

try:
    result = tracker.scrape_url("https://example.com")
    print(tracker.get_usage_report())
except Exception as e:
    print(f"에러: {e}")
```

### 대시보드 활용

```python
# Firecrawl 대시보드 API (예시)
def check_usage():
    """Firecrawl 대시보드에서 사용량 확인"""
    # 실제로는 대시보드(firecrawl.dev/app)에서 확인
    # API로 사용량 조회 가능 여부는 공식 문서 확인

    print("사용량 확인: https://firecrawl.dev/app")
```

---

## 셀프호스팅으로 비용 절감

### Docker 배포

```bash
# 오픈소스 버전 배포
git clone https://github.com/mendableai/firecrawl.git
cd firecrawl

# 환경 설정
cp .env.example .env
# .env 파일에서 필요한 설정 수정

# 실행
docker-compose up -d
```

### 셀프호스팅 vs 클라우드

| 항목 | 셀프호스팅 | 클라우드 |
|------|-----------|---------|
| 초기 비용 | 높음 (인프라) | 없음 |
| 운영 비용 | 서버 비용만 | 사용량 과금 |
| 관리 | 직접 관리 필요 | 관리 불필요 |
| 확장성 | 직접 구축 | 자동 |
| 적합 대상 | 대량 사용자 | 소~중규모 |

---

## 최적화 체크리스트

### 스크래핑 전

- [ ] Map으로 사이트 구조 파악
- [ ] 필요한 URL만 선별
- [ ] 크레딧 예상 계산
- [ ] 캐시 확인

### 스크래핑 설정

- [ ] 필요한 formats만 선택
- [ ] onlyMainContent 활용
- [ ] excludeTags로 불필요 요소 제외
- [ ] 적절한 limit 설정

### 운영

- [ ] 캐싱 레이어 구현
- [ ] 증분 크롤링 적용
- [ ] 사용량 모니터링
- [ ] 정기적인 캐시 정리

---

## 다음 단계

- [[../05-projects|실전 프로젝트]] - 최적화 적용 사례
- [[../cheatsheet|Cheatsheet]] - 빠른 참조
