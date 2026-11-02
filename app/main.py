from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import RedirectResponse, JSONResponse

from .ghn_client import GHNError, ghn
from .schemas import CreateOrderRequest, FeeRequest

app = FastAPI(
    title="GHN Logistics Service",
    description=(
        "Microservice demo tích hợp **GHN (Giao Hàng Nhanh) API**: "
        "tính phí vận chuyển, tạo đơn, theo dõi vận đơn."
    ),
    version="1.0.0",
)


@app.exception_handler(GHNError)
async def ghn_error_handler(request, exc: GHNError):
    return JSONResponse(status_code=exc.status_code,
                        content={"error": exc.message, "ghn_code": exc.code})


@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse("/docs")

# ---------------- Master data ----------------
@app.get("/master-data/provinces", tags=["Master data"], summary="Danh sách tỉnh/thành")
async def provinces():
    return await ghn.provinces()


@app.get("/master-data/districts", tags=["Master data"], summary="Quận/huyện theo tỉnh")
async def districts(province_id: int = Query(..., examples=[202])):
    return await ghn.districts(province_id)


@app.get("/master-data/wards", tags=["Master data"], summary="Phường/xã theo quận")
async def wards(district_id: int = Query(..., examples=[1444])):
    return await ghn.wards(district_id)


# ---------------- 1. Shipping fee ----------------
@app.post("/shipping/fee", tags=["1. Shipping fee"], summary="Ước tính phí")
async def shipping_fee(req: FeeRequest):
    data = req.model_dump()

    if data["weight"] >= 20000:
        data["service_type_id"] = 5
        data["items"] = [
            {
                "name": "Hàng hóa",
                "quantity": 1,
                "weight": data["weight"],
                "length": data["length"],
                "width": data["width"],
                "height": data["height"],
                "price": data.get("insurance_value", 0)
            }
        ]
    else:
        data["service_type_id"] = 2

    return await ghn.calculate_fee(data)    

# ---------------- 2. Order creation ----------------
@app.post("/orders", tags=["2. Order creation"], summary="Tạo đơn vận chuyển", status_code=201)
async def create_order(req: CreateOrderRequest):
    payload = req.model_dump(exclude_none=True)
    if not payload.get("items"):
        payload["items"] = [{"name": req.content, "quantity": 1, "weight": req.weight}]
    return await ghn.create_order(payload)


@app.post("/orders/{order_code}/cancel", tags=["2. Order creation"], summary="Huỷ đơn")
async def cancel_order(order_code: str):
    return await ghn.cancel_order(order_code)


# ---------------- 3. Tracking ----------------
@app.get("/orders/{order_code}/tracking", tags=["3. Shipment tracking"],
         summary="Theo dõi trạng thái vận đơn")
async def tracking(order_code: str):
    data = await ghn.order_detail(order_code)
    if not data:
        raise HTTPException(404, "Không tìm thấy đơn hàng")
    return {
        "order_code": data.get("order_code"),
        "status": data.get("status"),
        "log": data.get("log", []),
        "raw": data,
    }
