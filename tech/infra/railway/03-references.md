# Railway 참고 자료

## 공식 문서

### 핵심 문서
| 문서 | 링크 | 설명 |
|------|------|------|
| **공식 문서** | [docs.railway.app](https://docs.railway.app) | 모든 기능 상세 설명 |
| **API Reference** | [docs.railway.app/reference/cli-api](https://docs.railway.app/reference/cli-api) | CLI 및 API 레퍼런스 |
| **Changelog** | [railway.app/changelog](https://railway.app/changelog) | 업데이트 내역 |

### 주요 섹션별 링크
| 섹션 | 링크 |
|------|------|
| Quick Start | [docs.railway.app/quick-start](https://docs.railway.app/quick-start) |
| 배포 가이드 | [docs.railway.app/deploy/deployments](https://docs.railway.app/deploy/deployments) |
| 데이터베이스 | [docs.railway.app/databases](https://docs.railway.app/databases) |
| 환경 변수 | [docs.railway.app/develop/variables](https://docs.railway.app/develop/variables) |
| 네트워킹 | [docs.railway.app/deploy/exposing-your-app](https://docs.railway.app/deploy/exposing-your-app) |
| CLI | [docs.railway.app/develop/cli](https://docs.railway.app/develop/cli) |

---

## 학습 자료

### 튜토리얼
| 제목 | 유형 | 난이도 |
|------|------|--------|
| [Deploy Your First App](https://docs.railway.app/tutorials/getting-started) | 공식 | 입문 |
| [Deploy Django on Railway](https://blog.railway.app/p/django) | 블로그 | 초급 |
| [Full Stack with Railway](https://blog.railway.app) | 블로그 | 중급 |

### 영상 자료
| 제목 | 채널 | 링크 |
|------|------|------|
| Railway Overview | Railway 공식 | [YouTube](https://www.youtube.com/@Railway) |
| Railway + Next.js 배포 | 다양한 크리에이터 | YouTube 검색 |
| Railway vs Vercel | 비교 영상 | YouTube 검색 |

### 블로그 포스트
- [Railway 공식 블로그](https://blog.railway.app) - 신기능, 사용 사례
- [Dev.to Railway 태그](https://dev.to/t/railway) - 커뮤니티 튜토리얼
- [Medium Railway 검색](https://medium.com/search?q=railway) - 다양한 경험기

---

## 커뮤니티

### 공식 채널
| 플랫폼 | 링크 | 용도 |
|--------|------|------|
| **Discord** | [discord.gg/railway](https://discord.gg/railway) | 실시간 질문, 커뮤니티 |
| **Twitter/X** | [@Railway](https://twitter.com/Railway) | 공지, 업데이트 |
| **GitHub** | [github.com/railwayapp](https://github.com/railwayapp) | 이슈, 오픈소스 |

### 지원 받기
```
1. Discord #help 채널 - 커뮤니티 도움
2. GitHub Issues - 버그 리포트, 기능 요청
3. support@railway.app - 공식 지원 (Pro 플랜)
4. docs.railway.app - 문서 먼저 확인
```

---

## 유용한 도구

### CLI 도구
```bash
# Railway CLI 설치
npm install -g @railway/cli

# 또는 curl로 설치
curl -fsSL https://railway.app/install.sh | sh

# 버전 확인
railway --version
```

### 관련 도구
| 도구 | 용도 | 링크 |
|------|------|------|
| **Nixpacks** | Railway 빌드 시스템 | [github.com/railwayapp/nixpacks](https://github.com/railwayapp/nixpacks) |
| **railway-cli** | 명령줄 도구 | npm |
| **GitHub Actions** | CI/CD 연동 | [Actions Marketplace](https://github.com/marketplace) |

---

## 템플릿 갤러리

### 인기 템플릿
| 이름 | 설명 | 원클릭 배포 |
|------|------|------------|
| **Ghost** | 블로그 플랫폼 | [배포](https://railway.app/template/ghost) |
| **Strapi** | Headless CMS | [배포](https://railway.app/template/strapi) |
| **Metabase** | BI 도구 | [배포](https://railway.app/template/metabase) |
| **Plausible** | 웹 분석 | [배포](https://railway.app/template/plausible) |
| **n8n** | 워크플로우 자동화 | [배포](https://railway.app/template/n8n) |
| **Umami** | 웹 분석 | [배포](https://railway.app/template/umami) |

### 템플릿 갤러리
- [railway.app/templates](https://railway.app/templates) - 전체 템플릿 목록

---

## 예제 저장소

### 공식 예제
| 언어/프레임워크 | 저장소 |
|----------------|--------|
| Node.js/Express | [railwayapp/examples](https://github.com/railwayapp/examples) |
| Python/Django | 공식 문서 예제 |
| Go/Gin | 공식 문서 예제 |

### 커뮤니티 예제
- GitHub에서 `railway` + 원하는 기술 스택으로 검색
- 예: `railway nextjs`, `railway spring boot`

---

## 학습 로드맵

### 입문자 (1-2주)
```
1. 공식 Quick Start 따라하기
2. CLI 설치 및 기본 명령어
3. 환경 변수 설정
4. PostgreSQL 연결
```

### 중급자 (3-4주)
```
1. 멀티 서비스 구성
2. Private Network 활용
3. 커스텀 도메인 설정
4. CI/CD 파이프라인 구성
```

### 고급자 (5주+)
```
1. 대규모 트래픽 대응
2. 비용 최적화 전략
3. 모니터링 및 알림 시스템
4. 재해 복구 계획
```

---

## 문제 해결 리소스

### 자주 묻는 질문
| 문제 | 해결 방법 |
|------|----------|
| 빌드 실패 | Nixpacks 로그 확인, `railway.toml` 설정 |
| 배포 후 접속 불가 | PORT 환경변수 확인, 헬스체크 경로 |
| DB 연결 실패 | 환경 변수 확인, Private Network 설정 |
| 비용 급증 | 리소스 모니터링, 유휴 서비스 중지 |

### 디버깅 가이드
1. **로그 확인**: `railway logs` 또는 대시보드
2. **환경 변수**: `railway variables` 로 확인
3. **빌드 로그**: 대시보드 > Deployments > Build Logs
4. **Discord 검색**: 비슷한 문제 사례 찾기

---

## 다음 단계

- [[04-learning/01-quickstart|Quick Start]] - 실제 배포 시작하기
- [[cheatsheet|Cheatsheet]] - 명령어 빠른 참조
