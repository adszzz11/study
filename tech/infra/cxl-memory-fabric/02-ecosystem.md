---
date: 2026-11-17
tags: [tech]
type: tech-tool-study
status: draft
---

# CXL Ecosystem and Alternatives

## 비교

| 기술/방식 | Coherence | 주 역할 | 강점 | 제약/적합하지 않은 경우 |
|---|---:|---|---|---|
| CXL Type 3 | CPU–device memory | expansion, pooling, tiering | 표준 기반 capacity 확장 | local DDR보다 latency/bandwidth 불리, host·BIOS·OS 지원 필요 |
| CXL Type 2 | host–accelerator | accelerator memory 공유 | copy 감소, heterogeneous compute | production software 지원 범위가 진행 중 |
| DDR5/MRDIMM | CPU direct-attached | hot memory | 최저 latency, 예측 가능한 성능 | slot/channel/socket 용량 한계 |
| PCIe + DMA | 일반 I/O·accelerator | block/buffer transfer | 성숙한 toolchain과 호환성 | shared coherent memory가 아니며 copy 부담 |
| NVMe SSD / swap | 없음 | storage tier | 저비용 대용량 | CXL DRAM보다도 훨씬 높은 latency |
| NVIDIA NVLink/NVSwitch 등 | 주로 GPU domain | GPU-scale AI/HPC | vendor stack에서 높은 bandwidth | vendor 종속, 범용 CPU expansion 표준이 아님 |

## 생태계의 층

- **Host platform**: Intel Xeon 6, AMD EPYC 계열과 motherboard·BIOS/UEFI·slot wiring이 함께 기능을 결정한다.
- **Memory**: Samsung, Micron, SK hynix 등은 CXL memory module을 제공한다.
- **Connectivity**: Marvell, Astera Labs, Montage 등은 controller, switch, retimer 또는 IP를 제공한다.
- **Software**: Linux kernel CXL subsystem, `ndctl/cxl-cli`, QEMU가 관찰·region 구성·emulation을 담당한다.

## 도입 판단

1. workload의 resident set과 hot/cold page 분포를 먼저 측정한다.
2. local DDR 증설, CXL capacity tier, NVMe tier 중 어느 계층이 목표 latency를 만족하는지 비교한다.
3. CPU·firmware·kernel·device의 지원 matrix와 RAS/telemetry 경로를 검증한다.
4. system RAM mode와 DAX mode를 각각 평가해 운영 모델을 결정한다.

상세 설계는 [[tech/infra/cxl-memory-fabric/04-learning/02-deep-dive|Deep Dive]]를, 1차 요약은 [[tech/infra/cxl-memory-fabric/cheatsheet|Cheatsheet]]를 참고한다.

## Sources

- https://www.intel.com/content/www/us/en/products/docs/xeon-6-product-brief.html
- https://computeexpresslink.org/integrators-list/
- https://product.skhynix.com/products/cmm/cmm.go
