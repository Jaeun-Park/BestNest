# BestNest — City Recommendation Web App

**BestNest** is an interactive app that helps users find their ideal U.S. city based on personalized priorities. Users select what matters most — like air quality, literacy, crime cost, and cost of living — and receive a ranked list of cities with insightful visualizations.

**Live Demo**: [https://bestnest.streamlit.app/](https://bestnest.streamlit.app/)

---

## Key Features

* **Personalized City Recommendations**
  Generates rankings tailored to selected criteria

* **Interactive UI**
  Dropdown interface for selecting key factors in real-time

* **Visual Insights**

  * Top 10 Cities Table
  * Heatmap showing city-by-criteria performance

* **Lightweight Deployment**
  Built with Streamlit and Python for seamless use and modularity

---

## Sample Output

**2 Parameters Selected**
![2 Parameters](screenshots/2%20parameters.png)

**3 Parameters Selected**
![3 Parameters](screenshots/3%20parameters.png)

**4 Parameters Selected**
![4 Parameters](screenshots/4%20parameters.png)

---

## How It Works

1. User selects preferred features (e.g., crime cost, literacy rate)
2. The app scores and ranks cities based on weighted inputs
3. Results include ranking table and heatmap visualizations

---

## Tech Stack

* **Python** — data processing and backend logic
* **Streamlit** — UI and deployment
* **Seaborn / Matplotlib** — visualizations
* **Pandas / NumPy** — data handling

---

## File Structure

```
BestNest/
├── BestNest.py           # Main Streamlit app
├── Merge_dataset.py      # Data preprocessing script
├── requirements.txt      # Python dependencies
└── screenshots/          # Demo screenshots
```

---

## Run Locally

```bash
pip install -r requirements.txt
streamlit run BestNest.py
```

---

## Contact

Created by **Jaeun Park**
[LinkedIn](https://www.linkedin.com/in/jaeun-park/) · [GitHub](https://github.com/Jaeun-Park)
