---
date: 2026-11-01
tags: [tech]
type: tech-tool-study
status: draft
---

# ego(lite) 시작하기

[[tech/scraping/egolite-agent-browser/README|README]] · [[tech/scraping/egolite-agent-browser/04-learning/02-deep-dive|심화]] · [[tech/scraping/egolite-agent-browser/cheatsheet|Cheatsheet]]

## 1. 설치와 profile import

ego(lite)를 설치한 뒤 Chrome profile import 여부를 신중히 결정한다. import는 기존 로그인과 bookmarks를 편하게 가져오지만, agent가 승인된 authenticated webpage content를 볼 수 있다는 의미이기도 하다. 최소 권한 account 또는 read-only task부터 시작한다.

`ego-browser` Skill을 설치하거나 desktop app이 제공한 CLI를 사용하고, 다음으로 확인한다.

```bash
command -v ego-browser
ego-browser --help
```

## 2. 첫 Task Space

구체 API는 현재 설치된 version의 type definition과 Quick start를 우선한다. 흐름은 `taskSpace()` 또는 `useOrCreateTaskSpace()`로 task를 열고, `Page`를 연 뒤 Snapshot을 읽는 것이다.

```ts
// API 이름과 import 경로는 설치한 ego-browser version의 문서를 확인한다.
const space = await ego.useOrCreateTaskSpace({ name: "read-only-research" });
const page = await space.newPage();

await page.goto("https://example.com");
const text = await page.snapshotText();
console.log(text);
```

## 3. ref 기반 조작

1. `snapshot()` 또는 `snapshotText()`로 현재 UI와 ref를 읽는다.
2. Snapshot에서 확인한 ref로 click·fill을 수행한다.
3. navigation, submit, tab switch, dynamic rerender 뒤에는 새 Snapshot을 얻는다.

```ts
const snapshot = await page.snapshot();
// 예: snapshot에서 확인한 ref만 사용한다.
await page.click("@92");
await page.fill("@104", "검색어");
```

ref는 Snapshot 시점에만 유효한 임시 식별자다. 추측한 CSS selector나 오래된 ref에 의존하지 않는다.

## 4. handoff boundary

CAPTCHA, SMS/QR login, hardware key, OAuth authorization, 결제, publish/delete 직전에는 task를 중지하고 사용자에게 control을 넘긴다. export와 submit은 명시적 confirmation을 workflow 조건으로 둔다.

## Sources

- https://www.egolite.app/document/en/docs/quick-start
- https://github.com/citrolabs/ego-lite/blob/main/skills/ego-browser/references/install.md
- https://www.egolite.app/document/en/docs/snapshot

