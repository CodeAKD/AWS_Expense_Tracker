# 🧾 Expense Tracker — Serverless AWS Application
link to URL : https://expense-tracker-web-hosting.s3.us-east-1.amazonaws.com/expense_tracker_cognito.html

![AWS](https://img.shields.io/badge/AWS-Cloud-orange?logo=amazonaws)
![Python](https://img.shields.io/badge/Python-Backend-blue?logo=python)
![HTML](https://img.shields.io/badge/HTML-Frontend-red?logo=html5)
![CSS](https://img.shields.io/badge/CSS-Style-blue?logo=css3)
![JavaScript](https://img.shields.io/badge/JavaScript-Logic-yellow?logo=javascript)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 💡 Overview

The **Expense Tracker** is a fully **serverless web application** built using **AWS Cloud Services**.  
It allows users to securely **add, view, and delete expenses**, while automatically sending **email alerts** via **SNS** when spending exceeds a defined threshold.

The application consists of a **static HTML/CSS/JS frontend** hosted on **Amazon S3** and a **Python-based backend** running on **AWS Lambda**, integrated through **API Gateway** and secured with **Cognito authentication**.

---

## ⚙️ Features

✅ User authentication using **AWS Cognito**  
✅ Add, view, and delete expenses in **DynamoDB**  
✅ **Email notifications** when spending crosses a limit via **AWS SNS**  
✅ Fully **serverless** — zero manual server management  
✅ Simple and responsive **frontend UI**  
✅ Secured API integration via **API Gateway**

---

## 🧠 AWS Services Used

| Service | Purpose |
|----------|----------|
| **Amazon S3** | Hosts the static frontend (HTML, CSS, JS) |
| **AWS Cognito** | Handles user signup, login, and authentication |
| **AWS Lambda (Python)** | Backend functions for expense management |
| **Amazon DynamoDB** | Stores expense data securely |
| **AWS API Gateway** | Exposes secure REST APIs to frontend |
| **AWS SNS** | Sends email alerts when threshold exceeded |
| **AWS CloudWatch** | Tracks logs and performance metrics |

---

## 🧩 Architecture Diagram

```plaintext
        +--------------------------+
        |      HTML / CSS / JS     |
        |   (Hosted on S3 Bucket)  |
        +------------+-------------+
                     |
                     v
            +------------------+
            |  AWS API Gateway |
            +------------------+
                     |
        +------------+-------------+
        |        AWS Lambda        |
        | (Python Functions)       |
        |  postExpense.py          |
        |  getExpense.py           |
        |  deleteExpense.py        |
        +------------+-------------+
                     |
            +------------------+
            |  DynamoDB Table  |
            | (Stores Expenses)|
            +------------------+
                     |
                     v
             +-----------------+
             |     AWS SNS     |
             | (Email Alerts)  |
             +-----------------+

        +----------------------------+
        |     AWS Cognito Pool       |
        |  (User Auth & Management)  |
        +----------------------------+
## 🧰 Folder Structure
ExpenseTracker/
│
├── frontend/
│   ├── expense_tracker.html
│   ├── style.css
│   └── script.js
│
├── backend/
│   ├── postExpense.py
│   ├── getExpense.py
│   └── deleteExpense.py
│
└── README.md
