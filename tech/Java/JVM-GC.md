---
date: 2025-01-18
tags:
  - tech
  - concept
  - java
  - jvm
  - performance
status: learning
type: tech-concept
---

# JVM Garbage Collection

## 1. What - 개념 정의

> **한 줄 정의**: JVM이 더 이상 사용되지 않는 객체의 메모리를 자동으로 해제하는 메모리 관리 기법

### 핵심 개념

- **Heap**: 객체가 저장되는 메모리 영역
- **GC Root**: 참조 추적의 시작점 (Stack 변수, Static 변수 등)
- **Reachability**: GC Root에서 도달 가능 여부로 생존 판단
- **Stop-the-World (STW)**: GC 실행 중 애플리케이션 일시 정지

### 주요 용어

| 용어 | 설명 |
|------|------|
| **Young Generation** | 새로 생성된 객체 영역 (Eden + Survivor) |
| **Old Generation** | 오래 살아남은 객체 영역 |
| **Minor GC** | Young 영역만 수집 (빠름) |
| **Major/Full GC** | 전체 Heap 수집 (느림) |
| **Pause Time** | STW로 인한 애플리케이션 정지 시간 |
| **Throughput** | GC 외 애플리케이션 실행 시간 비율 |

### Heap 메모리 구조

```
┌────────────────────────────────────────────────────┐
│                      Heap                          │
├──────────────────────┬─────────────────────────────┤
│   Young Generation   │      Old Generation         │
├────────┬─────────────┤                             │
│  Eden  │  Survivor   │                             │
│        │  S0  │  S1  │                             │
└────────┴──────┴──────┴─────────────────────────────┘
         │             │
    Minor GC 대상       Major GC 대상
```

---

## 2. Why - 등장 배경 & 필요성

### 해결하려는 문제

- **메모리 누수 방지**: 개발자의 수동 메모리 해제 실수 제거
- **Dangling Pointer 방지**: 해제된 메모리 참조 문제 해결
- **개발 생산성 향상**: 메모리 관리 부담 감소

### 기존 방식의 한계

| 문제 | C/C++ (수동) | Java (GC) |
|------|-------------|-----------|
| 메모리 누수 | 흔함 | 거의 없음 |
| Dangling Pointer | 발생 | 불가능 |
| Double Free | 발생 | 불가능 |
| 개발 복잡도 | 높음 | 낮음 |

---

## 3. How - 동작 원리

### GC 기본 동작 흐름

```
1. 객체 생성 → Eden 영역에 할당
        ↓
2. Eden 가득 참 → Minor GC 실행
        ↓
3. 살아남은 객체 → Survivor로 이동 (age +1)
        ↓
4. age 임계값 초과 → Old Generation으로 승격
        ↓
5. Old 가득 참 → Major GC 실행
```

### GC 종류별 특징

| GC | 특징 | Pause Time | 적합한 상황 |
|----|------|------------|------------|
| **Serial GC** | 단일 스레드, 가장 단순 | 길다 | 작은 힙, 클라이언트 |
| **Parallel GC** | 멀티 스레드 | 중간 | Throughput 중시 |
| **G1GC** | Region 기반, 예측 가능 | 100-200ms | **범용 (기본값 since JDK 9)** |
| **ZGC** | 초저지연, 동시 수행 | **< 10ms** | 대용량 힙, 저지연 필수 |
| **Shenandoah** | 동시 압축 | < 10ms | 저지연 필요 |

### G1GC vs ZGC 상세 비교 (Java 21 기준)

```
              G1GC                          ZGC
         ┌──────────────┐            ┌──────────────┐
   Pause │  50~150ms    │            │   1~3ms      │
         │  (최대 500ms)│            │  (최대 10ms) │
         └──────────────┘            └──────────────┘

   Heap  │  < 16GB 적합  │            │  > 32GB 적합 │
         │              │            │  (TB 가능)   │
         └──────────────┘            └──────────────┘
```

| 항목 | G1GC | ZGC (Generational, JDK 21+) |
|------|------|------------------------------|
| 기본값 | JDK 9~ | JDK 23~ |
| Pause Time | 50-150ms (최대 500ms+) | 1-3ms (최대 10ms) |
| Throughput | 높음 | G1 대비 -10% → 동등 수준 |
| 힙 크기 | < 16GB 권장 | 32GB+ ~ TB 가능 |
| 메모리 오버헤드 | 낮음 | 높음 → 75% 감소 (Gen ZGC) |
| 튜닝 필요성 | 중간 | 거의 없음 |

> 💡 **Netflix 사례**: G1에서 Generational ZGC로 전환 후, 동일 CPU 사용률에서 P99 지연시간 개선

### JVM 메모리 영역 전체

```
┌─────────────────────────────────────────┐
│              JVM Memory                 │
├─────────────────────────────────────────┤
│  Method Area    │ 클래스 정보, static   │
├─────────────────┼───────────────────────┤
│  Heap Area      │ new Object() 저장     │ ← GC 대상
├─────────────────┼───────────────────────┤
│  Stack Area     │ 스레드별 지역변수      │
├─────────────────┼───────────────────────┤
│  PC Register    │ 실행 명령 위치        │
├─────────────────┼───────────────────────┤
│  Native Stack   │ Native 메소드 정보    │
└─────────────────┴───────────────────────┘
```

---

## 4. 실무 적용

### GC 선택 가이드

```
힙 크기가 16GB 이하?
├── Yes → 지연 시간 중요?
│         ├── Yes → G1GC
│         └── No  → Parallel GC
└── No  → ZGC (Generational)
```

### JVM 옵션 예시

```bash
# G1GC (기본값, 범용)
java -XX:+UseG1GC -Xmx4g -jar app.jar

# G1GC 튜닝
java -XX:+UseG1GC \
     -XX:MaxGCPauseMillis=200 \
     -XX:G1HeapRegionSize=16m \
     -Xmx8g -jar app.jar

# ZGC (Java 21+, 저지연)
java -XX:+UseZGC -XX:+ZGenerational -Xmx32g -jar app.jar

# Parallel GC (Throughput 중시)
java -XX:+UseParallelGC -Xmx4g -jar app.jar
```

### GC 로그 분석

```bash
# GC 로그 활성화
java -Xlog:gc*:file=gc.log:time -jar app.jar

# GC 로그 예시
[0.015s] GC(0) Pause Young (Normal) 24M->8M(256M) 5.123ms
#        ^^^^  ^^^^^^^^^^^^^        ^^^^^^^^^^^^  ^^^^^^^
#        GC번호  GC 종류             힙 변화       소요시간
```

### Best Practices

- **힙 크기 설정**: 전체 메모리의 50-70%
- **모니터링**: GC 로그 + APM (Datadog, Prometheus)
- **기본값 시작**: 튜닝 전 기본 설정으로 측정 먼저

### Anti-patterns (주의사항)

- ❌ `System.gc()` 직접 호출 → JVM에 위임
- ❌ 과도한 객체 생성 → Object Pool 고려
- ❌ 큰 객체 반복 할당 → 재사용 또는 스트리밍
- ❌ Finalizer 사용 → try-with-resources 사용

---

## 5. 비교 분석

### GC 선택 매트릭스

| 시나리오 | 권장 GC | 이유 |
|---------|--------|------|
| 웹 서버 (일반) | G1GC | 균형 잡힌 성능 |
| 실시간 거래 시스템 | ZGC | 초저지연 필수 |
| 배치 처리 | Parallel GC | Throughput 최대화 |
| 컨테이너 (< 2GB) | Serial GC | 오버헤드 최소화 |
| 대용량 캐시 서버 | ZGC | 대용량 힙 + 저지연 |

### vs 다른 언어 메모리 관리

| 항목 | Java (GC) | Rust (Ownership) | Go (GC) |
|------|-----------|------------------|---------|
| 자동화 | O | △ (컴파일타임) | O |
| Pause | 있음 | 없음 | 있음 |
| 학습 곡선 | 낮음 | 높음 | 낮음 |

---

## 6. 학습 체크리스트

### 이해도 점검

- [x] GC가 왜 필요한지 설명할 수 있다
- [x] Young/Old Generation 차이를 설명할 수 있다
- [x] G1GC vs ZGC 선택 기준을 설명할 수 있다
- [x] GC 로그를 읽을 수 있다
- [ ] 실제 GC 튜닝 경험

### 추가 학습

- [ ] VisualVM으로 GC 모니터링 실습
- [ ] JFR (Java Flight Recorder) 분석
- [ ] Generational ZGC 심화 학습

---

## 7. References

- [Netflix: G1GC to ZGC Journey](https://netflixtechblog.com/bending-pause-times-to-your-will-with-generational-zgc-256629c9386b)
- [Halodoc: G1GC to ZGC Transition](https://blogs.halodoc.io/enhancing-java-application-performance-transitioning-from-g1gc-to-zgc-at-halodoc/)
- [Red Hat: How to Choose GC](https://developers.redhat.com/articles/2021/11/02/how-choose-best-java-garbage-collector)
- [JDK 21 GC Improvements](https://kstefanj.github.io/2023/12/13/jdk-21-the-gcs-keep-getting-better.html)
- 관련 노트: [[JVM]], [[Java-Memory-Model]]
