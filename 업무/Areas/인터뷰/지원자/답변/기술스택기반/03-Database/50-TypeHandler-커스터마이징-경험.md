# TypeHandler 커스터마이징 경험은?

## 답변

[여기에 답변 작성]

## 핵심 키워드

- TypeHandler
- MyBatis Type Conversion
- Custom Type Mapping
- JDBC Type
- Java Type
- JSON 변환
- Enum 처리

## TypeHandler란?

- JDBC Type과 Java Type 간 변환
- ResultSet에서 값 가져오기
- PreparedStatement에 값 설정
- 기본 TypeHandler 제공
- 커스텀 TypeHandler 작성 가능

## 커스터마이징 필요 상황

- JSON 컬럼을 Java 객체로 변환
- Enum을 특정 값으로 매핑
- 암호화/복호화 처리
- Custom 타입 변환
- Legacy DB 컬럼 변환

## 구현 방법

- BaseTypeHandler 상속
- setNonNullParameter 구현
- getNullableResult 구현
- @MappedTypes, @MappedJdbcTypes 어노테이션

## 코드/쿼리 예시

```java
// JSON TypeHandler 예시
@MappedTypes(OrderMetadata.class)
@MappedJdbcTypes(JdbcType.VARCHAR)
public class JsonTypeHandler extends BaseTypeHandler<OrderMetadata> {

    private static final ObjectMapper objectMapper = new ObjectMapper();

    @Override
    public void setNonNullParameter(PreparedStatement ps, int i,
                                    OrderMetadata parameter, JdbcType jdbcType)
            throws SQLException {
        try {
            ps.setString(i, objectMapper.writeValueAsString(parameter));
        } catch (JsonProcessingException e) {
            throw new SQLException("Error converting OrderMetadata to JSON", e);
        }
    }

    @Override
    public OrderMetadata getNullableResult(ResultSet rs, String columnName)
            throws SQLException {
        return parseJson(rs.getString(columnName));
    }

    @Override
    public OrderMetadata getNullableResult(ResultSet rs, int columnIndex)
            throws SQLException {
        return parseJson(rs.getString(columnIndex));
    }

    @Override
    public OrderMetadata getNullableResult(CallableStatement cs, int columnIndex)
            throws SQLException {
        return parseJson(cs.getString(columnIndex));
    }

    private OrderMetadata parseJson(String json) throws SQLException {
        if (json == null || json.isEmpty()) {
            return null;
        }
        try {
            return objectMapper.readValue(json, OrderMetadata.class);
        } catch (IOException e) {
            throw new SQLException("Error parsing JSON to OrderMetadata", e);
        }
    }
}

// Enum TypeHandler 예시 (코드값 매핑)
@MappedTypes(OrderStatus.class)
@MappedJdbcTypes(JdbcType.VARCHAR)
public class OrderStatusTypeHandler extends BaseTypeHandler<OrderStatus> {

    @Override
    public void setNonNullParameter(PreparedStatement ps, int i,
                                    OrderStatus parameter, JdbcType jdbcType)
            throws SQLException {
        ps.setString(i, parameter.getCode()); // "01", "02" 등
    }

    @Override
    public OrderStatus getNullableResult(ResultSet rs, String columnName)
            throws SQLException {
        return OrderStatus.fromCode(rs.getString(columnName));
    }

    @Override
    public OrderStatus getNullableResult(ResultSet rs, int columnIndex)
            throws SQLException {
        return OrderStatus.fromCode(rs.getString(columnIndex));
    }

    @Override
    public OrderStatus getNullableResult(CallableStatement cs, int columnIndex)
            throws SQLException {
        return OrderStatus.fromCode(cs.getString(columnIndex));
    }
}

// Enum 정의
public enum OrderStatus {
    PENDING("01", "대기"),
    CONFIRMED("02", "확인"),
    SHIPPED("03", "배송중"),
    DELIVERED("04", "배송완료"),
    CANCELLED("99", "취소");

    private final String code;
    private final String description;

    OrderStatus(String code, String description) {
        this.code = code;
        this.description = description;
    }

    public String getCode() {
        return code;
    }

    public static OrderStatus fromCode(String code) {
        if (code == null) return null;
        for (OrderStatus status : values()) {
            if (status.code.equals(code)) {
                return status;
            }
        }
        throw new IllegalArgumentException("Unknown code: " + code);
    }
}

// 암호화 TypeHandler 예시
@MappedTypes(String.class)
@MappedJdbcTypes(JdbcType.VARCHAR)
public class EncryptedStringTypeHandler extends BaseTypeHandler<String> {

    private final EncryptionService encryptionService;

    public EncryptedStringTypeHandler(EncryptionService encryptionService) {
        this.encryptionService = encryptionService;
    }

    @Override
    public void setNonNullParameter(PreparedStatement ps, int i,
                                    String parameter, JdbcType jdbcType)
            throws SQLException {
        ps.setString(i, encryptionService.encrypt(parameter));
    }

    @Override
    public String getNullableResult(ResultSet rs, String columnName)
            throws SQLException {
        String encrypted = rs.getString(columnName);
        return encrypted != null ? encryptionService.decrypt(encrypted) : null;
    }

    @Override
    public String getNullableResult(ResultSet rs, int columnIndex)
            throws SQLException {
        String encrypted = rs.getString(columnIndex);
        return encrypted != null ? encryptionService.decrypt(encrypted) : null;
    }

    @Override
    public String getNullableResult(CallableStatement cs, int columnIndex)
            throws SQLException {
        String encrypted = cs.getString(columnIndex);
        return encrypted != null ? encryptionService.decrypt(encrypted) : null;
    }
}

// Entity에서 사용
public class Order {
    private Long id;
    private OrderStatus status; // OrderStatusTypeHandler 자동 적용
    private OrderMetadata metadata; // JsonTypeHandler 자동 적용

    // getters, setters
}

// MyBatis Configuration
@Configuration
public class MyBatisConfig {

    @Bean
    public SqlSessionFactory sqlSessionFactory(DataSource dataSource) throws Exception {
        SqlSessionFactoryBean sessionFactory = new SqlSessionFactoryBean();
        sessionFactory.setDataSource(dataSource);

        // TypeHandler 등록
        TypeHandlerRegistry registry = sessionFactory.getObject()
            .getConfiguration()
            .getTypeHandlerRegistry();

        registry.register(OrderStatus.class, OrderStatusTypeHandler.class);
        registry.register(OrderMetadata.class, JsonTypeHandler.class);

        return sessionFactory.getObject();
    }
}
```

```xml
<!-- MyBatis Mapper에서 명시적 사용 -->
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE mapper PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN"
  "http://mybatis.org/dtd/mybatis-3-mapper.dtd">
<mapper namespace="com.example.mapper.OrderMapper">

  <!-- TypeHandler 자동 적용 -->
  <select id="getOrder" resultType="Order">
    SELECT id, status, metadata
    FROM orders
    WHERE id = #{id}
  </select>

  <!-- TypeHandler 명시적 지정 -->
  <select id="getOrderWithExplicitHandler" resultType="Order">
    SELECT
      id,
      status,
      metadata
    FROM orders
    WHERE status = #{status, typeHandler=com.example.handler.OrderStatusTypeHandler}
  </select>

  <resultMap id="OrderResultMap" type="Order">
    <id property="id" column="id"/>
    <result property="status" column="status"
            typeHandler="com.example.handler.OrderStatusTypeHandler"/>
    <result property="metadata" column="metadata"
            typeHandler="com.example.handler.JsonTypeHandler"/>
  </resultMap>

  <select id="getOrderWithResultMap" resultMap="OrderResultMap">
    SELECT * FROM orders WHERE id = #{id}
  </select>

</mapper>
```

## 참고 자료

- MyBatis TypeHandler Documentation
- Custom TypeHandler Examples
- MyBatis Configuration Guide
