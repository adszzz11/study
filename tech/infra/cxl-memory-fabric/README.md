---
date: 2026-11-17
tags: [tech]
type: tech-tool-study
status: draft
---

# CXL (Compute Express Link) — Coherent Memory Expansion & Fabric

> **한 줄 정의**: CXL은 PCIe 물리 계층 위에서 CPU·메모리·가속기 사이의 cache coherence를 제공해 memory expansion, pooling, accelerator 연결을 가능하게 하는 개방형 interconnect 표준이다.

## Overview

AI inference, in-memory database, VM consolidation, HPC는 CPU에 직접 연결한 DDR의 slot·channel·비용 한계에 자주 닿는다. CXL은 device-attached memory를 CPU가 memory semantics로 다루게 하고, 일부 accelerator가 host memory를 coherent cache로 접근하게 한다.

- 현재의 현실적인 출발점은 **Type 3 memory expander**를 capacity tier로 쓰는 일이다.
- CXL-attached memory는 local DDR보다 latency가 높거나 bandwidth가 낮을 수 있다. hot working set의 DDR 대체가 아니라 colder page와 capacity 확장을 위한 tier로 설계한다.
- CXL version과 device type은 별개다. 2025년 11월 공개된 CXL 4.0은 128 GT/s를 제시하지만, 2025–2026 배포의 중심은 여전히 CXL 2.0 Type 3이다.

## Learning Path

- [ ] [[tech/infra/cxl-memory-fabric/01-overview|Overview]] — protocol, device type, topology의 공통 언어 익히기
- [ ] [[tech/infra/cxl-memory-fabric/02-ecosystem|Ecosystem]] — DDR, PCIe DMA, NVMe, proprietary fabric과 비교하기
- [ ] [[tech/infra/cxl-memory-fabric/04-learning/01-getting-started|시작하기]] — host 지원 여부와 Linux 관찰 경로 확인하기
- [ ] [[tech/infra/cxl-memory-fabric/04-learning/02-deep-dive|Deep Dive]] — region, interleave, tiering 및 emulation 다루기
- [ ] [[tech/infra/cxl-memory-fabric/05-projects|Projects]] — 검증·실험 과제 수행하기
- [ ] [[tech/infra/cxl-memory-fabric/03-references|References]] — specification과 kernel 문서의 기준점 찾기
- [ ] [[tech/infra/cxl-memory-fabric/cheatsheet|Cheatsheet]] — 용어·명령·설계 판단 빠르게 참조하기

## When To Use

- DDR 슬롯만으로 부족한 memory capacity를 Type 3 expander로 보완할 때
- page temperature를 구분할 수 있고, local DDR와 CXL memory의 tiering 정책을 운영할 수 있을 때
- CXL 지원 CPU, firmware/BIOS, slot wiring, Linux kernel을 함께 검증할 수 있을 때
- 장기적으로 pooled/disaggregated memory 또는 heterogeneous accelerator memory를 평가할 때

## When Not To Use

- 최저 latency와 예측 가능한 bandwidth가 절대적인 hot working set만 처리할 때
- host platform의 CXL 지원 여부를 확인하지 않은 채 device만 추가하려 할 때
- NVMe/swap 수준의 비용 효율만 필요하거나, software tiering·NUMA 정책을 운영할 여력이 없을 때
- vendor 전용 GPU fabric의 최고 bandwidth만이 목표인 GPU-domain 작업일 때

## Related Notes

- [[MOCs/Index]]
- [[MOCs/Infra]]
- [[tech/infra/kubernetes/README|Kubernetes]]

## Sources

- https://computeexpresslink.org/cxl-specification/
- https://docs.kernel.org/driver-api/cxl/linux/cxl-driver.html
- https://www.kernel.org/doc/html/next/driver-api/cxl/memory-devices.html
- https://www.intel.com/content/www/us/en/products/docs/xeon-6-product-brief.html
