# Extract API - AI 기반 구조화 데이터 추출

## 개요

Extract API는 **LLM을 사용하여 웹 페이지에서 구조화된 데이터를 자동으로 추출**하는 API이다. 스키마를 정의하면 AI가 페이지를 분석하여 해당 형식에 맞는 JSON 데이터를 반환한다.

```
URL + 스키마 정의 → Firecrawl + LLM → 구조화된 JSON 데이터
```

---

## 기본 사용법

### Python

```python
from firecrawl import FirecrawlApp
from pydantic import BaseModel
from typing import List, Optional

app = FirecrawlApp(api_key="fc-YOUR_API_KEY")

# Pydantic 스키마 정의
class ProductInfo(BaseModel):
    name: str
    price: float
    description: Optional[str]
    features: List[str]

# Extract API 호출
result = app.scrape_url("https://shop.example.com/product/123", {
    "formats": ["extract"],
    "extract": {
        "schema": ProductInfo.model_json_schema()
    }
})

# 결과 확인
print(result["extract"])
# {"name": "상품명", "price": 29900, "description": "...", "features": [...]}
```

### Node.js

```javascript
import FirecrawlApp from '@mendable/firecrawl-js';
import { z } from 'zod';

const app = new FirecrawlApp({ apiKey: 'fc-YOUR_API_KEY' });

// Zod 스키마 정의
const productSchema = z.object({
  name: z.string(),
  price: z.number(),
  description: z.string().optional(),
  features: z.array(z.string())
});

const result = await app.scrapeUrl('https://shop.example.com/product/123', {
  formats: ['extract'],
  extract: {
    schema: productSchema
  }
});

console.log(result.extract);
```

---

## 스키마 정의 방법

### 방법 1: Pydantic (Python)

```python
from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum

class Category(str, Enum):
    ELECTRONICS = "electronics"
    CLOTHING = "clothing"
    FOOD = "food"

class Product(BaseModel):
    name: str = Field(description="제품 이름")
    price: float = Field(description="가격 (원)")
    category: Category = Field(description="제품 카테고리")
    in_stock: bool = Field(description="재고 여부")
    features: List[str] = Field(description="제품 특징 목록")
    rating: Optional[float] = Field(description="평점 (1-5)")
```

### 방법 2: JSON Schema 직접 정의

```python
schema = {
    "type": "object",
    "properties": {
        "name": {
            "type": "string",
            "description": "제품 이름"
        },
        "price": {
            "type": "number",
            "description": "가격 (원)"
        },
        "features": {
            "type": "array",
            "items": {"type": "string"},
            "description": "제품 특징 목록"
        }
    },
    "required": ["name", "price"]
}

result = app.scrape_url(url, {
    "formats": ["extract"],
    "extract": {"schema": schema}
})
```

### 방법 3: 프롬프트만 사용

```python
# 스키마 없이 프롬프트로만 추출
result = app.scrape_url(url, {
    "formats": ["extract"],
    "extract": {
        "prompt": "이 페이지에서 제품명, 가격, 주요 특징 3가지를 추출해주세요."
    }
})
```

---

## 실전 예제

### 예제 1: 제품 정보 추출

```python
from pydantic import BaseModel
from typing import List, Optional

class ProductReview(BaseModel):
    reviewer: str
    rating: int
    comment: str

class ProductDetails(BaseModel):
    name: str
    price: float
    original_price: Optional[float]
    discount_rate: Optional[int]
    description: str
    specifications: dict
    reviews: List[ProductReview]
    average_rating: float

def extract_product(url):
    result = app.scrape_url(url, {
        "formats": ["extract"],
        "extract": {
            "schema": ProductDetails.model_json_schema()
        }
    })
    return ProductDetails(**result["extract"])

# 사용
product = extract_product("https://shop.example.com/product/123")
print(f"제품: {product.name}")
print(f"가격: {product.price:,}원")
print(f"평점: {product.average_rating}")
```

### 예제 2: 뉴스 기사 분석

```python
from pydantic import BaseModel
from typing import List
from datetime import datetime

class NewsArticle(BaseModel):
    title: str
    author: str
    published_date: str
    summary: str
    main_topics: List[str]
    sentiment: str  # positive, negative, neutral
    key_quotes: List[str]

def analyze_news(url):
    result = app.scrape_url(url, {
        "formats": ["extract", "markdown"],
        "extract": {
            "schema": NewsArticle.model_json_schema(),
            "prompt": "뉴스 기사의 감정은 positive, negative, neutral 중 하나로 분류해주세요."
        }
    })
    return {
        "structured": NewsArticle(**result["extract"]),
        "full_text": result["markdown"]
    }
```

### 예제 3: 회사 정보 추출

```python
from pydantic import BaseModel
from typing import List, Optional

class ContactInfo(BaseModel):
    email: Optional[str]
    phone: Optional[str]
    address: Optional[str]

class CompanyInfo(BaseModel):
    name: str
    description: str
    founded_year: Optional[int]
    employees: Optional[str]
    industry: str
    products_services: List[str]
    contact: ContactInfo

def extract_company_info(url):
    result = app.scrape_url(url, {
        "formats": ["extract"],
        "extract": {
            "schema": CompanyInfo.model_json_schema()
        }
    })
    return CompanyInfo(**result["extract"])

# 사용
company = extract_company_info("https://company.com/about")
print(f"회사: {company.name}")
print(f"산업: {company.industry}")
print(f"연락처: {company.contact.email}")
```

### 예제 4: 채용 공고 파싱

```python
from pydantic import BaseModel
from typing import List, Optional

class JobPosting(BaseModel):
    title: str
    company: str
    location: str
    employment_type: str  # 정규직, 계약직, 인턴
    salary_range: Optional[str]
    experience_required: str
    skills_required: List[str]
    responsibilities: List[str]
    benefits: List[str]
    application_deadline: Optional[str]

def parse_job_posting(url):
    result = app.scrape_url(url, {
        "formats": ["extract"],
        "extract": {
            "schema": JobPosting.model_json_schema()
        }
    })
    return JobPosting(**result["extract"])
```

---

## 여러 페이지에서 추출 (Batch Extract)

```python
from firecrawl import FirecrawlApp
from pydantic import BaseModel
from typing import List

app = FirecrawlApp(api_key="fc-YOUR_API_KEY")

class ProductSummary(BaseModel):
    name: str
    price: float
    category: str

def batch_extract_products(urls: List[str]):
    """여러 URL에서 제품 정보 추출"""
    results = []

    for url in urls:
        try:
            result = app.scrape_url(url, {
                "formats": ["extract"],
                "extract": {
                    "schema": ProductSummary.model_json_schema()
                }
            })
            results.append({
                "url": url,
                "data": ProductSummary(**result["extract"])
            })
        except Exception as e:
            results.append({
                "url": url,
                "error": str(e)
            })

    return results

# 사용
urls = [
    "https://shop.example.com/product/1",
    "https://shop.example.com/product/2",
    "https://shop.example.com/product/3"
]
products = batch_extract_products(urls)
```

---

## 프롬프트 엔지니어링

### 명확한 지시

```python
result = app.scrape_url(url, {
    "formats": ["extract"],
    "extract": {
        "schema": schema,
        "prompt": """
        다음 규칙을 따라 데이터를 추출해주세요:
        1. 가격은 숫자만 추출 (원, 달러 기호 제외)
        2. 날짜는 YYYY-MM-DD 형식으로 변환
        3. 정보가 없으면 null로 표시
        4. 리스트는 최대 5개 항목까지만
        """
    }
})
```

### 언어 지정

```python
result = app.scrape_url(url, {
    "formats": ["extract"],
    "extract": {
        "schema": schema,
        "prompt": "모든 텍스트는 한국어로 추출해주세요. 영어 원문이 있어도 번역해서 추출합니다."
    }
})
```

---

## Extract vs Scrape 비교

| 항목 | Scrape | Extract |
|------|--------|---------|
| 출력 | Markdown/HTML | 구조화된 JSON |
| 처리 | 단순 변환 | LLM 분석 |
| 크레딧 | 1 크레딧 | 추가 크레딧 |
| 용도 | 전체 콘텐츠 | 특정 정보 추출 |
| 정확도 | 원본 그대로 | AI 해석 의존 |

---

## 팁과 주의사항

### 스키마 설계 팁

```python
# 좋은 예: 명확한 설명과 적절한 타입
class GoodSchema(BaseModel):
    name: str = Field(description="제품의 정식 명칭")
    price: float = Field(description="할인 적용 전 원래 가격 (원)")

# 나쁜 예: 모호한 필드명
class BadSchema(BaseModel):
    n: str
    p: float
```

### 비용 최적화

```python
# 필요한 필드만 정의
class MinimalSchema(BaseModel):
    name: str
    price: float
    # 불필요한 필드는 제외
```

### 복잡한 페이지 처리

```python
# 특정 영역만 추출하도록 제한
result = app.scrape_url(url, {
    "formats": ["extract"],
    "extract": {
        "schema": schema,
        "prompt": "페이지의 '제품 상세' 섹션에서만 정보를 추출해주세요."
    },
    "includeTags": [".product-details"]
})
```

---

## 에러 핸들링

```python
def safe_extract(url, schema):
    """안전한 데이터 추출"""
    try:
        result = app.scrape_url(url, {
            "formats": ["extract"],
            "extract": {"schema": schema.model_json_schema()}
        })

        # 추출 결과 검증
        if "extract" not in result:
            return None, "추출 결과 없음"

        # Pydantic 검증
        return schema(**result["extract"]), None

    except ValidationError as e:
        return None, f"스키마 검증 실패: {e}"
    except Exception as e:
        return None, f"추출 실패: {e}"

# 사용
data, error = safe_extract(url, ProductInfo)
if error:
    print(f"에러: {error}")
else:
    print(f"추출 성공: {data}")
```

---

## 다음 단계

- [[03-crawl|Crawl API]] - 웹사이트 전체 크롤링
- [[05-langchain|LangChain 통합]] - RAG 파이프라인에서 활용
