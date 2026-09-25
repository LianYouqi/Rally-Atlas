# Rally Atlas

*(formerly "Badminton Shot Statistics")*

A Python project analyzing shot-type distributions in elite singles badminton, using the human-annotated [ShuttleSet](https://arxiv.org/abs/2306.04948) dataset, and comparing them against personal gameplay data.

Rally Atlas currently covers **elite singles** matches. The longer-term goal is to train a machine learning model that can identify shot types automatically from video, which would remove the dependency on hand-annotated data and let the project expand beyond singles into **doubles and mixed doubles**.

Data is broken out by gender (male/female) and outcome (winner/loser), and can be compared directly against a personal `.csv` of your own match data.

## How the Raw Data Is Processed

Raw ShuttleSet match CSVs are turned into per-shot-type summary statistics through the following pipeline (`procressing.py`):

1. **Filter columns** — each raw match CSV is reduced to just the `player`, `type`, and `backhand` columns.
2. **Translate shot labels** — the `type` column's Chinese stroke labels are mapped to broader English shot categories using the `TRANSLATION` dictionary (see Methodology below).
3. **Normalize player and stroke fields** — `player` codes are mapped to `'Winner'`/`'Loser'`, and `backhand` is coerced to a boolean (missing values treated as `False`, i.e. forehand).
4. **Tally shot counts** — the cleaned rows are grouped by `(player, backhand)` and counted per shot type, producing four count dictionaries: winner-forehand, winner-backhand, loser-forehand, and loser-backhand.
5. **Aggregate across matches** — these counts are summed across every raw CSV in a gender's folder (`raw_data/male/` or `raw_data/female/`), so the result reflects the full set of matches rather than a single game.
6. **Compute summary statistics** — for each shot type, the pipeline derives:
   - `count` — total times the shot was played (forehand + backhand)
   - `overall frequency` — that shot's share of all shots played
   - `forehand ratio` / `backhand ratio` — the split between forehand and backhand for that shot
7. **Write output CSVs** — one summary CSV is written per gender/outcome pair (e.g. `processed_data/male_win.csv`, `processed_data/female_lose.csv`), indexed by shot type.

Personal match data is expected to be pre-processed into this same summary schema (see Data Setup below) so it can be compared directly against the elite summaries.

## Methodology: Why the Shot Categories Are Broad

ShuttleSet's raw annotations are quite granular — for example, it distinguishes `殺球` ("smash") from `點扣` ("wrist smash") as separate stroke labels, even though both are functionally the same shot for the purposes of this analysis.

In `procressing.py`, the active `TRANSLATION` dictionary deliberately **collapses these fine-grained labels into broader shot categories**. For example:

```python
'殺球': 'smash',
'點扣': 'smash',
```

A finer-grained version of the mapping (`TRANSLATION_VER_B`) is preserved as a comment in the same file, showing what a more granular label set would look like (e.g. `smash` vs. `wrist smash`, `push` vs. `rush`).

**Why broaden the categories now, rather than keep the original granularity?**

The eventual goal is to replace manual annotation with an ML model that identifies shot types on its own. Some of ShuttleSet's finer distinctions aren't really recoverable from a single shot in isolation — they depend on *sequence*, not just the stroke itself. For instance, telling a "return net shot" apart from a plain "net shot" requires knowing what the *previous* shot was, since the distinction is about context (returning an opponent's shot) rather than the mechanics of the shot itself. A model that only looks at one shot at a time (rather than a sequence with memory, e.g. an RNN/LSTM or another temporal architecture) can't make that distinction reliably.

So, for now, shot categories are broadened to the level that's identifiable from a single shot alone. This keeps the initial classification problem tractable for a first model, while the finer-grained mapping is kept on hand as a target for a later, sequence-aware version of the model that has the temporal context needed to recover those distinctions.

## Project Structure

| File | Purpose |
|---|---|
| `procressing.py` | Cleans raw ShuttleSet match CSVs, translates shot-type labels from Chinese to English (using the broadened `TRANSLATION` mapping described above), tallies forehand/backhand counts by winner/loser, and writes summary CSVs to `processed_data/`. |
| `load_files.py` | Loads a processed summary CSV (elite or personal) into a `DataFrame` indexed by shot type. |
| `analysis.py` | Computes cosine similarity between a personal sample and each elite sample across `overall frequency`, `forehand ratio`, and `backhand ratio`, then prints a comparison report. |
| `visualizations.py` | Generates horizontal bar charts (via an interactive CLI menu) for a single elite group, two groups compared, or personal vs. elite. |
| `upload.py` | Planned: an ML model to auto-identify shot types from uploaded match video and append the results to `processed_data/`. This is also the eventual gateway to supporting doubles and mixed doubles. Not yet implemented. |
| `CITATIONS.md` | Citation for the ShuttleSet dataset. |

## Requirements

- Python 3.10+ (uses `match` statements and `X | Y` type hints)
- `pandas`
- `numpy`
- `matplotlib`

```bash
pip install pandas numpy matplotlib
```

## Data Setup

1. **Raw data**: place ShuttleSet match CSVs (with `player`, `type`, and `backhand` columns) under:
   ```
   raw_data/male/*.csv
   raw_data/female/*.csv
   ```
2. **Personal data**: to compare your own gameplay, add a `personal.csv` to `processed_data/` matching the summary schema (indexed by `shot type`, with `count`, `forehand`, `backhand`, `overall frequency`, `forehand ratio`, `backhand ratio` columns) — the same schema the pipeline below produces.

## Usage

### 1. Process raw match data into summary CSVs

```bash
python procressing.py male
python procressing.py female
```

Or run with no argument to be prompted interactively. This writes files like `processed_data/male_win.csv` and `processed_data/male_lose.csv`.

### 2. Run the personal-vs-elite similarity analysis

```python
from analysis import summary
summary()
```

Prints a raw comparison table, a per-sample breakdown, and the closest elite match for each feature.

### 3. Generate visualizations

```bash
python visualizations.py
```

Walks you through choosing a statistic (count/frequency, forehand, or backhand), a sample group, and a view (single-group distribution, two-group comparison, or personal vs. elite).

## Roadmap

- [ ] Train an ML model to auto-identify shot types from video (`upload.py`), starting from the broad shot categories described above
- [ ] Once a model has temporal/sequence context, reintroduce finer-grained shot categories (see `TRANSLATION_VER_B`) where they depend on shot history
- [ ] Expand beyond singles to doubles and mixed doubles matches
- [ ] Resolve outstanding label mismatches in the shot-type translation table
- [ ] Formalize a `main.py` entry point tying the pipeline together

## Citation

See [`CITATIONS.md`](./CITATIONS.md) for the ShuttleSet dataset citation.