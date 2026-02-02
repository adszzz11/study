# Map API - 사이트 URL 목록 수집

## 개요

Map API는 **웹사이트의 모든 URL을 빠르게 수집**하는 API이다. 실제 콘텐츠를 스크래핑하지 않고 URL 목록만 반환하므로 크롤링 전 사이트 구조를 파악하거나 특정 페이지만 선별하는 데 유용하다.

```
시작 URL → 링크 탐색 → URL 목록 반환 (콘텐츠 없음)
```

---

## 기본 사용법

### Python

```python
from firecrawl import FirecrawlApp

app = FirecrawlApp(api_key="fc-YOUR_API_KEY")

# 사이트 URL 목록 가져오기
result = app.map_url("https://docs.example.com")

print(f"발견된 URL: {len(result['links'])}개")
for url in result["links"][:10]:
    print(f"  - {url}")
```

### Node.js

```javascript
import FirecrawlApp from '@mendable/firecrawl-js';

const app = new FirecrawlApp({ apiKey: 'fc-YOUR_API_KEY' });

const result = await app.mapUrl('https://docs.example.com');
console.log(`Found ${result.links.length} URLs`);
```

### REST API

```bash
curl -X POST https://api.firecrawl.dev/v1/map \
  -H "Authorization: Bearer fc-YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://docs.example.com"
  }'
```

---

## 결과 구조

```python
{
    "success": True,
    "links": [
        "https://docs.example.com/",
        "https://docs.example.com/getting-started",
        "https://docs.example.com/api/overview",
        "https://docs.example.com/api/authentication",
        "https://docs.example.com/guides/quickstart",
        # ... 더 많은 URL
    ]
}
```

---

## 주요 옵션

### 검색 쿼리 필터

```python
# 특정 키워드가 포함된 URL만
result = app.map_url("https://docs.example.com", {
    "search": "api"
})

# 결과: API 관련 페이지만 반환
# - /api/overview
# - /api/authentication
# - /guides/api-integration
```

### URL 패턴 필터

```python
# 특정 경로 포함
result = app.map_url("https://example.com", {
    "includePaths": ["/blog/*", "/docs/*"]
})

# 특정 경로 제외
result = app.map_url("https://example.com", {
    "excludePaths": ["/admin/*", "/internal/*"]
})
```

### 최대 URL 수

```python
# 최대 100개 URL만
result = app.map_url("https://example.com", {
    "limit": 100
})
```

---

## 실전 예제

### 예제 1: 크롤링 전 사이트 분석

```python
def analyze_site_structure(url):
    """크롤링 전 사이트 구조 파악"""
    result = app.map_url(url)
    urls = result["links"]

    # URL 패턴 분석
    patterns = {}
    for u in urls:
        # 첫 번째 경로 세그먼트 추출
        path = u.replace(url, "").split("/")
        if len(path) > 1 and path[1]:
            section = f"/{path[1]}/"
            patterns[section] = patterns.get(section, 0) + 1

    print(f"총 {len(urls)}개 URL 발견")
    print("\n섹션별 페이지 수:")
    for section, count in sorted(patterns.items(), key=lambda x: -x[1]):
        print(f"  {section}: {count}개")

    return urls, patterns

# 사용
urls, patterns = analyze_site_structure("https://docs.example.com")
```

### 예제 2: 선택적 크롤링

```python
def selective_crawl(base_url, target_sections):
    """원하는 섹션만 크롤링"""
    # 1단계: 전체 URL 목록 가져오기
    map_result = app.map_url(base_url)
    all_urls = map_result["links"]

    # 2단계: 원하는 URL 필터링
    target_urls = [
        url for url in all_urls
        if any(section in url for section in target_sections)
    ]

    print(f"전체 {len(all_urls)}개 중 {len(target_urls)}개 선택")

    # 3단계: 선택된 URL만 스크래핑
    results = []
    for url in target_urls:
        try:
            result = app.scrape_url(url, {"formats": ["markdown"]})
            results.append({
                "url": url,
                "content": result["markdown"]
            })
        except Exception as e:
            print(f"실패: {url} - {e}")

    return results

# 사용
docs = selective_crawl(
    "https://docs.example.com",
    target_sections=["/api/", "/reference/"]
)
```

### 예제 3: 사이트맵 생성

```python
def generate_sitemap(url):
    """사이트맵 생성"""
    result = app.map_url(url)
    urls = sorted(result["links"])

    # 트리 구조로 변환
    def build_tree(urls, base_url):
        tree = {}
        for url in urls:
            path = url.replace(base_url, "").strip("/")
            parts = path.split("/") if path else ["(root)"]

            current = tree
            for part in parts:
                if part not in current:
                    current[part] = {}
                current = current[part]
        return tree

    tree = build_tree(urls, url)

    # 출력
    def print_tree(node, indent=0):
        for key, value in sorted(node.items()):
            print("  " * indent + f"├── {key}")
            if value:
                print_tree(value, indent + 1)

    print(f"📁 {url}")
    print_tree(tree)

    return tree

# 사용
sitemap = generate_sitemap("https://docs.example.com")
```

### 예제 4: 변경 감지

```python
import json
from datetime import datetime

def detect_changes(url, previous_urls_file):
    """사이트 URL 변경 감지"""
    # 현재 URL 목록
    current = set(app.map_url(url)["links"])

    # 이전 URL 목록 로드
    try:
        with open(previous_urls_file, "r") as f:
            data = json.load(f)
            previous = set(data["urls"])
    except FileNotFoundError:
        previous = set()

    # 비교
    added = current - previous
    removed = previous - current

    print(f"새로 추가된 페이지: {len(added)}개")
    for url in sorted(added)[:10]:
        print(f"  + {url}")

    print(f"\n삭제된 페이지: {len(removed)}개")
    for url in sorted(removed)[:10]:
        print(f"  - {url}")

    # 현재 상태 저장
    with open(previous_urls_file, "w") as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "urls": list(current)
        }, f, indent=2)

    return added, removed

# 사용
added, removed = detect_changes(
    "https://docs.example.com",
    "previous_urls.json"
)
```

### 예제 5: 크롤링 비용 추정

```python
def estimate_crawl_cost(url):
    """크롤링 전 비용 추정"""
    result = app.map_url(url)
    total_urls = len(result["links"])

    # Firecrawl 요금 기준
    cost_per_credit = 0.001  # 예시 가격

    estimates = {
        "total_urls": total_urls,
        "scrape_only": {
            "credits": total_urls,
            "estimated_cost": total_urls * cost_per_credit
        },
        "with_extract": {
            "credits": total_urls * 2,  # Extract 추가 크레딧
            "estimated_cost": total_urls * 2 * cost_per_credit
        }
    }

    print(f"총 페이지 수: {total_urls}")
    print(f"Scrape만: ~{estimates['scrape_only']['credits']} 크레딧")
    print(f"Extract 포함: ~{estimates['with_extract']['credits']} 크레딧")

    return estimates

# 사용
estimate_crawl_cost("https://docs.example.com")
```

---

## Map vs Crawl 비교

| 항목 | Map | Crawl |
|------|-----|-------|
| 반환값 | URL 목록만 | URL + 콘텐츠 |
| 속도 | 매우 빠름 | 느림 |
| 크레딧 | 1 크레딧 | 페이지당 1 크레딧 |
| 용도 | 사이트 구조 파악 | 실제 데이터 수집 |

---

## 워크플로우

### 권장 순서

```python
# 1. Map으로 사이트 구조 파악
map_result = app.map_url(base_url)
all_urls = map_result["links"]

# 2. 필요한 URL 필터링
target_urls = [url for url in all_urls if "/docs/" in url]

# 3. 비용 확인
print(f"크롤링할 페이지: {len(target_urls)}개")

# 4. Crawl 또는 개별 Scrape
if len(target_urls) <= 50:
    # 소량은 개별 스크래핑
    for url in target_urls:
        result = app.scrape_url(url)
else:
    # 대량은 Crawl API
    result = app.crawl_url(base_url, {
        "includePaths": ["/docs/*"]
    })
```

---

## 옵션 전체 목록

| 옵션 | 타입 | 기본값 | 설명 |
|------|------|--------|------|
| `search` | string | null | URL 필터링 검색어 |
| `includePaths` | array | [] | 포함할 URL 패턴 |
| `excludePaths` | array | [] | 제외할 URL 패턴 |
| `limit` | number | 5000 | 최대 URL 수 |

---

## 팁과 주의사항

### 빠른 사이트 점검

```python
# 크롤링 전 항상 Map으로 점검
def quick_check(url):
    result = app.map_url(url, {"limit": 100})
    print(f"샘플 URL {len(result['links'])}개 발견")
    return result["links"]
```

### 대형 사이트

```python
# 대형 사이트는 limit 설정 필수
result = app.map_url("https://large-site.com", {
    "limit": 1000  # 너무 많으면 시간 오래 걸림
})
```

### URL 정규화

```python
# Map 결과는 정규화되지 않을 수 있음
def normalize_urls(urls):
    normalized = set()
    for url in urls:
        # 후행 슬래시 제거
        url = url.rstrip("/")
        # 쿼리 파라미터 제거 (필요시)
        url = url.split("?")[0]
        normalized.add(url)
    return list(normalized)
```

---

## 다음 단계

- [[05-langchain|LangChain 통합]] - 수집 데이터로 RAG 구축
- [[06-optimization|캐싱과 비용 최적화]]
