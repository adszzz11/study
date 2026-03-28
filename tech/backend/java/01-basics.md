---
date: 2025-01-18
tags:
  - tech
  - basics
  - java
  - oop
parent: "[[README]]"
---

# Java - 기초

> ⬅️ [[README|목차로 돌아가기]] | ➡️ [[02-core|다음: JVM 심화]]

---

## 1. What - 개념 정의

> **한 줄 정의**: 객체지향, 플랫폼 독립적, 강타입 언어로 엔터프라이즈 애플리케이션의 표준

### Java 철학

```
"Write Once, Run Anywhere" (WORA)
```

- **플랫폼 독립성**: JVM만 있으면 어디서든 실행
- **객체지향**: 모든 것이 객체 (primitive 제외)
- **강타입**: 컴파일 타임에 타입 체크
- **가비지 컬렉션**: 자동 메모리 관리

### 핵심 용어

| 용어 | 설명 |
|------|------|
| **JDK** | Java Development Kit - 개발 도구 포함 |
| **JRE** | Java Runtime Environment - 실행 환경 |
| **JVM** | Java Virtual Machine - 바이트코드 실행 |
| **Bytecode** | .class 파일, JVM이 해석하는 중간 코드 |
| **GC** | Garbage Collector - 자동 메모리 해제 |

---

## 2. Why - 등장 배경

### 해결하려는 문제

- **플랫폼 종속성**: C/C++는 OS마다 재컴파일 필요
- **메모리 관리**: 수동 메모리 관리로 인한 버그
- **보안**: 네트워크 환경에서의 안전한 실행

### 역사

```
1991: Oak 프로젝트 시작 (James Gosling)
1995: Java 1.0 출시
2004: Java 5 (Generics, Annotations)
2014: Java 8 (Lambda, Stream API)
2017: 6개월 릴리즈 주기 시작
2021: Java 17 LTS
2023: Java 21 LTS (Virtual Threads)
```

### LTS 버전 선택 가이드

| 버전 | 지원 종료 | 핵심 기능 | 권장 |
|------|----------|----------|------|
| Java 8 | 2030 | Lambda, Stream | 레거시 유지 |
| Java 11 | 2026 | var, HTTP Client | 안정적 운영 |
| Java 17 | 2029 | Sealed Class, Pattern Matching | **권장** |
| Java 21 | 2031 | Virtual Threads, Pattern Matching | 신규 프로젝트 |

---

## 3. 핵심 문법

### 데이터 타입

```java
// Primitive Types
byte b = 127;           // 1 byte
short s = 32767;        // 2 bytes
int i = 2147483647;     // 4 bytes
long l = 9223372036854775807L;  // 8 bytes

float f = 3.14f;        // 4 bytes
double d = 3.14159;     // 8 bytes

char c = 'A';           // 2 bytes (Unicode)
boolean bool = true;    // 1 bit

// Reference Types
String str = "Hello";
Integer num = 100;      // Wrapper class
List<String> list = new ArrayList<>();
```

### 객체지향 (OOP)

```java
// 캡슐화 (Encapsulation)
public class User {
    private String name;  // 외부 접근 제한

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }
}

// 상속 (Inheritance)
public class Admin extends User {
    private String role;
}

// 다형성 (Polymorphism)
User user = new Admin();  // 업캐스팅

// 추상화 (Abstraction)
public interface Repository<T> {
    T findById(Long id);
    void save(T entity);
}
```

### Java 8+ 핵심 기능

```java
// Lambda Expression
List<String> names = Arrays.asList("Alice", "Bob", "Charlie");
names.forEach(name -> System.out.println(name));

// Stream API
List<String> filtered = names.stream()
    .filter(name -> name.startsWith("A"))
    .map(String::toUpperCase)
    .collect(Collectors.toList());

// Optional
Optional<User> user = Optional.ofNullable(findUser(id));
String name = user.map(User::getName).orElse("Unknown");

// Method Reference
names.forEach(System.out::println);
```

### Java 17+ 기능

```java
// Record (불변 데이터 클래스)
public record Point(int x, int y) {}

// Sealed Class
public sealed class Shape
    permits Circle, Rectangle, Square {}

// Pattern Matching
if (obj instanceof String s) {
    System.out.println(s.length());
}

// Switch Expression
String result = switch (day) {
    case MONDAY, FRIDAY -> "Work";
    case SATURDAY, SUNDAY -> "Rest";
    default -> "Unknown";
};

// Text Blocks
String json = """
    {
        "name": "Java",
        "version": 21
    }
    """;
```

---

## 4. 장단점

### 장점

- ✅ **플랫폼 독립성**: JVM만 있으면 어디서든 실행
- ✅ **강력한 생태계**: Spring, Maven, 수많은 라이브러리
- ✅ **엔터프라이즈 검증**: 대규모 시스템에서 검증됨
- ✅ **하위 호환성**: 오래된 코드도 새 JVM에서 실행

### 단점

- ❌ **Verbose**: 보일러플레이트 코드가 많음
- ❌ **시작 시간**: 콜드 스타트가 느림
- ❌ **메모리 사용량**: JVM 오버헤드
- ❌ **Null 처리**: NullPointerException 빈발

---

## 5. vs 다른 언어

| 항목 | Java | Kotlin | Go |
|------|------|--------|-----|
| 패러다임 | OOP | OOP + FP | 절차적 |
| Null 안전성 | Optional | 내장 | 내장 |
| 문법 간결성 | 중간 | 높음 | 높음 |
| 시작 시간 | 느림 | 느림 | 빠름 |
| GC | JVM GC | JVM GC | 자체 GC |
| 주 사용처 | 엔터프라이즈 | Android, Server | 인프라, CLI |

---

## 다음 단계

> [!tip] 다음으로
> 기초 개념을 이해했다면 [[02-core|JVM 아키텍처]]에서 메모리 구조와 GC를 학습하세요.

---

## References

- [Oracle Java Documentation](https://docs.oracle.com/en/java/)
- [Baeldung - Java Tutorials](https://www.baeldung.com/)
- [Java Version History](https://en.wikipedia.org/wiki/Java_version_history)
