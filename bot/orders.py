from typing import Dict, Any, Optional
from bot.client import BinanceFuturesClient, BinanceAPIError
from bot.validators import validate_symbol, validate_side, validate_quantity, validate_price
from bot.logging_config import logger

def _format_order_response(response: Dict[str, Any]) -> str:
    """
    Helper function to parse the raw JSON response returned by Binance
    and format it into a clean, human-readable summary block for logging.
    """
    fmt = [
        f"Order ID: {response.get('orderId', 'N/A')}",
        f"Status: {response.get('status', 'N/A')}",
        f"Symbol: {response.get('symbol', 'N/A')}",
        f"Side: {response.get('side', 'N/A')}",
        f"Type: {response.get('type', 'N/A')}",
        f"Executed Qty: {response.get('executedQty', '0')}",
        f"Average Price: {response.get('avgPrice', '0.0')}",
    ]
    return "\n".join(fmt)

def place_market_order(
    client: BinanceFuturesClient, 
    symbol: str, 
    side: str, 
    quantity: float
) -> Dict[str, Any]:
    """
    Places a MARKET order on the Binance Futures Testnet.
    A Market order executes immediately at the currently available market price.
    
    Args:
        client (BinanceFuturesClient): An authenticated API client instance.
        symbol (str): The trading pair (e.g., "BTCUSDT").
        side (str): "BUY" or "SELL".
        quantity (float): The amount of base asset to trade.
        
    Returns:
        Dict[str, Any]: The executed order details from the Binance API.
    """
    
    # 1. Input Validation: Cleanse inputs before wasting an API call
    valid_symbol = validate_symbol(symbol)
    valid_side = validate_side(side)
    valid_qty = validate_quantity(quantity)
    
    # 2. Build Request Payload: Construct the required parameters for Binance
    params = {
        "symbol": valid_symbol,
        "side": valid_side,
        "type": "MARKET",
        "quantity": valid_qty,
        # Force Binance matching engine to return execution stats synchronously
        "newOrderRespType": "RESULT" 
    }
    
    logger.info(f"Attempting to place MARKET order: {params}")
    
    # 2. API Request
    try:
        response = client.post("/fapi/v1/order", signed=True, params=params)
        logger.info(f"MARKET order successful! Details:\n{_format_order_response(response)}")
        return response
    except BinanceAPIError as e:
        logger.error(f"MARKET order failed due to API Error: {e.text}")
        raise
    except Exception as e:
        logger.error(f"MARKET order failed: {e}")
        raise

def place_limit_order(
    client: BinanceFuturesClient, 
    symbol: str, 
    side: str, 
    quantity: float, 
    price: float
) -> Dict[str, Any]:
    """
    Places a LIMIT order on the Binance Futures Testnet.
    A Limit order is placed on the order book and only executes when the 
    market price reaches the user-specified limit price.
    
    Args:
        client (BinanceFuturesClient): An authenticated API client instance.
        symbol (str): The trading pair (e.g., "BTCUSDT").
        side (str): "BUY" or "SELL".
        quantity (float): The amount of base asset to trade.
        price (float): The target maximum/minimum price to execute at.
    """
    
    valid_symbol = validate_symbol(symbol)
    valid_side = validate_side(side)
    valid_qty = validate_quantity(quantity)
    valid_price = validate_price(price)
    
    params = {
        "symbol": valid_symbol,
        "side": valid_side,
        "type": "LIMIT",
        # Binance enforces that LIMIT orders MUST specify 'timeInForce'.
        # 'GTC' (Good Till Cancelled) means the order remains fully on the book
        # until it is fully filled by the market or manually cancelled.
        "timeInForce": "GTC", 
        "quantity": valid_qty,
        "price": valid_price,
        "newOrderRespType": "RESULT" # Request execution details synchronously
    }
    
    logger.info(f"Attempting to place LIMIT order: {params}")
    
    try:
        response = client.post("/fapi/v1/order", signed=True, params=params)
        logger.info(f"LIMIT order successful! Details:\n{_format_order_response(response)}")
        return response
    except BinanceAPIError as e:
        logger.error(f"LIMIT order failed due to API Error: {e.text}")
        raise
    except Exception as e:
        logger.error(f"LIMIT order failed: {e}")
        raise

def place_stop_order(
    client: BinanceFuturesClient, 
    symbol: str, 
    side: str, 
    quantity: float, 
    stop_price: float
) -> Dict[str, Any]:
    """
    Places a STOP_MARKET order on the Binance Futures Testnet.
    A Stop order acts as a trigger mechanism (often used as a stop-loss). 
    Once the market price hits the `stop_price`, a MARKET order is automatically spawned.
    
    Args:
        client (BinanceFuturesClient): An authenticated API client instance.
        symbol (str): The trading pair (e.g., "BTCUSDT").
        side (str): "BUY" or "SELL".
        quantity (float): The amount of base asset to trade.
        stop_price (float): The trigger price that converts this into a market order.
    """
    
    valid_symbol = validate_symbol(symbol)
    valid_side = validate_side(side)
    valid_qty = validate_quantity(quantity)
    valid_stop_price = validate_price(stop_price)
    
    params = {
        "symbol": valid_symbol,
        "side": valid_side,
        "type": "STOP_MARKET",
        "quantity": valid_qty,
        "stopPrice": valid_stop_price,
    }
    
    logger.info(f"Attempting to place STOP_MARKET order: {params}")
    
    try:
        response = client.post("/fapi/v1/order", signed=True, params=params)
        logger.info(f"STOP_MARKET order successful! Details:\n{_format_order_response(response)}")
        return response
    except BinanceAPIError as e:
        logger.error(f"STOP_MARKET order failed due to API Error: {e.text}")
        raise
    except Exception as e:
        logger.error(f"STOP_MARKET order failed: {e}")
        raise
