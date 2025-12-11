# 실행 계획 (Implementation Plan)

> Agentic Document Scraper 과제의 단계별 실행 계획

## 📋 개요

이 디렉터리는 과제 완수를 위한 구체적이고 실행 가능한 계획을 담고 있습니다.
각 Phase는 명확한 목표, 단계별 액션, 체크포인트를 포함합니다.

---

## 🗺️ 전체 로드맵

```
Phase 0          Phase 1           Phase 2              Phase 3
사전 조사     →   MVP 개발      →   확장 개발        →   완성 및 제출
(1-2일)          (3-5일)           (3-4일)              (1-2일)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
총 예상 기간: 8-13일 (full-time 기준)
```

---

## 📂 Phase별 문서 구조

| Phase | 문서 | 목표 | 예상 기간 | 상태 |
|-------|------|------|-----------|------|
| **Phase 0** | [사전 조사](./phase-0-research.md) | 웹사이트 분석 및 기술 검증 | 1-2일 | ⏳ 대기 |
| **Phase 1** | [MVP 개발](./phase-1-mvp.md) | 1개 지자체, 1개 문서 타입 | 3-5일 | ⏳ 대기 |
| **Phase 2** | [확장 개발](./phase-2-expansion.md) | 전체 지자체 및 문서 타입 | 3-4일 | ⏳ 대기 |
| **Phase 3** | [완성 및 제출](./phase-3-completion.md) | 문서화 및 최종 점검 | 1-2일 | ⏳ 대기 |

---

## 🎯 Phase별 핵심 목표

### Phase 0: 사전 조사 및 분석 (1-2일)
**목표**: 실제 구현 전에 모든 지자체 웹사이트를 조사하고 기술적 실현 가능성 검증

**핵심 산출물**:
- ✅ 4개 지자체 웹사이트 구조 분석 리포트
- ✅ 기술 스택 검증 (Playwright, LLM 테스트)
- ✅ MVP 지자체 선정 (가장 구현하기 쉬운 곳)
- ✅ 프로젝트 구조 및 개발 환경 설정

**상세 계획**: [phase-0-research.md](./phase-0-research.md)

---

### Phase 1: MVP 개발 (3-5일)
**목표**: 1개 지자체에서 1개 문서 타입 수집하는 완전히 동작하는 시스템 구축

**핵심 산출물**:
- ✅ 동작하는 스크래퍼 코드
- ✅ Hybrid Agentic 시스템 (LLM + 규칙 기반)
- ✅ 로컬 저장 및 메타데이터 DB
- ✅ 기본 에러 핸들링 및 로깅

**상세 계획**: [phase-1-mvp.md](./phase-1-mvp.md)

---

### Phase 2: 확장 개발 (3-4일)
**목표**: 나머지 3개 지자체와 3개 문서 타입 추가, Continuous Update 구현

**핵심 산출물**:
- ✅ 4개 지자체 모두 지원
- ✅ 4개 문서 타입 모두 수집
- ✅ Continuous Update 모드
- ✅ 통합 테스트 및 품질 검증

**상세 계획**: [phase-2-expansion.md](./phase-2-expansion.md)

---

### Phase 3: 완성 및 제출 (1-2일)
**목표**: 제출물 4가지 작성 및 최종 점검

**핵심 산출물**:
- ✅ Working Code (README 포함)
- ✅ Scoping Document
- ✅ Architecture Notes
- ✅ Questions Document

**상세 계획**: [phase-3-completion.md](./phase-3-completion.md)

---

## ⏱️ 타임라인

### 집중 개발 시나리오 (8-10일)
```
Day 1-2:   Phase 0 - 사전 조사
Day 3-7:   Phase 1 - MVP 개발
Day 8-11:  Phase 2 - 확장 개발
Day 12-13: Phase 3 - 문서화 및 제출
```

### 여유 있는 시나리오 (13일)
```
Day 1-2:   Phase 0 - 사전 조사 + 환경 설정
Day 3-8:   Phase 1 - MVP 개발 (디버깅 시간 포함)
Day 9-12:  Phase 2 - 확장 개발
Day 13:    Phase 3 - 문서화 및 제출
```

---

## 🔄 진행 방식

### 애자일 접근법
각 Phase는 독립적으로 완성 가능하며, 언제든 중단하고 제출 가능합니다.

```
Phase 0 완료 → 클라이언트 질의 가능
Phase 1 완료 → 부분 제출 가능 (MVP)
Phase 2 완료 → 완전 제출 가능
Phase 3 완료 → 최종 제출
```

### 체크포인트
각 Phase 종료 시:
1. ✅ 코드 리뷰 (자체 점검)
2. ✅ 테스트 실행
3. ✅ 문서 업데이트
4. ✅ 다음 Phase 진행 여부 결정

---

## 📊 성공 지표

### Phase별 성공 기준

| Phase | 최소 성공 | 이상적 성공 |
|-------|-----------|-------------|
| **Phase 0** | - 4개 사이트 구조 파악<br>- MVP 지자체 선정 | - 공통 패턴 발견<br>- 기술 스택 검증 완료 |
| **Phase 1** | - 1개 지자체 동작<br>- 10개 이상 문서 수집 | - 안정적 동작<br>- LLM 비용 $10 이하 |
| **Phase 2** | - 3개 이상 지자체<br>- 2개 이상 문서 타입 | - 4개 모두 동작<br>- Continuous Update |
| **Phase 3** | - 4가지 제출물 완성 | - 포괄적 문서<br>- 데모 가능 |

---

## 🛠️ 필요 리소스

### 기술 스택
- **언어**: Python 3.11+
- **스크래핑**: Playwright, BeautifulSoup4, httpx
- **LLM**: Anthropic Claude API (또는 OpenAI)
- **DB**: SQLite
- **기타**: APScheduler, structlog, pytest

### 개발 환경
- **OS**: macOS, Linux, or Windows (WSL)
- **IDE**: VS Code (권장) 또는 PyCharm
- **버전 관리**: Git
- **패키지 관리**: uv, poetry, or pip

### API 계정
- ✅ Anthropic API Key (Claude)
- △ OpenAI API Key (선택적 Fallback)

### 예상 비용
- **LLM API**: $50-100 (전체 과정)
- **인프라**: $0 (로컬 개발)

---

## ⚠️ 리스크 관리

### 주요 리스크 및 대응책

| 리스크 | 확률 | 영향 | 대응책 |
|--------|------|------|--------|
| **사이트 접근 불가** | 낮음 | 높음 | 다른 지자체로 대체 |
| **LLM 비용 초과** | 중간 | 중간 | 규칙 기반으로 전환 |
| **복잡한 사이트 구조** | 높음 | 중간 | MVP에서 제외, 나중에 도전 |
| **개발 시간 부족** | 중간 | 높음 | Phase 단위로 제출 |
| **기술 스택 이슈** | 낮음 | 높음 | Phase 0에서 조기 검증 |

---

## 📋 체크리스트

### 시작 전 준비
- [ ] 개발 환경 설정 완료
- [ ] API Key 발급 완료
- [ ] Git repository 생성
- [ ] 실행 계획 숙지

### Phase 0
- [ ] 4개 지자체 웹사이트 조사
- [ ] 기술 스택 검증
- [ ] MVP 지자체 선정
- [ ] 프로젝트 구조 생성

### Phase 1
- [ ] 스크래퍼 기본 구조
- [ ] LLM 통합
- [ ] 로컬 저장 구현
- [ ] 10개 이상 문서 수집 성공

### Phase 2
- [ ] 3개 지자체 추가
- [ ] 3개 문서 타입 추가
- [ ] Continuous Update 구현
- [ ] 통합 테스트

### Phase 3
- [ ] 4가지 제출물 작성
- [ ] 코드 정리 및 README
- [ ] 최종 테스트
- [ ] 제출

---

## 📚 참고 문서

### 요구사항 분석
- [분류 요약](../분류-요약.md)
- [확실한 요구사항](../specs/1-확실한-요구사항/)
- [검토 필요 사항](../specs/2-검토-필요-사항/)

### 실행 계획 상세
- [Phase 0: 사전 조사](./phase-0-research.md)
- [Phase 1: MVP 개발](./phase-1-mvp.md)
- [Phase 2: 확장 개발](./phase-2-expansion.md)
- [Phase 3: 완성 및 제출](./phase-3-completion.md)

---

## 🚀 시작 방법

### 1. 준비
```bash
# 실행 계획 확인
cat implementation-plan/README.md

# Phase 0 계획 숙지
cat implementation-plan/phase-0-research.md
```

### 2. 시작
```bash
# 개발 환경 설정
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install uv

# 프로젝트 생성 (Phase 0에서 진행)
```

### 3. 진행
각 Phase 문서를 참고하여 단계별로 진행합니다.

---

**작성일**: 2025-12-11
**최종 업데이트**: 2025-12-11
**상태**: 📋 계획 수립 완료
**다음 단계**: Phase 0 시작
