from pydantic import BaseModel, EmailStr, Field

class SignupRequest(BaseModel):
    name: str = Field(min_length=1, max_length=160)
    email: EmailStr
    password: str = Field(min_length=12, max_length=200)

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = 'bearer'

class AskRequest(BaseModel):
    question: str = Field(min_length=2, max_length=4000)
    document_id: str | None = None

class Claim(BaseModel):
    text: str
    unit_id: str
    page: int
    modality: str

class AnswerResponse(BaseModel):
    answer: str
    claims: list[Claim]
    found: bool
    warning: str = 'machine-generated, verify against sources'
