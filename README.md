# 🎉 MoMo Data Analysis Project

Welcome to the **MoMo Data Analysis** fullstack application! This project processes MTN MoMo SMS data, stores it in a database, and provides an interactive dashboard for exploring transaction insights.

---

## 🚀 Table of Contents

1. [Project Overview](#project-overview)
2. [Features](#features)
3. [Tech Stack](#tech-stack)
4. [Getting Started](#getting-started)

   * [Prerequisites](#prerequisites)
   * [Installation](#installation)
5. [Backend](#backend)

   * [XML Parsing & Cleaning](#xml-parsing--cleaning)
   * [Database Schema](#database-schema)
   * [Population Script](#population-script)
   * [Logging & Error Handling](#logging--error-handling)
6. [Frontend](#frontend)

   * [Dashboard Overview](#dashboard-overview)
   * [Usage & Interaction](#usage--interaction)
7. [Running the App](#running-the-app)
8. [Project Structure](#project-structure)
9. [Collaborators](#collaborators)
10. [License](#license)

---

## 🎯 Project Overview

This fullstack application ingests \~1,600 MTN MoMo SMS messages in **XML** format, cleans and categorizes each transaction, saves them into a **relational database**, and presents an **interactive dashboard** for visualization and analysis. Think of it as your personal MoMo insights hub!

### Why MoMo?

* MTN Mobile Money (MoMo) is Rwanda’s leading mobile payment service.
* Analyzing SMS notifications reveals spending habits, cash flows, and transaction trends.
* This app showcases enterprise-level design: **data pipelines**, **DB design**, and **UI/UX**.

---

## ✨ Features

* **Robust Parsing**: Handles many SMS formats (incoming, payments, transfers, withdrawals, airtime, cash power, deposits, OTPs).
* **Data Cleaning**: Normalizes amounts, timestamps, and handles edge cases.
* **Relational Schema**: SQLite database with normalized tables for transactions and types.
* **Error Logging**: Unmatched SMS messages logged for review.
* **Interactive Dashboard**:

  * Search & filter by date, amount, type
  * Bar, pie, and line charts (Chart.js) for volume, monthly trends, distributions
  * Detail view for individual transactions
* **Bonus**: Flask API endpoints for future mobile or external integrations.

---

## 🛠 Tech Stack

| Layer         | Technology                        |
| ------------- | --------------------------------- |
| Backend       | Python 3, SQLite                  |
| Parsing       | `xml.etree.ElementTree`, `re`     |
| API (Bonus)   | Flask / FastAPI                   |
| Frontend      | HTML5, CSS3, JavaScript, Chart.js |
| Version Ctrl. | Git & GitHub                      |

---

## 🏁 Getting Started

### Prerequisites

* Python 3.8+ installed
* `pip` package manager
* `sqlite3` CLI (optional)
* Modern browser (Chrome, Firefox, Edge)

### Installation

1. **Clone Repo**

   ```bash
   git clone https://github.com/JesseWK100/MoMo-Data-Analysis.git
   cd MoMo-Data-Analysis
   ```
2. **Create & Activate Virtualenv**

   ```bash
   python3 -m venv venv
   source venv/bin/activate     # on Windows: venv\Scripts\activate
   ```
3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

---

## 🔧 Backend

### XML Parsing & Cleaning

* **File**: `extract_process.py`
* **Approach**:

  1. Load `modified_sms_v2.xml` via `xml.etree.ElementTree`.
  2. For each `<sms>`, extract `body`, `date`, `address`, etc.
  3. Apply **regex patterns** to categorize into types:

     * Incoming, Payment, Transfer, Deposit, Airtime, Cash Power, Withdrawal, OTP
  4. Convert amounts to integers, normalize timestamps to `YYYY-MM-DD HH:MM:SS`.
  5. Log unmatched SMS bodies to `unprocessed.log`.

### Database Schema

* **File**: `schema.sql`
* **Tables**:

  * `transaction_types (id, name)`
  * `transactions (id, sms_id, raw_body, tx_type_id, amount, currency, fee, balance_after, tx_timestamp, from_party, to_party, momo_tx_id, agent_id, extra_info)`

### Population Script

* **File**: `populate_db.py`
* **Workflow**:

  1. Read cleaned records via `extract_process.extract_all()`.
  2. Insert or ignore transaction types.
  3. Insert each transaction into `transactions` with foreign-key link to `transaction_types`.

### Logging & Error Handling

* **Logging**: all unparsed messages go into `unprocessed.log` with timestamp.
* **Error Cases**: duplicate SMS are skipped (`INSERT OR IGNORE`).

---

## 🎨 Frontend

### Dashboard Overview

* **HTML/CSS**: Clean, responsive layout using **Flexbox** and **Grid**.
* **JavaScript**: Fetch data (static JSON or via Flask API) and render charts.
* **Chart.js**:

  * **Bar Chart**: total volume per transaction type
  * **Line Chart**: monthly totals
  * **Pie Chart**: distribution of incoming vs outgoing

![Dashboard Preview](./docs/dashboard-screenshot.png)

### Usage & Interaction

* **Search**: by date range, amount threshold, or keywords in `raw_body`.
* **Filter**: dropdown to select transaction types.
* **Detail Modal**: click a bar or pie slice to see transaction list.
* **Bonus API**: `GET /api/transactions`, `GET /api/types` (returns JSON).

---

## ▶️ Running the App

1. **Initialize DB**

   ```bash
   sqlite3 momo.db < schema.sql
   ```
2. **Populate Data**

   ```bash
   python extract_process.py
   python populate_db.py
   ```
3. **Serve Frontend**

   * **Static**: open `frontend/index.html` in browser.
   * **With API**: start Flask:

     ```bash
     export FLASK_APP=app.py
     flask run
     ```
4. **Explore**: Navigate to `http://localhost:5000/`.

---

## 📁 Project Structure

```
MoMo-Data-Analysis/
├── backend/
│   ├── extract_process.py
│   ├── populate_db.py
│   ├── schema.sql
│   └── modified_sms_v2.xml
├── frontend/
│   ├── index.html
│   ├── styles.css
│   └── app.js
├── docs/
│   └── dashboard-screenshot.png
├── unprocessed.log
├── momo.db
├── requirements.txt
└── README.md    <-- you are here!
```

---

## 👥 Collaborators

* **Jesse Kisaale Walusansa** *(Backend)* — [JesseWK100](https://github.com/JesseWK100)
* **Allan Ntare** *(Backend)* — [Ntare-GAMA](https://github.com/Ntare-GAMA)
* **Andrew Ogayo** *(Frontend)* — [OgayoTK1](https://github.com/OgayoTK1)
* **Sam Kwizera** *(Frontend)* — [samkwizera](https://github.com/samkwizera)

---

## 📜 License

This project is licensed under the **MIT License**. See [LICENSE](./LICENSE) for details.

---

> *“Data is the new oil, but like oil, it needs refinement.”* 💡

