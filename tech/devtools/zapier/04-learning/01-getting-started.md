---
date: 2026-08-24
tags: [tech]
type: tech-tool-study
status: draft
---

# Zapier — Getting Started

> [[../03-references|이전: References]] · [[../README|목차로 돌아가기]] · [[02-deep-dive|다음: Deep Dive]]

## 목표

첫 Zap을 만드는 것보다 **중복 없이 안전하게 운영 가능한 작은 workflow**를 만드는 데 초점을 둔다.

```text
Form submission → validate → create CRM lead → notify Slack
```

## 1. Contract부터 정의하기

UI를 열기 전에 input, output, 실패 정책을 적는다.

| 항목 | 예시 |
|---|---|
| Trigger | Zapier Forms의 새 submission |
| Unique key | `submission_id` 또는 normalized email |
| Required fields | `email`, `company`, `consent` |
| External write | CRM lead create/update |
| Notification | 담당 Slack channel |
| Failure owner | RevOps on-call |

## 2. Trigger 연결과 sample 고르기

1. 새 Zap에서 Trigger app과 event를 선택한다.
2. 최소 권한 account를 연결한다.
3. 정상값, 빈 optional field, 특수문자를 포함한 sample을 준비한다.
4. Trigger가 Instant인지 Polling인지 확인한다.
5. sample field를 production schema로 착각하지 않는다.

> [!warning]
> test sample 하나에만 존재하는 field를 무조건 매핑하면 production에서 null/누락으로 실패할 수 있다.

## 3. Validate와 normalize

Formatter, Filter 또는 Code step으로 외부 write 전 입력을 정리한다.

```javascript
const email = (inputData.email || '').trim().toLowerCase();
if (!email.includes('@')) throw new Error('invalid email');
return { email };
```

- required field가 없으면 early stop한다.
- 날짜, phone, currency, enum을 target app 형식에 맞춘다.
- raw input과 normalized value를 구분한다.
- secret 또는 불필요한 PII를 downstream에 전달하지 않는다.

## 4. Search 후 Create/Update

중복을 피하려면 곧바로 Create하지 말고 stable key로 기존 record를 찾는다.

```text
Find lead by external_id
  ├─ found     → update allowed fields
  └─ not found → create with external_id
```

가능하면 target app의 native upsert와 unique constraint를 사용한다. Search→Create만으로는 동시 실행 race를 완전히 막지 못한다.

## 5. Notification은 마지막에

- CRM write가 성공한 뒤 Slack에 알린다.
- 메시지에 record URL, run ID, 핵심 상태를 넣는다.
- channel mention과 고객 PII 노출을 최소화한다.
- 실패 알림과 성공 알림을 다른 목적·channel로 분리한다.

## 6. 테스트와 publish

| 테스트 | 기대 결과 |
|---|---|
| 정상 input | CRM write 1회, Slack 알림 1회 |
| 동일 event 재전송 | 중복 create 없음 |
| required field 누락 | 외부 write 전 중단 |
| target API 일시 실패 | retry 후에도 duplicate 없음 |
| 이미 존재하는 lead | update path 실행 |

Publish 전 월간 task를 추정한다.

```text
expected tasks/month
≈ events × paid steps per event × fan-out × (1 + retry rate)
```

## 7. 운영 checklist

- [ ] Zap owner와 failure owner 지정
- [ ] credential을 개인 계정 대신 적절한 service/team account로 연결
- [ ] unique key와 loop prevention field 문서화
- [ ] Zap History와 alert 확인 주기 정의
- [ ] 변경 전후 test sample과 결과 보관
- [ ] replay 전에 외부 side effect 중복 가능성 검토
- [ ] 월간 task usage budget과 경고 설정

## Sources

- [What is a Zap?](https://help.zapier.com/hc/en-us/articles/8496309697421-What-is-a-Zap)
- [How Zap triggers work](https://help.zapier.com/hc/en-us/articles/8496244568589-How-Zap-triggers-work)
- [View and manage Zap history](https://help.zapier.com/hc/en-us/articles/8496291146637-View-and-manage-your-Zap-history)
- [Zapier task usage rates](https://zapier.com/pricing/rates)

