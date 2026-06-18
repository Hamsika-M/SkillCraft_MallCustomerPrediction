# 🛍️ Customer Segmentation Using K-Means Clustering
## SkillCraft Technology Internship — Task 02
## 📌 Task Description
This project implements a K-Means Clustering algorithm
to group customers of a retail store based on their
annual income and spending score. The goal is to help
the mall understand their customers better and create
targeted marketing strategies for each customer group.

## 🎯 Objective
- Analyze customer purchase behavior
- Group similar customers into segments
- Find the optimal number of clusters
- Provide business insights for each segment
- Build an interactive web application

## 📊 Dataset Information
- **Source:** Kaggle Mall Customer Segmentation Dataset
- **Created by:** Vijay Choudhary
- **Size:** 200 customers (rows)
- **Features:** 5 columns

### Dataset Columns:
| Column | Description | Type |
|--------|-------------|------|
| CustomerID | Unique customer ID | Integer |
| Genre | Gender of customer | String |
| Age | Age of customer | Integer |
| Annual Income (k₹) | Yearly income in thousands | Integer |
| Spending Score (1-100) | Mall assigned score | Integer |

### What is Spending Score?
Spending Score is a value between 1 and 100
assigned by the mall to each customer based on:
- How frequently they visit the mall
- How much money they spend per visit
- Their overall purchase behavior and loyalty
- Score 1 means very low spender
- Score 100 means very high spender

## 🤖 Algorithm — K-Means Clustering

### What is K-Means?
K-Means is an unsupervised machine learning
algorithm that groups similar data points together
automatically without any predefined labels.

### How K-Means Works:
1. Choose number of clusters K
2. Place K random centroids on graph
3. Each customer joins nearest centroid
4. Move centroid to center of its group
5. Repeat until clusters are stable
6. Final result is K customer segments

### Why Unsupervised Learning?
- No labeled data needed
- Algorithm finds patterns on its own
- Discovers hidden customer groups
- No prior knowledge of segments required

---

## 🔍 Finding Best K — Elbow Method

To find the optimal number of clusters we used
the Elbow Method:

- Tested K values from 1 to 10
- Calculated inertia for each K
- Plotted inertia vs K graph
- Found the elbow bend at K=5
- K=5 chosen as optimal clusters

### Inertia Values:
| K | Inertia | Improvement |
|---|---------|-------------|
| 1 | 269981 | — |
| 2 | 181363 | Large drop |
| 3 | 106348 | Large drop |
| 4 | 73679 | Large drop |
| 5 | 44448 | Large drop ← Best K |
| 6 | 37233 | Small drop |
| 7 | 30259 | Very small |
| 8+ | — | Negligible |

---

## 👥 Customer Segments Discovered

### Cluster 0 — 💎 Premium Customers
- **Income:** High (above ₹70k)
- **Spending Score:** High (above 60)
- **Behavior:** Earn a lot and spend a lot
- **Strategy:** Send VIP offers and luxury brand promotions
- **Size:** ~39 customers

### Cluster 1 — 💰 Careful Spenders
- **Income:** High (above ₹70k)
- **Spending Score:** Low (below 40)
- **Behavior:** Earn a lot but save carefully
- **Strategy:** Send value for money deals
- **Size:** ~23 customers

### Cluster 2 — 🛍️ Impulsive Buyers
- **Income:** Low (below ₹40k)
- **Spending Score:** High (above 60)
- **Behavior:** Low income but love shopping
- **Strategy:** Send flash sales and limited time offers
- **Size:** ~81 customers

### Cluster 3 — 💚 Budget Customers
- **Income:** Low (below ₹40k)
- **Spending Score:** Low (below 40)
- **Behavior:** Low income and spend carefully
- **Strategy:** Send heavy discount coupons
- **Size:** ~22 customers

### Cluster 4 — 📊 Average Customers
- **Income:** Medium (₹40k to ₹70k)
- **Spending Score:** Medium (40 to 60)
- **Behavior:** Normal shopping behavior
- **Strategy:** Send regular newsletters and loyalty points
- **Size:** ~35 customers

---

## 🌐 Web Application
Built an interactive Streamlit web application where:
- User enters Annual Income using slider
- User enters Spending Score using slider
- App predicts which customer segment they belong to
- Shows segment name and business strategy
- Displays all cluster visualizations
- Shows elbow curve and distribution graphs

## 📁 Project Structure
Task02_CustomerSegmentation/
├── app.py
├── requirements.txt
├── README.md
├── dataset/
│   └── Mall_Customers.csv
├── notebooks/
│   └── Task02_CustomerSegmentation.ipynb
├── models/
│   ├── kmeans_model.pkl
│   └── model_info.json
└── images/
├── clusters.png
├── elbow_curve.png
└── distributions.png

## 🛠️ Tech Stack
| Technology | Purpose |
|-----------|---------|
| Python 3.12 | Programming Language |
| Pandas | Data loading and manipulation |
| NumPy | Numerical computations |
| Scikit-learn | K-Means clustering algorithm |
| Matplotlib | Creating visualizations |
| Seaborn | Statistical plots |
| Streamlit | Web application |
| Joblib | Saving and loading model |

## 🚀 How to Run This Project

### Step 1 — Clone Repository
git clone your_repo_link
cd Task02_CustomerSegmentation

### Step 2 — Install Requirements
pip install -r requirements.txt

### Step 3 — Run Website
streamlit run app.py

### Step 4 — Open Browser
Website opens at:
http://localhost:8501


## 💡 Key Learnings
- Understood unsupervised machine learning
- Learned K-Means clustering algorithm
- Applied Elbow Method for optimal K
- Performed customer behavior analysis
- Built interactive prediction website
- Gained business insights from data

## 📚 References
- Dataset: Kaggle Mall Customer Segmentation
- Algorithm: Scikit-learn KMeans Documentation
- Deployment: Streamlit Documentation

## 👤 Intern Details
- **Name:** Medipalli Satya Sreepradha Hamsika
- **Internship:** SkillCraft Technology
- **Task:** 02 — K-Means Clustering
- **Domain:** Machine Learning
