# 4-2. `>` 연산자 — 통신 흐름

## 🔁 핵심 규칙

```python
Agency([
    A,            # 사용자 ↔ A
    [A, B],       # A → B
    [A, C],       # A → C
    [B, C],       # B → C
    # C → A는 없음 (역방향 불가)
])
```

리스트 안에 단일 에이전트면 **사용자 진입점**.
2-튜플은 **방향 통신**.

## 🚫 흔한 오해

```python
# ❌ 이건 양방향 아님. A → B만 허용
[A, B]

# ✅ 양방향 원하면 둘 다 명시
[A, B],
[B, A],
```

## 🎯 패턴: 위계형 조직

```
    CEO
   / | \
  A  B  C
  |  |  |
  …  …  …
```

```python
Agency([
    CEO(),
    [CEO(), A], [CEO(), B], [CEO(), C],
    [A, A_subordinate], [B, B_subordinate], ...,
])
```

## 🎯 패턴: 평등 + 조정자

```
        Coordinator
       /     |     \
  A ──→     ←── B
       \     |     /
         C
```

```python
Agency([
    Coordinator(),
    [Coordinator(), A], [Coordinator(), B], [Coordinator(), C],
    [A, B], [B, A],
    [B, C], [C, B],
])
```

## 🎯 패턴: 파이프라인

```
User → CEO → Stage1 → Stage2 → Stage3
```

```python
Agency([
    CEO(),
    [CEO(), Stage1()],
    [Stage1(), Stage2()],
    [Stage2(), Stage3()],
])
```

## 🤝 위임 메커니즘

CEO가 dev 호출하면 내부적으로:
1. CEO가 SendMessage 도구로 dev에 메시지 전달
2. 별도 thread에서 dev 실행
3. dev의 응답이 CEO로 반환
4. CEO가 사용자에게 종합 답변

> thread는 OpenAI Assistants API의 thread 개념. 영속 가능.

## ✅ 체크포인트
- [ ] 잘못된 방향 호출 시 에러 발생 확인
- [ ] CEO가 여러 직원에 fan-out 위임
- [ ] thread 영속 (다음 실행 시 컨텍스트 유지)

## 🔗 다음 → [03-tools-pydantic.md](03-tools-pydantic.md)
