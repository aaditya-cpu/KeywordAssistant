# KeywordAssistant

## Overview
KeywordAssistant is a Flask-based application designed to process CSV files containing keyword statistics, compute various metrics, and store the results in an SQLite database for easy keyword analysis. It supports uploading CSV files through a web interface and automatically generates a comprehensive keyword analysis database.

## Features
- Upload CSV files via a web interface.
- Computes metrics such as high potential keywords, trending keywords, and stable keywords.
- Stores results in an SQLite database.

## Installation

1. Clone the repository:

git clone https://github.com/yourusername/KeywordAssistant.git

markdown


2. Install the required packages:

pip install -r requirements.txt

markdown


3. Run the Flask application:

python app.py



Visit `http://localhost:5000` to access the application.

## Configuration
Ensure your CSV files are formatted correctly with the necessary columns for processing.

## Contributing
Contributions are welcome. Please open an issue or submit a pull request with your suggestions.

## License
Distributed under the MIT License. See `LICENSE` for more information.