import hashlib
import hmac
import time
import requests
from typing import Dict, Any

from bot.logging_config import logger

class BinanceAPIError(Exception):
    """
    Custom exception for Binance API errors.
    Captures the HTTP status code and the JSON error response
    from Binance (e.g., {"code": -1121, "msg": "Invalid symbol."}).
    """
    def __init__(self, response, status_code, text):
        self.response = response
        self.status_code = status_code
        self.text = text
        super().__init__(f"Binance API Error [{status_code}]: {text}")


class BinanceFuturesClient:
    """
    Client wrapper for interacting securely with the Binance Futures Testnet API.
    Handles authentication, HMAC SHA256 signature generation, and HTTP request
    dispatching with robust error handling.
    """

    BASE_URL = "https://testnet.binancefuture.com"  

    def __init__(self, api_key: str, api_secret: str):
        self.api_key = api_key
        self.api_secret = api_secret

        # Persistent session for performance
        self.session = requests.Session()
        self.session.headers.update({"X-MBX-APIKEY": self.api_key})

    def _generate_signature(self, query_string: str) -> str:
        """Generate HMAC SHA256 signature required by Binance."""
        return hmac.new(
self.api_secret.encode("utf-8"),
            query_string.encode("utf-8"),
            hashlib.sha256
        ).hexdigest()

    def _get_timestamp(self) -> int:
        """Return current timestamp in milliseconds."""
        return int(time.time() * 1000)

    def _dispatch_request(self, method: str, endpoint: str, signed: bool = False, **kwargs) -> Dict[str, Any]:
        url = self.BASE_URL + endpoint
        params = kwargs.pop("params", {})

        if signed:
            params["timestamp"] = self._get_timestamp()
            params = {k: str(v) for k, v in params.items()}
            query_string = "&".join([f"{k}={v}" for k, v in sorted(params.items())])
            signature = self._generate_signature(query_string)
            url = f"{url}?{query_string}&signature={signature}"
            params = None  # prevent double appending

        try:
            logger.info(f"Sending {method} request to {endpoint}")
            logger.debug(f"Params: {params}")

            response = self.session.request(method, url, params=params, timeout=5, **kwargs)
            response.raise_for_status()

            data = response.json()
            logger.debug(f"Response: {data}")

            
            if isinstance(data, dict) and "code" in data and data["code"] < 0:
                logger.error(f"Binance API Error: {data}")
                raise BinanceAPIError(response, response.status_code, data.get("msg", "Unknown error"))

            return data

        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP Error: {e.response.status_code} - {e.response.text}")
            raise BinanceAPIError(e.response, e.response.status_code, e.response.text)
        except requests.exceptions.ConnectionError as e:
            logger.error(f"Connection Error: {e}")
            raise Exception("Network Error: Could not connect to Binance Testnet.")
        except requests.exceptions.Timeout as e:
            logger.error(f"Timeout Error: {e}")
            raise Exception("Timeout Error: The request to Binance Testnet timed out.")
        except requests.exceptions.RequestException as e:
            logger.error(f"Request Error: {e}")
            raise Exception(f"Request Error: {e}")

    def get(self, endpoint: str, signed: bool = False, **kwargs) -> Dict[str, Any]:
        """Convenience wrapper for GET requests."""
        return self._dispatch_request("GET", endpoint, signed, **kwargs)

    def post(self, endpoint: str, signed: bool = True, **kwargs) -> Dict[str, Any]:
        """Convenience wrapper for POST requests (usually signed)."""
        return self._dispatch_request("POST", endpoint, signed, **kwargs)

    def ping(self) -> Dict[str, Any]:
        """Test connectivity to Binance Futures Testnet."""
        return self.get("/fapi/v1/ping", signed=False)
