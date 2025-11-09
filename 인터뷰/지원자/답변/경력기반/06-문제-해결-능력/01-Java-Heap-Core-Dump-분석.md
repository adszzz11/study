# Java Heap 충돌로 인한 Tomcat Fatal down 문제를 core dump 분석으로 해결했다고 했는데, 구체적인 분석 과정은?

## 답변

[여기에 답변 작성]

## 핵심 키워드

- Java Heap
- Core Dump
- OutOfMemoryError
- Heap Dump 분석
- Memory Leak

## 문제 상황

### 증상
-

### 발생 빈도
-

## Core Dump 수집 및 분석

### 1. Dump 파일 생성
```bash
# JVM 옵션
-XX:+HeapDumpOnOutOfMemoryError
-XX:HeapDumpPath=/path/to/dump
```

### 2. 분석 도구 사용
- MAT (Memory Analyzer Tool)
- jhat
- VisualVM

### 3. 분석 과정
```
1. Heap 사용량 확인
2. Dominator Tree 분석
3. GC Root 추적
4. Object Retention 확인
```

## 근본 원인

-

## 해결 방법

-

## 재발 방지 대책

-

## 참고 자료

-
