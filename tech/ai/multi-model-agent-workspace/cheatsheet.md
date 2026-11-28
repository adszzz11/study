---
date: 2026-11-27
tags: [tech]
type: tech-tool-study
status: draft
---

# Cheatsheet

## 핵심 구분

- **Role ≠ Model:** 업무 책임과 추론·생성 모델은 별개다.
- **통합 UI ≠ Orchestration:** 한 화면에서 접근 가능해도 자동 인계를 뜻하지 않는다.
- **Context ≠ Memory:** 이번 입력과 실행 사이 유지 정보를 구분한다.
- **관찰 ≠ 검증:** Dossier의 화면 관찰과 직접 재현 결과를 구분한다.

## SkillTree에 대해 말할 수 있는 것

| 항목 | 현재 범위 |
|---|---|
| Workspace | 여러 부서 agent와 모델을 한 공간에 모으는 구성 |
| Model | Claude·GPT·Gemini 등장; 선택·routing 미확인 |
| Agent | 부서별 역할 관찰; 자율 실행·협업 미확인 |
| 검증 과제 | Orchestration, context·memory, 권한, 실행 기록 |

## 평가 질문 5개

1. 모델은 사용자·agent 설정·자동 routing 중 누가 선택하는가?
2. 앞선 결과가 다음 agent에 어떤 형식으로 전달되는가?
3. 공통 자료와 부서 전용 자료의 경계가 있는가?
4. 중단·재시도·검토·승인은 어디서 하는가?
5. 어떤 입력·역할·모델이 결과를 만들었는지 추적 가능한가?

## 실험 순서

```text
동일 모델 + 역할 변경
→ 동일 역할 + 모델 변경
→ 인계 형식 비교
→ context 범위 비교
→ 실행 기록과 검토
```

모델 버전·날짜·입출력·검토 결과를 기록한다. 가격·실행 시간은 측정값만 사용한다. 원본 출처 URL이 없으므로 제품의 현재 사양·우열을 확정하지 않는다.

[[tech/ai/multi-model-agent-workspace/README|학습 경로로 돌아가기]]

## Sources

- 제공된 dossier: SkillTree 및 함께 소개된 도구의 영상 요약. 원본 URL은 제공되지 않았다.
- 출처 URL: 미제공. 영상 제목·시점의 구체 값도 현재 dossier에 없어 원문 대조가 불가능하다. URL을 추정하거나 새 출처를 추가하지 않았다.
