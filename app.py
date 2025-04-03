from flask import Flask, render_template, request
from datetime import date
from flask_sqlalchemy import SQLAlchemy # type: ignore
import random

app = Flask(__name__)

# Cấu hình cơ sở dữ liệu
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///horoscopes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Định nghĩa mô hình User
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    day_of_birth = db.Column(db.Integer, nullable=False)
    month_of_birth = db.Column(db.Integer, nullable=False)
    zodiac_sign = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    prediction = db.Column(db.String(500), nullable=False)
    lucky_number = db.Column(db.Integer, nullable=False)

# Khởi tạo cơ sở dữ liệu
with app.app_context():
    db.create_all()

# Dữ liệu mô phỏng
descriptions = {
    'Aries' : 'You have an enthusiastic, humorous, adventurous, and passionate character. \nBut sometimes, you are also prone to selfishness, intolerance, impulsiveness, and impatience.',
    'Taurus' : 'You have a calm, patient, reliable, loyal, ambitious, and determined character character. \nBut sometimes, you are also prone to hedonism, laziness, inflexibility, and jealousy.',
    'Gemini' : 'You have a sociable, fun-loving, versatile, liberal, intelligent, and friendly character. \nBut sometimes, you are also prone to moodiness, inconsistency, superficiality, restlessness, and laziness.',
    'Cancer' : 'You have a kind, emotional, romantic, imaginative, sympathetic, and intuitive character. \nBut sometimes, you are also prone to changeability, moodiness, hypersensitivity, depression, and clinginess',
    'Leo' : 'You have a generous, hospitable, caring, warm, authoritative, active, and open character. \nBut sometimes, you are also  prone to laziness, often choosing to take the easy way out.',
    'Virgo' : 'You have a diligent, analytical, self-sufficient, orderly, and modest character. \nBut sometimes, you are also  prone to fussiness, perfectionism, harsh criticism, coldness, and hypochondria.',
    'Libra' : 'You have a pleasant, articulate, charming, social, charismatic, fair and even-tempered character. \nBut sometimes, you are also thought to be indecisive, lazy, aloof, flirtatious, and shallow.',
    'Scorpio' : 'You have a complex, analytical, patient, keenly perceptive, inquisitive, focused and determined character. \nBut sometimes, you are also  prone to extremity, jealousy, envy, possessiveness, and cruelty.',
    'Sagittarius' : 'You have a straight-forward, extremely clever, generous, compassionate, and energetic character. \nBut sometimes, you are also prone to restlessness, impulsiveness, impatience, and recklessness.',
    'Capricorn' : 'You have an ambitious, modest, responsible, stable, powerful, intellectual, and persistent character. \nBut sometimes, you are also prone to coldness, conservatism, rigidity, materialism, and dullness.',
    'Aquarius' : 'You have a modest, creative, inquisitive, progressive, stimulating, nocturnal, and independent character. \nBut sometimes, you are also prone to rebelliousness, coldness, indecisiveness, and impracticality.',
    'Pisces' : 'You have a tolerant, modest, dreamy, romantic, humorous, generous, emotional and receptive character. \nBut sometimes, you are also prone to exaggeration, fickleness, passiveness, and hypersensitivity.',

}

horoscope_predictions = {
    "Aries": [
        "Spend more time in a relationship.",
        "Professional tasks may seem challenging but you will handle it.",
    ],
    "Taurus": [
        "A happy romantic relationship will wait for you.",
        "Enjoy strong financial status.",
    ],
    "Gemini": [
        "A diligent love affair is what the horoscope predicts for you",
        "Multitask to accomplish every task within the time limit.",
        "Financial health will be good today.",
    ],
    "Cancer": [
        "A happy love life backed by professional success will make your day.",
        "Minor financial issues will exist and handle them carefully.",
        "Check the health as well.",
    ],
    "Leo": [
        "Avoid toxic relationships today.",
        "Professional success will be at your side.",
        "Stay happy as both wealth and health are good throughout the day.",
    ],
    "Virgo": [
        "Walk into the old relationship today.",
        "Utilize professional opportunities to grow.",
        "Make smart money decisions & enjoy good health.",
    ],
    "Libra": [
        "Handle love-related issues with a mature attitude.",
        "Professional challenges will exist but handle them.",
        "Both finance and health will be at your side today.",
        "Watch for opportunities.",
    ],
    "Scorpio": [
        "A happy romantic relationship is waiting for you.",
        "Despite challenges, you will do professionally well.",
        "Today is good for investments.",
    ],
    "Sagittarius": [
        "Be sensible while handling romantic issues today.",
        "Professional challenges exist but you will troubleshoot them.",
        "Financial fortune will be at your side.",
    ],
    "Capricorn": [
        "The horoscope suggests resolving issues in relationships.",
        "Professional tasks may seem challenging but handle them smartly.",
    ],
    "Aquarius": [
        "Embrace the happiness in the love life today.",
        "Professional challenges will be turned into opportunities.",
        "Stay healthy.",
    ],
    "Pisces": [
        "Be sincere in the relationship today and skip unwanted debates.",
        "Official responsibilities will keep you busy throughout the day.",
    ],
}

def is_valid_date(day, month):
    max_days_per_month = {
        1: 31, 2: 29, 3: 31, 4: 30, 5: 31, 6: 30,
        7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31
    }
    return 1 <= month <= 12 and 1 <= day <= max_days_per_month.get(month, 0)


def get_zodiac_sign(day_of_birth, month_of_birth):
    if (month_of_birth == 3 and 21 <= day_of_birth <= 31) or (month_of_birth == 4 and 1 <= day_of_birth <= 19):
        return "Aries"
    elif (month_of_birth == 4 and 20 <= day_of_birth <= 30) or (month_of_birth == 5 and 1 <= day_of_birth <= 20):
        return "Taurus"
    elif (month_of_birth == 5 and 21 <= day_of_birth <= 31) or (month_of_birth == 6 and 1 <= day_of_birth <= 20):
        return "Gemini"
    elif (month_of_birth == 6 and 21 <= day_of_birth <= 30) or (month_of_birth == 7 and 1 <= day_of_birth <= 22):
        return "Cancer"
    elif (month_of_birth == 7 and 23 <= day_of_birth <= 31) or (month_of_birth == 8 and 1 <= day_of_birth <= 22):
        return "Leo"
    elif (month_of_birth == 8 and 23 <= day_of_birth <= 31) or (month_of_birth == 9 and 1 <= day_of_birth <= 22):
        return "Virgo"
    elif (month_of_birth == 9 and 23 <= day_of_birth <= 30) or (month_of_birth == 10 and 1 <= day_of_birth <= 22):
        return "Libra"
    elif (month_of_birth == 10 and 23 <= day_of_birth <= 31) or (month_of_birth == 11 and 1 <= day_of_birth <= 21):
        return "Scorpio"
    elif (month_of_birth == 11 and 22 <= day_of_birth <= 30) or (month_of_birth == 12 and 1 <= day_of_birth <= 21):
        return "Sagittarius"
    elif (month_of_birth == 12 and 22 <= day_of_birth <= 31) or (month_of_birth == 1 and 1 <= day_of_birth <= 19):
        return "Capricorn"
    elif (month_of_birth == 1 and 20 <= day_of_birth <= 31) or (month_of_birth == 2 and 1 <= day_of_birth <= 18):
        return "Aquarius"
    elif (month_of_birth == 2 and 19 <= day_of_birth <= 29) or (month_of_birth == 3 and 1 <= day_of_birth <= 20):
        return "Pisces"
    else:
        return None


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            name = request.form.get("name")
            day_of_birth = int(request.form.get("day", 0))
            month_of_birth = int(request.form.get("month", 0))

            if not is_valid_date(day_of_birth, month_of_birth):
                return render_template("index.html", error="Invalid date for zodiac calculation.")

            zodiac_sign = get_zodiac_sign(day_of_birth, month_of_birth)
            if not zodiac_sign:
                return render_template("index.html", error="Could not determine zodiac sign.")

            description = descriptions.get(zodiac_sign, "No description available.")
            prediction = " ".join(horoscope_predictions.get(zodiac_sign, ["No predictions available."]))
            lucky_number = random.randint(1, 30) + len(zodiac_sign)

            new_user = User(
                name=name,
                day_of_birth=day_of_birth,
                month_of_birth=month_of_birth,
                zodiac_sign=zodiac_sign,
                description=description,
                prediction=prediction,
                lucky_number=lucky_number
            )
            db.session.add(new_user)
            db.session.commit()

            return render_template("result.html",
                                   zodiac_sign=zodiac_sign,
                                   description=description,
                                   prediction=prediction,
                                   lucky_number=lucky_number)

        except ValueError:
            return render_template("index.html", error="Please enter valid numeric values.")

    return render_template("index.html")

@app.route("/history")
def history():
    users = User.query.all()
    return render_template("history.html", users=users)

if __name__ == "__main__":
    app.run(debug=True)
