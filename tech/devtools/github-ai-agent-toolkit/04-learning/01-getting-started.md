---
date: 2026-11-01
tags: [tech]
type: tech-tool-study
status: draft
---

# 시작하기: 작은 skill과 private gateway

[[tech/devtools/github-ai-agent-toolkit/README|README]]의 첫 실습은 새 권한을 최소화하고, 결과와 위험을 함께 기록하는 것이다.

## 1. Ponytail로 작은 diff 만들기

1. own bug-fix repository와 test를 하나 고른다.
2. 변경 전 diff 크기와 test 결과를 기록한다.
3. Ponytail의 YAGNI 기준으로 요구사항 밖의 refactor를 제외한다.
4. 변경 후 diff, test, 제외한 변경을 비교한다.

## 2. Taste Skill 결과 비교

같은 frontend 요구사항을 기본 agent와 Taste Skill에 각각 실행한다. typography, spacing, motion, keyboard navigation, contrast를 screenshot과 함께 비교한다. browser inspection은 test profile에서만 한다.

## 3. FreeLLMAPI localhost 실습

Docker 배포는 documentation의 최신 명령을 확인한 후 localhost에만 bind한다. OpenAI-compatible client로 streaming과 provider fallback을 시험하되, production key를 공유하지 않는다.

```text
client -> http://127.0.0.1:<port>/v1 -> gateway -> provider A
                                           -> fallback provider B
```

외부 공개 전에는 auth, encrypted storage, backup, key rotation 정책을 준비한다.

## 완료 기준

- [ ] third-party source와 install script를 읽었다.
- [ ] 실행·파일·network·credential permission을 기록했다.
- [ ] localhost bind와 test key를 사용했다.
- [ ] rollback 또는 uninstall 방법을 확인했다.

심화: [[tech/devtools/github-ai-agent-toolkit/04-learning/02-deep-dive|Deep Dive]]

## Sources

- https://github.com/DietrichGebert/ponytail
- https://github.com/Leonxlnx/taste-skill
- https://github.com/tashfeenahmed/freellmapi/blob/main/docs/en/README.md
