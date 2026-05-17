from typing import Annotated

from pydantic import BaseModel, EmailStr, Field, StringConstraints, field_validator


Username = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        min_length=3,
        max_length=30,
        pattern=r"^[A-Za-z0-9_.-]+$",
    ),
]
LoginPassword = Annotated[str, StringConstraints(min_length=1, max_length=128)]
StrongPassword = Annotated[str, StringConstraints(min_length=8, max_length=128)]
TokenText = Annotated[str, StringConstraints(min_length=20, max_length=512)]


def validate_strong_password(value: str) -> str:
    if not any(char.isupper() for char in value):
        raise ValueError("A jelszónak tartalmaznia kell nagybetűt.")
    if not any(char.islower() for char in value):
        raise ValueError("A jelszónak tartalmaznia kell kisbetűt.")
    if not any(char.isdigit() for char in value):
        raise ValueError("A jelszónak tartalmaznia kell számot.")
    return value


class GoalValue(BaseModel):
    value: int = Field(ge=0, le=1000)


class LoginUser(BaseModel):
    name: Username
    password: LoginPassword


class RegisterUser(BaseModel):
    name: Username
    password: StrongPassword
    email: EmailStr
    age: int = Field(ge=13, le=120)

    @field_validator("password")
    @classmethod
    def password_is_strong(cls, value: str) -> str:
        return validate_strong_password(value)


class ForgottenPassword(BaseModel):
    user_name: Username


class ChangePassword(BaseModel):
    old_password: LoginPassword
    new_password: StrongPassword

    @field_validator("new_password")
    @classmethod
    def new_password_is_strong(cls, value: str) -> str:
        return validate_strong_password(value)


class RefreshRequest(BaseModel):
    refresh_token: TokenText


class PasswordResetConfirm(BaseModel):
    reset_token: TokenText
    new_password: StrongPassword

    @field_validator("new_password")
    @classmethod
    def reset_password_is_strong(cls, value: str) -> str:
        return validate_strong_password(value)
