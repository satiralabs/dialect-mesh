# DialectMesh

> **Offline-First Edge Semantic Router & NLU Engine for Low-Resource Languages.**  
> *Deterministic intent matching and slot extraction for Amharic, Afaan Oromo, Kiswahili, and Somali without cloud latency or GPU overhead.*

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-green.svg)](https://www.python.org/downloads/)
[![Zero-Dependency](https://img.shields.io/badge/dependencies-zero-brightgreen.svg)]()
[![Edge Ready](https://img.shields.io/badge/latency-%3C1ms-brightgreen.svg)]()

---

## 🎯 Motivation

Most state-of-the-art LLMs struggle with low-resource African languages due to severe tokenization penalties, high inference latency, and lack of offline accessibility in remote agricultural or financial contexts. Furthermore, running frontier neural models on low-power rural edge devices (Raspberry Pi, mobile POS, offline kiosks) is prohibitively expensive.

**DialectMesh** brings deterministic, sub-millisecond natural language understanding directly to the edge. It combines:
1. **Fidäl & Qubee Orthographic Normalization**: Unifies homophones and diacritics.
2. **Sub-Word Character N-Gram Alignment**: Resilient against dialectal and phonemic spelling variations.
3. **Deterministic Slot Extraction**: Extracts numbers, currencies, and phone numbers natively.
4. **Structured Tool Dispatch**: Converts vernacular user intent into API payloads for banking, health, and agriculture.

---

## ⚡ Features

- **Pure Standard Library**: Zero dependencies; runs instantly on embedded hardware.
- **Latency < 1ms**: Average routing takes 0.003 seconds on basic low-power CPUs.
- **Multi-Lingual Support**: Out-of-the-box support for Amharic, Afaan Oromo, and Kiswahili.
- **Configurable Domain Packs**: Define custom domain intents and tool bindings using simple dictionaries or JSON schemas.

---

## 🚀 Quickstart

```bash
git clone https://github.com/abenih/dialect-mesh.git
cd dialect-mesh
./bin/dialect-mesh route "ለአቤል 500 ብር ላክለት"
```

Output:
```json
{
  "matched": true,
  "intent": "transfer_money",
  "confidence": 0.884,
  "tool_target": "banking.transfer_money",
  "slots": {
    "amount": 500
  }
}
```

---

## 📄 License
MIT License. Created by [Susan (Abenezer)](https://satiralabs.com) at SatiraLabs.
