---
date: 2026-11-27
tags: [tech]
type: tech-tool-study
status: draft
---

# Cheatsheet

## 기억할 구조

```text
운영 관점: 서버 확보 → 도구 운영 → 업무 자동화 → 접속 설정
기능 분해: 문의 발생 → 흐름 실행 → 응답 결정 → 응답 전달
```

두 줄 모두 학습용 정리다. 실제로 확인된 단일 통합 시스템 구조를 의미하지 않는다.

| 기억할 사실 | 피할 결론 |
|---|---|
| n8n이 문의 자동 응답 용도로 등장 | AI·LLM·RAG 사용 확정 |
| 영상에 12GB·2코어 소개 | 현재 무료 조건·처리량 보장 |
| Docker·Coolify·Twenty 등장 | n8n과의 실제 연동 확정 |
| 접속 실패와 80·443 표시 | 방화벽 원인·해결 성공 확정 |
| 초기 응대 감소가 기대 목적 | 개선 수치가 입증됐다는 주장 |

## 실습 전후 체크

- [ ] 문의 범위와 정상 응답을 정의했는가?
- [ ] 입력·Trigger·결정 규칙·전달 채널을 기록했는가?
- [ ] 실행 성공과 수신 측 전달 성공을 구분했는가?
- [ ] 접속 경로와 Workflow를 각각 검증했는가?
- [ ] 무료 범위·자원 배정·비용 조건을 현재 자료로 확인했는가?
- [ ] 확인된 연결만 아키텍처에 포함했는가?
- [ ] 공개 기록에서 개인정보와 Credential을 제거했는가?

## 기술스택 요약

- 자동화: n8n 문의 자동 응답. AI 사용과 상세 Workflow 미확인.
- 인프라: Oracle Always Free 소개. 영상 사양은 메모리 12GB·코어 2개.
- 배포·실습: Docker·Coolify 등장. n8n의 실제 배포 구성 미확인.
- 고객 관리·운영: Twenty와 80·443 설정 단서. 연동과 접속 실패 원인 미확인.

## Sources

- 사용자 제공 dossier: 영상 수집 요약. 원본 영상 URL은 제공되지 않아 원문 대조가 불가능하다.
- n8n 공식 문서: https://docs.n8n.io/ — 후속 확인용이며 영상 구현의 증거는 아니다.
- Oracle Free Tier 공식 안내: https://www.oracle.com/cloud/free/ — 현재 조건을 별도로 확인할 자료다.

## Related Notes

- [[tech/backend/n8n-inquiry-auto-response/README|학습 경로로 돌아가기]]
