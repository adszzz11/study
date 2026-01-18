---
date: 2025-01-18
tags:
  - tech
  - concept
  - network
  - protocol
status: learning
type: tech-concept
---

# TCP (Transmission Control Protocol)

## 1. What - 개념 정의

> **한 줄 정의**: 신뢰성 있는 데이터 전송을 보장하는 연결 지향적 전송 계층 프로토콜

### 핵심 개념

- **연결 지향 (Connection-oriented)**: 데이터 전송 전 3-way handshake로 연결 수립
- **신뢰성 (Reliability)**: 데이터 전달 보증, 순서 보장, 오류 검출
- **흐름 제어 (Flow Control)**: 수신자 버퍼 오버플로우 방지
- **혼잡 제어 (Congestion Control)**: 네트워크 혼잡 방지

### 주요 용어

| 용어 | 설명 |
|------|------|
| **Segment** | TCP 데이터 단위 |
| **Sequence Number** | 전송 데이터 순서 번호 |
| **ACK (Acknowledgment)** | 수신 확인 응답 |
| **Window Size** | 한 번에 전송 가능한 데이터 크기 |
| **MSS (Maximum Segment Size)** | 최대 세그먼트 크기 |
| **RTT (Round Trip Time)** | 패킷 왕복 시간 |

### 인터넷 프로토콜 스택 4계층

```
┌─────────────────────────────┐
│  Application Layer          │  HTTP, FTP, SMTP
├─────────────────────────────┤
│  Transport Layer            │  TCP, UDP  ← 여기!
├─────────────────────────────┤
│  Internet Layer             │  IP
├─────────────────────────────┤
│  Network Interface Layer    │  Ethernet, WiFi
└─────────────────────────────┘
```

---

## 2. Why - 등장 배경 & 필요성

### 해결하려는 문제

- IP만으로는 **데이터 손실**, **순서 뒤바뀜**, **중복 전송** 문제 해결 불가
- 비연결형 프로토콜의 신뢰성 부재
- 네트워크 혼잡 시 데이터 유실

### 기존 방식의 한계

| 문제 | IP만 사용 시 | TCP 사용 시 |
|------|-------------|------------|
| 패킷 손실 | 감지 불가 | 재전송으로 복구 |
| 순서 보장 | 보장 안 됨 | Sequence Number로 정렬 |
| 흐름 제어 | 없음 | Sliding Window |
| 혼잡 제어 | 없음 | Slow Start, Congestion Avoidance |

---

## 3. How - 동작 원리

### 3-Way Handshake (연결 수립)

```
Client                           Server
   │                               │
   │ ───── 1. SYN (seq=x) ──────▶ │
   │       "연결 요청"              │
   │                               │
   │ ◀── 2. SYN+ACK (seq=y,       │
   │         ack=x+1) ──────────── │
   │       "요청 수락 + 내 요청"    │
   │                               │
   │ ───── 3. ACK (ack=y+1) ────▶ │
   │       "확인"                  │
   │                               │
   │ ══════ 연결 수립 완료 ══════ │
```

1. **SYN**: 클라이언트 → 서버 연결 요청
2. **SYN+ACK**: 서버 → 클라이언트 요청 수락 + 서버의 연결 요청
3. **ACK**: 클라이언트 → 서버 확인 응답

> 💡 **왜 3-way?**: 양방향 연결이므로 SYN 2개 + ACK 2개 필요. 서버의 SYN과 클라이언트 ACK가 하나로 합쳐져 3개로 최적화

### 4-Way Handshake (연결 종료)

```
Client                           Server
   │                               │
   │ ───── 1. FIN ───────────────▶│
   │                               │
   │ ◀──── 2. ACK ─────────────── │
   │                               │
   │ ◀──── 3. FIN ─────────────── │
   │                               │
   │ ───── 4. ACK ───────────────▶│
   │                               │
```

### 흐름 제어 (Flow Control)

- **목적**: 수신자 버퍼 오버플로우 방지
- **방식**: Sliding Window
- **rcv_wnd (Receiver Window)**: 수신자가 ACK에 포함시켜 전송 가능량 알림

```
┌───┬───┬───┬───┬───┬───┬───┬───┐
│ 1 │ 2 │ 3 │ 4 │ 5 │ 6 │ 7 │ 8 │
└───┴───┴───┴───┴───┴───┴───┴───┘
 ▲───────────▲
 │  Window   │
 └───────────┘
 전송 가능 범위
```

### 혼잡 제어 (Congestion Control)

- **목적**: 네트워크 혼잡 방지 (라우터 버퍼 오버플로우 방지)
- **cwnd (Congestion Window)**: 송신자가 관리하는 전송 제한

| 알고리즘 | 동작 |
|---------|------|
| **Slow Start** | cwnd를 1 MSS부터 시작, ACK마다 지수적 증가 |
| **Congestion Avoidance** | 임계점(ssthresh) 도달 후 선형 증가 |
| **Fast Retransmit** | 3개 중복 ACK 시 즉시 재전송 |
| **Fast Recovery** | 재전송 후 Slow Start 대신 Congestion Avoidance로 |

```
cwnd
 │            ╱
 │         ╱    Congestion Avoidance
 │      ╱       (선형 증가)
 │    ╱
 │  ╱  Slow Start
 │╱    (지수 증가)
 └──────────────────▶ time
       ssthresh
```

---

## 4. 실무 적용

### 사용 사례

- **HTTP/HTTPS**: 웹 통신 (신뢰성 필요)
- **FTP**: 파일 전송
- **SMTP/IMAP**: 이메일
- **SSH**: 원격 접속
- **Database 연결**: MySQL, PostgreSQL 등

### 코드 예시 (Java Socket)

```java
// TCP Server
ServerSocket serverSocket = new ServerSocket(8080);
Socket clientSocket = serverSocket.accept();  // 3-way handshake

BufferedReader in = new BufferedReader(
    new InputStreamReader(clientSocket.getInputStream()));
PrintWriter out = new PrintWriter(clientSocket.getOutputStream(), true);

String message = in.readLine();  // 데이터 수신
out.println("Response");         // 데이터 송신

clientSocket.close();  // 4-way handshake
```

```java
// TCP Client
Socket socket = new Socket("localhost", 8080);  // 3-way handshake

PrintWriter out = new PrintWriter(socket.getOutputStream(), true);
BufferedReader in = new BufferedReader(
    new InputStreamReader(socket.getInputStream()));

out.println("Request");           // 데이터 송신
String response = in.readLine();  // 데이터 수신

socket.close();  // 4-way handshake
```

### Best Practices

- 적절한 **SO_TIMEOUT** 설정으로 무한 대기 방지
- **Keep-Alive** 활용으로 연결 재사용 (HTTP/1.1)
- 대용량 전송 시 **버퍼 크기** 조정

### Anti-patterns (주의사항)

- ❌ 실시간 스트리밍에 TCP 사용 (지연 발생) → UDP 권장
- ❌ 매 요청마다 새 연결 → Connection Pool 사용
- ❌ 작은 패킷 다수 전송 → Nagle 알고리즘 고려

---

## 5. 비교 분석

### vs UDP

| 비교 항목 | TCP | UDP |
|-----------|-----|-----|
| 연결 방식 | 연결 지향 | 비연결 |
| 신뢰성 | 보장 (재전송, 순서) | 미보장 |
| 속도 | 느림 (오버헤드) | 빠름 |
| 헤더 크기 | 20~60 bytes | 8 bytes |
| 흐름/혼잡 제어 | 있음 | 없음 |
| 적합한 용도 | 웹, 파일 전송, 이메일 | 스트리밍, 게임, DNS |

### 선택 기준

- **TCP 선택**: 데이터 정확성이 중요할 때 (금융, 파일 전송)
- **UDP 선택**: 속도가 중요하고 일부 손실 허용 가능할 때 (실시간 영상, 게임)

---

## 6. 학습 체크리스트

### 이해도 점검

- [x] 한 문장으로 설명할 수 있다
- [x] 3-way handshake를 그림으로 그릴 수 있다
- [x] TCP vs UDP 차이를 설명할 수 있다
- [x] 흐름 제어와 혼잡 제어 차이를 설명할 수 있다
- [ ] 실제 패킷을 Wireshark로 분석할 수 있다

### 추가 학습

- [ ] TCP Fast Open 학습
- [ ] QUIC 프로토콜 비교 (HTTP/3)
- [ ] Wireshark로 TCP 패킷 분석 실습

---

## 7. References

- [Wikipedia - TCP](https://en.wikipedia.org/wiki/Transmission_Control_Protocol)
- [GeeksforGeeks - TCP](https://www.geeksforgeeks.org/computer-networks/what-is-transmission-control-protocol-tcp/)
- [RFC 5681 - TCP Congestion Control](https://datatracker.ietf.org/doc/html/rfc5681)
- 관련 노트: [[UDP]], [[IP]], [[HTTP]]
