from fastapi import APIRouter, HTTPException, Request
from typing import List

from app.schemas import UserRead, UserCreate, EmailRequest, MessageCreate, MessageRead, ListMessageResponse, Message, ListInboxResponse, InboxMessage, Recipient, InboxMessageDetailSender, InboxMessageDetailRecipients, markAsRead  # Pydantic schemas
from . import services

router = APIRouter()

@router.get("/users", response_model=List[UserRead])
def get_users():
    users_db = services.get_list_users()
    return [UserRead.from_orm(user) for user in users_db]

@router.post("/users/byEmail", response_model=UserRead)
def get_user_by_email(request: EmailRequest):
    print(f"Query parameters: {request.email}")
    if request.email:
        user = services.find_user_by_mail(request.email)
        if user:
            return UserRead.from_orm(user)
        else:
            raise HTTPException(status_code=404, detail="User not found")
    elif not request.email:
        raise HTTPException(status_code=400, detail="Email query parameter is required")

@router.post("/users", response_model=UserRead)
def create_user(user: UserCreate):
    print(f"Creating user with email: {user.email} and name: {user.name}")
    if not user.email or not user.name:
        raise HTTPException(status_code=400, detail="Email and name are required")
    find_user = services.find_user_by_mail(user.email)
    if find_user:
        print(f"User with email {find_user.email} already exists")
        raise HTTPException(status_code=400, detail="User with this email already exists")
    else:
        new_user = services.create_user(user.email, user.name)
        return UserRead.from_orm(new_user)

@router.post("/message/sendMessage", response_model=MessageRead)
def send_message(message: MessageCreate):
    if not message.sender_email or not message.recipient_email or not message.content:
        raise HTTPException(status_code=400, detail="Sender email, recipient email(s), and content are required")

    sender = services.find_user_by_mail(message.sender_email)

    if not sender:
        raise HTTPException(status_code=404, detail="Sender user not found")

    recipients = []
    for email in message.recipient_email:
        recipient = services.find_user_by_mail(email)
        if recipient:
            recipients.append(recipient)
        else:
            raise HTTPException(status_code=404, detail=f"Recipient user with email {email} not found")

    new_message = services.create_message(sender, recipients, message.subject, message.content)
    # print(f"Message created with ID: {new_message.id}")
    return MessageRead.from_orm(new_message)

@router.post("/message/byMail", response_model = ListMessageResponse)
def get_message_by_mail(request: EmailRequest):
    if not request.email:
        raise HTTPException(status_code=400, detail="Email query parameter is required")
    
    print(f"Query parameters: {request.email}")
    messages = services.find_message_by_mail(request.email)
    if messages!=[]:
        return ListMessageResponse(
            messages=[Message.from_orm(msg) for msg in messages],
            sender=request.email
            )
    else:
        raise HTTPException(status_code=404, detail="Message not found for the given email")
    
@router.post("/message/inbox", response_model=ListInboxResponse)
def get_inbox_messages(request: EmailRequest):
    if not request.email:
        raise HTTPException(status_code=400, detail="Email query parameter is required")
    
    print(f"Query parameters: {request.email}")

    inbox_messages = services.find_message_inbox(request.email)
    if inbox_messages != []:
        return ListInboxResponse(
            messages=[InboxMessage.from_orm(msg) for msg in inbox_messages],
            mailUser=request.email
        )
    else:
        raise HTTPException(status_code=404, detail="No messages found in the inbox for the given email")
    
@router.post("/message/inboxUnread", response_model=ListInboxResponse)
def get_unread_inbox_messages(request: EmailRequest):
    if not request.email:
        raise HTTPException(status_code=400, detail="Email query parameter is required")
    
    print(f"Query parameters: {request.email}")

    inbox_messages = services.find_message_inbox_unread(request.email)
    if inbox_messages != []:
        return ListInboxResponse(
            messages=[InboxMessage.from_orm(msg) for msg in inbox_messages],
            mailUser=request.email
        )
    else:
        raise HTTPException(status_code=404, detail="No messages found in the inbox for the given email")
    
@router.get("/message/senderDetail/{message_id}", response_model=InboxMessageDetailSender)
def get_message_by_id(message_id: str):
    if not message_id:
        raise HTTPException(status_code=400, detail="Message ID is required")
    
    print(f"Query parameters: {message_id}")

    message = services.find_message_sender_detail(message_id)

    if message:
        # Chuyển từng recipient dict thành đối tượng Recipient
        recipients = [Recipient(**r) for r in message["recipients"]]

        # Tạo đối tượng InboxMessageDetailSender
        message_detail = InboxMessageDetailSender(
            id=message["id"],
            sender=message["sender"],
            subject=message["subject"],
            content=message["content"],
            timestamp=message["timestamp"],
            recipients=recipients
        )

        return message_detail

    else:
        raise HTTPException(status_code=404, detail="Message not found")
    
@router.post("/message/markAsRead", response_model=InboxMessageDetailRecipients)
def mark_message_as_read(markAsRead: markAsRead):
    print(f"Received markAsRead: {markAsRead}")
    if not markAsRead.message_id or not markAsRead.recipient_id:
        raise HTTPException(status_code=400, detail="Message ID and recipient email are required")
    
    print(f"Marking message {markAsRead.message_id} as read for recipient {markAsRead.recipient_id}")

    updated_message = services.find_message_recipient_detail(message_id=markAsRead.message_id, recipient_id=markAsRead.recipient_id)

    if updated_message:
        return InboxMessageDetailRecipients.from_orm(updated_message)
    else:
        raise HTTPException(status_code=404, detail="Message or recipient not found")