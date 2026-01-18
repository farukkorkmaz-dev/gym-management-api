# 🏋️‍♂️ Gym Management System API

A professional backend API developed with **Python** and **FastAPI** to manage gym memberships, track access logs, and handle balance transactions.

## 🚀 Features
* **Member Management:** Create, list, and delete members.
* **Access Control:** Turnstile simulation with balance check.
* **Business Logic:** Automatically denies access if the balance is insufficient.
* **Reporting:** Real-time dashboard for total members and revenue.

## 🛠️ Tech Stack
* **Language:** Python 3.10+
* **Framework:** FastAPI
* **Database:** SQLite
* **Documentation:** Swagger UI (Auto-generated)

## 🗺️ Roadmap (Future Plans)
* [ ] **Admin Authentication:** Secure login for managers using JWT (JSON Web Tokens).
* [ ] **Docker Support:** Containerization for easy deployment.
* [ ] **Frontend Interface:** A simple web dashboard using React or Vue.js.

## ⚙️ Installation & Usage

1. **Install Dependencies:**
   pip install fastapi uvicorn

2. **Run the Server:**
   uvicorn main:app --reload

3. **Test the API:**
   Open your browser and go to: http://127.0.0.1:8000/docs

## 🧪 How to Test (Scenario)
1. **Add Member:** Use `POST /members` to add a member with **$100** balance.
2. **First Entry:** Use `POST /access` with action "Check-in". (**$50** deducted).
3. **Second Entry:** Use `POST /access` again. (**$50** deducted, Balance: $0).
4. **Denial:** Try "Check-in" a third time. You should see an **"Insufficient balance"** error.

---
*Developed by [Your Name]*
