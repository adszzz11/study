---
date: 2026-11-17
tags: [tech]
type: tech-tool-study
status: draft
---

# CXL References

## Specification and consortium

1. [CXL Specification 4.0](https://computeexpresslink.org/cxl-specification/) — 공개 specification의 기준점.
2. [CXL 4.0 release announcement (2025-11-18)](https://computeexpresslink.org/wp-content/uploads/2025/11/CXL_4.0-Specification-Release_FINAL_Website-Copy.pdf) — 128 GT/s 발표 자료.
3. [CXL 4.0 architecture/RAS white paper](https://computeexpresslink.org/wp-content/uploads/2025/11/CXL_4.0-White-Paper_FINAL.pdf) — bundled port와 RAS의 개요.
4. [CXL 3.2 specification](https://computeexpresslink.org/wp-content/uploads/2024/11/CXL-Specification_rev3p2_ver1p0_2024October2_evalcopy.pdf) — fabric 세대 기능을 읽을 때의 기준.
5. [Tested integrators list](https://computeexpresslink.org/integrators-list/) — interoperability 확인의 출발점.

## Linux and tooling

1. [Linux CXL memory devices](https://www.kernel.org/doc/html/next/driver-api/cxl/memory-devices.html)
2. [Linux CXL driver operation](https://docs.kernel.org/driver-api/cxl/linux/cxl-driver.html)
3. [Linux CXL documentation project](https://cxl.docs.kernel.org/)
4. [`cxl create-region`](https://pmem.io/ndctl/cxl/cxl-create-region.html)
5. [QEMU CXL emulation](https://www.qemu.org/docs/master/system/devices/cxl.html)

## Platform and memory examples

- [Intel Xeon 6 product brief](https://www.intel.com/content/www/us/en/products/docs/xeon-6-product-brief.html)
- [SK hynix CMM-DDR5 CXL memory](https://product.skhynix.com/products/cmm/cmm.go)

이 노트의 실습 순서는 [[tech/infra/cxl-memory-fabric/04-learning/01-getting-started|시작하기]]와 [[tech/infra/cxl-memory-fabric/04-learning/02-deep-dive|Deep Dive]]에 정리했다.

## Sources

- https://computeexpresslink.org/cxl-specification/
- https://cxl.docs.kernel.org/
- https://www.qemu.org/docs/master/system/devices/cxl.html
