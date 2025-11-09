# Dynamic SQL 작성 시 주의사항은?

## 답변

[여기에 답변 작성]

## 핵심 키워드

- Dynamic SQL
- SQL Injection
- Parameter Binding
- PreparedStatement
- MyBatis Dynamic SQL
- 성능 최적화
- SQL 가독성

## 주요 주의사항

1. SQL Injection 방지
2. Parameter Binding 사용
3. NULL 처리
4. 빈 WHERE 절 방지
5. 동적 쿼리 재사용성
6. 실행 계획 캐싱
7. 가독성 유지

## SQL Injection 방지

- PreparedStatement 사용
- #{} 파라미터 바인딩 (MyBatis)
- ${} 직접 치환 지양
- 입력값 검증

## MyBatis Dynamic SQL 태그

- `<if>`: 조건부 포함
- `<choose>`, `<when>`, `<otherwise>`: switch-case
- `<where>`: WHERE 절 자동 처리
- `<set>`: SET 절 자동 처리
- `<foreach>`: 반복 처리
- `<trim>`: 접두/접미어 제거

## 성능 고려사항

- 동적 쿼리 캐싱
- 불필요한 동적 조건 최소화
- 인덱스 활용 가능한 구조
- OR 조건 최소화

## 코드/쿼리 예시

```xml
<!-- MyBatis Dynamic SQL 예시 -->
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE mapper PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN"
  "http://mybatis.org/dtd/mybatis-3-mapper.dtd">
<mapper namespace="com.example.mapper.UserMapper">

  <!-- if 태그 사용 -->
  <select id="searchUsers" resultType="User">
    SELECT * FROM users
    <where>
      <if test="username != null and username != ''">
        AND username LIKE CONCAT('%', #{username}, '%')
      </if>
      <if test="email != null and email != ''">
        AND email = #{email}
      </if>
      <if test="status != null">
        AND status = #{status}
      </if>
    </where>
  </select>

  <!-- choose 태그 사용 (switch-case) -->
  <select id="getUsersByType" resultType="User">
    SELECT * FROM users
    WHERE 1=1
    <choose>
      <when test="type == 'ACTIVE'">
        AND status = 'ACTIVE' AND last_login > DATE_SUB(NOW(), INTERVAL 30 DAY)
      </when>
      <when test="type == 'INACTIVE'">
        AND status = 'INACTIVE' OR last_login &lt;= DATE_SUB(NOW(), INTERVAL 30 DAY)
      </when>
      <otherwise>
        AND status = 'PENDING'
      </otherwise>
    </choose>
  </select>

  <!-- foreach 태그 사용 (IN 절) -->
  <select id="getUsersByIds" resultType="User">
    SELECT * FROM users
    WHERE id IN
    <foreach collection="ids" item="id" open="(" separator="," close=")">
      #{id}
    </foreach>
  </select>

  <!-- set 태그 사용 (UPDATE) -->
  <update id="updateUser">
    UPDATE users
    <set>
      <if test="username != null">username = #{username},</if>
      <if test="email != null">email = #{email},</if>
      <if test="status != null">status = #{status},</if>
      updated_at = NOW()
    </set>
    WHERE id = #{id}
  </update>

  <!-- trim 태그 사용 -->
  <select id="searchWithTrim" resultType="User">
    SELECT * FROM users
    <trim prefix="WHERE" prefixOverrides="AND |OR ">
      <if test="username != null">
        AND username = #{username}
      </if>
      <if test="email != null">
        AND email = #{email}
      </if>
    </trim>
  </select>

  <!-- 잘못된 예시 (SQL Injection 취약) -->
  <select id="badExample" resultType="User">
    SELECT * FROM users
    WHERE username = '${username}'  <!-- ❌ 위험! -->
  </select>

  <!-- 올바른 예시 -->
  <select id="goodExample" resultType="User">
    SELECT * FROM users
    WHERE username = #{username}  <!-- ✅ 안전 -->
  </select>

  <!-- 복잡한 동적 쿼리 예시 -->
  <select id="complexSearch" resultType="Order">
    SELECT
      o.*,
      c.customer_name,
      COUNT(oi.id) as item_count
    FROM orders o
    INNER JOIN customers c ON o.customer_id = c.id
    LEFT JOIN order_items oi ON o.id = oi.order_id
    <where>
      <if test="customerId != null">
        AND o.customer_id = #{customerId}
      </if>
      <if test="startDate != null">
        AND o.order_date >= #{startDate}
      </if>
      <if test="endDate != null">
        AND o.order_date &lt;= #{endDate}
      </if>
      <if test="statusList != null and statusList.size() > 0">
        AND o.status IN
        <foreach collection="statusList" item="status" open="(" separator="," close=")">
          #{status}
        </foreach>
      </if>
      <if test="minAmount != null">
        AND o.total_amount >= #{minAmount}
      </if>
    </where>
    GROUP BY o.id, c.customer_name
    <if test="sortBy != null">
      <choose>
        <when test="sortBy == 'DATE_DESC'">
          ORDER BY o.order_date DESC
        </when>
        <when test="sortBy == 'AMOUNT_DESC'">
          ORDER BY o.total_amount DESC
        </when>
        <otherwise>
          ORDER BY o.id DESC
        </otherwise>
      </choose>
    </if>
    LIMIT #{offset}, #{limit}
  </select>

</mapper>
```

```java
// Java Code에서 사용
@Mapper
public interface UserMapper {
    List<User> searchUsers(
        @Param("username") String username,
        @Param("email") String email,
        @Param("status") String status
    );

    List<User> getUsersByIds(@Param("ids") List<Long> ids);

    int updateUser(User user);
}

// Service Layer
@Service
public class UserService {

    @Autowired
    private UserMapper userMapper;

    public List<User> search(String username, String email, String status) {
        // null이나 빈 문자열도 그대로 전달 가능 (XML에서 처리)
        return userMapper.searchUsers(username, email, status);
    }

    public List<User> getUsersByIds(List<Long> ids) {
        if (ids == null || ids.isEmpty()) {
            return Collections.emptyList();
        }
        return userMapper.getUsersByIds(ids);
    }
}
```

## 참고 자료

- MyBatis Dynamic SQL Documentation
- SQL Injection Prevention Guide
- MyBatis Best Practices
