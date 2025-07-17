
# 🏆 Sports Event Platform

**A modern web application for managing sports events, auctions, packages, services, and payments.**

---

## 🚀 Why This Project Stands Out
- **Full-stack Python & Flask:** End-to-end solution using popular frameworks.
- **MongoDB Integration:** Scalable, cloud-ready data storage.
- **Live Auction Bidding:** Real-time auction experience for users.
- **Modular Architecture:** Clean separation of models, views, and assets.
- **Responsive UI:** Mobile-friendly, recruiter-ready landing page.
- **Secure by Design:** Secrets managed via environment variables, `.env` protected.

---

## 🧩 Key Features
- Event creation, management, and tracking
- Auction system with live bidding
- Service and package listings with dynamic pricing
- Payment tracking and reporting
- User-friendly, responsive landing page
- Extendable service management (add, update, delete)

---

## 📁 Project Structure
```
├── app.py                # Main Flask app & routing
├── main.py               # Application entry point
├── db_init.py            # Database initialization scripts
├── check_collections.py  # Utility: Check DB collections
├── view_database.py      # Utility: View DB contents
├── view_events.py        # Utility: View events
├── view_payments.py      # Utility: View payments
├── models/               # Data models (auction, event, package, payment, service)
├── pages/                # HTML pages (auction, checkout, customize, etc.)
├── css/                  # Stylesheets (responsive design)
├── js/                   # JavaScript (auction logic, form validation)
├── index.html            # Landing page
├── pyproject.toml        # Python project config
├── .gitignore            # Git ignore rules
```

---

## ⚡ Quick Start
1. **Clone the repository:**
   ```powershell
   git clone https://github.com/Harshal-2004/Sports-Event-Platform.git
   cd Sports-Event-Platform
   ```
2. **Create a Python virtual environment:**
   ```powershell
   python -m venv .venv
   .venv\Scripts\activate
   ```
3. **Install dependencies:**
   ```powershell
   pip install -r requirements.txt
   ```
4. **Configure secrets:**
   Create a `.env` file in the root directory:
   ```
   MONGODB_URI=your_mongodb_uri_here
   ```
5. **Run the application:**
   ```powershell
   python main.py
   ```

---

## 🔒 Security Best Practices
- `.env` is **never** uploaded to GitHub (see `.gitignore`).
- All sensitive keys and credentials are loaded from environment variables.

---

## 📬 Contact & License
- **Contact:** [Harshal-2004](https://github.com/Harshal-2004)
- **License:** Educational use only