# Olist E-commerce: Seller Churn & Performance Analysis

## Overview
This project analyzes seller performance and churn risk using the Olist e-commerce dataset. It combines SQL, Python, PostgreSQL, and Power BI to build business health indicators and support seller retention decisions.

Instead of reporting historical sales, the analysis focuses on uncovering signals of business decline (logistics issues, negative reviews, and revenue drop) that enable the support team to proactively retain valuable sellers before they become inactive.

---

## Business Questions
The project addresses five core questions:
*   Which performance factors are the strongest indicators of seller churn?
*   Does delivery performance significantly affect customer satisfaction?
*   Which sellers should the support team prioritize this week?
*   How much GMV is currently exposed to churn risk?
*   Which geographic regions require logistics improvements?

---

## Dataset & Metrics

### Data Sources
The analysis integrates Olist's core tables: `Orders`, `Order Items`, `Customers`, `Products`, `Payments`, `Reviews`, and `Sellers` (downloaded via Kaggle API).

### Key Metrics
To evaluate seller health, the following indicators were generated using Advanced SQL:

| Metric | Business Meaning |
|--------|------------------|
| **Recency** | Number of days since the seller's last order (identifies inactivity) |
| **Late Delivery Rate** | Percentage of orders delivered past the estimated delivery date |
| **Revenue Trend** | Identifies consecutive months of declining revenue (Gaps & Islands problem) |
| **Recent Reviews** | Average review score in the last 90 days (current customer satisfaction) |
| **Historical Reviews** | Historical average review score used as a baseline for service quality |
| **Churn Risk Score** | Composite health score (0-100) based on performance thresholds |

---

## Dashboard Preview
![Dashboard](assets/dashboard.png)

The dashboard is designed for support managers to quickly identify at-risk sellers and prioritize retention efforts based on financial exposure:
*   **KPIs:** Estimated GMV at Risk, number of high-risk sellers.
*   **Risk Distribution:** Classification of sellers into Critical, High, and Medium risk.
*   **Performance Correlation:** Relationship between logistics delays and customer review scores.
*   **Priority Action List:** Automatically generated action items (e.g., suggest commission discounts for critical sellers).

---

## Key Findings & Business Value

### Key Findings
1.  **Logistics is the primary driver:** Delivery delays are the strongest indicator of a seller becoming inactive.
2.  **The 20% threshold:** Customer satisfaction (Review Score) drops rapidly once a seller's late delivery rate exceeds 20%.
3.  **Revenue warning:** Two consecutive months of revenue decline is the most reliable warning signal of impending churn.
4.  **Geographic risk:** Sellers located in remote states (e.g., Amazonas - AM) face systemic logistics challenges that severely affect retention.

### Potential Business Value
*   Identify sellers with high churn risk.
*   Help prioritize seller support.
*   Estimate GMV currently exposed to churn risk (approximately **$375,000**).

---

## Pipeline
The project follows a Medallion Architecture with Bronze, Silver, and Gold layers.

*   **Data Ingestion:** Download source data and validate it using Great Expectations.
*   **Storage & Transform:** PostgreSQL cleans and denormalizes raw tables into a single `orders_master` table (Silver layer).
*   **Analytics & Scoring:** Advanced SQL calculates metrics, risk scores, and aggregates data in a Materialized View (Gold layer).
*   **Orchestration:** Python schedules daily runs via APScheduler, wraps API/database queries in Tenacity retries, and logs pipeline runs in a Postgres audit table.
*   **Visualization:** Power BI.

---

## Getting Started

### Prerequisites
Download your Kaggle API token (`kaggle.json`) from your Kaggle Account Settings and place it in the `.kaggle` directory:
*   Windows: `C:\Users\<Username>\.kaggle\kaggle.json`
*   Linux/macOS: `~/.kaggle/kaggle.json`

### Setup & Run
1.  **Environment Setup:**
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # Windows: .venv\Scripts\activate
    pip install -r requirements.txt
    cp .env.example .env
    ```
2.  **Start Database:**
    ```bash
    docker-compose up -d
    ```
3.  **Run Pipeline:**
    ```bash
    python src/pipeline.py
    ```
