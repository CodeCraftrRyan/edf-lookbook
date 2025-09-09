from flask import Flask, render_template, request, send_file, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash 
from user_models import db, User  # type: ignore
import os 
import pandas as pd
from docx import Document
from docx.shared import Inches, RGBColor 
from docx.enum.table import WD_ALIGN_VERTICAL
from PIL import Image as PILImage
from datetime import datetime
from flask_mail import Mail, Message 
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from io import BytesIO
import csv

# Login and registration features are temporarily disabled for testing

app = Flask(__name__, instance_relative_config=True)
# Email configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your_email@gmail.com'   
app.config['MAIL_PASSWORD'] = 'your_email_password'       
app.config['MAIL_DEFAULT_SENDER'] = 'your_email@gmail.com' 

mail = Mail(app)

db_path = os.path.join(app.instance_path, 'users.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
app.secret_key = 'dolefoundation'  

#login_manager = LoginManager()
#login_manager.init_app(app)
#login_manager.login_view = 'login' 

# Folders 
app.config['UPLOAD_FOLDER'] = "uploads"
IMAGE_FOLDER = "static/images"
TEMP_IMAGE_FOLDER = "processed_images"

#Create folders if needed
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(TEMP_IMAGE_FOLDER, exist_ok=True)

#Flask-Login user loader
#@login_manager.user_loader
#def load_user(user_id):
#    return User.query.get(int(user_id))

#Login route 
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#   if request.method == 'POST':
#         username = request.form.get('username')
#         password = request.form.get('password')
#         user = User.query.filter_by(username=username).first()
#         if user and user.check_password(password):
#             login_user(user)
#             return redirect(url_for('upload_csv'))
#         else:
#             flash("Invalid username or password.")
#     return render_template('login.html')

'''
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        
        # ✅ Restrict to EDF domain
        if not email.endswith("@elizabethdolefoundation.org"):
            flash("Only EDF staff emails are allowed.")
            return redirect(url_for("register"))

        # Check if username already exists in the database
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash("Username already taken. Please choose another.")
            return redirect(url_for("register"))
        
        if User.query.filter_by(email=email).first():
            flash("Email already in use.")
            return redirect(url_for("register"))

        # Create and store new user
        new_user = User(username=username, email=email)
        new_user.set_password(password)  # securely hash password
        db.session.add(new_user)
        db.session.commit()

        flash("Account created! Please log in.")
        return redirect(url_for("login"))

    return render_template("register.html")
'''

'''
@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        username = request.form['username']
        user = User.query.filter_by(username=username).first()

        if user:
            reset_link = f"http://localhost:5001/reset_password/{user.id}"
            msg = Message("Reset Your Password",
                          recipients=[user.email])
            msg.body = f"Hi {user.username},\n\nClick here to reset your password: {reset_link}\n\nIf you didn’t ask for this, you can ignore it."
            mail.send(msg)
            flash("✅ Reset email sent!")
        else:
            flash("⚠️ No user found with that username.")

        return redirect(url_for('login'))

    return render_template("forgot_password.html")
'''
# Utility function to set column width
from docx.shared import Inches

def set_column_width(table, column_idx, width_in_inches):
    for cell in table.columns[column_idx].cells:
        cell.width = Inches(width_in_inches)

#Main upload + PDF generation route
@app.route("/", methods=["GET", "POST"])
#@login_required
def upload_csv():
    if request.method == "POST":
        file = request.files["file"]
        if file and file.filename.endswith(".csv"):
            csv_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(csv_path)

            # Load CSV
            df = pd.read_csv(csv_path)
            df.fillna("", inplace=True)

            output_path = "lookbook output.docx"
            doc = Document()
            doc.add_heading("Elizabeth Dole Foundation Look-Book", 0)
            doc.add_paragraph("Generated on: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            doc.add_page_break()
            

            from docx.shared import RGBColor

            for index, row in df.iterrows():
                name = row.get("Name", "")
                title_text = row.get("Title", "")
                company = row.get("Company", "")
                additional = row.get("Additional", "")
                description = row.get("Description", "")
                image_name = row.get("Headshot", "").strip()
                image_path = os.path.join(IMAGE_FOLDER, image_name)
                table = doc.add_table(rows=2, cols=3)
                
                # Set column widths
                set_column_width(table, 0, 1.5)  # First column 2 inches
                set_column_width(table, 1, 3)  # Second column 3 inches
                set_column_width(table, 2, 1)  # Third column 1 inch                   

                # Column 1: Image
                img_cell = table.cell(0, 0)
                img_cell.vertical_alignment = WD_ALIGN_VERTICAL.TOP
                if os.path.exists(image_path):
                    try:
                        img_para = img_cell.paragraphs[0]
                        img_para.paragraph_format.space_after = 0
                        run = img_para.add_run()
                        run.add_picture(image_path, width=Inches(1.4))
                    except Exception as e:
                        img_cell.text = "[Image error]"
                else:
                    img_cell.text = "[Image not found]"

                # Column 2: Text content
                text_cell = table.cell(0, 1)
                # Name (Heading 2) at the top, in its own paragraph
                name_para = text_cell.paragraphs[0]
                name_para.style = 'Heading 2'
                name_para.add_run(name)
                # Company, title, and additional info in the paragraph below name
                info_para = text_cell.add_paragraph()
                info_para.add_run(f"{company}, {title_text}\n")
                if additional:
                    info_para.add_run("\n" + additional).italic = True

                # Row 2: Description across all four columns
                desc_cell = table.cell(1, 0)
                desc_cell.merge(table.cell(1, 2))
                desc_para = desc_cell.paragraphs[0]
                desc_para.add_run("\n")  # Add more space between headshot and description
                desc_para.add_run(description)
                doc.add_paragraph("\n")

            doc.save(output_path)
            return send_file(output_path, as_attachment=True)

    #GET request
    return render_template("upload.html")

#@app.route("/logout", methods=["GET"]) removed for testing
#@login_required temporarily removed for testing
#    logout_user()
#    flash("You’ve been logged out.")
#    return redirect(url_for("login"))

@app.route('/download-template')
def download_template():
    from io import StringIO
    import csv

    output = BytesIO()
    writer = csv.writer(output)
    
    import io
    text_stream = io.TextIOWrapper(output, encoding='utf-8')
    writer = csv.writer(text_stream)

    # Column headers
    writer.writerow(["Name", "Title", "Company", "Additional", "Description", "Headshot"])

    # Example row
    writer.writerow([
        "Jane Doe",
        "Senior Advisor",
        "Elizabeth Dole Foundation",
        "Military Caregiver Advocate",
        "Jane has dedicated over a decade to supporting caregivers across the country.",
        "jane_doe.jpg"
    ])

    text_stream.flush()
    output.seek(0)

    return send_file(
        output,
        mimetype='text/csv',
        as_attachment=True,
        download_name='LOOKBOOK_TEMPLATE.csv'
    )

#Run the app
if __name__ == '__main__':
    app.run(debug=True)