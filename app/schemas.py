from typing import List, Optional
from pydantic import BaseModel, Field


class FeeRequest(BaseModel):
    to_district_id: int = Field(..., examples=[1442])
    to_ward_code: str = Field(..., examples=["20314"])
    weight: int = Field(..., ge=1, description="Gram", examples=[500])
    length: int = Field(20, ge=1, description="cm")
    width: int = Field(15, ge=1, description="cm")
    height: int = Field(10, ge=1, description="cm")
    insurance_value: int = Field(0, ge=0, description="Giá trị hàng hóa (VND) để bảo hiểm")
    service_type_id: int = Field(2, description="2 = Hàng nhẹ (<20kg), 5 = Hàng nặng")


class OrderItem(BaseModel):
    name: str = Field(..., examples=["Áo thun"])
    code: Optional[str] = Field(None, examples=["SKU001"])
    quantity: int = Field(1, ge=1)
    price: int = Field(0, ge=0)
    weight: int = Field(200, ge=1, description="Gram")


class CreateOrderRequest(BaseModel):
    to_name: str = Field(..., examples=["Nguyễn Văn A"])
    to_phone: str = Field(..., examples=["0987654321"])
    to_address: str = Field(..., examples=["72 Thành Thái, Phường 14, Quận 10, TP.HCM"])
    to_ward_code: str = Field(..., examples=["20308"])
    to_district_id: int = Field(..., examples=[1444])
    cod_amount: int = Field(0, ge=0, description="Tiền thu hộ (VND)")
    weight: int = Field(..., ge=1, examples=[500])
    length: int = 20
    width: int = 15
    height: int = 10
    insurance_value: int = 0
    service_type_id: int = 2
    payment_type_id: int = Field(2, description="1 = Shop trả phí, 2 = Người nhận trả phí")
    required_note: str = Field(
        "KHONGCHOXEMHANG",
        description="CHOTHUHANG | CHOXEMHANGKHONGTHU | KHONGCHOXEMHANG",
    )
    note: Optional[str] = None
    content: str = Field("Quần áo", description="Mô tả hàng hóa")
    items: List[OrderItem] = []
