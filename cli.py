import json
import argparse
import sys
import os
from dotenv import load_dotenv

from bot.client import BinanceFuturesClient, BinanceAPIError
from bot.orders import place_market_order, place_limit_order, place_stop_order
from bot.validators import ValidationError
from bot.logging_config import logger

def main():
    """
    Main entry point for the Binance Futures CLI Trading Bot.
    
    Parses command-line arguments to determine the desired order type 
    (MARKET, LIMIT, STOP) and parameters (symbol, side, quantity, price).
    Authenticates with Binance via `.env` credentials, dispatches the order 
    to the appropriate logic handler, and formats the final API response 
    for the user's terminal.
    """
    parser = argparse.ArgumentParser(
        description="Binance Futures Testnet Trading Bot",
        formatter_class=argparse.RawTextHelpFormatter
    )

    # Subparsers isolate arguments specific to different order types
    subparsers = parser.add_subparsers(dest="order_type", help="Order type to place")
    subparsers.required = True

    # 1. MARKET Order Arguments
    market_parser = subparsers.add_parser("MARKET", help="Place a MARKET order")
    market_parser.add_argument("--symbol", required=True, help="Trading pair symbol (e.g., BTCUSDT)")
    market_parser.add_argument("--side", required=True, choices=["BUY", "SELL"], help="Order side (BUY or SELL)")
    market_parser.add_argument("--quantity", required=True, type=float, help="Order quantity")

    # 2. LIMIT Order Arguments (Requires --price)
    limit_parser = subparsers.add_parser("LIMIT", help="Place a LIMIT order")
    limit_parser.add_argument("--symbol", required=True, help="Trading pair symbol (e.g., BTCUSDT)")
    limit_parser.add_argument("--side", required=True, choices=["BUY", "SELL"], help="Order side (BUY or SELL)")
    limit_parser.add_argument("--quantity", required=True, type=float, help="Order quantity")
    limit_parser.add_argument("--price", required=True, type=float, help="Limit price")

    # 3. STOP Order Arguments (Requires --price as trigger)
    stop_parser = subparsers.add_parser("STOP", help="Place a STOP_MARKET order")
    stop_parser.add_argument("--symbol", required=True, help="Trading pair symbol (e.g., BTCUSDT)")
    stop_parser.add_argument("--side", required=True, choices=["BUY", "SELL"], help="Order side (BUY or SELL)")
    stop_parser.add_argument("--quantity", required=True, type=float, help="Order quantity")
    stop_parser.add_argument("--price", required=True, type=float, help="Stop trigger price")

    args = parser.parse_args()

    # Authentication Phase: Load environment variables safely
    load_dotenv()
    api_key = os.getenv("BINANCE_API_KEY")
    api_secret = os.getenv("BINANCE_API_SECRET")

    # Ensure credentials exist before sending network requests
    if not api_key or not api_secret:
        logger.error("API credentials not found. Please set BINANCE_API_KEY and BINANCE_API_SECRET in your .env file.")
        sys.exit(1)

    logger.info("Initializing Binance Futures Testnet Client...")
    client = BinanceFuturesClient(api_key=api_key, api_secret=api_secret)

    try:
        # Execution Phase: Route request to correct logic handler based on subparser
        if args.order_type == "MARKET":
            print(f"\n📋 Order Request Summary:")
            print(f"   Type:     MARKET")
            print(f"   Symbol:   {args.symbol}")
            print(f"   Side:     {args.side}")
            print(f"   Quantity: {args.quantity}")
            response = place_market_order(client, args.symbol, args.side, args.quantity)
        
        elif args.order_type == "LIMIT":
            print(f"\n📋 Order Request Summary:")
            print(f"   Type:     LIMIT")
            print(f"   Symbol:   {args.symbol}")
            print(f"   Side:     {args.side}")
            print(f"   Quantity: {args.quantity}")
            print(f"   Price:    {args.price}")
            response = place_limit_order(client, args.symbol, args.side, args.quantity, args.price)

        elif args.order_type == "STOP":
            print(f"\n📋 Order Request Summary:")
            print(f"   Type:     STOP_MARKET")
            print(f"   Symbol:   {args.symbol}")
            print(f"   Side:     {args.side}")
            print(f"   Quantity: {args.quantity}")
            print(f"   Stop Trigger Price: {args.price}")
            response = place_stop_order(client, args.symbol, args.side, args.quantity, args.price)

        # Print order response details
        print(f"\n Order Placed Successfully!")
        print(f"   Order ID:      {response.get('orderId', 'N/A')}")
        print(f"   Status:        {response.get('status', 'N/A')}")
        print(f"   Symbol:        {response.get('symbol', 'N/A')}")
        print(f"   Side:          {response.get('side', 'N/A')}")
        print(f"   Type:          {response.get('type', 'N/A')}")
        print(f"   Executed Qty:  {response.get('executedQty', '0')}")
        print(f"   Average Price: {response.get('avgPrice', '0.0')}")
        
    except ValidationError as e:
        logger.error(f"Input Validation Error: {e}")
        print(f"\n❌ Validation Error: {e}")
        sys.exit(1)
        
    except BinanceAPIError as e:
        try:
            # Attempt to parse the Binance JSON error body
            error_data = json.loads(e.text)
            msg = error_data.get("msg", "Unknown error")
            code = error_data.get("code", "N/A")
            print(f"\n❌ Binance API Rejected Order!")
            print(f"   Reason: [{code}] {msg}")
        except json.JSONDecodeError:
            # Fallback if the error isn't valid JSON
            print(f"\n❌ Binance API Error [{e.status_code}]: {e.text}")
        sys.exit(1)
        
    except Exception as e:
        logger.error(f"Execution Error: {e}")
        print(f"\n❌ Error processing order: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
