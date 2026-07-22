from typing import Literal

from pydantic import BaseModel, Field

RegisterableRole = Literal["employee", "manager", "administrator"]


class RegisterRequest(BaseModel):
    email: str = Field(min_length=3, max_length=255)
    password: str = Field(min_length=1, max_length=256)
    role: RegisterableRole


class RegisterResponse(BaseModel):
    message: str


class VerifyEmailRequest(BaseModel):
    token: str


class LoginRequest(BaseModel):
    email: str
    password: str


class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    access_token_expires_at: int


class RefreshRequest(BaseModel):
    refresh_token: str


class RefreshResponse(BaseModel):
    access_token: str
    refresh_token: str
    access_token_expires_at: int


class ForgotPasswordRequest(BaseModel):
    email: str


class GenericMessageResponse(BaseModel):
    message: str


class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str


class MeResponse(BaseModel):
    subject_id: str
    session_id: str
    roles: list[str]
    permissions: list[str]


class AreaSummary(BaseModel):
    key: str
    label: str
    path: str
    permission: str
    available: bool


class HomeResponse(BaseModel):
    subject_id: str
    roles: list[str]
    areas: list[AreaSummary]


class ProfileResponse(BaseModel):
    subject_id: str
    roles: list[str]


class ReportsResponse(BaseModel):
    message: str


class AdministrationResponse(BaseModel):
    message: str
