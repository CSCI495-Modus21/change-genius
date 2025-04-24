# api.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3
from sqlite3 import Error
import json
from dotenv import load_dotenv
import os
import requests
import pandas as pd

load_dotenv()
app = FastAPI()
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")

class ChangeRequest(BaseModel):
    project_name: str
    change_number: str
    requested_by: str
    date_of_request: str
    presented_to: str
    change_name: str
    description: str
    reason: str
    cost_items: list

class QueryRequest(BaseModel):
    question: str

def create_connection():
    """Create a connection to the SQLite database."""
    db_path = os.path.abspath('../database/change_requests.db')
    print(f"Connecting to database at {db_path}")
    try:
        conn = sqlite3.connect(db_path)
        print("Database connection established.")
        return conn
    except Error as e:
        print(f"Database connection error: {e}")
        return None

def create_table():
    """Create the change_requests table if it doesn’t exist."""
    conn = create_connection()
    if conn:
        try:
            c = conn.cursor()
            c.execute('''CREATE TABLE IF NOT EXISTS change_requests
                         (id INTEGER PRIMARY KEY AUTOINCREMENT,
                          project_name TEXT,
                          change_number TEXT,
                          requested_by TEXT,
                          date_of_request DATE,
                          presented_to TEXT,
                          change_name TEXT,
                          description TEXT,
                          reason TEXT,
                          cost_items TEXT,
                          category TEXT,
                          timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
            conn.commit()
            print("Table created successfully or already exists.")
        except Error as e:
            print(f"Table creation error: {e}")
        finally:
            conn.close()
    else:
        print("Failed to create table: No database connection.")

create_table()

def call_together_api(prompt: str, max_tokens: int = 500, temperature: float = 0.0, stop: list = ["\n\n"]):
    """Helper function to call the Together AI API."""
    try:
        response = requests.post(
            "https://api.together.xyz/v1/completions",
            headers={
                "Authorization": f"Bearer {TOGETHER_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
                "prompt": prompt,
                "max_tokens": max_tokens,
                "temperature": temperature,
                "top_p": 0.95,
                "stop": stop
            }
        )
        response.raise_for_status()
        result = response.json()
        return result.get("choices", [{}])[0].get("text", "").strip()
    except requests.RequestException as e:
        print(f"Together API error: {e}")
        return f"API error: {e}"

def categorize_description(description: str) -> str:
    """Categorize the description using Together AI API."""
    categories = ["hardware issue", "software issue", "personnel issue", "other"]
    prompt = (
        f"Classify the following description the best that you can. Here are some example categories: "
        f"hardware issue, software issue, personnel issue, other. "
        f"You are not limited to the list. "
        f"Description: {description} Category:"
    )
    generated_text = call_together_api(prompt, max_tokens=10, stop=["\n"])
    if isinstance(generated_text, str) and "API error" in generated_text:
        print(f"Description: '{description}' categorized as 'other' due to API error.")
        return "other"
    for category in categories:
        if category in generated_text.lower():
            print(f"Description: '{description}' categorized as '{category}'.")
            return category
    print(f"Description: '{description}' categorized as 'other' (no match found).")
    return "other"

@app.post("/change_requests")
def create_change_request(change_request: ChangeRequest):
    """Create a new change request with automated categorization."""
    print("Creating new change request...")
    category = categorize_description(change_request.description)
    cost_items_json = json.dumps(change_request.cost_items)

    conn = create_connection()
    if not conn:
        print("Failed to create change request: No database connection.")
        raise HTTPException(status_code=500, detail="Database connection error")
    try:
        c = conn.cursor()
        c.execute(
            "INSERT INTO change_requests (project_name, change_number, requested_by, date_of_request, presented_to, change_name, description, reason, cost_items, category) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (change_request.project_name, change_request.change_number, change_request.requested_by, change_request.date_of_request, change_request.presented_to, change_request.change_name, change_request.description, change_request.reason, cost_items_json, category)
        )
        conn.commit()
        print(f"Change request created with ID {c.lastrowid} and category '{category}'.")
        return {"message": "Change request created", "id": c.lastrowid, "category": category}
    except Error as e:
        print(f"Database error during change request creation: {e}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        conn.close()

def load_change_requests():
    """Load change requests from the database into a DataFrame."""
    print("Loading change requests from database...")
    conn = create_connection()
    if conn:
        try:
            print("Executing SQL query...")
            df = pd.read_sql_query("SELECT * FROM change_requests", conn)
            print(f"Loaded {len(df)} rows from database.")
            return df
        except Exception as e:
            print(f"Error loading data: {e}")
            return pd.DataFrame()
        finally:
            conn.close()
    else:
        print("Could not connect to database.")
        return pd.DataFrame()

def convert_df_to_text(df):
    """Convert DataFrame to text for inclusion in the prompt."""
    print("Converting DataFrame to text...")
    total_rows = len(df)
    columns = ", ".join(df.columns)
    data_text = f"Database: change_requests\nTotal Entries: {total_rows}\nColumns: {columns}\n\n"
    for i, (_, row) in enumerate(df.iterrows(), 1):
        data_text += f"Change Request {i}:\n"
        for col in df.columns:
            data_text += f"  **{col}**: {row[col]}\n"
        data_text += "\n"
    print(f"Generated text with {total_rows} rows, length: {len(data_text)} characters.")
    return data_text

def create_prompt(database_text, question):
    """Create the prompt for the LLM."""
    print("Creating prompt...")
    max_db_length = 26000  # ~7,000 tokens, leaving room for prompt overhead
    if len(database_text) > max_db_length:
        database_text = database_text[:max_db_length] + "... [truncated]"
        print(f"Warning: Database text truncated to {max_db_length} characters.")
    prompt = f"""You are a precise database assistant. Answer the user's question based on the provided database content. Follow these rules:
- Provide clear and concise answers using all available data.
- Use 'Total Entries' for total counts.
- For queries about 'issues', check the '**category**' field unless another field (e.g., '**description**') is specified.
- For lists or detailed responses, provide complete information.

Database content:
{database_text}

Question: {question}

Answer:"""
    print(f"Prompt created, length: {len(prompt)} characters.")
    return prompt

def get_llm_response(question: str) -> str:
    """Generate response from the LLM based on the user's question."""
    print(f"Processing question: {question}")
    df = load_change_requests()
    if df.empty:
        print("Database is empty or could not be loaded.")
        return "Error: Could not load database."
    database_text = convert_df_to_text(df)
    prompt = create_prompt(database_text, question)
    print("Calling Together API...")
    answer = call_together_api(prompt)
    print(f"Received response: {answer}")
    return answer

@app.post("/query")
def query_database(request: QueryRequest):
    """Endpoint to query the database using the LLM."""
    print("Received query request.")
    try:
        response = get_llm_response(request.question)
        if response.startswith("API error"):
            print(f"Query failed: {response}")
            raise HTTPException(status_code=500, detail=response)
        print("Query successful.")
        return {"response": response}
    except Exception as e:
        print(f"Query endpoint error: {e}")
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")