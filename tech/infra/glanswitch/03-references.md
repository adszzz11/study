---
date: 2026-10-29
tags: [tech]
type: tech-tool-study
status: draft
---

# Glanswitch References

## 용어 해석

- [GLANSwitch 조달 문서 용례](https://smlouvy.gov.cz/smlouva/soubor/11721259/SOD.PDF) — 독립 제품으로 단정하지 않고 GLAN switch 문맥으로 해석한 출발점.

## Switching, VLAN, L3 경계

- [NETGEAR — Why unmanaged switches have no firmware changes](https://kb.netgear.com/1135/Why-unmanaged-switches-have-no-firmware-changes) — unmanaged switch의 기본 동작 설명.
- [Juniper — Bridging and VLANs](https://www.juniper.net/documentation/us/en/software/junos/multicast-l2/topics/topic-map/bridging-and-vlans.html) — VLAN과 bridging 개념.
- [Juniper — Ethernet switching interfaces and IRB](https://www.juniper.net/documentation/us/en/software/junos/interfaces-fundamentals/interfaces-ethernet-switches/topics/topic-map/switches-interface-understanding.html) — IRB/L3 interface의 역할.

## PoE

- [Cisco — PoE Configuration Guide](https://www.cisco.com/c/en/us/td/docs/switches/lan/c9000/infra/poe/poe-configuration-guide/g-poe/c-poe.html) — PoE class, power negotiation, configuration 참고.
- [Cisco — What is Power over Ethernet?](https://www.cisco.com/site/us/en/learn/topics/networking/what-is-power-over-ethernet.html) — PoE 개요와 적용 사례.

## 제품 ecosystem과 운영

- [Juniper — EX Series switches](https://www.juniper.net/us/en/products/switches/ex-series.html)
- [Ubiquiti — UniFi Switch Settings](https://help.ui.com/hc/en-us/articles/33402927617047-UniFi-Switch-Settings)
- [TP-Link — Managed switches](https://www.tp-link.com/us/business-networking/omada/switch/managed/)

> [!note]
> Vendor UI와 CLI의 세부 명령은 모델·firmware에 따라 달라진다. 이 노트의 절차는 개념 검증용이며 production 변경은 해당 모델의 release-matched manual로 재확인한다.
