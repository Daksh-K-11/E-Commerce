from .user_schema import UserCreate, UserOut

class SellerCreate(UserCreate):
    store_name: str
    business_license: str
    tax_id: str


class SellerOut(UserOut):
    store_name: str
    business_license: str
    tax_id: str