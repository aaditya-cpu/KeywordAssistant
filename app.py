import os
import pandas as pd
import sqlite3
from flask import Flask, request, render_template

app = Flask(__name__)

def clean_and_compute_metrics(df):
    """
    Cleans the DataFrame and computes necessary metrics for keyword analysis.
    """
    df['Three month change'] = pd.to_numeric(df['Three month change'].replace('∞', '1'), errors='coerce').fillna(0)
    df['YoY change'] = pd.to_numeric(df['YoY change'].replace('∞', '1'), errors='coerce').fillna(0)
    df['Search Volume to Competition Ratio'] = df['Avg. monthly searches'] / (df['Competition (indexed value)'] + 1)
    df['Trending'] = df['Three month change'] > 0
    df['Seasonal/Long-term Trend'] = df['YoY change'] > 0
    df['Stable'] = (df['Three month change'] == 0) & (df['YoY change'] == 0)
    
    max_searches = df['Avg. monthly searches'].max()
    max_competition_index = df['Competition (indexed value)'].max()
    max_three_month_change = max(df['Three month change'].max(), 0.01)  # Avoid division by zero

    df['Keyword Opportunity Index'] = ((df['Avg. monthly searches'] / max_searches) + 
                                       (1 - df['Competition (indexed value)'] / max_competition_index) + 
                                       (df['Three month change'] / max_three_month_change)) / 3
    return df

def process_csv(file_path, project_name):
    """
    Processes the CSV file to compute various metrics and store results in an SQLite database.
    """
    df = pd.read_csv(file_path)

    # Clean and prepare data
    df = clean_and_compute_metrics(df)

    # Filter keywords into categories
    categories = {
        'High_Potential_Keywords': df.sort_values(by='Search Volume to Competition Ratio', ascending=False),
        'Trending_Keywords': df[df['Trending']].sort_values(by='Three month change', ascending=False),
        'Seasonal_Long_Term_Trends': df[df['Seasonal/Long-term Trend']].sort_values(by='YoY change', ascending=False),
        'Top_Opportunity_Keywords': df.sort_values(by='Keyword Opportunity Index', ascending=False),
        'Stable_Keywords': df[df['Stable']]
    }

    # Save to SQLite database
    db_name = f"{project_name}_keywords.db"
    db_path = os.path.join(os.getcwd(), db_name)

    try:
        with sqlite3.connect(db_path) as conn:
            for category, data in categories.items():
                data.to_sql(category, conn, if_exists='replace', index=False)
        print(f"Database {db_name} created successfully at {db_path}.")
    except Exception as e:
        print(f"Error creating database: {e}")

@app.route('/upload', methods=['POST'])
def upload_file():
    """
    Flask route to upload CSV file and process data.
    """
    file = request.files['file']
    project_name = request.form.get('project_name')
    if not file or not project_name:
        return "Missing file or project name", 400
    
    # Temporary save or directly process
    file_path = f"/tmp/{file.filename}"
    file.save(file_path)
    
    # Process CSV and create SQLite DB
    process_csv(file_path, project_name)
    
    return f"Database {project_name}_keywords.db created successfully."

@app.route('/')
def home():
    """
    Route to display the upload form.
    """
    return render_template('upload_form.html')  # Ensure you have an 'upload_form.html' template in your templates directory

if __name__ == '__main__':
    app.run(debug=True)
