# Claude Code 변경사항

> 출처: https://code.claude.com/docs/en/changelog

---

## v2.1.170 (2026-06-09)

### Claude Fable 5 지원

- Claude Fable 5 (`claude-fable-5`) 사용 가능
- Mythos-class 모델 — 일반 공개 최고 성능
- `claude code update` 로 v2.1.170으로 업데이트 필요

### 버그 수정

- VS Code integrated terminal 또는 Claude Code 환경 변수를 상속한 셸에서 실행 시:
  - 세션 트랜스크립트 저장 안 됨
  - `--resume` 목록에 세션이 나타나지 않음
  - → **수정됨**

---

## v2.1.169 (2026-06-08)

### 신규 기능

- **`post-session` lifecycle hook**: 세션 종료 후 실행되는 훅
- **`--safe-mode` 플래그**: 안전 모드로 Claude Code 실행
- **`/cd` 커맨드**: 작업 디렉터리 변경
- **Enterprise MCP policy 버그 수정** 다수

---

## 관련 링크

- Claude Code 전체 CHANGELOG: https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md
- Claude Code 문서: https://code.claude.com/docs
