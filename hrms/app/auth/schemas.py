from pydantic import BaseModel, EmailStr


class RegisterRequest(BaseModel):
    token: str
    password: str 


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class ChangePasswordRequest(BaseModel):
    old_password: str
    new_password: str


class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class VerifyOTPRequest(BaseModel):
    email: EmailStr
    otp: str


class ResetPasswordRequest(BaseModel):
    email: EmailStr
    new_password: str
    # old_password: str
    

class AuthUserResponse(BaseModel):
    id: int
    employee_id: int

    class Config:
        from_attributes = True