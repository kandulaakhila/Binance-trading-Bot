from typing import Literal

VALID_SIDES = {"BUY", "SELL"}
VALID_ORDER_TYPES = {"MARKET", "LIMIT", "STOP"}

class ValidationError(ValueError):
    """Custom exception for validation errors."""
    pass

def validate_symbol(symbol: str) -> str:
    """
    Validates and formats the trading symbol.
    
    Args:
        symbol (str): The trading pair (e.g., 'btcusdt').
        
    Returns:
        str: The uppercase, formatted symbol (e.g., 'BTCUSDT').
        
    Raises:
        ValidationError: If the symbol is not a valid string.
    """
    if not symbol or not isinstance(symbol, str):
        raise ValidationError("Symbol must be a non-empty string")
    return symbol.upper()

def validate_side(side: str) -> Literal["BUY", "SELL"]:
    """
    Validates the order side against Binance's accepted enum values.
    
    Args:
        side (str): The user's requested side (e.g., 'buy', 'SELL').
        
    Returns:
        Literal["BUY", "SELL"]: The strictly formatted side enum.
        
    Raises:
        ValidationError: If the side is not in VALID_SIDES.
    """
    side_upper = str(side).upper()
    if side_upper not in VALID_SIDES:
        raise ValidationError(f"Invalid side '{side}'. Must be one of {VALID_SIDES}")
    return side_upper # type: ignore

def validate_order_type(order_type: str) -> Literal["MARKET", "LIMIT", "STOP"]:
    """
    Validates the order type against the bot's supported types.
    
    Args:
        order_type (str): The requested order type.
        
    Returns:
        Literal["MARKET", "LIMIT", "STOP"]: The uppercase order type enum.
        
    Raises:
        ValidationError: If the order type is not supported.
    """
    type_upper = str(order_type).upper()
    if type_upper not in VALID_ORDER_TYPES:
        raise ValidationError(f"Invalid order type '{order_type}'. Must be one of {VALID_ORDER_TYPES}")
    return type_upper # type: ignore

def validate_quantity(quantity: float) -> float:
    """
    Validates that the requested order quantity is a usable mathematical value.
    Binance API requires positive, non-zero quantities.
    
    Args:
        quantity (float): The amount to trade.
        
    Returns:
        float: The parsed and validated float quantity.
        
    Raises:
        ValidationError: If the quantity is zero, negative, or not a number.
    """
    try:
        qty = float(quantity)
        if qty <= 0:
            raise ValueError
        return qty
    except (ValueError, TypeError):
        raise ValidationError(f"Invalid quantity '{quantity}'. Must be a positive number.")

def validate_price(price: float) -> float:
    """
    Validates that the target price is a usable mathematical value.
    Used exclusively for LIMIT and STOP orders.
    
    Args:
        price (float): The target execution or trigger price.
        
    Returns:
        float: The parsed and validated float price.
        
    Raises:
        ValidationError: If the target price is zero, negative, or not a number.
    """
    try:
        p = float(price)
        if p <= 0:
            raise ValueError
        return p
    except (ValueError, TypeError):
        raise ValidationError(f"Invalid price '{price}'. Must be a positive number.")
