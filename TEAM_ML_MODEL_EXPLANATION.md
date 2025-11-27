# NBA Finals Team ML Model - Code Explanation

## Overview
This notebook builds a **Random Forest Regression model** to predict NBA Finals game outcomes (Nuggets vs Heat) based on team performance metrics from the 2022-23 season. It trains on historical data and predicts win probabilities for Games 3, 4, and 5.

---

## Code Workflow

### 1. **Imports & Data Loading**
```python
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
```

**What it does:**
- Imports necessary libraries for data manipulation (pandas), visualization (matplotlib), and machine learning (scikit-learn)
- Loads the 2022-23 NBA season team metrics from CSV: `NBA Stats 202223 Team Metrics Away-Home-Last 5 Splits.csv`

**Key Variables:**
- `df`: DataFrame containing 8 features selected from the baseline data
- `selected_features`: List of metrics used:
  - `GP`: Games Played
  - `PPG`: Points Per Game (team scored)
  - `oPPG`: Opponent Points Per Game
  - `pDIFF`: Point Differential per game
  - `W`: Wins
  - `L`: Losses
  - `WIN%`: Win percentage
  - `eWIN%`: Expected Win Percentage (target variable)

---

### 2. **Helper Functions**

#### `prepare_team_data(csv_path, selected_features)`
**Purpose:** Transforms raw game stats into model-ready features

**Process:**
1. Reads game statistics from CSV (Win/Loss columns and Points)
2. Calculates Games Played (`GP = Wins + Losses`)
3. Extracts Points Per Game (`PPG`)
4. Gets opponent points using `iloc[::-1]` (reverses row order to get opponent)
5. Calculates Point Differential per game
6. Returns a formatted DataFrame with all 7 features (excluding the target)

**Example:** If Game 1&2 data shows Nuggets: 110 PPG and Heat: 105 PPG, it calculates `pDIFF = (110-105)/2 = 2.5`

#### `predict_game(model, team_data, team_names=['Nuggets', 'Heat'], game_name="")`
**Purpose:** Makes predictions and normalizes probabilities

**Process:**
1. Runs the trained model on team data to get raw predictions
2. Normalizes predictions to sum to 100% (converts raw scores to win probabilities)
3. Prints formatted probability output (e.g., "Nuggets: 55.23%, Heat: 44.77%")
4. Returns results as a dictionary

**Why normalize?** Raw model outputs may not sum to 100%, so normalization ensures valid probabilities.

---

### 3. **Model Training**

```python
X = df.drop(columns='eWIN%')  # Features
y = df["eWIN%"] * 100         # Target (scaled to 0-100)
```

**Data Preparation:**
- `X`: 7 input features (GP, PPG, oPPG, pDIFF, W, L, WIN%)
- `y`: Expected win percentage (scaled to 0-100 range for easier interpretation)

```python
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
```

**Train/Test Split:**
- 80% of data used for training (~25 teams)
- 20% reserved for testing (~6 teams)
- `random_state=42` ensures reproducibility

```python
model = RandomForestRegressor(n_estimators=400, random_state=42)
model.fit(X_train, y_train)
```

**Model Configuration:**
- **Algorithm:** Random Forest Regressor (ensemble of 400 decision trees)
- **Why Random Forest?** Handles non-linear relationships well, robust to outliers, provides good generalization

**Model Evaluation:**
```python
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
```

- **MSE (Mean Squared Error):** Measures prediction error magnitude (lower is better)
- **R² Score:** Explains variance in predictions (1.0 = perfect, 0.0 = random guessing)

---

### 4. **Game Predictions**

```python
games = {
    'Game 3': 'CSV/NBA Finals Team Stats_Current (games 1&2).csv',
    'Game 4': 'CSV/NBA Finals Team Stats_Current (games 1,2 &3).csv',
    'Game 5': 'CSV/NBA Finals Team Stats_Current (games 1-4).csv'
}
```

**Process:**
1. Loops through each game's CSV file
2. Prepares team data using `prepare_team_data()`
3. Makes prediction using the trained model
4. Normalizes and prints win probabilities
5. Stores results in `all_predictions` dictionary

**Example Output:**
```
Probability of Nuggets Winning Game 3: 58.45%
Probability of Heat Winning Game 3: 41.55%
```

---

### 5. **Visualization**

```python
fig, axes = plt.subplots(1, 3, figsize=(15, 4))
```

**Creates:** 3 side-by-side pie charts (one per game)

**For Each Game:**
1. Extracts win probabilities from `all_predictions`
2. Creates pie chart showing Nuggets vs Heat split
3. Displays percentage labels
4. Sets game name as title

**Output:** Visual comparison of model confidence across all three games

---

## Key Improvements Made

### Before (Original Code):
- ❌ Repeated data loading 3 times
- ❌ Trained model 3 separate times
- ❌ 80+ lines of duplicated code
- ❌ Inconsistent output formatting

### After (Refactored):
- ✅ Single model training pass
- ✅ Reusable `prepare_team_data()` and `predict_game()` functions
- ✅ Reduced to ~50 lines of clean code
- ✅ Consistent probability normalization
- ✅ Better evaluation metrics (added R² score)
- ✅ Unified visualization

---

## Model Assumptions & Limitations

1. **Stationarity:** Assumes 2022-23 season metrics are representative of Finals performance
2. **Limited Data:** Training on ~30 teams; small dataset for ML standards
3. **No Recent Form:** Doesn't account for changes in team composition or momentum
4. **Opponent Reversal:** Uses `iloc[::-1]` to get opponent data—assumes teams are in consistent row order
5. **Feature Selection:** Only uses basic box score stats; advanced metrics (pace, efficiency, etc.) not included

---

## How to Extend This Model

- **Add features:** Three-point percentage, defensive efficiency, bench scoring
- **Temporal weighting:** Weight recent games more heavily than early season
- **Feature engineering:** Streak indicators, rest days, player injuries
- **Cross-validation:** Use k-fold CV instead of simple train/test split
- **Hyperparameter tuning:** Optimize `n_estimators`, `max_depth`, `min_samples_leaf`
- **Ensemble methods:** Combine Random Forest with other models (XGBoost, Neural Networks)

---

## Running the Notebook

1. **Cell 1:** Imports and loads baseline season data
2. **Cell 2:** Defines helper functions
3. **Cell 3:** Trains the model on historical data
4. **Cell 4:** Makes predictions for all three games
5. **Cell 5:** Displays pie charts

**Expected Runtime:** < 5 seconds

**Requirements:**
- `pandas`, `scikit-learn`, `matplotlib`, `hvplot` installed
- CSV files in `CSV/` subdirectory
