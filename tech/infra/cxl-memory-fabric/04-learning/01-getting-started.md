---
date: 2026-11-17
tags: [tech]
type: tech-tool-study
status: draft
---

# CXL 시작하기: 지원 확인과 Linux 관찰

## 목표

실제 장비 또는 QEMU에서 CXL topology를 확인하고 `memdev`·`decoder`·`region`·NUMA node가 어떻게 연결되는지 읽는다. CXL device만 지원해도 충분하지 않다. CPU, motherboard BIOS/UEFI, PCIe slot wiring, memory module, Linux kernel configuration이 모두 맞아야 한다.

## 1. 개념을 먼저 분리한다

- **CXL version**은 protocol 세대이고, **Type 1/2/3**은 device capability 분류다.
- `CXL.io`는 관리/I/O 경로, `CXL.cache`는 device의 host-memory cache, `CXL.mem`은 host의 device memory 접근이다.
- 초기 실습의 핵심 대상은 보통 Type 3 memory expander다.

## 2. Host 지원 matrix 점검

| 확인 대상 | 확인할 내용 |
|---|---|
| CPU/platform | CXL 세대·device type 지원, root port 수 |
| BIOS/UEFI | CXL enablement, memory mode, firmware 버전 |
| Board/slot | 해당 slot의 CXL wiring과 bifurcation 제약 |
| Device | firmware, capacity, volatile/persistent capability |
| Linux | 충분히 최신 kernel, CXL driver와 userspace tool 설치 |

vendor 문서와 interoperability list를 함께 확인하고, production 도입 전에는 해당 조합으로 재현 시험한다.

## 3. Linux topology 관찰

```bash
# userspace CXL objects 확인
cxl list
cxl list -M       # memdev 중심 보기
cxl list -D       # decoder 중심 보기

# kernel이 노출한 device 확인
find /sys/bus/cxl/devices -maxdepth 1 -mindepth 1 -printf '%f\n'

# CXL region이 NUMA memory로 online된 경우 node 관찰
numactl -H
```

출력에서 다음 연결을 추적한다.

```text
memdev(s) → decoder → region → system RAM NUMA node 또는 dax_region
```

`cxl list`에 object가 보이지 않으면 먼저 BIOS/UEFI 설정, kernel boot log, module과 hardware compatibility를 조사한다. 임의로 system RAM에 online하기 전에 data path와 운영 절차를 정한다.

## 4. 완료 기준

- [ ] host와 device의 지원 조합을 문서로 남겼다.
- [ ] 최소 하나의 `memdev`와 연결된 decoder를 식별했다.
- [ ] region이 system RAM인지 DAX인지, 그리고 해당 NUMA node를 확인했다.
- [ ] local DDR 대비 latency/bandwidth 측정 계획을 만들었다.

다음: [[tech/infra/cxl-memory-fabric/04-learning/02-deep-dive|Deep Dive]]에서 region과 memory tiering을 설계한다.

## Sources

- https://docs.kernel.org/driver-api/cxl/linux/cxl-driver.html
- https://www.kernel.org/doc/html/next/driver-api/cxl/memory-devices.html
- https://cxl.docs.kernel.org/
