# 🖼️ EDF Lookbook Generator

The EDF Lookbook Generator is a secure, internal web tool designed for the Elizabeth Dole Foundation. It allows staff to upload a CSV file containing contact information and automatically generate a beautifully formatted PDF lookbook — complete with headshots, names, roles, and descriptions.

Built with Flask and SQLAlchemy, the app supports secure staff login, user registration (restricted to @elizabethdolefoundation.org emails), and CSV-to-PDF conversion with dynamic image handling.

---

## 🔐 Features

- 📥 Upload CSV file and generate a downloadable PDF lookbook
- 🧑‍💻 User registration & login system with hashed passwords
- 🛡️ Email restriction: Only `@elizabethdolefoundation.org` users can create accounts
- 🖼️ Auto-matched image support (via Salesforce file names)
- 🎨 Clean user interface with custom CSS
- 📦 GitHub + Render deployment ready
- 🔒 Uses Flask-Login and SQLAlchemy for security and persistence

---

## 📁 CSV Format Requirements

Your CSV should include the following columns (headers in lowercase):

- `headshot` *(file name like `first_last1.jpg`)*
- `name`
- `company`
- `title`
- `additional`
- `description`

Images must be stored in `/static/images/` and should match the `headshot` file names.

---

## 🚀 Setup Instructions

1. **Clone the repo:**

```bash
git clone https://github.com/your-username/flask-lookbook.git
cd flask-lookbook
