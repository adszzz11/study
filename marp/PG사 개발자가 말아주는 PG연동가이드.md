---
marp: true
theme: gaia
paginate: true
backgroundImage: url('https://source.unsplash.com/1600x900/?payment,technology')
backgroundSize: cover
---

<br><br><br><br>

# 💳 **PG사 개발자가 말아주는 PG연동가이드**
#### 실무에서 놓치기 쉬운 포인트들

<br><br>

##### 👨‍💻 **실무 PG 개발자** &nbsp;&nbsp; 📍 2025

---
## 👋 **소개**

<table style="width: 100%;">
  <tr>
    <td style="width: 60%; vertical-align: top; text-align: left; padding-right: 2em;">
      경력 : PG사 시스템 개발 5년차<br>
      담당 : 결제 시스템, 가맹점 연동 API<br>
      특기 : 결제 장애 대응, 보안 이슈 해결<br>
      현실 : 새벽 3시 장애 콜을 받는 것이 일상<br>
      목표 : 안정적인 결제 시스템 구축
    </td>
    <td style="width: 40%; text-align: right;">
      🏦 PG (Payment Gateway)<br>
      💸 결제 처리<br>
      🔒 보안<br>
      📊 정산<br>
      🚨 장애 대응
    </td>
  </tr>
</table>

---

<br><br><br><br>

# **PG 연동의 기본**
- 결제가 단순해 보이지만 실제로는...

---
## 🏦 **PG(Payment Gateway)란?**

<br><br>

### 온라인 결제를 중개하는 서비스
### 가맹점과 카드사/은행 사이의 다리 역할

<br>

**🔄 간단한 결제 흐름**: 고객 → 가맹점 → PG → 카드사/은행 → PG → 가맹점 → 고객

---

## 💳 **실제 결제 프로세스 - 전체 흐름**

### **1단계: 결제 요청 (사용자 → 가맹점)**
```
👤 사용자: "결제하기" 버튼 클릭
📱 가맹점 앱/웹: 주문 정보 생성 (주문번호, 금액, 상품명)
🏪 가맹점 서버: 결제 토큰 생성 및 PG 결제창 URL 요청
```

### **2단계: 결제창 호출 (가맹점 → PG)**
```
🏪 가맹점 → 🏦 PG: 결제 준비 API 호출
   - merchantId, amount, orderNo, returnUrl 전송
🏦 PG: 결제창 URL 생성 및 응답
📱 가맹점: 결제창 팝업/리다이렉트
```

---

## 💳 **실제 결제 프로세스 - 결제 진행**

### **3단계: 카드 정보 입력 (사용자 → PG)**
```
👤 사용자: PG 결제창에서 카드 정보 입력
   - 카드번호, 유효기간, CVC, 생년월일
🏦 PG: 카드 정보 검증 및 토큰화
   - 실제 카드번호는 즉시 암호화/토큰화
```

### **4단계: 카드사 승인 요청 (PG → VAN → 카드사)**
```
🏦 PG → 🏢 VAN (Value Added Network)
   - 카드 정보 + 거래 정보 전송
🏢 VAN → 🏛️ 카드사 (신한, 삼성, 현대 등)
   - 카드 유효성, 한도, 잔액 확인
🏛️ 카드사: 승인/거절 결정
   - 승인번호 생성 (성공 시)
```

---

## 💳 **실제 결제 프로세스 - 승인 완료**

### **5단계: 승인 결과 전달 (카드사 → PG)**
```
🏛️ 카드사 → 🏢 VAN → 🏦 PG
   - 승인번호, 결과코드, 결과메시지
🏦 PG: 결제 결과 저장 및 처리
   - 승인 시: 결제 완료 상태로 변경
   - 거절 시: 실패 사유와 함께 거절 처리
```

### **6단계: 결과 통지 (PG → 가맹점 → 사용자)**
```
🏦 PG → 🏪 가맹점 서버: 웹훅(Webhook) 전송
   - 실시간 결제 결과 통지
🏪 가맹점: 주문 상태 업데이트, 상품 지급
📱 가맹점 → 👤 사용자: 결제 완료 페이지 표시
```

---

## 🔄 **상세 시퀀스 다이어그램**

```
👤사용자    📱가맹점앱    🏪가맹점서버    🏦PG    🏢VAN    🏛️카드사
  │          │           │           │       │        │
  │ 결제요청 │           │           │       │        │
  ├─────────►│           │           │       │        │
  │          │ 주문생성 │           │       │        │
  │          ├──────────►│           │       │        │
  │          │           │결제준비API│       │        │
  │          │           ├──────────►│       │        │
  │          │           │결제창URL  │       │        │
  │          │           ◄───────────┤       │        │
  │          │결제창팝업│           │       │        │
  │          ◄───────────┤           │       │        │
  │ 카드정보입력        │           │       │        │
  ├──────────────────────────────────►│       │        │
  │          │           │           │승인요청│        │
  │          │           │           ├───────►│        │
  │          │           │           │        │승인요청│
  │          │           │           │        ├───────►│
  │          │           │           │        │승인응답│
  │          │           │           │        ◄────────┤
  │          │           │           │승인응답│        │
  │          │           │           ◄────────┤        │
  │          │           │ 웹훅통지 │       │        │
  │          │           ◄───────────┤       │        │
  │          │ 완료페이지│           │       │        │
  │          ◄───────────┤           │       │        │
  │ 결제완료 │           │           │       │        │
  ◄─────────┤           │           │       │        │
```

---
## 💳 **결제 방식의 종류**

1. **💻 웹 결제 (PC/Mobile Web)**
   - 결제창 팝업, 리다이렉트 방식
   - 가장 일반적인 형태

2. **📱 앱 결제 (In-App)**
   - SDK 연동, 앱 내 결제
   - 사용자 편의성 높음

3. **🔗 API 결제**
   - 서버 간 직접 통신
   - 정기결제, B2B 결제에 주로 사용

---

## 🔐 **결제 보안의 핵심**

### **PCI DSS (Payment Card Industry Data Security Standard)**
- 카드 정보 보호를 위한 국제 표준
- **절대 규칙**: 가맹점 서버에 카드번호 저장 금지

### **토큰화 (Tokenization)**
- 실제 카드번호 대신 토큰 사용
- PG에서 안전하게 관리

### **3D Secure**
- 카드사의 추가 인증 시스템
- 온라인 결제 사기 방지

---

<br><br><br><br>

# **실무에서 자주 놓치는 포인트들**
- 이론과 현실의 차이

---

## ⚠️ **1. 테스트 환경과 운영 환경의 차이**

### **흔한 실수들**
- 테스트에서는 잘 되는데 운영에서 실패
- API 키 설정 실수
- 네트워크 정책 차이

### **해결책**
```javascript
// 환경별 설정 분리
const pgConfig = {
  development: {
    apiUrl: 'https://api.sandbox.pg.com',
    merchantId: 'test_merchant',
    secretKey: process.env.PG_TEST_SECRET
  },
  production: {
    apiUrl: 'https://api.pg.com',
    merchantId: 'real_merchant',
    secretKey: process.env.PG_PROD_SECRET
  }
}
```

---

## ⚠️ **2. 타임아웃과 네트워크 이슈**

### **문제점**
- PG 응답 지연 시 사용자 중복 결제 시도
- 네트워크 불안정으로 인한 결제 상태 불일치

### **해결책**
```javascript
// 적절한 타임아웃 설정
const paymentRequest = axios.create({
  timeout: 30000, // 30초
  retry: 3,
  retryDelay: 1000
});

// 중복 방지를 위한 orderNo 생성
const orderNo = `${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
```

### **실무 팁**
- 결제 버튼 중복 클릭 방지 필수
- 타임아웃은 30초 이상 권장

---

## ⚠️ **3. 웹훅(Webhook) 처리의 함정**

### **놓치기 쉬운 부분**
```javascript
// ❌ 잘못된 예
app.post('/webhook', (req, res) => {
  // 서명 검증 없음 - 보안 위험!
  const paymentData = req.body;
  updatePaymentStatus(paymentData);
  res.send('OK');
});
```

### **올바른 처리**
```javascript
// ✅ 올바른 예
app.post('/webhook', async (req, res) => {
  try {
    // 1. 서명 검증
    const signature = req.headers['x-pg-signature'];
    if (!verifySignature(req.body, signature)) {
      return res.status(401).send('Unauthorized');
    }

    // 2. 멱등성 보장 (중복 처리 방지)
    const webhookId = req.headers['x-webhook-id'];
    if (await isProcessed(webhookId)) {
      return res.status(200).send('Already processed');
    }

    // 3. 트랜잭션 처리
    await processPaymentWebhook(req.body, webhookId);
    res.status(200).send('OK');
  } catch (error) {
    console.error('Webhook error:', error);
    res.status(500).send('Internal Server Error');
  }
});
```

---

## ⚠️ **4. 결제 상태 관리의 복잡성**

### **결제 상태 종류**
- `PENDING`: 결제 요청 중
- `SUCCESS`: 결제 성공
- `FAILED`: 결제 실패
- `CANCELLED`: 결제 취소
- `PARTIAL_CANCELLED`: 부분 취소

### **상태 전이 다이어그램**
```
PENDING → SUCCESS → CANCELLED
   ↓         ↓         ↑
FAILED   PARTIAL_CANCELLED
```

### **실무에서 주의사항**
- 동시성 문제로 인한 상태 불일치
- 부분 취소 시 재고 관리
- 정산 시점과 결제 완료 시점의 차이

---

## ⚠️ **5. 에러 처리와 로깅**

### **필수 로그 항목**
```javascript
const paymentLog = {
  timestamp: new Date().toISOString(),
  orderNo: orderData.orderNo,
  amount: orderData.amount,
  pgTxId: response.txId,
  resultCode: response.resultCode,
  resultMessage: response.resultMessage,
  userAgent: req.headers['user-agent'],
  ipAddress: req.ip,
  processingTime: Date.now() - startTime
};

// 성공/실패 여부와 관계없이 모든 결제 시도를 로깅
logger.info('Payment attempt', paymentLog);
```

### **에러 코드 매핑**
```javascript
const PG_ERROR_CODES = {
  'INSUFFICIENT_FUNDS': '잔액이 부족합니다',
  'CARD_EXPIRED': '카드 유효기간이 만료되었습니다',
  'INVALID_CARD': '유효하지 않은 카드입니다',
  'LIMIT_EXCEEDED': '한도를 초과했습니다'
};
```

---

<br><br><br><br>

# **결제 연동 체크리스트**
- 출시 전 반드시 확인해야 할 항목들

---

## ✅ **개발 단계 체크리스트**

### **🔧 기본 설정**
- [ ] 환경별 API 키 분리 설정
- [ ] HTTPS 통신 강제 적용
- [ ] CORS 정책 설정
- [ ] 타임아웃 설정 (30초 이상)

### **💳 결제 플로우**
- [ ] 중복 결제 방지 로직
- [ ] 결제 취소 기능 구현
- [ ] 부분 취소 지원 여부 확인
- [ ] 정기결제 (빌링) 구현 시 해지 기능

### **🔒 보안**
- [ ] 카드 정보 비저장 원칙 준수
- [ ] API 서명 검증 구현
- [ ] 웹훅 서명 검증 구현
- [ ] 민감 정보 로깅 방지

---

## ✅ **테스트 단계 체크리스트**

### **🧪 기능 테스트**
- [ ] 정상 결제 시나리오
- [ ] 결제 실패 시나리오 (잔액 부족, 카드 오류 등)
- [ ] 네트워크 지연/끊김 상황
- [ ] 동시 결제 요청 처리
- [ ] 웹훅 중복 수신 처리

### **📊 성능 테스트**
- [ ] 동시 사용자 부하 테스트
- [ ] 피크 시간대 안정성 확인
- [ ] 메모리 누수 확인
- [ ] 데이터베이스 부하 테스트

### **🔍 모니터링**
- [ ] 결제 성공률 모니터링 구축
- [ ] 응답 시간 모니터링
- [ ] 에러율 추적
- [ ] 알림 설정 (실패율 임계값 초과 시)

---

## ✅ **운영 준비 체크리스트**

### **📋 문서화**
- [ ] API 연동 가이드 작성
- [ ] 에러 코드 정의서
- [ ] 장애 대응 매뉴얼
- [ ] 정산 처리 프로세스 문서화

### **🚨 장애 대응**
- [ ] 24시간 모니터링 체계
- [ ] 장애 알림 시스템 구축
- [ ] 롤백 절차 수립
- [ ] 비상 연락망 구축

### **📈 정산 및 리포팅**
- [ ] 일별/월별 정산 보고서
- [ ] 환불/취소 내역 추적
- [ ] 수수료 계산 로직 검증
- [ ] 세금계산서 발행 연동

---

<br><br><br><br>

# **자주 묻는 질문 (FAQ)**
- 실무에서 자주 받는 질문들

---

## ❓ **Q: 결제창이 모바일에서 제대로 안 떠요**

### **A: 모바일 환경 이슈**
```javascript
// 모바일 앱에서 결제창 호출 시
if (isMobileApp()) {
  // 앱 내 웹뷰에서는 popup 대신 redirect 방식 사용
  location.href = paymentUrl;
} else {
  // PC에서는 popup 방식 사용
  window.open(paymentUrl, 'payment', 'width=500,height=600');
}
```

**해결책**
- iOS Safari: popup 차단 이슈 → redirect 방식 사용
- Android WebView: intent 스키마 처리 필요
- 하이브리드 앱: 네이티브 브릿지 활용

---

## ❓ **Q: 결제는 성공했는데 상품이 지급되지 않았어요**

### **A: 웹훅 처리 실패**

**원인 분석**
1. 웹훅 URL 응답 지연 (30초 초과)
2. 서버 에러로 인한 500 응답
3. 웹훅 처리 중 예외 발생

**해결 방법**
```javascript
// 웹훅 재처리를 위한 배치 작업
async function retryFailedWebhooks() {
  const failedPayments = await getPaymentsWithoutWebhook();

  for (const payment of failedPayments) {
    try {
      // PG사에 결제 상태 조회
      const status = await queryPaymentStatus(payment.pgTxId);
      if (status === 'SUCCESS') {
        await processPaymentSuccess(payment);
      }
    } catch (error) {
      console.error(`Failed to retry payment ${payment.id}:`, error);
    }
  }
}

// 매 10분마다 실행
setInterval(retryFailedWebhooks, 10 * 60 * 1000);
```

---

## ❓ **Q: 정기결제가 갑자기 실패하기 시작했어요**

### **A: 빌링키 만료 또는 카드 상태 변경**

**일반적인 원인**
- 카드 재발급 (카드번호/유효기간 변경)
- 카드 한도 초과
- 카드 정지/해지
- 빌링키 만료

**대응 방안**
```javascript
// 빌링 실패 시 자동 재시도 로직
const retryBilling = async (billingKey, amount, retryCount = 0) => {
  if (retryCount >= 3) {
    // 고객에게 카드 정보 업데이트 요청
    await notifyCardUpdateRequired(billingKey);
    return;
  }

  try {
    const result = await processBilling(billingKey, amount);
    if (result.status === 'FAILED') {
      // 1일 후 재시도
      setTimeout(() => retryBilling(billingKey, amount, retryCount + 1), 24 * 60 * 60 * 1000);
    }
  } catch (error) {
    console.error('Billing retry failed:', error);
  }
};
```

---

## ❓ **Q: PG 수수료를 줄일 수 있는 방법이 있나요?**

### **A: 수수료 최적화 전략**

**1. 결제 방식별 수수료 차이 활용**
- 계좌이체 < 카드결제
- 일반카드 < 체크카드
- 국내카드 < 해외카드

**2. 거래액 기반 협상**
```javascript
// 월 거래액별 수수료 차등 적용
const getFeeRate = (monthlyVolume) => {
  if (monthlyVolume > 100000000) return 2.2; // 1억 이상
  if (monthlyVolume > 50000000) return 2.5;  // 5천만 이상
  if (monthlyVolume > 10000000) return 2.8;  // 1천만 이상
  return 3.2; // 기본
};
```

**3. 복수 PG 운영**
- 주 PG + 백업 PG 구성
- 수수료/성공률 기반 라우팅

---

<br><br><br><br>

# **마무리: 안정적인 결제 시스템을 위해**
- 놓치지 말아야 할 핵심들

---

## 🎯 **핵심 원칙**

### **1. 보안 우선**
- 카드 정보는 절대 저장하지 말 것
- 모든 통신은 HTTPS 사용
- API 서명 검증 필수

### **2. 사용자 경험**
- 결제 프로세스는 최대한 단순하게
- 명확한 에러 메시지 제공
- 모바일 최적화 필수

### **3. 안정성**
- 장애 상황에 대한 대비책 마련
- 모니터링과 알림 시스템 구축
- 정기적인 테스트와 점검

---

## 📋 **마지막 체크포인트**

### **개발자가 반드시 기억해야 할 것들**
1. **멱등성**: 같은 요청은 같은 결과를 보장
2. **원자성**: 결제와 상품 지급은 하나의 트랜잭션
3. **일관성**: 결제 상태와 비즈니스 로직의 일치
4. **격리성**: 동시 요청 간 간섭 방지
5. **지속성**: 결제 데이터의 영구 보존

### **운영팀이 준비해야 할 것들**
- 24시간 모니터링 체계
- 장애 대응 매뉴얼
- 고객 문의 대응 가이드
- 정산 및 세무 처리 프로세스

---

## 💡 **실무 팁**

### **개발 시**
- 로컬에서도 HTTPS 환경 구성 권장
- 테스트 카드 번호 외 실제 카드로 테스트 금지
- 웹훅 테스트를 위한 ngrok 등 터널링 도구 활용

### **운영 시**
- 새벽 시간대 정기점검 스케줄링
- 결제 관련 로그는 최소 1년 보관
- 고객 문의 시 pgTxId로 빠른 추적 가능

### **트러블슈팅**
- 결제 실패 시 PG사 로그와 자사 로그 교차 확인
- 네트워크 이슈는 타임아웃 로그로 판단
- 카드사별 에러 코드 차이점 숙지

---

<!-- _class: lead -->

# **QnA**
### 궁금한 점이 있으시면 언제든지 질문해주세요!

---

<!-- _class: lead -->

# **감사합니다**
### 안전하고 안정적인 결제 시스템을 만들어 나가요! 💳✨