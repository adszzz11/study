# 4-4. 점진적 개발 (Incremental Development)

## 🎯 문제

한 번에 "전체 앱 만들어" 하면:
- 결과물 거대 → 검토 부담
- 실패 시 처음부터
- LLM context 폭주

## 💡 해결: 단계적 요구사항

```bash
# 1단계: MVP
metagpt "할 일 관리 앱 MVP. 백엔드 FastAPI, DB SQLite, 기본 CRUD"

# 2단계: 인증 추가 (이전 워크스페이스에 이어서)
metagpt --inc --project-path workspace/todo "JWT 인증 추가"

# 3단계: 알림
metagpt --inc --project-path workspace/todo "이메일 알림 기능"
```

`--inc` 옵션으로 기존 코드베이스에 변경분만 추가.

## 🔄 워크스페이스 구조

```
workspace/todo/
├── docs/
│   ├── prd.md
│   ├── system_design.json
│   └── task.md
├── src/
│   └── ... (코드)
├── tests/
└── .meta/
    └── history.json   # 이전 요구사항 누적
```

## 🚦 변경 vs 신규 판단

`--inc` 시 MetaGPT가:
1. 기존 PRD/설계 로드
2. 새 요구사항과 비교
3. 변경 영향 분석
4. 영향 받는 파일만 수정

## ✅ 체크포인트
- [ ] MVP → 추가 기능 점진 빌드
- [ ] `.meta/history.json`에 누적 기록 확인
- [ ] 변경 영향 받지 않는 파일은 그대로 (불필요한 재생성 없음)
- [ ] git diff로 실제 변경분만 추가됐는지

## 🔗 다음 → [../05-projects.md](../05-projects.md)
