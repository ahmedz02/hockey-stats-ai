import pandas as pd
import openai
from dotenv import load_dotenv
import os

load_dotenv()

openai.api_key= os.getenv("OPENAI_API_KEY")

# Load the dataset
df = pd.read_csv("nhl_player_stats.csv")

def ai_generate_pandas_code(query):
    """Uses AI to generate pandas code for a user query."""
    prompt = f"""
    You are an AI that converts user hockey stats queries into pandas operations.
    DataFrame (df) has these columns: {', '.join(df.columns)}

    User Query: "{query}"
    Generate Python pandas code (only code, no explanation) to get the requested data.
    """
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": prompt}]
    )
    
    pandas_code = response["choices"][0]["message"]["content"]
    return pandas_code.strip()

def process_query(query):
    """Uses AI to generate pandas code and execute it."""
    try:
        pandas_code = ai_generate_pandas_code(query)
        print(f"\nGenerated Code:\n{pandas_code}")  # For debugging
        
        # Execute the pandas command dynamically
        result = eval(pandas_code, {"df": df, "pd": pd})
        
        # Display result
        print("\nQuery Result:")
        print(result)
    
    except Exception as e:
        print(f"\nError: {e}")
        print("Sorry, I couldn't process that query.")

# CLI Loop
while True:
    user_query = input("\nAsk me a hockey stats question (or type 'exit' to quit): ")
    if user_query.lower() == "exit":
        print("Goodbye!")
        break
    process_query(user_query)