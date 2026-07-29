# Badminton Shot Statistics

A personal data analysis project that processes and analyzes shot distribution data from top professional singles badminton athletes, with the goal of enabling comparison against amateur players.

> **Note:** This project is actively in development. Planned features include doubles and mixed doubles analysis, personal match recording tools, and machine learning-based shot detection.

---

## What This Does

Using the [ShuttleSet dataset](https://github.com/wywyWang/CoachAI-Projects/tree/main/ShuttleSet) — a human-annotated stroke-level singles dataset from KDD 2023 — this project:

- Processes raw match CSV files across male and female professional singles players
- Translates shot type labels from Chinese to English
- Aggregates forehand and backhand shot counts across all matches
- Outputs a clean summary CSV with shot frequencies and usage percentages

---

## Project Structure

```
badminton-shot-statistics/
├── processed_data/
│   └── processed/                  # Generated output files
├── raw_data/                       # ShuttleSet CSV files (not included — see Data Setup)
│   ├── male/
│   └── female/
├── src/
│   ├── __init__.py
│   ├── data.py                     # Data loading functions
│   ├── metrics.py                  # Shot distribution metrics
│   └── visualize.py                # Matplotlib visualizations
├── outputs/
│   └── figures/                    # Generated plots
├── notebooks/
│   └── exploration.ipynb           # Scratch work and experimentation
├── processing.py                   # Main processing pipeline
├── requirements.txt
└── README.md
```

---

## Data Source

This project uses **ShuttleSet** — a human-annotated stroke-level singles dataset for badminton tactical analysis.

> Wang, Wei-Yao, Yung-Chang Huang, Tsi-Ui Ik, and Wen-Chih Peng.
> "ShuttleSet: A Human-Annotated Stroke-Level Singles Dataset for Badminton Tactical Analysis."
> *KDD 2023.* https://doi.org/10.1145/3580305.3599906

The raw data is **not included** in this repository. To obtain it, submit a request through the [CoachAI Projects GitHub](https://github.com/wywyWang/CoachAI-Projects/tree/main/ShuttleSet).

---

## Setup

**Requirements:**
- Python 3.14.6
- pip

**1. Clone the repository:**
```bash
git clone https://github.com/<your-username>/badminton-shot-statistics.git
cd badminton-shot-statistics
```

**2. Install dependencies:**
```bash
pip install -r requirements.txt
```

**3. Add the ShuttleSet data:**

Once you have access to ShuttleSet, place the match CSV files in the following structure:
```
raw_data/
├── male/
│   ├── Player_A_vs_Player_B/
│   │   └── match.csv
│   └── ...
└── female/
    ├── Player_C_vs_Player_D/
    │   └── match.csv
    └── ...
```

---

## Usage

Run the processing pipeline and follow the prompt:

```bash
python processing.py
```

You will be asked to select a gender group:

```
Which dataset group of professional singles badminton player would you like to process?
For 'Professional male athletes', type 'male'
For 'Professional female athletes', type 'female'
:
```

**Output files generated:**

| File | Description |
|------|-------------|
| `Badminton Shot Distribution (Male).csv` | Shot statistics for male professional players |
| `Badminton Shot Distribution (Female).csv` | Shot statistics for female professional players |

Each output file contains the following columns:

| Column | Description |
|--------|-------------|
| `shot type` | English shot type label |
| `count` | Total occurrences across all matches |
| `(%) of all shots` | Proportion of total shots |
| `FH (count)` | Forehand count |
| `FH usage (%)` | Forehand proportion within shot type |
| `BH (count)` | Backhand count |
| `BH usage (%)` | Backhand proportion within shot type |

---

## Shot Types

The following 19 shot types are recognized:

| English | Chinese |
|---------|---------|
| Net shot | 放小球 |
| Return net | 擋小球 |
| Smash | 殺球 |
| Wrist smash | 點扣 |
| Lift | 挑球 |
| Defensive return lift | 防守回挑 |
| Clear | 長球 |
| Drive | 平球 |
| Driven flight | 小平球 |
| Back-court drive | 後場抽平球 |
| Drop | 切球 |
| Passive drop | 過度切球 |
| Push | 推球 |
| Rush | 撲球 |
| Defensive return drive | 防守回抽 |
| Cross-court net shot | 勾球 |
| Short service | 發短球 |
| Long service | 發長球 |
| Unnamed shot | 未知球種 |

---

## Roadmap

- [x] Phase 1 — Data processing pipeline for male and female professional singles
- [ ] Phase 2 — Matplotlib visualizations of shot distributions
- [ ] Phase 3 — Personal match recording and comparison against professionals
- [ ] Phase 4 — Doubles and mixed doubles support
- [ ] Phase 5 — Machine learning-based automatic shot detection from video

---

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---

## Acknowledgements

ShuttleSet dataset provided by the Advanced Database System Laboratory, National Yang Ming Chiao Tung University, supervised by Prof. Wen-Chih Peng.