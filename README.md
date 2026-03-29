 🤖 Binance Futures Testnet Trading Bot

A lightweight, production-ready **Python CLI application** to place **Market** and **Limit orders** on Binance Futures Testnet (USDT-M).

This project demonstrates **clean architecture**, **secure credential handling**, and **real-world API integration practices**.

---

 🚀 Features

* ✅ Place **Market & Limit Orders**
* 🔐 Secure API key management using `.env`
* ⏱️ Automatic **clock synchronization**
* 📋 Structured **logging system**
* 🧠 Input **validation before API calls**
* 🏗️ Modular and scalable **project structure**

---

 📁 Project Structure

```
trading_bot/
├── bot/
│   ├── __init__.py
│   ├── client.py          # Binance client with clock sync
│   ├── orders.py          # Order execution logic
│   ├── validators.py      # Input validation
│   └── logging_config.py  # Logging setup
├── cli.py                 # CLI entry point
├── .env                   # API credentials (ignored)
├── .gitignore
├── README.md
└── requirements.txt
```

---

 ⚙️ Setup Instructions

 1️⃣ Clone Repository

```
git clone https://github.com/your-username/trading_bot.git
cd trading_bot
```

 2️⃣ Install Dependencies

```
pip install -r requirements.txt
```

 3️⃣ Configure API Keys

Create a `.env` file in the root directory:

```
API_KEY=your_testnet_api_key
API_SECRET=your_testnet_api_secret
```

⚠️ **Important**

* Never upload `.env` to GitHub
* Keep your API keys private

---

 🔑 Get Binance Testnet API Keys

1. Visit: https://testnet.binancefuture.com
2. Register / Login
3. Create API Key → **System Generated**
4. Copy API Key & Secret
5. Use **Faucet** to add test USDT

---

 ▶️ Usage

 🟢 Market Orders

```
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.002
python cli.py --symbol BTCUSDT --side SELL --type MARKET --quantity 0.002
```

---

 🟡 Limit Orders

```
python cli.py --symbol BTCUSDT --side BUY --type LIMIT --quantity 0.002 --price 80000
python cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.002 --price 100000
```

---

 📌 CLI Arguments

| Argument   | Required      | Description    | Example |
| ---------- | ------------- | -------------- | ------- |
| --symbol   | ✅ Yes         | Trading pair   | BTCUSDT |
| --side     | ✅ Yes         | BUY / SELL     | BUY     |
| --type     | ✅ Yes         | MARKET / LIMIT | MARKET  |
| --quantity | ✅ Yes         | Order quantity | 0.002   |
| --price    | ⚠️ Limit only | Order price    | 90000   |

---

 📤 Sample Output

```
--- Order Request Summary ---
Symbol     : BTCUSDT
Side       : BUY
Order Type : MARKET
Quantity   : 0.002
-----------------------------

--- Order Response ---
Order ID     : 12880868466
Status       : NEW
Executed Qty : 0.000
Avg Price    : 0.00
----------------------

✅ Order placed successfully!
```

---

 📋 Logging

All logs are stored in:

```
trading_bot.log
```

Example:

```
INFO  | client | Client initialized. Clock offset: -2ms
INFO  | orders | Placing MARKET BUY order
INFO  | orders | Order response received
```

---

 🛠️ Tech Stack

* Python 3.x
* python-binance
* requests
* python-dotenv

---

 🧠 Key Concepts Implemented

* 🔐 Secure environment variable handling
* ⏱️ Server-client time synchronization
* 🧱 Modular architecture
* 📊 CLI-based interaction
* ✅ Input validation before execution

---

 ⚠️ Important Notes

* This bot is for **Binance Testnet only**
* Do **NOT** use real funds
* Always **restrict API keys with IP** (for production)

---

 👤 Author

**Akhila**
Built as part of **Python Developer Internship Preparation** 
