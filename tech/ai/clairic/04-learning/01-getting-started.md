---
date: 2026-10-22
tags: [tech]
type: tech-tool-study
status: draft
---

# Getting started

## 1. Worker AI binding 준비

Cloudflare Worker에 AI binding을 설정한 뒤 `env.AI.run()`에서 Clairic model ID를 호출한다. binding 이름과 세부 request shape는 배포 전 [공식 model schema](https://developers.cloudflare.com/workers-ai/models/clairic/)에서 확인한다.

```ts
export default {
  async fetch(request: Request, env: Env) {
    const result = await env.AI.run("@cf/cloudflare/clairic", {
      state: invoiceText,
      fields: {
        invoice_number: { type: "text", instruction: "Invoice ID" },
        issued: { type: "date", instruction: "Issue date" },
        due_date: { type: "date", instruction: "Payment due date" },
        total: { type: "number", unit: "currency", decimals: 2 },
        contacts: {
          type: "list",
          items: { type: "text", instruction: "Contact name or email" },
        },
      },
    });
    return Response.json(result);
  },
};
```

위 코드는 학습용 형태다. 실제 property 이름·허용 `unit` 값·응답 object 구조는 Preview API 변경 가능성이 있으므로 공식 schema에 맞춰 고정한다.

## 2. Schema를 바꿔 관찰하기

- `number.decimals`를 0, 2, 4로 변경해 통화/수량 표현을 비교한다.
- `unit`과 field instruction을 명확히 해 amount와 tax, subtotal을 혼동하는지 확인한다.
- `date` instruction에 기대 형식과 의미(issued vs due)를 쓴다.
- `list.items`를 좁혀 contact, line item, recipient를 각각 별도 field로 둔다.

각 변경마다 동일한 invoice corpus와 expected answer로 validity·null rate·review rate를 기록한다.

## 3. 안전한 소비

```ts
const total = result.fields.total;
if (total.value === null || total.confidence < 0.95 || total.p_null > 0.1) {
  await enqueueHumanReview({ field: "total", source: invoiceId, total });
} else {
  await stageForValidation(total.value);
}
```

threshold는 예시일 뿐이다. 금액 한도, downstream 영향, corpus 정확도를 함께 반영한다. 자동 지급·법적 통지처럼 영향이 큰 행위에는 별도 business validation과 사람 승인을 둔다.

## 4. 완료 기준

1. 최소 20개 이상의 대표 문서에 ground truth를 만든다.
2. 각 field의 accuracy, null rate, human-review rate를 측정한다.
3. 인식 실패·모호한 원문·OCR 오류를 별도 failure class로 분류한다.
4. 원문과 span을 나란히 보여 review가 가능한지 확인한다.

## Sources

- https://developers.cloudflare.com/workers-ai/models/clairic/
- https://developers.cloudflare.com/workers-ai/configuration/bindings/
