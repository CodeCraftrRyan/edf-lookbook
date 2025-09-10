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
- 🔒 Users can forget password and answer security questions

---

## 📁 CSV Format Requirements

Your CSV should include the following columns (exact headers):

- `lookbookID` *(unique identifier for each entry, e.g., LB-0001)*
- `Full Name`
- `Primary Organization (Lookbook)`
- `Primary Affiliation Role (Lookbook)`
- `Bio/About Me`

Images should be stored in `/static/images/` and their file names should match the values you provide in the image column (if used).

### Example Row

| lookbookID | Full Name  | Primary Organization (Lookbook) | Primary Affiliation Role (Lookbook) | Bio/About Me |
|------------|------------|---------------------------------|-------------------------------------|--------------|
| LB-0001    | Jane Doe   | Elizabeth Dole Foundation       | Senior Advisor                      | Jane has dedicated over a decade to supporting caregivers across the country. |

---

## 🚀 Setup Instructions

1. **Clone the repo:**

```bash
git clone https://github.com/your-username/flask-lookbook.git
cd flask-lookbook