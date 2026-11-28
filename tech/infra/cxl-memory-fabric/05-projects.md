---
date: 2026-11-17
tags: [tech]
type: tech-tool-study
status: draft
---

# CXL Projects

## Project 1: Platform compatibility inventory

목표는 구매나 배포 전에 end-to-end 지원 여부를 증명하는 것이다.

- CPU, BIOS/UEFI, board slot wiring, device firmware, kernel, `cxl-cli` version을 표로 기록한다.
- `cxl list`, `/sys/bus/cxl/devices`, `numactl -H` snapshot을 보관한다.
- known-good configuration과 firmware update/rollback 절차를 적는다.

**완료 기준**: Type 3 device가 `memdev`부터 region 또는 NUMA node까지 추적되고, 지원되지 않는 조합도 명확히 분류했다.

## Project 2: Two-device interleaved region benchmark

두 Type 3 memdev(또는 QEMU topology)로 interleaved region 설계를 문서화한다.

1. decoder capability와 interleave way/granularity를 확인한다.
2. system RAM mode와 DAX mode 중 하나씩 실험 계획을 만든다.
3. local DDR, single CXL device, interleaved CXL region을 같은 workload로 비교한다.
4. median뿐 아니라 P99 latency, bandwidth, CPU cost, memory pressure를 기록한다.

**완료 기준**: 어떤 working set과 access pattern에서 CXL tier가 유효한지, 어떤 경우 DDR이 필요한지 결론을 낸다.

## Project 3: Tiering runbook and failure drill

- hot/cold data placement 원칙과 NUMA policy를 정한다.
- CXL capacity가 사라지거나 media error가 발생할 때의 detect→isolate→recover 절차를 작성한다.
- VM consolidation 또는 in-memory database 중 한 workload에서 capacity benefit와 tail-latency cost를 측정한다.

**완료 기준**: telemetry dashboard, alert, owner, rollback 또는 workload evacuation 절차가 있다.

기초 명령은 [[tech/infra/cxl-memory-fabric/cheatsheet|Cheatsheet]], 설계 근거는 [[tech/infra/cxl-memory-fabric/03-references|References]]에서 확인한다.

## Sources

- https://cxl.docs.kernel.org/
- https://pmem.io/ndctl/cxl/cxl-create-region.html
- https://www.qemu.org/docs/master/system/devices/cxl.html
