# 4-1. 본 vault에 LLM Wiki 부트스트랩

> 시간 ~15분. 결과: 본 vault에 raw/, wiki/, CLAUDE.md 셋업 + 첫 ingest 1개.

## 📌 본 vault의 현재 상태

좋은 소식: 이미 LLM Wiki에 가까운 구조.

```
leetangle/Note/
├── study/              ← 이미 wiki/처럼 동작 중
├── activity/
├── work/
├── templates/
└── CLAUDE.md           ← 있음 (확장 필요)
```

추가할 것:
- `raw/` 디렉터리 (불변 원본)
- `wiki/` 디렉터리 또는 `study/` 안에 통합
- CLAUDE.md에 LLM Wiki 운영 매뉴얼 섹션

## 💻 셋업 (옵션 1: `/wiki init` skill 사용)

```bash
cd /Users/sm/code/leetangle/Note

# 본 환경에 이미 설치된 /wiki skill 사용
/wiki init
```

자동으로:
- `raw/` 디렉터리 + `raw/assets/`
- `wiki/index.md`, `wiki/log.md` 헤더 작성
- 본 vault `CLAUDE.md`에 wiki 스키마 섹션 추가

## 💻 셋업 (옵션 2: 수동 - 본 vault 컨벤션 맞춤)

본 vault는 이미 `study/`를 카테고리별로 잘 정리해뒀으니, **wiki/를 따로 만들지 말고 study/ 안에서 점진적으로 LLM-maintained화**가 자연스럽습니다.

```bash
mkdir -p raw/assets

# raw/는 git 추적은 하되 LLM이 안 건드리는 영역
echo "raw/는 LLM이 read-only로만 접근" > raw/README.md

# wiki/는 study/ 하위의 LLM-maintained 영역 (선택)
mkdir -p study/wiki/{concepts,entities,comparisons}
touch study/wiki/index.md study/wiki/log.md
```

## 📝 CLAUDE.md 확장 (핵심)

본 vault의 CLAUDE.md에 다음 섹션 추가:

```markdown
## LLM Wiki 운영 규칙 (Karpathy 패턴)

### 디렉터리 책임
- `raw/` — **불변 원본**. LLM은 read-only. 새 파일 추가는 사람만.
- `study/wiki/concepts/` — LLM이 작성·갱신. 한 개념 = 한 파일.
- `study/wiki/entities/` — 사람·프로젝트·도구 페이지.
- `study/wiki/index.md` — 카탈로그 (LLM 갱신).
- `study/wiki/log.md` — 작업 이력 (append-only, `## [YYYY-MM-DD] action | title`).

### Wiki 페이지 컨벤션
- frontmatter 필수: `tags`, `date`, `source_count`, `maintained_by: llm-wiki`
- 페이지당 한 개념. 500단어 이내 요약 우선.
- cross-ref: `[[concept-slug]]` (한국어 slug OK).
- 모순 발견 시 `> ⚠️ Contradiction: ...` 콜아웃.

### Ingest 워크플로우
1. `raw/<source>` 파일 읽기 (PDF는 텍스트 추출)
2. 사용자와 핵심 takeaway 대화
3. summary 페이지 생성 또는 갱신
4. 영향받는 concept/entity 페이지 10-15개 동시 갱신
5. cross-ref 추가
6. `index.md` 갱신
7. `log.md` 한 줄 append

### Do / Don't
- ✅ wiki/ 안에서 자유롭게 페이지 생성·수정
- ✅ 모순 발견 시 flag로 표시 (자동 삭제 ✗)
- ❌ raw/ 절대 수정 금지
- ❌ 사람이 작성한 study/tech/* 같은 기존 노트 임의 수정 ✗ (요청 시에만)
- ❌ 영문 slug 강제 ✗ (한국어 wikilink 허용)
```

## ⚡ 첫 Ingest

원본 1개 준비 (본인이 최근 본 자료):

```bash
# 예시: 이번 작업에서 본 Karpathy gist를 raw/에 떨어뜨림
curl -s https://gist.githubusercontent.com/karpathy/442a6bf555914893e9891c11519de94f/raw \
  > raw/karpathy-llm-wiki-gist.md
```

Claude Code 또는 `/wiki ingest`:

```bash
/wiki ingest raw/karpathy-llm-wiki-gist.md
```

기대 결과:
- `study/wiki/concepts/llm-wiki-pattern.md` 신규 생성
- `study/wiki/concepts/compounding-knowledge.md` 신규
- `study/wiki/concepts/rag-vs-llm-wiki.md` 신규
- `study/wiki/entities/karpathy.md` 신규 또는 갱신
- 본 vault 기존 [[autoresearch-study]] 와 cross-ref 추가
- `study/wiki/index.md` 갱신
- `study/wiki/log.md` 한 줄 추가

## ✅ 체크포인트

- [ ] raw/ 디렉터리 존재 + README 안내
- [ ] CLAUDE.md에 LLM Wiki 섹션 추가
- [ ] 첫 ingest로 wiki 페이지 3-5개 생성
- [ ] Obsidian Graph view에서 새 페이지 망 보임
- [ ] log.md에 첫 작업 기록

## ⚠️ 함정

| 함정 | 대응 |
|------|------|
| LLM이 raw/ 수정 | CLAUDE.md 강조 + Git pre-commit hook으로 차단 |
| 기존 study/tech 노트와 wiki 페이지 충돌 | wiki/는 별도 폴더 (`study/wiki/`) — 점진 통합 |
| 영문 slug 강제 | CLAUDE.md에 한국어 wikilink 허용 명시 |
| 너무 큰 페이지 | 500단어 이내 요약 우선, 디테일은 별도 페이지로 |
| 한 번에 너무 많은 ingest | 일 1-3개로 제한. 토큰 비용 통제 |

## 🔗 다음

→ Ingest/Query/Lint 깊이 → [02-ingest-query-lint.md](02-ingest-query-lint.md)
