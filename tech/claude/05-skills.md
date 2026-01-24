---
date: 2026-01-24
tags:
  - tech
  - claude
  - skills
  - plugin
parent: "[[README]]"
---

# Claude Code - Skills

> ⬅️ [[04-advanced|이전: 심화]] | [[README|목차]] | ➡️ [[06-hooks|다음: Hooks]]

---

## 1. Skills란?

> Claude Code의 기능을 확장하는 커스텀 플러그인 시스템

### 핵심 개념

- `SKILL.md` 파일을 포함한 폴더
- 자동 또는 수동으로 활성화
- 슬래시 명령어(`/skill-name`)로 호출 가능

### Skill의 범위 (Scope)

| 범위 | 위치 | 설명 |
|------|------|------|
| Enterprise | 조직 설정 | 조직 전체 공유 |
| Personal | `~/.claude/skills/` | 개인 전역 설정 |
| Project | `.claude/skills/` | 프로젝트별 설정 |

---

## 2. Skill 구조

### 기본 폴더 구조

```
.claude/skills/
└── my-skill/
    ├── SKILL.md      ← 필수: 스킬 정의
    ├── templates/     ← 선택: 템플릿 파일들
    └── scripts/       ← 선택: 스크립트들
```

### SKILL.md 구조

```markdown
---
name: my-skill
description: 스킬 설명
version: 1.0.0
disable-model-invocation: false  # true면 수동 호출만
allowed-tools:                    # 허용할 도구 목록
  - Read
  - Write
  - Edit
context: normal                   # normal | fork
---

# 스킬 지시사항

여기에 Claude가 따라야 할 지시사항 작성
```

---

## 3. SKILL.md 필드

### 주요 필드

| 필드 | 타입 | 설명 |
|------|------|------|
| `name` | string | 스킬 이름 (슬래시 명령어) |
| `description` | string | 스킬 설명 |
| `disable-model-invocation` | boolean | 자동 호출 비활성화 |
| `allowed-tools` | array | 사용 가능한 도구 제한 |
| `context` | string | `normal` 또는 `fork` |

### context: fork

별도의 서브에이전트 컨텍스트에서 실행

```yaml
context: fork  # 메인 대화와 분리된 컨텍스트
```

---

## 4. 동적 컨텍스트 주입

### 셸 명령어 실행

`!`command`` 문법으로 셸 명령어 결과를 주입

```markdown
# 프로젝트 구조 스킬

현재 프로젝트 구조:
!`tree -L 2 -I node_modules`

package.json 내용:
!`cat package.json`
```

### 파일 내용 주입

```markdown
# 스타일 가이드 스킬

코딩 스타일:
!`cat .eslintrc.json`

이 스타일 가이드를 따라 코드를 작성하세요.
```

---

## 5. 실전 예시

### 코드 리뷰 스킬

```markdown
---
name: code-review
description: 코드 리뷰 수행
allowed-tools:
  - Read
  - Grep
  - Glob
---

# 코드 리뷰어

## 리뷰 기준
1. 코드 가독성
2. 성능 이슈
3. 보안 취약점
4. 테스트 커버리지

## 출력 형식
- **파일**: 파일 경로
- **라인**: 라인 번호
- **심각도**: 높음/중간/낮음
- **설명**: 문제점과 개선 제안
```

### 마크다운 작성 스킬

```markdown
---
name: md-writer
description: 한국어 마크다운 작성
disable-model-invocation: true
---

# 마크다운 작성자

## 규칙
- 모든 내용은 한국어로 작성
- Obsidian wiki-link 문법 사용: [[링크]]
- 이모지 사용 금지

## 템플릿
!`cat templates/note-template.md`
```

### Git 커밋 스킬

```markdown
---
name: commit
description: Gitmoji 커밋 메시지 생성
---

# Git 커밋 도우미

## 커밋 메시지 형식
`<gitmoji> [type] <설명>`

## Gitmoji 목록
!`cat .github/gitmoji.md`

## 사용법
1. 변경사항 분석
2. 적절한 gitmoji 선택
3. 한국어로 커밋 메시지 생성
```

---

## 6. 스킬 호출

### 자동 호출

Claude가 컨텍스트에 맞게 자동으로 스킬 활성화

```
> 코드 리뷰해줘
# code-review 스킬이 자동 활성화
```

### 수동 호출

슬래시 명령어로 직접 호출

```
> /code-review src/main.js
> /md-writer 새 노트 작성
> /commit
```

### 자동 호출 비활성화

```yaml
disable-model-invocation: true
```

설정 시 `/skill-name`으로만 호출 가능

---

## 7. 도구 제한

### allowed-tools

스킬이 사용할 수 있는 도구 제한

```yaml
allowed-tools:
  - Read      # 파일 읽기만
  - Grep      # 검색만
  - Glob      # 파일 찾기만
```

### 읽기 전용 스킬

```yaml
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash  # 읽기 명령만 허용
```

---

## 8. 스킬 Hot-Reload

### v2.1.0+ 기능

스킬 파일 수정 시 즉시 반영 (재시작 불필요)

```bash
# 스킬 수정
vim .claude/skills/my-skill/SKILL.md

# 바로 사용 가능
> /my-skill
```

---

## 9. Best Practices

### DO ✅

- 명확한 목적의 스킬 작성
- 필요한 도구만 허용
- 동적 컨텍스트로 최신 정보 주입
- 버전 관리

### DON'T ❌

- 너무 범용적인 스킬
- 모든 도구 허용
- 민감 정보 하드코딩
- 복잡한 의존성

---

## 다음 단계

> [!tip] 다음으로
> Skills를 이해했다면 [[06-hooks|Hooks]]에서 자동화를 배워보세요.

---

## References

- [Claude Code Skills 공식 문서](https://docs.anthropic.com/claude/docs/claude-code-skills)
- [Agent Skills 표준](https://github.com/anthropics/agent-skills)
