# Phase 3: 완성 및 제출

> 제출물 4가지 작성 및 최종 점검

## 🎯 Phase 목표

**주요 목표:**
1. ✅ Working Code 정리 및 README 작성
2. ✅ Scoping Document 작성
3. ✅ Architecture Notes 작성
4. ✅ Questions Document 작성
5. ✅ 최종 테스트 및 품질 검증

**예상 기간**: 1-2일 (8-16시간)

**성공 기준:**
- 4가지 제출물 완성
- 코드 실행 가능 (재현 가능)
- 문서 품질 우수 (오타 없음, 명확함)
- 데모 준비 완료

---

## 📋 Step-by-Step 실행 계획

### Step 1: Working Code 정리 (3-4시간)

#### 1.1 코드 리뷰 및 정리

**체크리스트:**
- [ ] 사용하지 않는 코드 제거
- [ ] TODO/FIXME 주석 처리
- [ ] 함수 docstring 완성
- [ ] Type hints 일관성 확인
- [ ] 하드코딩된 값 설정 파일로 이동

**도구:**
```bash
# 린트 실행
ruff check scraper/

# 타입 체크
mypy scraper/

# 포맷팅
ruff format scraper/
```

---

#### 1.2 README.md 작성

**파일**: `README.md`

```markdown
# Zonagent Document Scraper

An agentic system to automatically scrape meeting documents from Georgia municipal websites.

## 🎯 Features

- ✅ **4 Jurisdictions**: Cherokee County, Holly Springs, Alpharetta, Marietta
- ✅ **4 Document Types**: Minutes, Agendas, Packets, Video links
- ✅ **Hybrid Agentic**: LLM-powered + rule-based scraping
- ✅ **Two Modes**: Backfill (historical) + Continuous updates
- ✅ **Smart Caching**: LLM rules cached for cost efficiency

## 📦 Installation

### Prerequisites
- Python 3.11+
- Anthropic API key

### Setup

\`\`\`bash
# 1. Clone repository
git clone <repo-url>
cd zonagent-scraper

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Install Playwright browsers
playwright install chromium

# 5. Configure API key
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY
\`\`\`

## 🚀 Usage

### Backfill Mode
Scrape historical documents (past 6 months):

\`\`\`bash
# Single jurisdiction
python main.py --jurisdiction cherokee --months 6

# All jurisdictions
for jur in cherokee holly_springs alpharetta marietta; do
    python main.py --jurisdiction $jur --months 6
done
\`\`\`

### Continuous Update Mode
Check for new documents since last run:

\`\`\`bash
python main.py --jurisdiction cherokee --continuous
\`\`\`

### Scheduled Scraping
Run daily at 2 AM:

\`\`\`bash
# Start scheduler
python scheduler.py

# Or use system cron
0 2 * * * cd /path/to/scraper && python scheduler.py
\`\`\`

### Dry Run
Find documents without downloading:

\`\`\`bash
python main.py --jurisdiction cherokee --months 1 --dry-run
\`\`\`

## 📁 Project Structure

\`\`\`
zonagent-scraper/
├── scraper/
│   ├── core/
│   │   ├── base_scraper.py       # Abstract base class
│   │   ├── llm_agent.py           # LLM integration
│   │   ├── rule_cache.py          # Rule caching
│   │   ├── storage.py             # Download & save
│   │   └── database.py            # SQLite operations
│   ├── jurisdictions/
│   │   ├── cherokee.py            # Cherokee County
│   │   ├── holly_springs.py       # Holly Springs
│   │   ├── alpharetta.py          # Alpharetta
│   │   └── marietta.py            # Marietta
│   └── models.py                  # Data models
├── data/
│   ├── documents/                 # Downloaded PDFs
│   │   └── <jurisdiction>/        # Organized by date
│   ├── rules/                     # LLM-generated rules
│   └── metadata.db                # SQLite database
├── tests/
│   └── test_*.py
├── docs/
│   ├── SCOPING.md                 # What was built
│   ├── ARCHITECTURE.md            # System design
│   └── QUESTIONS.md               # Production questions
├── main.py                        # CLI entry point
├── scheduler.py                   # Scheduled scraping
└── README.md
\`\`\`

## 🧪 Testing

\`\`\`bash
# Run all tests
pytest tests/ -v

# Run specific test
pytest tests/test_integration.py -v

# With coverage
pytest --cov=scraper tests/
\`\`\`

## 💰 Cost

Estimated LLM API costs:

- **Initial setup**: $8-12 (4 jurisdictions × $2-3 each)
- **Backfill (1 year)**: $10-20
- **Continuous updates**: $5-10/month

**Total first month**: ~$25-40
**Ongoing monthly**: ~$5-10

## 🔧 Configuration

Edit \`.env\`:

\`\`\`
ANTHROPIC_API_KEY=sk-ant-...
LOG_LEVEL=INFO
MAX_CONCURRENT_DOWNLOADS=5
\`\`\`

## 📊 Output

### Downloaded Files
\`\`\`
data/documents/cherokee_county/2024/11/2024-11-15_minutes.pdf
\`\`\`

### Database
SQLite database at \`data/metadata.db\`:
- \`documents\` table: All scraped documents
- \`scraping_runs\` table: Execution history
- \`rules\` table: LLM-generated scraping rules

### Logs
- \`scraper.log\`: Detailed execution log

## ⚠️ Troubleshooting

**LLM analysis fails**:
- Check API key in \`.env\`
- Verify internet connection

**No documents found**:
- Run with \`--dry-run\` first
- Check website URL in Phase 0 research

**Download fails**:
- Check network connection
- Increase timeout in config

## 📚 Documentation

- [Scoping Document](docs/SCOPING.md) - What was built and why
- [Architecture Notes](docs/ARCHITECTURE.md) - How it works
- [Questions for Production](docs/QUESTIONS.md) - What to decide before deployment

## 🙏 Acknowledgments

Built for the Zonagent assignment using:
- Anthropic Claude 3.5 Sonnet
- Playwright for dynamic pages
- BeautifulSoup for HTML parsing

## 📄 License

MIT
\`\`\`

**체크리스트:**
- [ ] README.md 작성
- [ ] 모든 명령어 테스트
- [ ] 링크 확인
- [ ] 오타 확인

---

#### 1.3 requirements.txt 및 설정 파일

**파일**: `requirements.txt`

\`\`\`
# Core
python-dotenv==1.0.0

# Web scraping
playwright==1.40.0
beautifulsoup4==4.12.2
httpx==0.25.2
lxml==4.9.3

# LLM
anthropic==0.8.0

# Database
# (sqlite3 is built-in)

# Scheduling
APScheduler==3.10.4

# Utilities
tenacity==8.2.3
structlog==23.2.0

# Testing
pytest==7.4.3
pytest-asyncio==0.21.1
pytest-cov==4.1.0

# Code quality
ruff==0.1.8
mypy==1.7.1
\`\`\`

**파일**: `.env.example`

\`\`\`
# Anthropic API Key
ANTHROPIC_API_KEY=your_api_key_here

# Optional: OpenAI fallback
# OPENAI_API_KEY=your_openai_key

# Logging
LOG_LEVEL=INFO

# Performance
MAX_CONCURRENT_DOWNLOADS=5
REQUEST_TIMEOUT=60
\`\`\`

**체크리스트:**
- [ ] requirements.txt 생성
- [ ] .env.example 생성
- [ ] .gitignore 업데이트

---

### Step 2: Scoping Document 작성 (2-3시간)

**파일**: `docs/SCOPING.md`

```markdown
# Scoping Document

## What Was Built

### Implemented Features ✅

#### 1. Jurisdictions (4/4)
- ✅ **Cherokee County** - Fully implemented, tested
- ✅ **City of Holly Springs** - Implemented with Playwright for dynamic rendering
- ✅ **City of Alpharetta** - Fully implemented, tested
- ✅ **City of Marietta** - Implemented with custom logic

#### 2. Document Types (4/4)
- ✅ **Meeting Minutes** - PDF download and metadata extraction
- ✅ **Meeting Agendas** - PDF download and classification
- ✅ **Agenda Packets** - Large PDF handling with streaming
- ✅ **Video Recording Links** - JSON storage with platform detection

#### 3. Operating Modes (2/2)
- ✅ **Backfill Mode** - Historical data collection (configurable period)
- ✅ **Continuous Update Mode** - Incremental updates since last run

#### 4. Agentic Features
- ✅ **LLM-powered Analysis** - Claude 3.5 Sonnet for page structure understanding
- ✅ **Rule Caching** - Generated selectors cached for cost efficiency
- ✅ **Adaptive Scraping** - Falls back to LLM when rules fail

#### 5. Data Management
- ✅ **Hierarchical Storage** - Documents organized by jurisdiction/year/month
- ✅ **SQLite Database** - Metadata tracking and duplicate prevention
- ✅ **Checksum Verification** - SHA256 for integrity

#### 6. Automation
- ✅ **Scheduler** - APScheduler for daily runs
- ✅ **Error Handling** - Retry logic with exponential backoff
- ✅ **Logging** - Structured logging with file and console output

---

### Deferred Features 🔄

#### 1. Advanced LLM Features
**Deferred**: Full autonomous agent (decides all strategies dynamically)
**Why**: Hybrid approach (LLM + rules) is more cost-effective
**Future**: Could enable for complex edge cases

#### 2. Cloud Deployment
**Deferred**: AWS Lambda / ECS deployment
**Why**: Local/server deployment sufficient for MVP
**Future**: Easy migration with current architecture

#### 3. Advanced Monitoring
**Deferred**: Grafana dashboards, Sentry integration
**Why**: Basic logging sufficient for initial deployment
**Future**: Add when scaling to more jurisdictions

#### 4. OCR for Scanned PDFs
**Deferred**: Text extraction from image-based PDFs
**Why**: Most PDFs are text-based; OCR adds complexity
**Future**: Add if needed for specific jurisdictions

#### 5. Video Processing
**Deferred**: Video download, transcription
**Why**: Assignment only requires links; processing is expensive
**Future**: Could add YouTube-DL + Whisper API

---

### Not Implemented ❌

#### 1. Web UI/Dashboard
**Reason**: CLI sufficient for MVP; UI not in requirements
**Effort**: 1-2 weeks
**Value**: Medium (nice-to-have)

#### 2. Real-time Monitoring (WebSockets)
**Reason**: Daily batch processing is adequate
**Effort**: 1 week
**Value**: Low (overkill for current scale)

#### 3. Multi-state Support
**Reason**: Assignment specifies Georgia only
**Effort**: Architecture supports it, 1-2 days per state
**Value**: High if expanding scope

---

## Implementation Decisions

### Why Hybrid Agentic?
**Decision**: LLM for initial analysis + rule-based execution
**Alternatives**:
- Full rule-based: Brittle, breaks on site changes
- Full LLM: Expensive ($100+/month), slow

**Rationale**:
- 90% cost savings after initial learning
- Fast execution (no API calls after rules generated)
- Still adapts to changes (LLM fallback)

### Why SQLite?
**Decision**: SQLite for metadata
**Alternatives**:
- PostgreSQL: Overkill for single-user/server
- JSON files: No query capabilities

**Rationale**:
- Zero setup, single file
- Sufficient for 10,000+ documents
- Easy migration to PostgreSQL later

### Why Local Storage?
**Decision**: Local filesystem
**Alternatives**:
- S3: Adds complexity, cost
- Database BLOBs: Not recommended for large files

**Rationale**:
- Simple, fast
- S3 migration straightforward
- Keep costs low for MVP

---

## Metrics

### Code Statistics
- **Lines of Code**: ~2,000
- **Files**: ~20
- **Test Coverage**: >80%

### Data Collected (Backfill 1 Year)
- **Documents**: 300-400
- **Storage**: ~1.5-2 GB
- **Jurisdictions**: 4/4
- **Document Types**: 4/4

### Performance
- **Backfill Speed**: ~50-100 docs/hour
- **Continuous Update**: <5 minutes
- **LLM Cost**: $25-40 total (first month)
- **Ongoing Cost**: $5-10/month

---

## Known Limitations

### 1. Site Structure Changes
**Impact**: Rules may fail if site redesigned
**Mitigation**: LLM automatically regenerates rules

### 2. Rate Limiting
**Impact**: May be blocked if too aggressive
**Mitigation**: Configurable delays, polite scraping

### 3. Authentication Required Sites
**Impact**: Cannot access if login required
**Current Status**: All 4 sites are public (no auth)

### 4. PDF Parsing
**Impact**: Cannot extract text from PDFs currently
**Mitigation**: Acceptable for MVP (links + metadata)

---

## Future Enhancements

### Short-term (1-2 weeks)
1. Web dashboard for browsing documents
2. Email notifications on failures
3. Document text extraction (PyPDF2)

### Medium-term (1-2 months)
1. Expand to 10+ Georgia municipalities
2. PostgreSQL migration
3. S3 storage
4. API for external access

### Long-term (3-6 months)
1. Multi-state support
2. Video transcription (Whisper API)
3. AI-powered document analysis
4. Public web interface

---

**Last Updated**: 2025-12-11
**Version**: 1.0 (MVP)
```

**체크리스트:**
- [ ] Scoping document 작성
- [ ] 구현/미구현 명확히 구분
- [ ] 근거 설명 추가

---

### Step 3: Architecture Notes 작성 (2-3시간)

**파일**: `docs/ARCHITECTURE.md`

```markdown
# Architecture Notes

## System Overview

Zonagent is a **hybrid agentic document scraper** that combines LLM-powered intelligence with rule-based efficiency.

```
┌─────────────────────────────────────────────────────────┐
│                     USER / SCHEDULER                     │
└────────────────────────┬────────────────────────────────┘
                         │
                         ▼
              ┌──────────────────────┐
              │      CLI / API        │
              │      main.py          │
              └──────────┬───────────┘
                         │
         ┌───────────────┼───────────────┐
         ▼               ▼               ▼
    ┌────────┐      ┌────────┐      ┌────────┐
    │Cherokee│      │ Holly  │      │Alphar- │  ...
    │ County │      │Springs │      │ etta   │
    └────┬───┘      └───┬────┘      └───┬────┘
         │              │                │
         └──────────────┼────────────────┘
                        ▼
              ┌──────────────────────┐
              │   BaseScraper        │
              │   (Abstract Class)    │
              └──────────┬───────────┘
                         │
        ┌────────────────┼────────────────┐
        ▼                ▼                ▼
   ┌─────────┐    ┌──────────┐    ┌──────────┐
   │   LLM   │    │  Rule    │    │ Storage  │
   │  Agent  │    │  Cache   │    │ Database │
   └─────────┘    └──────────┘    └──────────┘
```

---

## Core Components

### 1. BaseScraper (Abstract Class)

**Purpose**: Define common scraping workflow

**Key Methods**:
```python
def scrape(since: date) -> List[Document]:
    # 1. Fetch HTML
    html = self.fetch_html(url)

    # 2. Parse meetings
    meetings = self.parse_meetings(html, since)

    # 3. Extract documents
    documents = [self.parse_documents(m) for m in meetings]

    return documents
```

**Benefits**:
- Code reuse across jurisdictions
- Consistent error handling
- Easy testing

---

### 2. LLM Agent

**Purpose**: Understand page structure and generate selectors

**How it Works**:

```
Step 1: First Visit
┌──────────────┐
│  Sample HTML │ (truncated to 10K chars)
└──────┬───────┘
       │
       ▼
┌──────────────────────────────────────┐
│   Claude 3.5 Sonnet                   │
│   "Find all meeting minutes links"    │
└──────┬───────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────┐
│  JSON Response:                       │
│  {                                    │
│    "selectors": {                     │
│      "meeting_rows": "table tr",      │
│      "date": "td:first-child",        │
│      "links": "a[href$='.pdf']"       │
│    },                                 │
│    "confidence": 0.95                 │
│  }                                    │
└──────┬───────────────────────────────┘
       │
       ▼
 Save to rules/cherokee_county.json

Step 2: Subsequent Visits
┌──────────────┐
│ Load Cached  │
│    Rules     │
└──────────────┘
       │
       ▼
 Use selectors directly (no LLM call!)

Step 3: If Rules Fail
┌──────────────┐
│ Parsing Error│
└──────┬───────┘
       │
       ▼
 Regenerate rules with LLM
```

**Cost Optimization**:
- First analysis: ~$0.02-0.05
- Cached execution: $0.00
- Re-analysis only when needed

---

### 3. Rule Cache

**Purpose**: Persist LLM-generated selectors

**Storage**: JSON files in `data/rules/`

**Example**:
```json
{
  "jurisdiction": "cherokee_county",
  "selectors": {
    "meeting_rows": "table.calendar tbody tr",
    "date": "td.date",
    "title": "td.title",
    "document_links": "a[href$='.pdf']"
  },
  "date_format": "MM/DD/YYYY",
  "confidence": 0.95,
  "created_at": "2024-12-11",
  "validated": true
}
```

---

### 4. Storage Manager

**Purpose**: Download and organize documents

**File Structure**:
```
data/documents/
├── cherokee_county/
│   ├── 2024/
│   │   ├── 01/
│   │   │   ├── 2024-01-15_minutes.pdf
│   │   │   ├── 2024-01-15_agenda.pdf
│   │   │   └── 2024-01-15_packet.pdf
│   │   └── 02/
│   └── 2023/
└── alpharetta/
```

**Features**:
- Hierarchical organization
- Automatic directory creation
- Duplicate detection (checksum)
- Large file streaming

---

### 5. Database (SQLite)

**Schema**:
```sql
documents
├── id (PK)
├── jurisdiction
├── doc_type
├── meeting_date
├── title
├── source_url (UNIQUE)
├── file_path
├── checksum
└── scraped_at

scraping_runs
├── id (PK)
├── jurisdiction
├── run_type (backfill/continuous)
├── started_at
├── finished_at
├── documents_found
└── documents_downloaded

rules
├── id (PK)
├── jurisdiction (UNIQUE)
├── selectors (JSON)
├── confidence
└── created_at
```

---

## Data Flow

### Backfill Mode

```
1. User runs: python main.py --jurisdiction cherokee --months 6

2. Calculate since date: today - 6 months

3. CherokeeScraper.scrape(since)
   │
   ├─▶ fetch_html(meeting_list_url)
   │   └─▶ httpx.get() or Playwright.render()
   │
   ├─▶ ensure_rules(html)
   │   ├─▶ RuleCache.load()
   │   └─▶ LLM.analyze() if not cached
   │
   ├─▶ parse_meetings(html, since)
   │   └─▶ BeautifulSoup + selectors
   │
   └─▶ parse_documents(meeting)
       └─▶ Extract PDF links

4. For each document:
   ├─▶ Storage.download_document()
   │   ├─▶ httpx.get(pdf_url)
   │   └─▶ save to data/documents/...
   │
   └─▶ Database.insert_document()
       └─▶ INSERT INTO documents

5. Return summary
```

### Continuous Update Mode

```
1. User runs: python main.py --jurisdiction cherokee --continuous

2. Database.get_last_scrape_date(cherokee)
   └─▶ SELECT MAX(meeting_date) FROM documents

3. Scrape only documents since last_date

4. Insert only new documents (UNIQUE constraint)

5. Log: "Found 3 new documents" or "No new documents"
```

---

## Agentic Approach

### What Makes This "Agentic"?

**Traditional Scraper**:
```python
# Hardcoded selectors
rows = soup.select("table tbody tr")
date = row.select_one("td:first-child").text
```
❌ Breaks when site changes

**Agentic Scraper**:
```python
# LLM decides selectors
rules = llm.analyze_page(html, goal="Find meeting links")
rows = soup.select(rules['selectors']['meeting_rows'])
```
✅ Adapts to changes

### Levels of Agency

| Feature | Traditional | Our System | Full Agentic |
|---------|-------------|------------|--------------|
| **Selectors** | Hardcoded | LLM-generated | LLM decides on each request |
| **Error Recovery** | Fails | LLM regenerates rules | LLM tries multiple strategies |
| **New Sites** | Manual coding | LLM + plugin | LLM only (zero code) |
| **Cost** | $0 | $10-40/month | $100+/month |
| **Speed** | Fast | Fast (cached) | Slow (always LLM) |

**Our Choice**: Middle ground (Hybrid)

---

## Design Decisions

### 1. Plugin Architecture

**Why**: Easy to add jurisdictions

**How**:
```python
# Each jurisdiction is a plugin
class CherokeeScraper(BaseScraper):
    def get_meeting_list_url(self):
        return "http://..."

# Registry pattern
SCRAPERS = {
    'cherokee': CherokeeScraper,
    'alpharetta': AlpharettaScraper,
    # Easy to add more
}
```

### 2. Static vs Dynamic Rendering

**Decision**: Support both

| Site | Method | Reason |
|------|--------|--------|
| Cherokee | httpx (static) | Faster, cheaper |
| Holly Springs | Playwright (dynamic) | React app, needs JS |

### 3. Error Handling Strategy

**Tenacity for retries**:
```python
@retry(stop=stop_after_attempt(3),
       wait=wait_exponential(min=2, max=10))
def fetch_html(url):
    ...
```

**Graceful degradation**:
- Network error → Retry 3x
- Parsing error → LLM regenerate
- LLM error → Fail with clear message

---

## Scalability Considerations

### Current Limits
- **Jurisdictions**: 4 (easily 10-50)
- **Documents**: ~400/year (easily 10,000+)
- **Concurrent downloads**: 5 (configurable)

### Scaling Path

**10-20 jurisdictions**:
- Current architecture sufficient
- Add more plugins
- Consider PostgreSQL

**50-100 jurisdictions**:
- PostgreSQL required
- S3 for storage
- Distributed scraping (Celery)

**1000+ jurisdictions**:
- Kubernetes / Serverless
- Full agentic (zero-code new sites)
- Advanced monitoring

---

## Security & Ethics

### Rate Limiting
- 500ms delay between requests
- Respectful User-Agent
- Honors robots.txt (sites are public)

### Data Privacy
- Only public documents
- No personal information scraped
- Transparent scraping (identifiable UA)

### API Key Security
- .env files (not committed)
- Environment variables in production

---

## Testing Strategy

### Unit Tests
```python
def test_date_parsing():
    assert parse_date("12/11/2024") == date(2024, 12, 11)
```

### Integration Tests (Mock HTML)
```python
def test_cherokee_scraper():
    html = Path("fixtures/cherokee.html").read_text()
    scraper = CherokeeScraper()
    meetings = scraper.parse_meetings(html)
    assert len(meetings) > 0
```

### End-to-End Tests (Real Sites)
```python
@pytest.mark.e2e
def test_live_cherokee():
    scraper = CherokeeScraper()
    docs = scraper.scrape(since=date.today() - timedelta(days=30))
    assert len(docs) > 0
```

---

## Future Architecture

### Phase 4: Multi-Region
```
┌─────────────────────────────────────┐
│     Federation Layer                │
│  (Coordinate multiple regions)      │
└─────────────────────────────────────┘
         │
    ┌────┴────┐
    ▼         ▼
 Georgia   California  ...
```

### Phase 5: Microservices
```
┌─────────┐  ┌─────────┐  ┌─────────┐
│Scraper  │  │  LLM    │  │ Storage │
│ Service │→│ Service │→│ Service │
└─────────┘  └─────────┘  └─────────┘
```

---

**Last Updated**: 2025-12-11
**Author**: Claude Sonnet 4.5 + Human
```

**체크리스트:**
- [ ] Architecture document 작성
- [ ] 다이어그램 포함
- [ ] 기술 결정 근거 설명

---

### Step 4: Questions Document 작성 (1-2시간)

**파일**: `docs/QUESTIONS.md`

```markdown
# Questions for Production Deployment

## Critical (Must Answer Before Deployment)

### 1. Document Usage
**Question**: How will the collected documents be used?

**Options**:
- [ ] Search engine (full-text indexing)
- [ ] AI analysis (need text extraction)
- [ ] Archiving only (metadata + files)
- [ ] Data extraction (structured output)

**Impact**: Determines if we need OCR, text extraction, or additional processing

**Current Assumption**: Metadata + original files (no text extraction)

---

### 2. Deployment Environment
**Question**: Where will this system run?

**Options**:
- [ ] AWS (which services?)
- [ ] GCP
- [ ] On-premises server
- [ ] Local machine

**Impact**: Affects storage (S3 vs local), database (RDS vs SQLite), scheduling

**Current Assumption**: Local/server with filesystem storage

---

### 3. Backfill Period
**Question**: Exactly how many years of historical data are needed?

**Options**:
- [ ] 6 months
- [ ] 1 year (current default)
- [ ] 2 years
- [ ] All available
- [ ] Specific start date: ___

**Impact**: Initial runtime, storage requirements, costs

**Estimate** (1 year):
- Documents: ~300-400
- Storage: ~2 GB
- Time: 4-6 hours

---

### 4. Update Frequency
**Question**: How often should the system check for new documents?

**Options**:
- [ ] Real-time (hourly)
- [ ] Daily (current: 2 AM)
- [ ] Weekly
- [ ] On-demand only

**Impact**: Server resources, API costs, complexity

**Current Assumption**: Daily at 2 AM

---

## High Priority (Needed for Scaling)

### 5. Expansion Plans
**Question**: How many more jurisdictions will be added?

**Options**:
- [ ] 4 only (no expansion)
- [ ] 10-20 (Georgia cities)
- [ ] 50+ (all Georgia)
- [ ] Multiple states

**Impact**: Architecture complexity, automation level

**Current System**: Supports 10-20 easily, 50+ needs refactoring

---

### 6. Document Type Priority
**Question**: Which document types are most important?

**Ranking** (1-4):
- ___ Meeting Minutes
- ___ Meeting Agendas
- ___ Agenda Packets
- ___ Video Recordings

**Impact**: Resource allocation, testing focus

**Current Assumption**: Minutes > Agendas > Packets > Videos

---

### 7. API Budget
**Question**: What's the monthly budget for LLM API costs?

**Options**:
- [ ] $50
- [ ] $100
- [ ] $500
- [ ] Unlimited (within reason)

**Current Cost**: $5-10/month (after initial $25-40 setup)

**Scaling**: +10 jurisdictions = +$3-5/month

---

## Medium Priority (Operational Policies)

### 8. Failure Notifications
**Question**: How should failures be reported?

**Options**:
- [ ] Email
- [ ] Slack
- [ ] PagerDuty
- [ ] Dashboard only
- [ ] No alerts needed

**Impact**: Integration complexity

**Current**: Logs only

---

### 9. Data Retention
**Question**: How long should documents be kept?

**Options**:
- [ ] Forever
- [ ] 5 years
- [ ] 3 years, then archive to glacier storage

**Impact**: Storage costs, archiving strategy

**Current**: No deletion (keep forever)

---

### 10. Duplicate Handling
**Question**: If a document is updated/re-posted, what should happen?

**Options**:
- [ ] Keep only latest version
- [ ] Keep all versions (track changes)
- [ ] Ignore updates (keep first version)

**Impact**: Storage, version tracking

**Current**: Latest version only (checksum comparison)

---

### 11. Missing Document Tolerance
**Question**: How critical is 100% document collection?

**Options**:
- [ ] 100% required (manual verification)
- [ ] 95%+ acceptable
- [ ] Best effort

**Impact**: Verification rigor, manual intervention

**Current**: Best effort (~95%)

---

## Technical Infrastructure

### 12. Monitoring & Observability
**Question**: What monitoring is needed?

**Options**:
- [ ] Basic logs (current)
- [ ] Metrics dashboard (Grafana)
- [ ] Error tracking (Sentry)
- [ ] Full observability stack

**Impact**: Cost, maintenance

---

### 13. Concurrent Execution
**Question**: Can all jurisdictions be scraped simultaneously?

**Options**:
- [ ] Yes, full parallelism
- [ ] Sequential only (resource constrained)
- [ ] Limited (e.g., 2 at a time)

**Impact**: Performance, server specs

**Current**: Sequential (configurable)

---

### 14. Authentication
**Question**: Will any future sites require login?

**Options**:
- [ ] No (all public)
- [ ] Yes (need credential management)

**Impact**: Security, credential storage

**Current**: All public, no auth

---

## Legal & Compliance

### 15. Terms of Service
**Question**: Have we verified scraping is allowed?

**Status**:
- [ ] Reviewed robots.txt (all sites allow)
- [ ] Checked ToS
- [ ] Legal approval

**Current**: Public government documents, robots.txt compliant

---

### 16. Rate Limiting Policy
**Question**: What rate limit should we enforce?

**Options**:
- [ ] 1 request/second (very polite)
- [ ] 2 requests/second (current: ~500ms)
- [ ] As fast as possible

**Impact**: Scraping speed, server friendliness

---

## Data Quality

### 17. Validation Requirements
**Question**: How should data quality be verified?

**Options**:
- [ ] Automated checks only
- [ ] Sample manual review (10%)
- [ ] Full manual review

**Impact**: QA process, staffing

**Current**: Automated (checksum, required fields)

---

### 18. Site Change Detection
**Question**: How quickly should site changes be addressed?

**Options**:
- [ ] Automatic (LLM re-learns, current)
- [ ] Alert developer, manual fix within 24h
- [ ] Weekly maintenance window

**Impact**: Automation level, on-call needs

**Current**: Automatic retry with LLM, then alert

---

## Integration

### 19. API Requirements
**Question**: Do other systems need to access this data?

**Options**:
- [ ] No (standalone)
- [ ] Yes, REST API needed
- [ ] Yes, direct database access
- [ ] Yes, file share (S3)

**Impact**: API development

**Current**: Standalone (files + DB)

---

### 20. Output Format
**Question**: Besides PDFs, what output is needed?

**Options**:
- [ ] PDFs only (current)
- [ ] Extracted text (TXT)
- [ ] JSON metadata
- [ ] CSV exports

**Impact**: Post-processing pipeline

---

## Summary

**Immediate decisions needed (before production)**:
1. Document usage (#1)
2. Deployment environment (#2)
3. Exact backfill period (#3)
4. Update frequency (#4)

**Can defer until scaling**:
- Expansion plans (#5)
- Advanced monitoring (#12)
- API integration (#19)

**Current defaults are reasonable for**:
- Small-scale deployment (4-10 jurisdictions)
- Internal use (no external API)
- Daily batch processing

---

**Last Updated**: 2025-12-11
**Recommendation**: Start with current assumptions, adjust based on usage
```

**체크리스트:**
- [ ] Questions document 작성
- [ ] 우선순위 명확히 구분
- [ ] 현재 가정 명시

---

### Step 5: 최종 테스트 및 검증 (2-3시간)

#### 5.1 전체 시스템 테스트

**테스트 시나리오**:

```bash
# 1. 클린 설치 테스트
rm -rf venv data/
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
playwright install chromium

# 2. Dry run 테스트
python main.py --jurisdiction cherokee --months 1 --dry-run

# 3. 실제 실행 테스트
python main.py --jurisdiction cherokee --months 1

# 4. Continuous update 테스트
python main.py --jurisdiction cherokee --continuous

# 5. 다른 지자체 테스트
python main.py --jurisdiction alpharetta --months 1

# 6. 데이터 검증
sqlite3 data/metadata.db "SELECT COUNT(*) FROM documents;"
ls -lh data/documents/
```

**체크리스트:**
- [ ] 클린 설치 성공
- [ ] Dry run 동작
- [ ] 실제 다운로드 성공
- [ ] Continuous update 동작
- [ ] 모든 지자체 테스트
- [ ] 데이터 무결성 확인

---

#### 5.2 문서 검증

**체크리스트:**
- [ ] README 모든 명령어 실행 가능
- [ ] SCOPING 정확성 확인
- [ ] ARCHITECTURE 다이어그램 확인
- [ ] QUESTIONS 완전성 확인
- [ ] 오타 및 문법 검사

---

### Step 6: 데모 준비 (1-2시간)

#### 6.1 데모 스크립트

**파일**: `demo.sh`

```bash
#!/bin/bash
# Demo script for Zonagent Scraper

echo "=== Zonagent Document Scraper Demo ==="
echo ""

echo "1. Checking setup..."
source venv/bin/activate
python -c "import scraper; print('✅ Package imports OK')"

echo ""
echo "2. Dry run (Cherokee County, 1 month)..."
python main.py --jurisdiction cherokee --months 1 --dry-run

echo ""
echo "3. Actual scraping (limited)..."
python main.py --jurisdiction cherokee --months 1

echo ""
echo "4. Checking database..."
sqlite3 data/metadata.db "SELECT jurisdiction, COUNT(*) as count FROM documents GROUP BY jurisdiction;"

echo ""
echo "5. Showing downloaded files..."
ls -R data/documents/ | head -20

echo ""
echo "=== Demo Complete ==="
```

**체크리스트:**
- [ ] demo.sh 작성
- [ ] 실행 가능하도록 설정 (`chmod +x demo.sh`)
- [ ] 데모 스크립트 테스트

---

#### 6.2 스크린샷 준비

**필요한 스크린샷**:
- [ ] CLI 실행 화면
- [ ] 다운로드 진행 상황
- [ ] 파일 구조
- [ ] DB 쿼리 결과
- [ ] 로그 출력

---

## 📊 Phase 3 완료 체크리스트

### 제출물 (4개)
- [ ] ✅ Working Code + README.md
- [ ] ✅ Scoping Document (SCOPING.md)
- [ ] ✅ Architecture Notes (ARCHITECTURE.md)
- [ ] ✅ Questions Document (QUESTIONS.md)

### 코드 품질
- [ ] 린트 통과 (ruff)
- [ ] 타입 체크 통과 (mypy)
- [ ] 테스트 통과 (pytest)
- [ ] 문서화 완료

### 실행 가능성
- [ ] 클린 설치 가능
- [ ] README 명령어 동작
- [ ] 에러 없이 실행
- [ ] 데모 스크립트 동작

### 문서 품질
- [ ] 오타 없음
- [ ] 링크 작동
- [ ] 다이어그램 명확
- [ ] 코드 예시 정확

---

## 🎯 성공 기준

### 최소 성공 (제출 가능)
- ✅ 4가지 제출물 완성
- ✅ 코드 실행 가능
- ✅ 문서 읽기 쉬움
- ✅ 10개 이상 문서 수집 가능

### 이상적 성공
- ✅ 모든 문서 전문가 수준
- ✅ 코드 품질 우수
- ✅ 데모 매끄럽게 진행
- ✅ 질문 포괄적

---

## 📝 최종 산출물

### 1. 코드
```
zonagent-scraper/
├── scraper/          # 완성된 코드
├── tests/            # 테스트
├── docs/             # 3개 문서
├── README.md         # 메인 문서
├── main.py
└── demo.sh
```

### 2. 데이터
```
data/
├── documents/        # 다운로드한 문서
├── rules/            # LLM 규칙
└── metadata.db       # 데이터베이스
```

### 3. 문서
- README.md (사용 가이드)
- docs/SCOPING.md (구현 범위)
- docs/ARCHITECTURE.md (시스템 설계)
- docs/QUESTIONS.md (프로덕션 질문)

---

## ⚠️ 제출 전 최종 체크

- [ ] Git commit 및 정리
- [ ] 민감 정보 제거 (.env 등)
- [ ] 불필요한 파일 삭제
- [ ] README 정확성 재확인
- [ ] 모든 링크 테스트
- [ ] 데모 리허설

---

**완료!** 이제 과제를 제출할 준비가 되었습니다.

**작성일**: 2025-12-11
**예상 완료**: Phase 3 시작 후 1-2일
