# emotion_NASDAQ

Predict next-month NASDAQ Composite (NASDAQCOM) prices from monthly news-sentiment
scores derived from *The Guardian* articles. Article body text is scored with
FinBERT (`ProsusAI/finbert`), aggregated per article and per month, then merged
with NASDAQ price data and fed to Ridge, Lasso and ARIMAX models with
walk-forward validation.

## Pipeline

```
Guardian API           NASDAQ FRED CSV
     │                       │
     ▼                       ▼
fetch metadata          find first trade
(test.py)               day of each month
     │                       │
     ▼                       │
export bodyText              │
(export_bodytext.py)         │
     │                       │
     ▼                       │
split sentences              │
(split_sentences.py)         │
     │                       │
     ▼                       │
FinBERT sentiment            │
(test_FinBERT.py)            │
     │                       │
     ▼                       │
per-article weighted score   │
(calculate_emotion_each_article_score.py)
     │                       │
     ▼                       │
per-month weighted score     │
(calculate_each_month_score.py)
     │                       │
     └──────► merge ◄────────┘
              (make_L_data.py)
                   │
                   ▼
        Ridge / Lasso / ARIMAX
        with walk-forward validation
        (L1_L2_model.py, walk_forward_validation.py,
         arimax_model.py)
```

## Repository layout

```
emotion_NASDAQ/
├── emotion_dataset/                # Loughran–McDonald positive/negative word list
│   ├── emotion.json
│   └── emotion_dataset_process.py  # builds emotion.json from the L-M master CSV
│
├── the_guardian_test/              # Guardian-side text & sentiment pipeline
│   ├── test.py                                    # query Guardian API for one month
│   ├── export_bodytext.py                         # JSON -> per-article .txt
│   ├── split_sentences.py                         # .txt -> *_sentences.json
│   ├── calculate_emotion_each_article_score.py    # FinBERT rows -> per-article weighted score
│   ├── calculate_each_month_score.py              # per-article -> per-month weighted score
│   ├── guardian_metadata.json                     # cached Guardian metadata
│   ├── emotion_tendency.csv                       # FinBERT per-sentence output
│   ├── each_article_score.csv                     # weighted score per article
│   └── each_month_score.csv                       # weighted score per month
│
├── nasdaq_data/                    # NASDAQ price data
│   ├── NASDAQCOM.csv                              # daily NASDAQ composite (from FRED)
│   ├── find_first_trade_day_of_month.py           # reduces daily -> first trade day / month
│   └── first_trade_day_of_month.csv
│
├── math_prediction/                # Modelling
│   ├── make_L_data.py                             # merges sentiment + NASDAQ, builds target
│   ├── merged_monthly_data.csv
│   ├── L1_L2_model.py                             # 70/30 Ridge & Lasso
│   ├── walk_forward_validation.py                 # walk-forward Ridge & Lasso
│   ├── arimax_model.py                            # walk-forward ARIMAX(1,0,0)
│   ├── ridge_lasso_70_30_predictions.csv
│   ├── ridge_lasso_80_20_predictions.csv
│   ├── ridge_walk_forward_predictions.csv
│   ├── lasso_walk_forward_predictions.csv
│   └── arimax_walk_forward_predictions.csv
│
├── test_FinBERT.py                 # batch FinBERT scoring over *_sentences.json
├── requirements.txt
└── .gitignore
```

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
# extras used by the scripts but not pinned in requirements.txt:
pip install transformers torch nltk scikit-learn statsmodels
```

NLTK punkt tokenizers are downloaded automatically the first time
`split_sentences.py` runs.

## Running the pipeline

1. **Fetch Guardian articles** — set your `API_KEY` and target month in
   `the_guardian_test/test.py`, then run it to write
   `guardian_metadata_output/<YYYY-MM>.json`.
2. **Extract body text**
   `python3 the_guardian_test/export_bodytext.py guardian_metadata_output/2024-01.json`
   → writes `count_emotion_index/2024-01-<n>.txt`.
3. **Split sentences**
   `python3 the_guardian_test/split_sentences.py`
   → writes `*_sentences.json` next to each `.txt`.
4. **Score with FinBERT**
   `python3 test_FinBERT.py`
   → writes `the_guardian_test/emotion_tendency.csv`
   (one row per sentence: `year, source, line, tendency, score, sentence`).
5. **Aggregate to articles**
   `python3 the_guardian_test/calculate_emotion_each_article_score.py`
   → `each_article_score.csv` (`weighted_score = signed_total / sentence_count`).
6. **Aggregate to months**
   `python3 the_guardian_test/calculate_each_month_score.py`
   → `each_month_score.csv`.
7. **Reduce NASDAQ to monthly**
   `python3 nasdaq_data/find_first_trade_day_of_month.py`
   → `first_trade_day_of_month.csv`.
8. **Merge & build target**
   `python3 math_prediction/make_L_data.py`
   → `merged_monthly_data.csv` with `target_next_month_price = NASDAQCOM.shift(-1)`.
9. **Train / evaluate**
   - `python3 math_prediction/L1_L2_model.py` — 70/30 time-ordered split Ridge & Lasso.
   - `python3 math_prediction/walk_forward_validation.py` — walk-forward Ridge & Lasso (initial train = 12 months).
   - `python3 math_prediction/arimax_model.py` — walk-forward ARIMAX(1,0,0) with sentiment as exogenous regressor.

Each modelling script prints MAE / RMSE / R² and writes a predictions CSV.

## Data sources

- **News:** *The Guardian* Content API
  (`https://content.guardianapis.com/search`, query `q=NASDAQ`).
- **Prices:** NASDAQ Composite Index daily series from FRED
  (`NASDAQCOM.csv`).
- **Sentiment lexicon (optional):** Loughran–McDonald Master Dictionary
  (the cleaned CSV is git-ignored; see `emotion_dataset/emotion_dataset_process.py`).

## Notes

- Several scripts use hard-coded absolute paths like
  `~/final_project/...` or `/home/kayla/final_project/...`. Adjust them
  to your local checkout before running.
- `guardian_metadata_output/` and `news_article_process/` are git-ignored
  intermediate folders.
- The Guardian API key in `the_guardian_test/test.py` is a placeholder —
  replace it with your own key.
