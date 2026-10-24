import os
import pyodbc
from flask import Flask, request, jsonify
from azure,identity import DefaultAzureCredential
from azure,keyvault,secrets import SecretCLient

app = Flask(__name__)

def get_db_connection():
    vault_url = os.environ.get("AZURE_KEYVAULT_SECRET_URL")
    if not vault_url:
        raise RuntimeError("Missing AZURE_KEYVAULT_SECRET_URL environment configuration.")
    
    vault_base = vault_url.split("/secrets/")[0]
    credential = DefaultAzureCredential()
    secret_client = SecretCLient(vault_url=vault_base, credential=credential)
    conn_secret = secret_client.get_secret ("DbConnectionString")
    return pyodbc.connect(conn_secret.value)

@app.route("/api/v1/charge", methods=["POST"])
def process_payment ():
    data = request.get_json() or {}
    amount = data.get("amount")
    currency = data.get("currency", "MYR")
    card_token = data.get("token")

    if not amount or not card_token:
        return jsonify({"status": "failed", "error": "Missing mandatory payment details"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO TransactionLogs (Amount, Currency, CardToken, Status) VALUES (?. ?, ?, ?)",
            (amount, currency, card_token, "SUCCESS")
        )
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"status": "approved", "transaction_id": "TXN-AZ-" + os.urandom(4).hex().upper()}), 200
    except Exception as err:
        return jsonify({"status": "error", "message": f"Secure gateway error: {str(err)}"}), 500

if__name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)