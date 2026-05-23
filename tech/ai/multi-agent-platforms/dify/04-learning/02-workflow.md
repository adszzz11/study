# 4-2. 비주얼 Workflow

## 🎨 첫 워크플로우

대시보드 → Studio → Create App → **Workflow** 선택.

캔버스에서 노드 추가:
1. **Start** (필수): 입력 변수 정의 (text, file, etc)
2. **LLM**: 모델 선택 + 시스템 프롬프트
3. **End**: 최종 출력

## 🧱 자주 쓰는 노드

### LLM 노드
```
Model: claude-opus-4-7
System: "당신은 한국어 비서. 구체적으로 답변."
User: {{#start.user_input#}}
```

### Knowledge Retrieval
```
KB: my-docs
Query: {{#start.user_input#}}
Top K: 5
Score Threshold: 0.5
```

### Code (Python)
```python
def main(arg1: str) -> dict:
    return {"result": arg1.upper()}
```

### HTTP Request
```
GET https://api.weatherapi.com/v1/current.json
Headers: Authorization Bearer {{#env.WEATHER_KEY#}}
```

### If/Else
```
{{#llm.output#}} contains "긴급"
  → True → 알림 노드
  → False → 일반 응답
```

### Iteration
배열을 반복 처리. 예: 여러 PDF 페이지 요약.

## 🔄 변수 흐름

각 노드 출력이 다음 노드 입력으로 흐름. `{{#node_id.variable#}}` 문법으로 참조.

## 💾 DSL Export (버전 관리)

워크플로우를 YAML로 export → git에 commit → 다른 환경에서 import.

```yaml
# my-workflow.yml
version: 0.1.5
kind: workflow
spec:
  graph:
    nodes:
      - id: start
        type: start
      - id: llm-1
        type: llm
        model: claude-opus-4-7
    edges:
      - source: start
        target: llm-1
```

## 🧪 디버그 + 평가

- **Run**: 단일 실행, 노드별 출력 시각화
- **Logs**: 모든 실행 기록 + 토큰·비용
- **Evaluation**: 데이터셋으로 자동 평가 + LLM-as-judge

## ✅ 체크포인트
- [ ] Start → LLM → End 기본 워크플로우 동작
- [ ] KB Retrieval 노드 결과 정확
- [ ] If/Else 분기 동작
- [ ] DSL export/import
- [ ] Eval 데이터셋 1개 만들고 평가 실행

## 🔗 다음 → [03-rag.md](03-rag.md)
