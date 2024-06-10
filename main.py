import os
import pandas as pd
import google.generativeai as genai
from dotenv import load_dotenv
import ollama
import logging

# Load environment variables
load_dotenv()

# Configure Google API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Path to the Excel file
excel_file_path = r'C:\Users\user\Desktop\bankai\accounts-transactions.xls'

# Read the Excel file, skipping the first 7 rows
df = pd.read_excel(excel_file_path, skiprows=7, header=None)

# Assign the headers
df.columns = ['date', 'description', 'credit', 'debit', 'balance']


def gemini(text):
    try:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(
            prompt=['''You are a professional accountant tasked with assigning accounts to bank transactions based on accounting standards. Here is a row extracted from a bank transaction Excel sheet with the following headers:
    - Date
    - Description
    - Credit
    - Debit
    - Balance
    Please note:
    - If the transaction is a credit, the amount is coming into our account.
    - If the transaction is a debit, the amount is going out of our account.
    Based on accounting principles, please suggest the best account to assign this transaction to. Provide a direct answer without explanation.
    ''', text]
        )

        response_text = response[0].text
        logging.info(f"Gemini Response: {response_text}")
        return response_text
    except Exception as e:
        logging.error(f"Error during Gemini processing: {e}")
        return None


def ollama_ai(text):
    try:
        response = ollama.chat(model='llama3', messages=[
            {
                'role': 'user',
                'content': f'{text}\nYou are a professional accountant tasked with assigning accounts to bank transactions based on accounting standards. Here is a row extracted from a bank transaction Excel sheet with the following headers:\n'
                '- Date\n'
                '- Description\n'
                '- Credit\n'
                '- Debit\n'
                '- Balance\n'
                '\n'
                'Please note:\n'
                '- If the transaction is a credit, the amount is coming into our account.\n'
                '- If the transaction is a debit, the amount is going out of our account.\n'
                '\n'
                'Based on accounting principles, please suggest the best account to assign this transaction to. Provide a direct answer without explanation.\n'
            },
        ])

        response_content = response['message']['content']
        logging.info(f"Ollama Response: {response_content}")
        return response_content

    except Exception as e:
        logging.error(f"Error during Ollama processing: {e}")
        return None


# Prompt the user to choose the model
print("Choose the model to process the data with:")
print("1. Gemini")
print("2. Ollama")
choice = input("Enter the number of the model you want to use (1 or 2): ")

# Validate user input
if choice not in ['1', '2']:
    logging.error(
        "Invalid choice. Please run the script again and enter 1 or 2.")
    exit()

# Set the chosen model function
model_function = gemini if choice == '1' else ollama_ai

results = []

for index, row in df.iterrows():
    # Create a string representation of the row data
    row_data = f"date: {row['date']}, description: {row['description']}, credit: {row['credit']}, debit: {row['debit']}, balance: {row['balance']}"

    result = model_function(row_data)
    if result:
        results.append(result)
    else:
        results.append('')
        logging.error(f"Failed to process row: {row_data}")

# Add the results as a new column to the original DataFrame
df['account'] = results

# Print the processed DataFrame
print("\nProcessed DataFrame:")
print(df)

# Save the new DataFrame to an Excel file
output_file_path = r'C:\Users\user\Desktop\bankai\transactions-with-accounts.xlsx'
try:
    df.to_excel(output_file_path, index=False, engine='xlsx')
    logging.info(f"DataFrame successfully saved to {output_file_path}")
except Exception as e:
    logging.error(f"Error saving DataFrame to file: {e}")

logging.info("Script execution completed.")
