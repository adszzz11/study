---
date: 2026-11-17
tags: [tech]
type: tech-tool-study
status: draft
---

# CXL Deep Dive: Region, Tiering, Fabric

## 1. Region과 interleave

Linux CXL model에서 region은 하나 이상의 `memdev` capacity를 decoder와 연결해 만든 addressable 단위다. 여러 Type 3 memdev에 interleave를 적용하면 capacity와 bandwidth 분산을 얻을 수 있지만, device 균질성, failure domain, granularity, workload access pattern을 고려해야 한다.

`cxl create-region`은 일반적으로 interleave way와 granularity를 지정해 region을 만든다. 실제 명령은 topology·kernel·tool version에 따라 달라지므로, 먼저 `cxl list`로 target decoder와 memdev를 검증한다.

```bash
# 실제 대상 이름과 지원 capability를 확인한 뒤에만 실행한다.
cxl list -D -M
cxl create-region --help
```

## 2. System RAM mode와 DAX mode

| Mode | 소비 방식 | 장점 | 주의점 |
|---|---|---|---|
| System RAM | kernel이 NUMA memory로 online | 기존 application이 allocator/NUMA policy를 통해 사용 가능 | page placement와 reclaim/tiering 정책이 성능을 좌우 |
| DAX | filesystem/device-DAX를 통한 직접 addressability | application 또는 runtime이 명시적으로 tier를 제어 가능 | application 변경, lifecycle, error handling 설계 필요 |

어느 mode든 local DDR와 같은 성능이라고 가정하지 않는다. benchmark에는 random/sequential pattern, read/write ratio, working-set size, remote NUMA access를 포함한다.

## 3. Workload-aware tiering

```text
local DDR: latency-sensitive index, hot cache, scheduler-critical data
    CXL: large cold pages, capacity-heavy VM/DB data, less-frequent scans
   NVMe: durable storage, warm/cold overflow, recovery path
```

1. profiler와 memory telemetry로 page temperature 및 bandwidth pressure를 측정한다.
2. CXL placement 전후의 P50/P99 latency, throughput, tail amplification, CPU overhead를 비교한다.
3. NUMA policy와 allocator behavior가 의도한 tier를 실제로 사용하는지 검증한다.
4. firmware event, media error, region offline 같은 RAS failure path를 runbook에 넣는다.

## 4. Fabric과 emulation

CXL 2.0은 switch와 pooling을, CXL 3.x는 multi-level switching·fabric·sharing을 확장한다. 다만 fabric capability가 있다고 해서 multi-host sharing을 즉시 운영할 수 있다는 뜻은 아니다. ownership, isolation, security, orchestration, recovery를 platform별로 검증해야 한다.

hardware가 없으면 QEMU CXL emulation으로 host/bridge/device topology와 kernel object model을 먼저 익힌다. emulation은 topology와 관리 흐름 학습에는 좋지만 실제 latency, bandwidth, RAS 특성의 대체 benchmark는 아니다.

## Sources

- https://pmem.io/ndctl/cxl/cxl-create-region.html
- https://www.qemu.org/docs/master/system/devices/cxl.html
- https://docs.kernel.org/driver-api/cxl/linux/cxl-driver.html
- https://computeexpresslink.org/wp-content/uploads/2024/11/CXL-Specification_rev3p2_ver1p0_2024October2_evalcopy.pdf
