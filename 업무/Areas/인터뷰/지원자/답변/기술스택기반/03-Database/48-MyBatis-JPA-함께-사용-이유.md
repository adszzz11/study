# MyBatis와 JPA를 함께 사용한 이유는?

## 답변

[여기에 답변 작성]

## 핵심 키워드

- MyBatis
- JPA (Java Persistence API)
- Hibernate
- SQL Mapper vs ORM
- 하이브리드 접근
- 복잡한 쿼리

## MyBatis의 장점

- 복잡한 SQL 직접 작성
- Dynamic SQL 지원
- Legacy 시스템 통합 용이
- 세밀한 SQL 제어
- 학습 곡선 낮음

## JPA의 장점

- 객체 중심 개발
- CRUD 자동화
- 데이터베이스 독립성
- 1차 캐시, 지연 로딩
- 타입 세이프 쿼리 (Criteria API)

## 함께 사용하는 시나리오

- CRUD: JPA 사용
- 복잡한 조회/통계: MyBatis 사용
- 동적 검색 조건: MyBatis
- 배치 처리: MyBatis
- 레거시 DB 연동: MyBatis

## 주의사항

- 1차 캐시 동기화 문제
- 트랜잭션 경계 명확히
- Entity 변경 감지 고려
- 데이터 정합성 유지

## 코드/쿼리 예시

```java
// JPA Entity
@Entity
@Table(name = "orders")
public class Order {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String orderNumber;
    private LocalDateTime orderDate;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "customer_id")
    private Customer customer;

    // getters, setters
}

// JPA Repository (Simple CRUD)
@Repository
public interface OrderRepository extends JpaRepository<Order, Long> {
    List<Order> findByCustomerId(Long customerId);
}

// MyBatis Mapper Interface
@Mapper
public interface OrderMapper {
    // 복잡한 통계 쿼리
    List<OrderStatistics> getOrderStatistics(
        @Param("startDate") LocalDate startDate,
        @Param("endDate") LocalDate endDate,
        @Param("status") String status
    );

    // 동적 검색
    List<Order> searchOrders(OrderSearchCriteria criteria);
}
```

```xml
<!-- MyBatis Mapper XML -->
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE mapper PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN"
  "http://mybatis.org/dtd/mybatis-3-mapper.dtd">
<mapper namespace="com.example.mapper.OrderMapper">

  <!-- 복잡한 통계 쿼리 -->
  <select id="getOrderStatistics" resultType="OrderStatistics">
    SELECT
      DATE(order_date) as order_date,
      status,
      COUNT(*) as order_count,
      SUM(total_amount) as total_amount,
      AVG(total_amount) as avg_amount
    FROM orders
    WHERE order_date BETWEEN #{startDate} AND #{endDate}
    <if test="status != null">
      AND status = #{status}
    </if>
    GROUP BY DATE(order_date), status
    ORDER BY order_date DESC
  </select>

  <!-- 동적 검색 쿼리 -->
  <select id="searchOrders" resultType="Order">
    SELECT * FROM orders
    <where>
      <if test="customerName != null">
        AND customer_name LIKE CONCAT('%', #{customerName}, '%')
      </if>
      <if test="startDate != null">
        AND order_date >= #{startDate}
      </if>
      <if test="endDate != null">
        AND order_date &lt;= #{endDate}
      </if>
      <if test="status != null">
        AND status = #{status}
      </if>
    </where>
    ORDER BY order_date DESC
    LIMIT #{offset}, #{limit}
  </select>

</mapper>
```

```java
// Service Layer에서 함께 사용
@Service
@Transactional
public class OrderService {

    private final OrderRepository orderRepository; // JPA
    private final OrderMapper orderMapper; // MyBatis

    // JPA 사용 - Simple CRUD
    public Order createOrder(Order order) {
        return orderRepository.save(order);
    }

    public Order getOrder(Long id) {
        return orderRepository.findById(id)
            .orElseThrow(() -> new EntityNotFoundException());
    }

    // MyBatis 사용 - 복잡한 조회
    public List<OrderStatistics> getStatistics(
            LocalDate startDate, LocalDate endDate, String status) {
        return orderMapper.getOrderStatistics(startDate, endDate, status);
    }

    // MyBatis 사용 - 동적 검색
    public List<Order> searchOrders(OrderSearchCriteria criteria) {
        return orderMapper.searchOrders(criteria);
    }
}

// Configuration
@Configuration
public class DatabaseConfig {

    @Bean
    public SqlSessionFactory sqlSessionFactory(DataSource dataSource) throws Exception {
        SqlSessionFactoryBean sessionFactory = new SqlSessionFactoryBean();
        sessionFactory.setDataSource(dataSource);
        return sessionFactory.getObject();
    }
}
```

## 참고 자료

- MyBatis Official Documentation
- Spring Data JPA Reference
- Combining JPA and MyBatis Best Practices
