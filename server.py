from app import create_app
from flask_cors import CORS  # ✅ Add this

app = create_app()
CORS(app)  # ✅ Enable CORS for your Flask app

if __name__ == "__main__":
    app.run(debug=True)
