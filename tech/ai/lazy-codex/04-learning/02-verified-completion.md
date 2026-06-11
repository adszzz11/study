---
date: 2026-06-07
tags: [tech, ai, codex, lazycodex, verified-completion]
status: published
type: tech-tool-study
---

# 04-2. 검증 완료 메커니즘 — 거짓 완료를 잡는 법

> OmO/lazycodex가 게으름을 잡는 **5대 장치**. "실행 ≠ 검증" 분리가 핵심.

## 1. plan → execute → verify 루프

```text
/start-work (Prometheus 계획·인터뷰로 모호성 제거)
   → /ultrawork (Sisyphus 위임 → Hephaestus 실행)
      → Oracle 검증 + Ralph Loop (통과 못하면 재계획·재개, ≤500 iters)
         → durable 상태 .omo/ulw-loop/
```

## 2. 멀티에이전트 역할

| Agent | 역할 |
|-------|------|
| Prometheus | 계획·인터뷰 — 잘못 이해한 작업에 compute 낭비 방지 |
| Sisyphus | 오케스트레이터 — 분류·위임, **중도 포기 거부** |
| Hephaestus | 심층 자율 워커 — goal만 주면 end-to-end |
| **Oracle** | **검증** — 계획 대비 정합, 갭=실패 |
| Librarian | 검색·문서(context7/grep.app) |

## 3. 5대 거짓-완료 차단 장치

1. **Hashline (해시 앵커 편집)**
   ```text
   11#VK| function hello() {
   22#XJ|   return "world";
   ```
   `LINE#HASH`로 편집 → 파일 변경 시 해시 불일치로 **편집 거부(손상 전)**. *Grok Code Fast 1: 6.7% → 68.3%* (편집 메커니즘 교체만으로).
2. **Ralph Loop**(`/ulw-loop`): agent가 **자기 출력 재독** → 미완성 섹션 발견 시 계속.
3. **Todo Enforcer**: idle agent를 강제 재engage(놀지 못함).
4. **Oracle 검증 패스**: 완료물을 계획 대비 재검토 → 갭=실패→루프.
5. **Durable evidence**(`.omo/ulw-loop/`): 완료 상태 디스크 기록 → 추측 아닌 정확 재개.

## 4. 게이트 일부러 깨보기 (학습 포인트)

> 검증이 진짜 도는지 확인하려면 — 일부러 불완전/거짓 완료를 유도하고 게이트가 잡는지 본다.

- 미완성 함수(`TODO`/플레이스홀더)를 남기게 유도 → **Ralph Loop/Oracle이 다시 채우는지**.
- 테스트가 깨지는 변경 요청 → **검증 단계에서 실패로 잡고 재시도하는지**.
- 파일을 외부에서 수정 후 편집 → **Hashline이 stale edit 거부하는지**.

(기존 [[lazycodex-poc]] 런북에 "게이트 깨보기" 실습 절차가 있음 — 참고.)

## 5. hermes의 등가물 (대조)

| OmO | hermes |
|-----|--------|
| Oracle 검증 | `ops/gates/self-test.sh`(배포 전 게이트) |
| Ralph Loop | ralph-loop 플러그인 / autodeploy 재시도 |
| Hashline | (없음 — codex apply_patch 의존) → **차용 후보** |
| durable .omo | self-test 로그 + git 상태 |
| 사람 게이트 | **PR-only, 머지는 사람**(ADR-018, 강제) |

→ 통합 아이디어: [[lazy-codex/05-projects|05. Projects]]
