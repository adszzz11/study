---
date: 2026-11-10
tags: [tech]
type: tech-tool-study
status: draft
---

# Projects

[[tech/ai/https-www-instagram-com-reel-dfjbe2jlnhy/README|README]]의 방법을 적용하는 작은 프로젝트들이다. 현재 Reel의 미확인 내용을 구현 대상으로 삼지 않는다.

## 1. Evidence intake form

caption, screenshot, transcript를 받는 form을 만들고 다음 필드를 강제한다.

```text
source URL | supplied by | captured at | permission note
artifact type | original filename | transform history | redaction status
```

완료 조건: 입력 하나가 claim 없이도 검토 가능한 provenance record가 된다.

## 2. Claim-evidence review board

Markdown 또는 issue tracker에 `claim → evidence → reviewer → verdict` 링크를 둔다. `pending`, `supported`, `contradicted`, `unverifiable`를 구분한다.

완료 조건: “알 수 없음”이 누락이 아니라 유효한 verdict로 남는다.

## 3. Video-to-Skill handoff

검증된 화면 단계와 명령만 골라 [[tech/ai/video-to-skill-pipeline/README|Video-to-Skill Pipeline]]의 timestamped procedure로 넘긴다. credential, destructive action, 감춰진 설정은 별도 승인 없이는 자동화하지 않는다.

## Sources

- https://www.w3.org/TR/prov-overview/
- https://help.archive.org/help/save-pages-in-the-wayback-machine/
