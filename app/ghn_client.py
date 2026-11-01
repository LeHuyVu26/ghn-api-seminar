from typing import Any, Dict, Optional
from . import config
import httpx


class GHNError(Exception):
    def __init__(self, message: str, status_code: int = 502, code: Optional[int] = None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.code = code


class GHNClient:
    def __init__(self) -> None:
        self.base_url = config.BASE_URL
        self.shop_id = config.GHN_SHOP_ID
        self.headers = {
            "Token": config.GHN_TOKEN,
            "ShopId": str(config.GHN_SHOP_ID),
            "Content-Type": "application/json",
        }

    # ---------- HTTP core ----------
    async def _request(self, method: str, path: str, *,
                       json: Optional[dict] = None, params: Optional[dict] = None) -> Any:
        if not config.GHN_TOKEN:
            raise GHNError("Chưa cấu hình GHN_TOKEN trong file .env", 500)
        try:
            async with httpx.AsyncClient(timeout=15) as client:
                resp = await client.request(
                    method, f"{self.base_url}{path}",
                    headers=self.headers, json=json, params=params,
                )
        except httpx.RequestError as e:
            raise GHNError(f"Không kết nối được GHN: {e}", 503)

        try:
            body = resp.json()
        except ValueError:
            raise GHNError(f"GHN trả về dữ liệu không hợp lệ ({resp.status_code})", 502)

        # GHN trả {"code": 200, "message": "Success", "data": {...}}
        if resp.status_code != 200 or body.get("code") != 200:
            raise GHNError(
                body.get("code_message_value") or body.get("message", "GHN error"),
                resp.status_code if resp.status_code != 200 else 400,
                body.get("code"),
            )
        return body.get("data")

    # ---------- Master data ----------
    async def provinces(self):
        return await self._request("GET", "/master-data/province")

    async def districts(self, province_id: int):
        return await self._request("POST", "/master-data/district", json={"province_id": province_id})

    async def wards(self, district_id: int):
        return await self._request("POST", "/master-data/ward", json={"district_id": district_id})

    # ---------- Shipping fee ----------
    async def available_services(self, to_district_id: int):
        return await self._request("POST", "/v2/shipping-order/available-services", json={
            "shop_id": self.shop_id,
            "from_district": config.FROM_DISTRICT_ID,
            "to_district": to_district_id,
        })

    async def calculate_fee(self, data: Dict[str, Any]):
        payload = {
            "from_district_id": config.FROM_DISTRICT_ID,
            "from_ward_code": config.FROM_WARD_CODE,
            **data,
        }
        return await self._request("POST", "/v2/shipping-order/fee", json=payload)

    # ---------- Order ----------
    async def create_order(self, data: Dict[str, Any]):
        payload = {
            "from_district_id": config.FROM_DISTRICT_ID,
            "from_ward_code": config.FROM_WARD_CODE,
            **data,
        }
        return await self._request("POST", "/v2/shipping-order/create", json=payload)

    async def order_detail(self, order_code: str):
        """Dùng cho tracking: trả về status + log của đơn."""
        return await self._request("POST", "/v2/shipping-order/detail", json={"order_code": order_code})

    async def cancel_order(self, order_code: str):
        return await self._request("POST", "/v2/switch-status/cancel", json={"order_codes": [order_code]})

ghn = GHNClient()