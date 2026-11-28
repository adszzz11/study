---
date: 2026-11-29
tags: [tech]
type: tech-tool-study
status: draft
---

# Deep Dive: cache·chunk·section ID

## 1. 선택적 출력과 fetch 구분

첫 `sections` 또는 `content` 요청은 full wiki를 가져와 JSON cache로 저장한다. 이후 요청은 cache를 재사용한다. Context 입력량 감소와 최초 네트워크 전송량 감소를 같은 효과로 보고하지 않는다.

## 2. Cache 경로 우선순위

1. `CODEWIKI_CACHE_DIR` 환경변수
2. `cache directory <path>`로 저장한 설정
3. `$XDG_CACHE_HOME/codewiki-cli`
4. `XDG_CACHE_HOME`이 없으면 `~/.cache/codewiki-cli`

저장한 경로는 이후 실행에도 적용되지만 환경변수가 override한다. TTL·자동 만료 정책은 확인되지 않으므로 최신 문서가 필요하면 명시적으로 refresh한다.

```bash
node bin/run.js cache directory
node bin/run.js cache directory /tmp/codewiki-study-cache
node bin/run.js sections fastify/demo --refresh
# 위 목록에서 ID를 다시 선택한 뒤 실행한다. 1은 예시다.
node bin/run.js content fastify/demo 1 --chunks
```

## 3. ID 수명 실습

Wiki 갱신 시 숫자 ID가 바뀔 수 있다. `1`을 특정 주제의 영구 식별자로 저장하지 않는다. Anchor 역시 영구 안정성이 보장되지 않는다.

- [ ] refresh 전 목록과 선택한 제목·요약·anchor·ID를 기록한다.
- [ ] `sections --refresh` 후 목록을 다시 읽는다.
- [ ] 제목·요약·anchor를 함께 검토해 새 ID로 본문을 조회한다.
- [ ] ID 변경과 내용 변경을 구분해 기록한다.

`content --refresh`도 지원하지만 새 wiki에서 ID 의미가 바뀔 수 있으므로 자동화는 `sections --refresh` → 재선택 → `content` 순서로 구성하는 편이 적절하다.

## 4. Chunk와 성능 실험

`--chunks`는 Markdown heading·block 경계로 나눈다. 최대 크기·token 기준·overlap·세부 schema는 미확인이다. 특정 모델의 context limit 준수를 자동 보장한다고 가정하지 않는다.

| 비교 | 기록할 값 | 해석 주의 |
|---|---|---|
| 최초 요청 vs cache 재사용 | 경과 시간, cache 상태 | 네트워크·문서 크기 조건 기록 |
| 전체 문서 vs 섹션 vs chunk | 입력 문자·token 수, 답변 누락 | 전체 문서 baseline 확보 방식 명시 |
| refresh 전후 | 제목·anchor·본문 차이 | ID만으로 변경 판정 금지 |

표는 앞으로 수행할 실험 설계이며 측정 결과가 아니다. 전체 문서를 직접 출력하는 CLI 명령은 자료에서 확인되지 않았다.

## 5. 개발 검증

```bash
pnpm format:check
pnpm lint
pnpm typecheck
pnpm test
# CLI 수정 후 skill 배포본도 갱신
pnpm build:skill
```

추가 코드 검토에서는 RPC 실패, wiki 미제공, 잘못된 ID, cache 손상, Markdown 경계 처리를 확인한다. 위 명령의 실제 통과 여부·coverage는 미확인이다.

다음: [[tech/devtools/codewiki-cli-analysis-9fbbd58a/05-projects|적용 프로젝트]] · [[tech/devtools/codewiki-cli-analysis-9fbbd58a/README|학습 진입점]]


## Sources

- https://github.com/miinhho/codewiki-cli — 제공된 dossier의 README 기반 정리. 실습 및 성능 검증은 미실행.
