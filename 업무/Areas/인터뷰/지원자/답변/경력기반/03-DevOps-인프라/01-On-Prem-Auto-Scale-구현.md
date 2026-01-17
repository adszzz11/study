# On-Prem 환경에서 auto-scale을 구현한 임시 Shell의 동작 원리는?

## 답변

On-Premise 환경에서는 클라우드의 Auto Scaling Group과 같은 관리형 서비스가 없기 때문에, Shell Script 기반의 커스텀 오토스케일링 솔루션을 구현했습니다. 이는 주기적으로 시스템 메트릭을 모니터링하고, 임계값을 초과하면 자동으로 서버 인스턴스를 추가하거나 제거하는 방식으로 동작합니다.

금융 시스템 특성상 트래픽 패턴이 명확했기 때문에 (장 시작/종료 시간, 월말 정산 등), CPU/메모리 사용률과 함께 시간대별 예측 스케줄링을 결합하여 선제적인 스케일아웃을 수행했습니다.

## 핵심 키워드

- On-Premise Auto Scaling
- Shell Script
- 리소스 모니터링
- 동적 확장
- 인프라 자동화

## Shell 동작 원리

### 모니터링 메트릭
- **CPU 사용률**: `top`, `mpstat` 명령어를 통해 5분 평균 CPU 사용률 수집
- **메모리 사용률**: `free -m` 명령어로 실제 사용 가능한 메모리 확인
- **네트워크 I/O**: `sar -n DEV` 명령어로 네트워크 트래픽 측정
- **애플리케이션 응답 시간**: `/health` 엔드포인트 호출 후 응답 시간 측정
- **활성 커넥션 수**: `netstat -an | grep ESTABLISHED | wc -l`로 측정

### Scale-out 조건
- CPU 사용률이 **70% 이상**을 3회 연속 초과
- 메모리 사용률이 **80% 이상**
- 평균 응답 시간이 **500ms 초과**
- 활성 커넥션 수가 **설정된 임계값의 85% 초과**
- 또는 **예약된 스케줄**(장 시작 30분 전, 월말 정산 시간대)

### Scale-in 조건
- CPU 사용률이 **30% 이하**를 15분간 유지
- 메모리 사용률이 **50% 이하**
- 활성 커넥션 수가 **임계값의 40% 이하**
- 최소 인스턴스 수(2대) 유지 필수
- 스케일아웃 후 **최소 20분 쿨다운 타임** 보장

## 구현 코드 예시

```bash
#!/bin/bash

# 설정
MIN_INSTANCES=2
MAX_INSTANCES=8
CPU_THRESHOLD_HIGH=70
CPU_THRESHOLD_LOW=30
MEMORY_THRESHOLD_HIGH=80
COOLDOWN_SECONDS=1200  # 20분
HEALTHCHECK_ENDPOINT="http://localhost:8080/health"

# 로그 파일
LOGFILE="/var/log/autoscale.log"
METRICS_FILE="/tmp/metrics.txt"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a $LOGFILE
}

# 현재 활성 인스턴스 수 확인
get_active_instances() {
    # 서비스 디스커버리 또는 레지스트리에서 조회
    consul catalog services -tag=active | jq '.[] | select(.Service == "trading-api")' | wc -l
}

# CPU 사용률 측정 (5분 평균)
get_cpu_usage() {
    mpstat 1 5 | awk '/Average/ {print 100 - $NF}'
}

# 메모리 사용률 측정
get_memory_usage() {
    free | awk '/Mem:/ {printf("%.0f", $3/$2 * 100)}'
}

# 헬스체크 응답 시간 측정
get_response_time() {
    local response_time=$(curl -o /dev/null -s -w '%{time_total}\n' $HEALTHCHECK_ENDPOINT)
    echo "$response_time * 1000" | bc | awk '{print int($1)}'  # ms 단위
}

# 활성 커넥션 수
get_active_connections() {
    netstat -an | grep :8080 | grep ESTABLISHED | wc -l
}

# Scale-out 실행
scale_out() {
    local current_instances=$(get_active_instances)

    if [ $current_instances -ge $MAX_INSTANCES ]; then
        log "이미 최대 인스턴스($MAX_INSTANCES)에 도달했습니다."
        return 1
    fi

    log "스케일아웃 시작: 현재 인스턴스 수 = $current_instances"

    # VM 클론 생성 (VMware 또는 Proxmox 환경)
    local new_instance_id="trading-api-$(date +%s)"

    # VM 템플릿에서 클론 생성
    qm clone 100 $new_instance_id --name "$new_instance_id" --full

    # VM 시작
    qm start $new_instance_id

    # 헬스체크 대기 (최대 5분)
    local max_wait=300
    local elapsed=0
    while [ $elapsed -lt $max_wait ]; do
        if curl -sf "http://${new_instance_id}:8080/health" > /dev/null; then
            log "새 인스턴스 $new_instance_id 헬스체크 성공"

            # 로드밸런서에 등록
            consul services register -name=trading-api -id=$new_instance_id -address=${new_instance_id} -port=8080

            # 쿨다운 타임 기록
            echo "$(date +%s)" > /tmp/last_scaleout_time

            log "스케일아웃 완료"
            return 0
        fi
        sleep 10
        elapsed=$((elapsed + 10))
    done

    log "ERROR: 새 인스턴스 헬스체크 실패, VM 제거"
    qm stop $new_instance_id && qm destroy $new_instance_id
    return 1
}

# Scale-in 실행
scale_in() {
    local current_instances=$(get_active_instances)

    if [ $current_instances -le $MIN_INSTANCES ]; then
        log "이미 최소 인스턴스($MIN_INSTANCES)입니다."
        return 1
    fi

    log "스케일인 시작: 현재 인스턴스 수 = $current_instances"

    # 가장 오래된 인스턴스 찾기
    local oldest_instance=$(consul catalog services -tag=active | jq -r '.[0].ID')

    # 로드밸런서에서 제거 (Graceful Shutdown)
    consul services deregister -id=$oldest_instance

    # 드레이닝 대기 (30초)
    sleep 30

    # VM 종료 및 제거
    qm shutdown $oldest_instance --timeout 60
    qm destroy $oldest_instance

    log "스케일인 완료: $oldest_instance 제거"
}

# 쿨다운 체크
check_cooldown() {
    if [ -f /tmp/last_scaleout_time ]; then
        local last_time=$(cat /tmp/last_scaleout_time)
        local current_time=$(date +%s)
        local diff=$((current_time - last_time))

        if [ $diff -lt $COOLDOWN_SECONDS ]; then
            log "쿨다운 타임 중: $((COOLDOWN_SECONDS - diff))초 남음"
            return 1
        fi
    fi
    return 0
}

# 메인 모니터링 루프
main() {
    log "=== Auto Scale 모니터링 시작 ==="

    # 메트릭 수집
    local cpu_usage=$(get_cpu_usage)
    local memory_usage=$(get_memory_usage)
    local response_time=$(get_response_time)
    local connections=$(get_active_connections)
    local current_instances=$(get_active_instances)

    # 메트릭 로깅
    log "메트릭 - CPU: ${cpu_usage}%, MEM: ${memory_usage}%, RT: ${response_time}ms, CONN: ${connections}, INST: ${current_instances}"

    # 메트릭을 파일에 저장 (Prometheus 등에서 수집 가능)
    cat > $METRICS_FILE <<EOF
autoscale_cpu_usage $cpu_usage
autoscale_memory_usage $memory_usage
autoscale_response_time $response_time
autoscale_connections $connections
autoscale_instances $current_instances
EOF

    # Scale-out 결정
    if [ $(echo "$cpu_usage > $CPU_THRESHOLD_HIGH" | bc) -eq 1 ] || \
       [ $(echo "$memory_usage > $MEMORY_THRESHOLD_HIGH" | bc) -eq 1 ] || \
       [ $response_time -gt 500 ]; then

        if check_cooldown; then
            log "스케일아웃 조건 충족: CPU=$cpu_usage%, MEM=$memory_usage%, RT=${response_time}ms"
            scale_out
        fi

    # Scale-in 결정
    elif [ $(echo "$cpu_usage < $CPU_THRESHOLD_LOW" | bc) -eq 1 ] && \
         [ $(echo "$memory_usage < 50" | bc) -eq 1 ]; then

        log "스케일인 조건 충족: CPU=$cpu_usage%, MEM=$memory_usage%"
        scale_in
    else
        log "정상 범위 내 운영 중"
    fi
}

# Cron으로 1분마다 실행되도록 설정
# */1 * * * * /usr/local/bin/autoscale.sh >> /var/log/autoscale.log 2>&1

main
```

## 제약사항 및 한계

- **물리적 제약**: 실제 서버 대수에 한계가 있어 갑작스러운 트래픽 급증 대응에 한계
- **VM 프로비저닝 시간**: 클라우드 대비 VM 생성 및 부팅 시간이 길어 빠른 스케일아웃 어려움 (평균 2-3분)
- **네트워크 설정 복잡도**: IP 할당, VLAN 설정, 방화벽 규칙 등 수동 네트워크 구성 필요
- **상태 관리의 어려움**: 스크립트 자체의 단일 장애점(SPOF) 가능성, 분산 락 구현 필요
- **비용 비효율**: 유휴 서버 자원이 물리적으로 존재해야 하므로 비용 효율성 낮음
- **복잡한 롤백**: 스케일아웃 실패 시 수동 개입이 필요한 경우 발생

## Cloud vs On-Prem Auto Scaling 비교

| 항목 | Cloud (AWS ASG) | On-Premise (Custom Script) |
|------|-----------------|----------------------------|
| **설정 복잡도** | 낮음 (콘솔/IaC로 간단 설정) | 높음 (스크립트, VM 관리, 네트워크 직접 구성) |
| **프로비저닝 속도** | 빠름 (30초~1분) | 느림 (2~5분, VM 템플릿 방식에 따라 다름) |
| **비용 모델** | 종량제 (사용한만큼 과금) | 고정비 (미리 서버 확보 필요) |
| **확장성 한계** | 거의 무제한 | 물리 서버 수에 제한 |
| **장애 대응** | 자동 헬스체크 및 복구 | 수동 스크립트 작성 필요 |
| **통합성** | CloudWatch, ELB 등과 네이티브 연동 | Consul, Prometheus 등 직접 연동 구현 |
| **관리 오버헤드** | 낮음 (관리형 서비스) | 높음 (스크립트 유지보수, 인프라 관리) |
| **금융권 규제 대응** | 어려움 (데이터 외부 반출 제한) | 용이함 (온프레미스 데이터 보관) |

## 참고 자료

- [VMware vSphere API for VM Management](https://developer.vmware.com/apis/vsphere-automation/latest/)
- [Consul Service Discovery](https://developer.hashicorp.com/consul/docs/discovery/services)
- [HAProxy Runtime API for Dynamic Backend Management](http://www.haproxy.org/download/2.0/doc/management.txt)
- [Linux System Monitoring Commands (mpstat, sar, free)](https://www.man7.org/linux/man-pages/)
