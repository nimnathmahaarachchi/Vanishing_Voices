# 🗺️ Vanishing Voices

An immersive, educational wildlife conservation atlas built to let users discover endangered animal species through interactive maps, data visualization, and automated population auditing pipelines.

---

## 🛠️ Tech Stack & Architecture

A zero-framework, dependency-free application running entirely on native Python and standard browser technologies:

| Technology | Badge | Purpose |
| :--- | :--- | :--- |
| **Python** | ![Python](https://shields.io) | Powers the lightweight HTTP routing server, standard data validation, and remote API testing. |
| **JavaScript** | ![JavaScript](https://shields.io) | Manages searching, media galleries, map canvas events, and backend network operations. |
| **JSON** | ![JSON](https://shields.io) | Lightweight structured files used to bridge data states seamlessly into browser sessions. |
| **Vector & WebP** | ![SVG](https://shields.io) ![WebP](https://shields.io) | High-fidelity maps, scaling icons, and compressed high-performance asset photos. |
| **Web Basics** | ![HTML5](https://shields.io) ![CSS3](https://shields.io) | Structured layout architecture, fluid media sizing, and reduced-motion safe configurations. |

---

## ✨ Features

* **Targeted Profiles:** Deep data sets covering 10 distinct species: Tiger, Amur leopard, Asian elephant, Black rhinoceros, Mountain gorilla, Sumatran orangutan, Hawksbill turtle, Blue whale, Vaquita, and Kākāpō.
* **Interactive SVG Canvas:** Advanced geographic vector map supporting custom zoom events, dragging, and real-time species hotspots.
* **Advanced Query Controls:** Text indexing, regional territory sorting filters, and flexible order arrangements.
* **Rich Field Guides:** Comprehensive info cards covering habitat metrics, active survival threats, and current conservation rules.
* **Media Portfolios:** 3 fully high-definition photographs per creature, complete with detailed license and creator attribution metadata.
* **Audited Metrics:** Population markers paired explicitly with timeline records, measurement units, and citation links.
* **Automated Scraper API:** Built-in Python validation tools that hit external sources to double-check species statistics.

---

## 🚀 Getting Started

### Prerequisites
* **Python 3.9** or later

### Run Environment
1. Fire up a terminal instance inside the main project directory.
2. Launch the self-contained HTTP web server:

## 📂 Project Architecture
---
├── animals/
│   ├── animal_information.py      # Core data script tracking base animal metrics
│   ├── photograph_information.py  # Image license paths, alt tags, and credits
│   └── [species_folders]/         # Deep profile modules for the 10 monitored species
├── maps/                          # Scalable World and localized vector files
├── images/                        # 30 footprint-optimized WebP asset files
├── website-layout/                # Hub pages, style matrices, and main UI logic
├── website_server.py              # Custom operational server mapping the /api/populations path
├── check_animal_populations.py    # Remote check utility scraping population statistics
└── check_project_files.py         # Automated internal regression test pipeline

---

## 🧪 Testing & Data Verification

### Running Regression Checks
Run the full test suite covering population parsing logic, integrity loops, and file mapping setups:
```bash
python check_project_files.py
```
*(Note: Live external connections are automatically mocked inside the test engine for isolated reliability.)*

### Refreshing Population Metrics
Manually audit a specific animal species entry against live online records:
```bash
python check_animal_populations.py --species kakapo --refresh
```

