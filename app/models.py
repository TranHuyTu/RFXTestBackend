# SQLAlchemy or Tortoise models
import uuid
from datetime import datetime
from sqlalchemy import (
    Column,
    String,
    Text,
    DateTime,
    Boolean,
    ForeignKey,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)

    sent_messages = relationship('Message', back_populates='sender', cascade="all, delete-orphan")
    received_messages = relationship(
        'MessageRecipient',
        back_populates='recipient',
        cascade='all, delete-orphan'
    )

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, name={self.name})>"


class Message(Base):
    __tablename__ = 'messages'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    sender_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    subject = Column(String(255), nullable=True)
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)

    sender = relationship('User', back_populates='sent_messages')
    recipients = relationship('MessageRecipient', back_populates='message', cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Message(id={self.id}, sender_id={self.sender_id}, subject={self.subject})>"


class MessageRecipient(Base):
    __tablename__ = 'message_recipients'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    message_id = Column(UUID(as_uuid=True), ForeignKey('messages.id', ondelete='CASCADE'), nullable=False)
    recipient_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    read = Column(Boolean, nullable=False, default=False)
    read_at = Column(DateTime(timezone=True), nullable=True)

    message = relationship('Message', back_populates='recipients')
    recipient = relationship('User', back_populates='received_messages')

    def __repr__(self):
        return f"<MessageRecipient(id={self.id}, message_id={self.message_id}, recipient_id={self.recipient_id}, read={self.read})>"

