---
date: 2026-11-01
tags: [tech]
type: tech-tool-study
status: draft
---

# ego(lite) Cheatsheet

[[tech/scraping/egolite-agent-browser/README|README]] · [[tech/scraping/egolite-agent-browser/04-learning/01-getting-started|시작하기]]

## 설치 확인

```bash
command -v ego-browser
ego-browser --help
```

## 기본 작업 loop

```text
Task Space 생성/선택
  → Page 열기
  → snapshot() / snapshotText()
  → Snapshot의 현재 ref로 click / fill
  → 화면 변경
  → re-snapshot
```

## 규칙

| 상황 | 할 일 |
|---|---|
| navigation·submit·tab switch·rerender 뒤 | 기존 ref를 버리고 re-snapshot |
| CAPTCHA, SMS/QR, hardware key | agent 중지, 사용자 takeover |
| OAuth, 결제, publish/delete | 명시적 user confirmation 후 진행 |
| 반복 사이트 작업 | `learnings`에 manifest, notes, tools를 축적 |
| 동시 Space의 write action | 동일 account에서는 직렬화 |

## 기억할 개념

- **Task Space**: agent task의 tabs, cookies, storage를 분리하는 workspace
- **Snapshot**: accessibility tree에서 얻는 structured text와 임시 ref
- **human takeover**: 사용자가 바로 browser control을 이어받는 경계
- **authenticated content**: login된 페이지 내용; Space가 있어도 접근 권한의 영향을 받음

## Sources

- https://www.egolite.app/document/en/docs/quick-start
- https://www.egolite.app/document/en/docs/snapshot
- https://www.egolite.app/document/en/docs/space
