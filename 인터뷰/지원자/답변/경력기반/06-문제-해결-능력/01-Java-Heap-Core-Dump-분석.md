# Java Heap 충돌로 인한 Tomcat Fatal down 문제를 core dump 분석으로 해결했다고 했는데, 구체적인 분석 과정은?

## 답변

운영 중인 Tomcat 서버가 OutOfMemoryError로 인해 불시에 종료되는 문제가 발생했습니다. Heap Dump 분석을 통해 특정 객체가 메모리를 과도하게 점유하고 있음을 발견했고, 근본 원인을 파악하여 해결했습니다.

먼저 JVM 옵션에 `-XX:+HeapDumpOnOutOfMemoryError`를 설정하여 OOM 발생 시 자동으로 heap dump 파일을 생성하도록 했습니다. 생성된 dump 파일(약 2GB)을 Eclipse MAT(Memory Analyzer Tool)로 분석한 결과, Dominator Tree에서 특정 Cache 객체가 전체 heap의 약 70%를 점유하고 있었습니다.

Leak Suspects Report를 확인해보니, 캐시 만료 로직이 제대로 동작하지 않아 오래된 데이터가 계속 메모리에 축적되고 있었습니다. GC Root로부터 참조 체인을 추적한 결과, static HashMap에 저장된 캐시 데이터가 어떤 경우에도 제거되지 않는 구조였습니다.

해결책으로는 1) 캐시 크기 제한 설정(LRU 방식), 2) TTL 기반 만료 정책 추가, 3) WeakHashMap 도입 검토를 진행했고, 최종적으로 Guava Cache를 도입하여 maximumSize와 expireAfterWrite를 설정했습니다. 결과적으로 heap 사용률이 평균 30% 수준으로 안정화되었고, 더 이상 OOM이 발생하지 않았습니다.

## 핵심 키워드

- Java Heap
- Core Dump
- OutOfMemoryError
- Heap Dump 분석
- Memory Leak

## 문제 상황

### 증상
- Tomcat 서버가 주기적으로 OutOfMemoryError와 함께 비정상 종료
- 에러 발생 전 GC가 빈번하게 발생하며 응답 지연 급증
- 서버 재시작 후 일시적으로 정상 동작하다가 시간이 지나면서 다시 재발
- 힙 메모리 사용률이 지속적으로 증가하는 패턴 관찰

### 발생 빈도
- 초기: 주 1-2회 정도 발생
- 점차 빈도 증가하여 일 1회 수준으로 악화
- 피크 타임(오후 2-4시) 이후 발생 확률 높음
- 서버 재시작 후 약 6-8시간 후 메모리 임계치 도달

## Core Dump 수집 및 분석

### 1. Dump 파일 생성
```bash
# JVM 옵션 설정
-XX:+HeapDumpOnOutOfMemoryError
-XX:HeapDumpPath=/var/log/tomcat/heapdump/
-XX:+PrintGCDetails
-XX:+PrintGCDateStamps
-Xloggc:/var/log/tomcat/gc.log

# 또는 수동으로 heap dump 생성 (서버 운영 중)
jmap -dump:live,format=b,file=/tmp/heap_dump.hprof [PID]
```

### 2. 분석 도구 사용
- **MAT (Memory Analyzer Tool)**: 주 분석 도구로 사용
  - Leak Suspects Report 자동 생성
  - Dominator Tree를 통한 메모리 점유율 분석
  - Histogram으로 객체별 인스턴스 수/크기 확인
- **jhat**: 간단한 웹 기반 분석
  - `jhat -J-Xmx4g heap_dump.hprof`
  - 브라우저에서 http://localhost:7000 접속
- **VisualVM**: 실시간 모니터링 및 프로파일링
  - 힙 사용 추이 그래프 확인
  - GC 활동 모니터링

### 3. 분석 과정
```
1. Heap 사용량 확인
   - Overview: Total heap size 2GB, Used heap 1.8GB (90%)
   - Retained heap 분석으로 실제 메모리 점유 파악

2. Dominator Tree 분석
   - 가장 큰 메모리를 점유한 객체 식별
   - java.util.HashMap 인스턴스가 1.4GB (70%) 점유
   - 해당 HashMap이 Cache 용도로 사용 중인 것 확인

3. GC Root 추적
   - Path To GC Roots 기능으로 참조 체인 추적
   - Static 변수에서 시작된 강한 참조 발견
   - CacheManager 클래스의 static HashMap이 근본 원인

4. Object Retention 확인
   - Histogram에서 특정 DTO 객체가 150만 개 이상 존재
   - 객체 생성 시점 확인 결과, 일부는 5일 이상 유지
   - 캐시 만료 로직이 전혀 동작하지 않음을 확인
```

## 근본 원인

- **캐시 만료 로직 부재**: static HashMap에 데이터를 put만 하고 remove 로직이 없음
- **무제한 캐시 증가**: 캐시 크기 제한이 없어 요청이 있을 때마다 계속 누적
- **강한 참조 유지**: GC가 수집할 수 없는 static 변수에서 직접 참조
- **메모리 설계 오류**: 전체 데이터를 메모리에 올리려는 잘못된 캐싱 전략
- **모니터링 미흡**: 힙 메모리 증가 추이를 사전에 감지하지 못함

## 해결 방법

### 1. 즉시 조치 (임시 해결)
```bash
# Heap 크기 증설
-Xms2048m -Xmx4096m
# 하지만 근본 해결책은 아님 - 시간만 벌어주는 조치
```

### 2. 캐시 라이브러리 도입 (근본 해결)
```java
// 기존 코드
public class CacheManager {
    private static Map<String, Object> cache = new HashMap<>();

    public static void put(String key, Object value) {
        cache.put(key, value);  // 제거 로직 없음
    }
}

// 개선된 코드 - Guava Cache 사용
import com.google.common.cache.Cache;
import com.google.common.cache.CacheBuilder;
import java.util.concurrent.TimeUnit;

public class CacheManager {
    private static final Cache<String, Object> cache = CacheBuilder.newBuilder()
        .maximumSize(10_000)  // 최대 10,000개 항목
        .expireAfterWrite(30, TimeUnit.MINUTES)  // 30분 후 자동 만료
        .expireAfterAccess(10, TimeUnit.MINUTES)  // 10분간 미사용 시 제거
        .recordStats()  // 통계 수집
        .build();

    public static void put(String key, Object value) {
        cache.put(key, value);
    }

    public static Object get(String key) {
        return cache.getIfPresent(key);
    }
}
```

### 3. 모니터링 강화
```java
// 캐시 통계 주기적 로깅
@Scheduled(fixedRate = 60000)  // 1분마다
public void logCacheStats() {
    CacheStats stats = cache.stats();
    log.info("Cache stats - Size: {}, HitRate: {}, EvictionCount: {}",
        cache.size(), stats.hitRate(), stats.evictionCount());
}
```

## 재발 방지 대책

### 1. 모니터링 시스템 구축
- Prometheus + Grafana로 JVM 메트릭 실시간 모니터링
- Heap 사용률 80% 초과 시 알림 설정
- GC 시간이 전체 실행 시간의 10% 초과 시 경고

### 2. 정기 Heap Dump 분석
- 월 1회 운영 서버 heap dump 수집 및 분석
- 메모리 누수 징후 조기 발견

### 3. 코드 리뷰 강화
- static 변수 사용 시 반드시 리뷰 필수
- 캐시 구현 시 TTL/크기 제한 필수 체크리스트 추가

### 4. 로드 테스트
- JMeter로 장시간(8시간+) 부하 테스트 수행
- 메모리 프로파일링 결과를 배포 전 필수 검증 항목으로 추가

### 5. JVM 튜닝
```bash
# G1GC 사용으로 변경
-XX:+UseG1GC
-XX:MaxGCPauseMillis=200
-XX:G1HeapRegionSize=16m
```

## 참고 자료

- Eclipse MAT Documentation: https://www.eclipse.org/mat/
- Effective Java 3rd Edition - Item 7: Eliminate obsolete object references
- Java Performance: The Definitive Guide (O'Reilly)
- Guava Cache Guide: https://github.com/google/guava/wiki/CachesExplained
- Oracle Java SE Troubleshooting Guide: https://docs.oracle.com/javase/8/docs/technotes/guides/troubleshoot/
