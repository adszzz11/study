---
date: 2026-11-17
tags: [tech]
type: tech-tool-study
status: draft
---

# CXL Cheatsheet

## Protocol과 type

| 항목 | 요약 |
|---|---|
| CXL.io | discovery, configuration, interrupt, DMA control |
| CXL.cache | device가 host memory를 coherent cache로 사용 |
| CXL.mem | host가 device-attached memory를 coherent하게 접근 |
| Type 1 | local memory 없는 coherent accelerator/SmartNIC |
| Type 2 | local HBM/DDR이 있는 accelerator |
| Type 3 | memory expander; 초기 상용 memory expansion의 중심 |

## Linux object map

```text
firmware/ACPI → CXL port/decoder → memdev(s) → region → system RAM | dax_region
```

```bash
cxl list
cxl list -M
cxl list -D
find /sys/bus/cxl/devices -maxdepth 1 -mindepth 1 -printf '%f\n'
numactl -H
cxl create-region --help
```

## 설계 판단

| 질문 | 권장 판단 |
|---|---|
| 가장 낮은 latency가 필요한가? | local DDR에 둔다. |
| capacity는 더 필요하지만 page가 충분히 cold한가? | CXL Type 3 tier를 평가한다. |
| 훨씬 낮은 비용의 대용량만 필요한가? | NVMe/storage tier를 함께 검토한다. |
| 여러 CXL device를 묶는가? | interleave way, granularity, failure domain을 검증한다. |
| fabric sharing을 검토하는가? | ownership, isolation, security, recovery를 별도 설계한다. |

## 기억할 점

- CXL version과 device type은 서로 다른 축이다.
- CXL memory는 DRAM의 무조건적 대체재가 아니라 capacity/tiering 선택지다.
- device 지원만으로는 부족하다. host CPU, BIOS/UEFI, slot wiring, kernel, userspace가 모두 맞아야 한다.
- QEMU는 topology 학습용이며 hardware performance를 대신하지 않는다.

다음 단계: [[tech/infra/cxl-memory-fabric/05-projects|Projects]]로 검증 계획을 실행한다.

## Sources

- https://docs.kernel.org/driver-api/cxl/devices/device-types.html
- https://docs.kernel.org/driver-api/cxl/linux/cxl-driver.html
- https://cxl.docs.kernel.org/
