# 요구사항 및 분석

이 폴더에는 ZonAgent 프로젝트의 요구사항 분석 및 사전 조사 자료가 포함되어 있습니다.

## 📁 폴더 구조

### 주요 문서

- **Assignment-Description.md** - 원본 과제 설명서
- **요구사항-분류.md** - 요구사항 상세 분류 및 분석
- **과제-분석.md** - 과제 핵심 요구사항 분석
- **분류-요약.md** - 요구사항 분류 요약

### research/ - Phase 0 사전 조사 결과

**플랫폼 분석**:
- `platform-analysis.md` - 4개 플랫폼 상세 분석 (~13,000 라인)
  - HTML 구조 및 CSS Selector
  - 렌더링 방식 비교
  - 플랫폼별 특성 및 난이도
- `websites-found.md` - URL 발견 및 MVP 선정 과정

**분석 결과**:
- 4개 지자체 URL 발견
- 3개 플랫폼 분석 (Granicus, CivicEngage, CivicClerk)
- MVP 선정: Cherokee County (가장 단순한 구조)
- 렌더링 방식 분류 (서버 렌더링 vs JavaScript SPA)

### specs/ - 기술 스펙

프로젝트 기술 스펙 및 요구사항 문서:

**1-확실한-요구사항/**:
- `README.md` - 확실한 요구사항 개요
- `대상-범위-명세.md` - 4개 지자체 및 문서 타입
- `운영-모드-명세.md` - Backfill, Continuous 모드
- `제출물-명세.md` - 4가지 제출 문서

**2-검토-필요-사항/**:
- `README.md` - 검토 필요 사항 개요
- `기술적-검토-사항.md` - 기술 스택 및 구현 방법
- `클라이언트-질의-사항.md` - 클라이언트 확인 필요 사항

## 📊 Phase 0 성과

- **소요 시간**: 예상 9시간 (실제 시간 측정 필요)
- **문서 작성**: 8개 파일
- **주요 발견**:
  - Cherokee County가 가장 단순 (MVP로 최적)
  - Alpharetta/Holly Springs는 동일 플랫폼 (코드 재사용 가능)
  - 서버 렌더링 vs JavaScript SPA 분류

## 🔍 주요 인사이트

1. **MVP 선정**: Cherokee County (Granicus)
   - 서버 렌더링으로 가장 단순
   - Playwright 불필요
   - 개발 시간 50% 단축 예상

2. **플랫폼 난이도 순위**:
   - 🥇 Cherokee County (Granicus) - 가장 쉬움
   - 🥈 Marietta (CivicEngage) - 쉬움
   - 🥉 Alpharetta (CivicClerk SPA) - 중간
   - 4위 Holly Springs (CivicClerk SPA) - 중간

3. **코드 재사용 기회**:
   - Holly Springs는 Alpharetta와 동일 플랫폼
   - 한 번 구현하면 두 곳에서 재사용 가능

---

**작성일**: 2025-12-10 ~ 2025-12-11
**Phase**: 0 (사전 조사)
**상태**: ✅ 완료
