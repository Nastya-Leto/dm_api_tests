from pydantic import BaseModel,Field,ConfigDict


class ChangePassword(BaseModel):
    model_config = ConfigDict(extra='forbid') #обязательность проверки
    login: str = Field(...,description='Логин')
    token: str = Field(...,description='Пароль')
    oldPassword: str = Field(...,description='Старый пароль')
    newPassword: str = Field(..., description='Новый пароль')