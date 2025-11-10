# PA카드와 일반 카드 결제의 차이점은? BC카드 전문 통신에서 가장 어려웠던 점은?

## 답변

**PA카드(Private Label Card)와 일반 카드의 차이**

PA카드는 특정 브랜드나 기업이 자체 브랜드로 발행하지만, 실제 결제망은 기존 카드사(BC카드, 신한카드 등)의 인프라를 활용하는 제휴카드입니다. 저희가 구축한 선불전자지급수단 시스템에서는 자사 브랜드 PA카드를 BC카드 결제망을 통해 처리했습니다.

**주요 차이점:**
- **발급 주체**: PA카드는 자사가 발급하지만, 결제 처리는 BC카드 인프라 활용
- **승인 프로세스**: PA카드는 자사 시스템에서 1차 잔액 검증 후 BC카드 망으로 승인 요청
- **수수료**: 일반 카드 대비 낮은 수수료율 (자사 브랜드이므로 협상 가능)
- **사용처 제한**: PA카드는 특정 가맹점에서만 사용 가능하도록 제한 가능

**BC카드 전문 통신에서 가장 어려웠던 점**

1. **고정 길이 전문 파싱의 복잡성**
   - BC카드 전문은 고정 길이 포맷으로, 1바이트라도 틀리면 전체 파싱 실패
   - 한글 인코딩(EUC-KR) 처리 시 바이트 길이 계산 오류 빈번

2. **Socket 통신 안정성**
   - Keep-alive 관리, Connection Pool 최적화
   - 네트워크 끊김 시 재연결 로직 구현

3. **응답 타임아웃 처리**
   - BC카드 응답 지연 시 사용자 경험 저하
   - 타임아웃 후 거래 상태 확인(승인 조회) 필요

4. **에러 코드 매핑**
   - BC카드 응답 코드 수백 가지를 자사 에러 메시지로 변환
   - 사용자 친화적인 에러 메시지 제공

## 핵심 키워드

- PA카드 (Private Label Card)
- BC카드 전문
- 카드 결제 프로토콜
- 전문 통신
- Socket 통신

## PA카드 vs 일반 카드

| 구분 | PA카드 (자사 발행) | 일반 신용카드 |
|------|-------------------|--------------|
| 발급사 | 자사 (BC카드 제휴) | 카드사 (BC, 신한, 삼성 등) |
| 사용처 | 제한적 (지정 가맹점만) | 전국 모든 가맹점 |
| 승인 프로세스 | 자사 잔액 검증 → BC카드 승인 | 카드사 직접 승인 |
| 수수료 | 낮음 (자사 협상) | 일반 가맹점 수수료 (2~3%) |
| 잔액 관리 | 자사 원장 시스템 관리 | 카드사 시스템 관리 |
| 후불/선불 | 선불 (충전 후 사용) | 후불 (신용 한도) |
| 혜택 | 자사 맞춤 혜택 | 카드사 공통 혜택 |

**PA카드 승인 플로우:**
```
사용자 결제 요청
  ↓
자사 시스템 잔액 검증 (충분한지 확인)
  ↓
BC카드 전문 통신 (승인 요청)
  ↓
BC카드 VAN망 전송
  ↓
가맹점 확인 및 승인
  ↓
BC카드 응답 수신
  ↓
자사 원장 잔액 차감
  ↓
사용자에게 결과 응답
```

## BC카드 전문 통신 구조

### 전문 포맷

BC카드 전문은 **고정 길이 방식**으로, 각 필드가 정해진 바이트 수를 차지합니다.

**전문 구조 예시 (승인 요청):**
```
[헤더부] (고정 50바이트)
- 전문길이: 4바이트 (예: "0512")
- 전문구분: 4바이트 (예: "0200" = 승인요청)
- 가맹점번호: 10바이트
- 단말기번호: 10바이트
- 전송일시: 14바이트 (YYYYMMDDhhmmss)
- 기타 헤더 정보...

[데이터부] (가변, 최대 462바이트)
- 카드번호: 20바이트 (암호화)
- 유효기간: 4바이트 (YYMM)
- 거래금액: 12바이트 (우측 정렬, 왼쪽 0 패딩)
- 할부개월: 2바이트
- 승인번호: 12바이트
- 가맹점명: 40바이트 (EUC-KR 인코딩)
- 기타 데이터 필드...
```

**실제 전문 예시 (16진수 덤프):**
```
0512 0200 1234567890 T000000001 20241109143022 ...
[거래금액: 000000010000 = 10,000원]
[가맹점명: C4BF C6E4 ... (커피전문점, EUC-KR)]
```

### 통신 방식

**1. Socket 연결 (TCP/IP)**
```java
@Configuration
public class BcCardSocketConfig {

    @Value("${bccard.host}")
    private String bcCardHost;  // BC카드 VAN 서버 IP

    @Value("${bccard.port}")
    private int bcCardPort;     // 포트 (예: 5000)

    @Bean
    public SocketFactory bcCardSocketFactory() {
        // SSL/TLS Socket Factory (보안 통신)
        SSLContext sslContext = SSLContext.getInstance("TLSv1.2");
        sslContext.init(null, trustManagers, new SecureRandom());
        return sslContext.getSocketFactory();
    }

    @Bean
    public GenericObjectPoolConfig socketPoolConfig() {
        GenericObjectPoolConfig config = new GenericObjectPoolConfig();
        config.setMaxTotal(20);                 // 최대 연결 수
        config.setMaxIdle(10);                  // 유휴 연결 수
        config.setMinIdle(5);                   // 최소 연결 유지
        config.setMaxWaitMillis(3000);          // 대기 타임아웃
        config.setTestOnBorrow(true);           // 연결 유효성 검사
        config.setTestWhileIdle(true);
        return config;
    }
}
```

**2. 전문 송수신 서비스**
```java
@Service
public class BcCardMessageService {

    @Autowired
    private SocketConnectionPool socketPool;

    /**
     * BC카드 승인 요청
     */
    public BcCardResponse sendApprovalRequest(PaymentRequest request) {
        Socket socket = null;
        try {
            // 1. Connection Pool에서 Socket 획득
            socket = socketPool.borrowSocket();

            // 2. 전문 생성
            String requestMessage = buildApprovalMessage(request);

            // 3. 전문 전송
            OutputStream out = socket.getOutputStream();
            out.write(requestMessage.getBytes("EUC-KR"));
            out.flush();

            log.info("[BC카드 전송] length={}, data={}",
                requestMessage.length(), maskSensitiveData(requestMessage));

            // 4. 응답 수신 (타임아웃 30초)
            socket.setSoTimeout(30000);
            InputStream in = socket.getInputStream();

            byte[] buffer = new byte[512];
            int bytesRead = in.read(buffer);

            if (bytesRead == -1) {
                throw new BcCardException("응답 수신 실패: EOF");
            }

            String responseMessage = new String(buffer, 0, bytesRead, "EUC-KR");

            log.info("[BC카드 수신] length={}, data={}",
                responseMessage.length(), maskSensitiveData(responseMessage));

            // 5. 응답 파싱
            return parseResponse(responseMessage);

        } catch (SocketTimeoutException e) {
            log.error("[BC카드 타임아웃] 30초 초과", e);
            throw new BcCardTimeoutException("BC카드 응답 타임아웃", e);

        } catch (IOException e) {
            log.error("[BC카드 통신 오류]", e);
            throw new BcCardException("BC카드 통신 실패", e);

        } finally {
            // 6. Socket 반환
            if (socket != null) {
                socketPool.returnSocket(socket);
            }
        }
    }
}
```

## 구현 시 어려웠던 점

### 1. 전문 파싱

**문제: 고정 길이 전문 파싱의 복잡성**

```java
/**
 * BC카드 전문 빌더
 */
public class BcCardMessageBuilder {

    private static final Charset EUC_KR = Charset.forName("EUC-KR");

    /**
     * 승인 요청 전문 생성
     */
    public String buildApprovalMessage(PaymentRequest request) {
        StringBuilder sb = new StringBuilder();

        // 헤더부 (50바이트)
        sb.append(fixedLength("0200", 4));                          // 전문구분
        sb.append(fixedLength(request.getMerchantId(), 10));        // 가맹점번호
        sb.append(fixedLength(request.getTerminalId(), 10));        // 단말기번호
        sb.append(getCurrentDateTime());                            // 전송일시 (14바이트)
        sb.append(fixedLength(generateTraceNo(), 12));              // 추적번호

        // 데이터부
        sb.append(fixedLength(encryptCardNo(request.getCardNo()), 20));     // 카드번호 (암호화)
        sb.append(fixedLength(request.getExpiry(), 4));                     // 유효기간
        sb.append(rightPad(String.valueOf(request.getAmount()), 12, '0'));  // 금액 (우측정렬)
        sb.append(fixedLength(request.getInstallment(), 2));                // 할부

        // 한글 필드 처리 (가맹점명) - 바이트 길이 주의!
        sb.append(fixedLengthKorean(request.getMerchantName(), 40));

        String message = sb.toString();

        // 전문 길이를 맨 앞에 추가 (4바이트)
        int totalLength = message.getBytes(EUC_KR).length;
        return String.format("%04d", totalLength) + message;
    }

    /**
     * 고정 길이 문자열 생성 (ASCII)
     */
    private String fixedLength(String value, int length) {
        if (value == null) {
            value = "";
        }
        if (value.length() > length) {
            return value.substring(0, length);
        }
        return String.format("%-" + length + "s", value);  // 왼쪽 정렬, 공백 패딩
    }

    /**
     * 고정 길이 한글 문자열 생성 (EUC-KR 바이트 기준)
     * 어려웠던 부분: 한글은 1글자당 2바이트이므로 바이트 단위로 계산해야 함
     */
    private String fixedLengthKorean(String value, int byteLength) {
        if (value == null) {
            value = "";
        }

        byte[] bytes = value.getBytes(EUC_KR);

        if (bytes.length >= byteLength) {
            // 바이트 길이가 초과하면 자르기
            return new String(bytes, 0, byteLength, EUC_KR);
        } else {
            // 공백으로 패딩
            byte[] padded = new byte[byteLength];
            System.arraycopy(bytes, 0, padded, 0, bytes.length);
            Arrays.fill(padded, bytes.length, byteLength, (byte) 0x20);  // 공백
            return new String(padded, EUC_KR);
        }
    }

    /**
     * 우측 정렬, 0 패딩 (금액 필드용)
     */
    private String rightPad(String value, int length, char padChar) {
        if (value.length() >= length) {
            return value.substring(0, length);
        }
        return String.format("%" + length + "s", value).replace(' ', padChar);
    }
}
```

**파싱 시 발생한 실제 버그:**
```java
// 잘못된 코드 (한글 길이를 문자 단위로 계산)
String merchantName = "커피전문점";  // 5글자
String padded = String.format("%-40s", merchantName);  // 40글자로 패딩
byte[] bytes = padded.getBytes("EUC-KR");
// 결과: 45바이트 (한글 5글자*2 + 공백 35 = 45) - 40바이트 초과!

// 올바른 코드 (바이트 단위로 계산)
String merchantName = "커피전문점";
byte[] bytes = fixedLengthKorean(merchantName, 40);  // 정확히 40바이트
```

### 2. 에러 처리

**BC카드 응답 코드 매핑**
```java
@Service
public class BcCardErrorHandler {

    private static final Map<String, String> ERROR_CODE_MAP = new HashMap<>();

    static {
        ERROR_CODE_MAP.put("0000", "정상 승인");
        ERROR_CODE_MAP.put("1001", "잔액 부족");
        ERROR_CODE_MAP.put("1002", "한도 초과");
        ERROR_CODE_MAP.put("1003", "유효기간 만료");
        ERROR_CODE_MAP.put("1004", "분실/도난 카드");
        ERROR_CODE_MAP.put("2001", "가맹점 정보 오류");
        ERROR_CODE_MAP.put("9001", "시스템 오류");
        ERROR_CODE_MAP.put("9999", "타임아웃");
        // ... 총 200여 개의 에러 코드
    }

    /**
     * BC카드 응답 코드를 사용자 친화적 메시지로 변환
     */
    public String getUserFriendlyMessage(String bcCardCode) {
        return ERROR_CODE_MAP.getOrDefault(bcCardCode, "결제 처리 중 오류가 발생했습니다.");
    }

    /**
     * 재시도 가능 여부 판단
     */
    public boolean isRetryable(String bcCardCode) {
        return Arrays.asList("9001", "9999").contains(bcCardCode);
    }
}
```

### 3. 타임아웃 관리

**문제: 타임아웃 후 거래 상태 불명확**

BC카드 요청 후 30초 타임아웃 발생 시, 실제로 승인이 되었는지 알 수 없는 상황 발생.

**해결: 승인 조회 API 활용**
```java
@Service
public class BcCardApprovalService {

    /**
     * 타임아웃 시 승인 조회로 거래 상태 확인
     */
    @Transactional
    public PaymentResult processPaymentWithTimeout(PaymentRequest request) {
        String transactionId = generateTransactionId();

        try {
            // 1. BC카드 승인 요청
            BcCardResponse response = bcCardMessageService.sendApprovalRequest(request);

            if ("0000".equals(response.getResponseCode())) {
                // 정상 승인
                return saveApprovedTransaction(transactionId, response);
            } else {
                // 승인 거부
                return PaymentResult.rejected(response.getResponseCode());
            }

        } catch (BcCardTimeoutException e) {
            // 2. 타임아웃 발생 - 승인 조회 시도
            log.warn("[타임아웃 발생] transactionId={}, 승인 조회 시도", transactionId);

            try {
                Thread.sleep(5000);  // 5초 대기 후 조회

                BcCardResponse inquiryResponse = bcCardMessageService.sendInquiryRequest(
                    request.getMerchantId(),
                    request.getTerminalId(),
                    transactionId
                );

                if ("0000".equals(inquiryResponse.getResponseCode())) {
                    // 실제로 승인되어 있음
                    log.info("[타임아웃 후 승인 확인] transactionId={}", transactionId);
                    return saveApprovedTransaction(transactionId, inquiryResponse);
                } else {
                    // 승인 안됨 - 재시도 가능
                    log.info("[타임아웃 후 미승인 확인] transactionId={}", transactionId);
                    return PaymentResult.timeout();
                }

            } catch (Exception inquiryException) {
                log.error("[승인 조회 실패] transactionId={}", transactionId, inquiryException);
                // 상태 불명 - 수동 확인 필요
                return PaymentResult.unknown(transactionId);
            }
        }
    }
}
```

## 해결 방안

### 1. 전문 파싱 라이브러리 개발

```java
/**
 * 전문 파싱 유틸리티 (재사용 가능한 라이브러리로 개발)
 */
public class FixedLengthParser {

    private final Charset charset;
    private int position = 0;

    public FixedLengthParser(String message, Charset charset) {
        this.message = message;
        this.charset = charset;
    }

    /**
     * 고정 길이 문자열 읽기
     */
    public String readString(int length) {
        String value = message.substring(position, position + length).trim();
        position += length;
        return value;
    }

    /**
     * 고정 길이 숫자 읽기 (우측 정렬)
     */
    public long readNumeric(int length) {
        String value = readString(length);
        return Long.parseLong(value);
    }

    /**
     * 한글 필드 읽기 (바이트 기준)
     */
    public String readKorean(int byteLength) {
        byte[] bytes = message.getBytes(charset);
        byte[] fieldBytes = Arrays.copyOfRange(bytes, position, position + byteLength);
        position += byteLength;
        return new String(fieldBytes, charset).trim();
    }
}

// 사용 예시
BcCardResponse parseResponse(String responseMessage) {
    FixedLengthParser parser = new FixedLengthParser(responseMessage, EUC_KR);

    String messageType = parser.readString(4);
    String merchantId = parser.readString(10);
    String terminalId = parser.readString(10);
    String responseCode = parser.readString(4);
    long amount = parser.readNumeric(12);
    String approvalNo = parser.readString(12);
    String merchantName = parser.readKorean(40);

    return BcCardResponse.builder()
        .responseCode(responseCode)
        .approvalNo(approvalNo)
        .amount(amount)
        .build();
}
```

### 2. Connection Pool 안정화

```java
@Component
public class BcCardSocketConnectionPool {

    private GenericObjectPool<Socket> pool;

    public BcCardSocketConnectionPool(BcCardSocketConfig config) {
        this.pool = new GenericObjectPool<>(new SocketFactory(config), config.getPoolConfig());
    }

    public Socket borrowSocket() throws Exception {
        return pool.borrowObject();
    }

    public void returnSocket(Socket socket) {
        pool.returnObject(socket);
    }

    /**
     * Socket Factory (연결 생성 및 유효성 검사)
     */
    private static class SocketFactory extends BasePooledObjectFactory<Socket> {

        private final BcCardSocketConfig config;

        public SocketFactory(BcCardSocketConfig config) {
            this.config = config;
        }

        @Override
        public Socket create() throws Exception {
            Socket socket = config.getSocketFactory().createSocket(
                config.getHost(),
                config.getPort()
            );
            socket.setKeepAlive(true);
            socket.setTcpNoDelay(true);
            return socket;
        }

        @Override
        public PooledObject<Socket> wrap(Socket socket) {
            return new DefaultPooledObject<>(socket);
        }

        @Override
        public boolean validateObject(PooledObject<Socket> p) {
            Socket socket = p.getObject();
            return socket != null && socket.isConnected() && !socket.isClosed();
        }

        @Override
        public void destroyObject(PooledObject<Socket> p) throws Exception {
            Socket socket = p.getObject();
            if (socket != null) {
                socket.close();
            }
        }
    }
}
```

### 3. 모니터링 및 로깅

```java
@Aspect
@Component
public class BcCardMonitoringAspect {

    @Autowired
    private MeterRegistry meterRegistry;

    /**
     * BC카드 API 호출 메트릭 수집
     */
    @Around("execution(* com.example.payment.bccard.BcCardMessageService.*(..))")
    public Object monitorBcCardCall(ProceedingJoinPoint joinPoint) throws Throwable {
        String apiName = joinPoint.getSignature().getName();
        Timer.Sample sample = Timer.start(meterRegistry);

        try {
            Object result = joinPoint.proceed();

            // 성공 메트릭
            sample.stop(Timer.builder("bccard.api.call")
                .tag("api", apiName)
                .tag("status", "success")
                .register(meterRegistry));

            return result;

        } catch (BcCardTimeoutException e) {
            // 타임아웃 메트릭
            sample.stop(Timer.builder("bccard.api.call")
                .tag("api", apiName)
                .tag("status", "timeout")
                .register(meterRegistry));

            meterRegistry.counter("bccard.timeout", "api", apiName).increment();
            throw e;

        } catch (Exception e) {
            // 에러 메트릭
            sample.stop(Timer.builder("bccard.api.call")
                .tag("api", apiName)
                .tag("status", "error")
                .register(meterRegistry));

            throw e;
        }
    }
}
```

**Grafana 대시보드 지표:**
- BC카드 API 응답 시간 (평균/P95/P99)
- 타임아웃 발생 비율
- 에러 응답 코드 분포
- Connection Pool 사용률

## 참고 자료

- BC카드 VAN 전문 규격서 (버전 3.5)
- 금융결제원 전자결제 표준 가이드
- ISO 8583 카드 거래 메시지 표준
- Apache Commons Pool2 문서 (Connection Pool)
- EUC-KR vs UTF-8 인코딩 차이점
