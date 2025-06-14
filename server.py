from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)

    const cors = require('cors');
const express = require('express');
const app = express();

app.use(cors()); // Enable CORS for all routes
