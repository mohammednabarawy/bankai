# BankAi

BankAi is a Python script designed to assist professional accountants in assigning accounts to bank transaction records extracted from an Excel file. It utilizes two AI models, Google's Gemini and Ollama, to suggest the best accounts for each transaction based on provided details.

## Features

- **Flexible Model Selection** : Choose between Google's Gemini and Ollama for account assignment.
- **Robust Error Handling** : Handles temporary failures gracefully and logs errors for troubleshooting.
- **Excel Integration** : Reads transaction data from an Excel file and outputs results with assigned accounts.

## Prerequisites

- Python 3.x
- Libraries: pandas, google.generativeai, ollama, dotenv

## Setup

1. Clone this repository to your local machine.
2. Install the required Python libraries using `pip install -r requirements.txt`.
3. Obtain API keys for Google's GenerativeAI and configure them in a `.env` file (refer to `.env.example`).

## Usage

1. Place your bank transaction Excel file (`accounts-transactions.xls`) in the root directory.
2. Run the script `bank_transaction_assignment.py`.
3. Choose the desired model (Gemini or Ollama) for account assignment.
4. The script will process each transaction record, assign accounts, and output the results to the console.
5. The processed data with assigned accounts will be saved as `transactions-with-accounts.xls`.

## Contributing

Contributions are welcome! If you have any suggestions or improvements, please submit a pull request.
