# 4-3. Data Interpreter

## 🎯 개념

> ChatGPT의 Code Interpreter를 멀티 에이전트로 강화. **계획 → 코드 작성 → 실행 → 디버그**를 반복.

## ⚡ 사용

```bash
metagpt "이 CSV 분석해서 트렌드 추출 + 그래프"
# data/sales.csv 파일 자동 인식
```

또는 Python:
```python
from metagpt.roles.di.data_interpreter import DataInterpreter
import asyncio

async def main():
    di = DataInterpreter()
    result = await di.run("data/sales.csv 매출 트렌드 분석 + matplotlib 그래프")
    print(result)

asyncio.run(main())
```

## 🔄 내부 동작

```
1. 계획 수립 (Plan)
   ├─ "데이터 로드"
   ├─ "기본 통계"
   ├─ "월별 집계"
   └─ "시각화"

2. Step 1 실행
   ├─ 코드 작성 (LLM)
   ├─ 실행 (Jupyter kernel)
   └─ 결과 검증

3. 실패 시 디버그
   └─ 오류 + 코드를 LLM에 다시 보내 수정

4. Step 1 성공 → Step 2 …

5. 종합 보고서 작성
```

## 🏆 벤치마크 강점

- ML 작업에서 GPT-4 단독 대비 정확도 ↑ (논문 보고)
- 자동 디버그로 한 번 실패해도 회복
- 시각화 코드 잘 생성

## ⚠️ 주의

- 외부 파일 읽기/쓰기 권한 → Docker 격리 권장
- 데이터 크기 큰 경우 — 샘플링 후 분석
- 한 세션이 길어지면 context 폭주 → step별 분리

## ✅ 체크포인트
- [ ] CSV 자동 분석 동작
- [ ] 실패 시 자동 디버그 확인
- [ ] 시각화 파일 (.png) 생성됨
- [ ] Docker 모드에서 격리 실행

## 🔗 다음 → [04-incremental-dev.md](04-incremental-dev.md)
