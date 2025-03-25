from flask import Flask, render_template, request, send_file, redirect, url_for, session, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash 
from user_models import db, User 
import os 
import pandas as pd
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Image as RLImage, Paragraph, Spacer
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from PIL import Image as PILImage
from datetime import datetime


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
app.secret_key = 'dolefoundation'  

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login' 

# Folders 
UPLOAD_FOLDER = "uploads"
IMAGE_FOLDER = "static/images"
TEMP_IMAGE_FOLDER = "processed_images"

#Create folders if needed
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(TEMP_IMAGE_FOLDER, exist_ok=True)

#Flask-Login user loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#Login route 
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # ✅ Fetch from the database
        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('upload_csv'))
        else:
            flash("Invalid username or password.")

    return render_template('login.html')

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

#Main upload + PDF generation route
@app.route("/", methods=["GET", "POST"])
@login_required
def upload_csv():
    if request.method == "POST":
        file = request.files["file"]
        if file and file.filename.endswith(".csv"):
            csv_path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(csv_path)

            # Load CSV
            df = pd.read_csv(csv_path)
            df.fillna("", inplace=True)

            # Styles
            styles = getSampleStyleSheet()
            custom_title_color = colors.Color(28/255, 68/255, 108/255)
            custom_border_color = colors.Color(203/255, 212/255, 217/255)

            title_style = ParagraphStyle("TitleStyle", parent=styles["Title"], fontName="Times-Roman", fontSize=20,
                                         textColor=custom_title_color, alignment=1, spaceBefore=10, spaceAfter=10)
            name_style = ParagraphStyle("NameStyle", parent=styles["BodyText"], fontName="Times-Roman", fontSize=11,
                                        leading=18, spaceAfter=5)
            desc_style = ParagraphStyle("DescStyle", parent=styles["BodyText"], fontName="Times-Roman", fontSize=10,
                                        leading=14, spaceAfter=5)

            # Create PDF
            output_path = "output.pdf"
            doc = SimpleDocTemplate(output_path, pagesize=letter,
                                    leftMargin=0.5 * inch, rightMargin=0.5 * inch,
                                    topMargin=0.5 * inch, bottomMargin=0.5 * inch)

            elements = []

            # Title Page
            elements.append(Paragraph("Elizabeth Dole Foundation Look-Book", title_style))
            elements.append(Spacer(1, 10))

            # Loop through each row
            for index, row in df.iterrows():
                name = row.get("Name", "")
                title_text = row.get("Title", "")
                company = row.get("Company", "")
                additional = row.get("Additional", "")
                description = row.get("Description", "")
                image_name = row.get("Headshot", "").strip()
                image_path = os.path.join(IMAGE_FOLDER, image_name)
                
                # Process image with debug output
                headshot = None
                image_name = row.get("Headshot", "").strip()
                image_path = os.path.join(IMAGE_FOLDER, image_name)

                print(f"📸 Looking for image at: {image_path}")

                if os.path.exists(image_path):
                    try:
                        img = PILImage.open(image_path)
                        img = img.resize((75, 75), resample=PILImage.LANCZOS)
                        temp_path = os.path.join(TEMP_IMAGE_FOLDER, f"temp_{index}.jpg")
                        img.save(temp_path, quality=95)
                        headshot = RLImage(temp_path, width=1*inch, height=1*inch)
                        print(f"✅ Image processed successfully: {temp_path}")
                    except Exception as e:
                        print(f"❌ Error processing image {image_path}: {e}")
                else:
                    print(f"❌ Image not found: {image_path}")
                    pass

                # Format text
                info = f"<b>{name}</b><br/>{company}, {title_text}<br/><i>{additional}</i>"
                paragraph_name = Paragraph(info, name_style)
                paragraph_desc = Paragraph(description, desc_style)

                data = [
                    [headshot, paragraph_name],
                    [paragraph_desc, ""]
                ]

                table = Table(data, colWidths=[90, 450])
                table.setStyle(TableStyle([
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("LEFTPADDING", (0, 0), (-1, -1), 5),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                    ("BOX", (0, 0), (-1, -1), 2, custom_border_color),
                    ("SPAN", (0, 1), (1, 1)),
                ]))

                elements.append(table)
                elements.append(Spacer(1, 10))

            doc.build(elements)

            return send_file(output_path, as_attachment=True)

    #GET request
    return render_template("upload.html")

@app.route("/logout", methods=["GET"])
@login_required
def logout():
    logout_user()
    flash("You’ve been logged out.")
    return redirect(url_for("login"))

#Run the app
if __name__ == '__main__':
    app.run(debug=True)


