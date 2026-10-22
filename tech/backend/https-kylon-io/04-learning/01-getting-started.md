---
date: 2026-10-22
tags: [tech]
type: tech-tool-study
status: draft
---

# Kylon Getting Started

## Goal

가장 좁은 업무 하나를 최소 권한으로 운영한다.

> 예시: 매주 미납 invoice를 집계하고 follow-up email은 **draft로만** 생성한다.

## Step 1 — Scope the Work

brief에 다음을 먼저 쓴다.

| 항목 | 예시 |
| --- | --- |
| 입력 | billing mailbox의 invoice, CRM 담당자 정보 |
| 결과 | 미납 목록 record와 담당자별 email draft |
| 금지 | 자동 발송, CRM의 기존 금액 덮어쓰기 |
| 승인자 | AR 담당자 |
| 실패 시 | Room에 예외 목록과 근거를 남기고 중단 |

성공 기준을 “agent가 끝냈다”가 아니라, 사람이 검토할 수 있는 record·근거·draft가 생성되었는지로 정의한다.

## Step 2 — Create a Dedicated Room

- 업무 전용 Room을 만들고 필요한 담당자만 초대한다.
- Room membership과 agent access list를 각각 검토한다.
- agent에게 업무 목적, 허용된 data source, 결과 format, 승인 대상 action을 명시한다.

## Step 3 — Add Minimum Connections

처음에는 Gmail/Drive/CRM 등 필요한 Connection만 연결한다. workspace-wide 접근이나 write 권한을 기본값으로 주지 않는다.

```text
Invoice agent
  read: billing mailbox, invoice folder
  write: tracker의 정해진 field
  draft: customer follow-up email
  prohibited: send email, delete data, change member permission
```

권한을 준 뒤에는 agent가 실제로 사용할 계정과 대상 data가 맞는지 확인한다.

## Step 4 — Build and Review the App

tracker App을 쓴다면 publish 전에 preview에서 다음을 확인한다.

- record field 이름과 validation
- 모바일 화면에서의 입력성
- 공개 범위와 접근 주체
- record update가 workflow를 의도치 않게 trigger하지 않는지

## Step 5 — Add a Safe Workflow

schedule, webhook 또는 record change를 trigger로 설정한다. 첫 실행은 작은 샘플로 진행하고, email·공개 배포·권한 확대에는 approval card를 남긴다.

## Step 6 — Review Every Run

Room thread receipt, tool trace, run history를 함께 본다.

- 처리하지 못한 입력과 원인
- 예상보다 큰 credit 사용량
- 잘못된 Connection 또는 계정 사용 여부
- draft 품질과 사람이 수정한 패턴

수정이 반복되면 prompt를 길게 하는 대신 record schema, input 조건, result format을 명확하게 만든다.

## Next

- [[02-deep-dive|Permission, approval, App 운영 심화]]
- [[../05-projects|프로젝트 아이디어]]
