from pydantic import BaseModel 

class User(BaseModel):
    name: str
    tgid: str
    pay_state: str