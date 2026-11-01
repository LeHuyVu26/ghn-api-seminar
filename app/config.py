import os
from dotenv import load_dotenv

load_dotenv()

GHN_ENV = os.getenv("GHN_ENV", "dev")
BASE_URL = (
    "https://dev-online-gateway.ghn.vn/shiip/public-api"
    if GHN_ENV == "dev"
    else "https://online-gateway.ghn.vn/shiip/public-api"
)
GHN_TOKEN = os.getenv("GHN_TOKEN", "")
GHN_SHOP_ID = int(os.getenv("GHN_SHOP_ID", "0"))
FROM_DISTRICT_ID = int(os.getenv("GHN_FROM_DISTRICT_ID", "1454"))
FROM_WARD_CODE = os.getenv("GHN_FROM_WARD_CODE", "21211")