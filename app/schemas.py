# Pydantic models

from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import datetime
from typing import List
from typing import Optional


class UserCreate(BaseModel):
    email: EmailStr
    name: str

class UserRead(BaseModel):
    id: UUID
    email: EmailStr
    name: str
    created_at: datetime

    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    email: EmailStr = None
    name: str = None

class EmailRequest(BaseModel):
    email: EmailStr

class MessageCreate(BaseModel):
    sender_email: EmailStr
    recipient_email: List[EmailStr]
    subject: str
    content: str

    class Config:
        from_attributes = True

class Message(BaseModel):
    id: UUID
    sender_id: UUID
    subject: str
    content: str
    timestamp: datetime

    class Config:
        from_attributes = True


class ListMessageResponse(BaseModel):
    sender: EmailStr
    messages: List[Message]


class MessageRead(BaseModel):
    id: UUID
    sender : EmailStr
    subject: str
    content: str
    timestamp: datetime
    recipients: List[EmailStr] = []

    class Config:
        from_attributes = True
        orm_mode = True  # Enable ORM mode for compatibility with SQLAlchemy models

class InboxMessage(BaseModel):
    id: UUID
    sender: EmailStr
    subject: str
    content: str
    timestamp: datetime
    read: bool = False
    read_at: Optional[datetime]

    class Config:
        from_attributes = True
        orm_mode = True  # Enable ORM mode for compatibility with SQLAlchemy models

class ListInboxResponse(BaseModel):
    mailUser: EmailStr
    messages: List[InboxMessage]

    class Config:
        from_attributes = True
        orm_mode = True  # Enable ORM mode for compatibility with SQLAlchemy models

class Recipient(BaseModel):
    recipient_email: EmailStr
    recipient_name: str
    read: bool = False
    read_at: Optional[datetime] = None

    class Config:
        from_attributes = True
        orm_mode = True

class InboxMessageDetailSender(BaseModel):
    id: UUID
    sender: EmailStr
    subject: str
    content: str
    timestamp: datetime
    recipients: List[Recipient] = []

    class Config:
        from_attributes = True
        orm_mode = True  # Enable ORM mode for compatibility with SQLAlchemy models

class markAsRead(BaseModel):
    message_id: str
    recipient_id: str

class InboxMessageDetailRecipients(BaseModel):
    id: UUID
    sender: EmailStr
    subject: str
    content: str
    timestamp: datetime
    recipients: List[Recipient] = []
    read: bool = False
    read_at: Optional[datetime] = None

    class Config:
        from_attributes = True
        orm_mode = True  # Enable ORM mode for compatibility with SQLAlchemy models
