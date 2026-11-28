---
date: 2026-11-17
tags: [tech]
type: tech-tool-study
status: draft
---

# CXL Overview

## What: PCIe 위의 coherent interconnect

CXL은 PCIe PHY와 link initialization을 기반으로 하되, 단순 I/O 전송을 넘어 cache-coherent memory access를 제공한다. PCIe를 대체하는 기술이라기보다 CPU memory·device memory·accelerator 사이의 coherent use case를 확장한다.

| Protocol | 역할 |
|---|---|
| `CXL.io` | PCIe와 유사한 discovery, configuration, interrupt, DMA 제어 경로 |
| `CXL.cache` | device가 host memory를 coherent하게 cache하도록 함 |
| `CXL.mem` | host CPU가 device-attached HDM(Host-Managed Device Memory)을 coherent memory로 접근하도록 함 |

## Why: capacity와 copy 비용의 경계

직결 DDR은 가장 빠르지만 CPU socket당 DIMM slot·memory channel에 묶인다. PCIe 장치는 고속일 수 있어도 보통 DMA와 명시적 copy·synchronization을 요구한다. CXL은 CPU가 device memory를 memory semantics로 접근하도록 하여 capacity 확장과 memory tiering의 선택지를 추가한다.

핵심 trade-off는 명확하다. CXL memory는 대개 local DDR보다 더 먼 NUMA tier이며 latency와 bandwidth가 불리할 수 있다. 따라서 workload profiling, page placement, interleave 정책이 필요하다.

## Device type

| Type | Protocol | 대표 역할 |
|---|---|---|
| Type 1 | `CXL.io + CXL.cache` | local memory가 없는 coherent accelerator/SmartNIC |
| Type 2 | `CXL.io + CXL.cache + CXL.mem` | local HBM/DDR을 가진 GPU, FPGA, AI accelerator |
| Type 3 | `CXL.io + CXL.mem` | volatile/persistent memory expander |

Type 3가 현재 memory expansion의 가장 현실적인 상용 진입점이다. Type 2의 coherence는 유망하지만, production software와 platform 지원 범위는 use case별로 검증해야 한다.

## Topology와 세대

```text
Host CPU / root port
  ├─ direct-attached Type 3 memory expander
  └─ CXL switch ── Type 1 / Type 2 / Type 3 endpoints
```

- **CXL 2.0**: switch와 memory pooling을 확장했다.
- **CXL 3.x**: multi-level switching, fabric, memory sharing을 강화했다.
- **CXL 4.0**: 128 GT/s, native x2 width, 최대 4개 retimer, bundled port, memory RAS 개선을 추가했다.

bundled port는 여러 physical port traffic을 하나의 논리 연결로 분산해 accelerator bandwidth를 높인다. 표준 기능의 존재와 특정 server platform의 실제 배포 가능성은 구분한다.

## Linux 관점

firmware/ACPI가 topology와 decoder를 노출하고 Linux CXL driver가 `memdev`, `decoder`, `region`, `dax_region`을 구성한다. 여러 memdev를 interleave한 region은 system RAM 또는 DAX로 소비할 수 있다.

다음: [[tech/infra/cxl-memory-fabric/04-learning/01-getting-started|시작하기]]에서 host와 Linux 상태를 확인한다.

## Sources

- https://docs.kernel.org/driver-api/cxl/devices/device-types.html
- https://docs.kernel.org/driver-api/cxl/linux/cxl-driver.html
- https://computeexpresslink.org/wp-content/uploads/2025/11/CXL_4.0-White-Paper_FINAL.pdf
