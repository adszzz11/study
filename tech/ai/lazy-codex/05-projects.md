---
date: 2026-06-07
tags: [tech, ai, codex, lazycodex, hermes, projects]
status: published
type: tech-tool-study
---

# 05. Projects — 실전·hermes 통합

## 1. 실전 PoC (버리는 레포로)

> 자세한 런북은 기존 [[lazycodex-poc]] 참고. 요지:

1. 버리는 샘플 레포 생성(`lazycodex-poc`).
2. `npx lazycodex-ai install` → `/init-deep`.
3. `$ulw-loop "모호한 기능 구현"` 으로 검증 루프 체험.
4. **게이트 일부러 깨보기**(미완성/깨지는 테스트/stale edit) → Oracle/Ralph/Hashline이 잡는지 관찰.
5. 통째로 삭제, 결론만 기록.

## 2. hermes에 차용할 아이디어 (실 적용 후보)

| OmO 장치 | hermes 적용안 | 가치 |
|----------|---------------|------|
| **Hashline 편집 정합** | hermes-agent의 `--write` 편집을 해시 앵커로 검증 | stale/손상 편집 차단 (현재 apply_patch 의존) |
| **Oracle 독립 검증 agent** | hermes-task PR 전에 별도 review agent가 변경 검증 | self-test만으론 못 잡는 의미적 결함 |
| **Ralph Loop / Todo Enforcer** | hermes-task 장시간 작업의 idle·조기중단 방지 (ralph-loop 통합) | 거짓 완료/중단 방지 |
| **category 모델 라우팅** | hermes-route를 category 선언식으로 일반화 | quota 효율 |

## 3. 결합 아키텍처 (지향점)

```text
Discord(@Sang-MINI) → hermes-task (오케스트레이션, C)
   → hermes-repo 격리 워크트리 (격리)
   → hermes-agent --write (실행, X) + [Oracle식 검증 agent]  ← 차용
   → self-test 게이트 + Hashline 편집 정합  ← 차용
   → PR (사람 머지 게이트)  ← hermes 고유 강제
```

> lazycodex/OmO의 **검증 규율**을 hermes의 **격리+사람 게이트+운영 인프라**에 얹으면, "게으름 없는 자율 + 안전 운영" 둘 다 확보.

## 4. 도입 결정 메모
- **lazycodex 단독 도입?** → 단일-작업 검증이 필요하면 yes. 단 hermes와 역할 중복(둘 다 하니스).
- **차용만?** → 추천. Hashline·Oracle식 검증을 hermes-task에 흡수(별도 ADR로).
- **주의**: OmO는 OpenCode/Codex 종속. hermes는 codex app-server 직접 — 통합 시 어댑터 경계 고려([[multi-agent-platforms]]).

→ 빠른 참조: [[lazy-codex/cheatsheet|cheatsheet]]
