# Test message-related functionality
from fastapi.testclient import TestClient
from app.main import app

# app = FastAPI()
client = TestClient(app)

### Test Cases
def send_message(sender_email, recipient_emails, subject, content):
    response = client.post(
        "/api/message/sendMessage",
        json={
            "sender_email": sender_email,
            "recipient_email": recipient_emails,
            "subject": subject,
            "content": content
        }
    )
    return response

def test_send_message():
    response = send_message(
        sender_email="user1@gmail.com",
        recipient_emails=["user2@gmail.com", "user3@gmail.com"],
        subject="Test Subject",
        content="This is a test message."
    )
    assert response.status_code == 200
    data = response.json()
    assert data["sender"] == "user1@gmail.com"
    assert data["subject"] == "Test Subject"
    assert data["content"] == "This is a test message."
def test_send_message_invalid_sender():
    response = send_message(
        sender_email="user1",
        recipient_emails=["user2@gmail.com", "user3@gmail.com"],
        subject="Test Subject",
        content="This is a test message."
    )
    assert response.status_code == 422
    data = response.json()
    assert "detail" in data
    assert "sender_email" in data["detail"][0]["loc"]

def test_send_message_invalid_recipient():
    response = send_message(
        sender_email="user1@gmail.com",
        recipient_emails=["user", "user3@gmail.com"],
        subject="Test Subject",
        content="This is a test message."
    )
    assert response.status_code == 422
    data = response.json()
    assert "detail" in data
    assert "recipient_email" in data["detail"][0]["loc"]

def test_send_message_nonexistent_recipient():
    response = send_message(
        sender_email="user1@gmail.com",
        recipient_emails=[],
        subject="Test Subject",
        content="This is a test message."
    )
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert data["detail"] == "Sender email, recipient email(s), and content are required"
def test_send_message_nonexistent_sender():
    response = send_message(
        sender_email="",
        recipient_emails=["user2@gmail.com", "user3@gmail.com"],
        subject="Test Subject",
        content="This is a test message."
    )
    assert response.status_code == 422
    data = response.json()
    assert "detail" in data
    assert "sender_email" in data["detail"][0]["loc"]
# def test_send_message_nonexistent_recipient():
#     response = send_message(
#         sender_email="user1@gmail.com",
#         subject="Test Subject",
#         content="This is a test message."
#     )
#     assert response.status_code == 422
#     data = response.json()
#     assert "detail" in data
#     assert "recipient_emails" in data["detail"][0]["loc"]
def test_get_send_message_by_mail():
    response = client.post(
        "/api/message/byMail",
        json={"email": "user1@gmail.com"}
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "messages" in data
    assert "sender" in data
    assert isinstance(data["messages"], list)
    assert len(data["messages"]) > 0  # Assuming at least one message exists
def test_get_send_message_by_mail_missing_email():
    response = client.post(
        "/api/message/byMail",
        json={}
    )
    assert response.status_code == 422
    data = response.json()
    assert "detail" in data
    assert "email" in data["detail"][0]["loc"]
def test_get_send_message_by_mail_nonexistent_email():
    response = client.post(
        "/api/message/byMail",
        json={"email": "testuserewrew@example.com"}
    )
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert data["detail"] == "Message not found for the given email"
def test_get_send_message_by_mail_invalid_email():
    response = client.post(
        "/api/message/byMail",
        json={"email": "invalid-email"}
    )
    assert response.status_code == 422
    data = response.json()
    assert "detail" in data
    assert "email" in data["detail"][0]["loc"]
def test_get_send_message_by_mail_empty_email():
    response = client.post(
        "/api/message/byMail",
        json={"email": ""}
    )
    assert response.status_code == 422
    data = response.json()
    assert "detail" in data
    assert "email" in data["detail"][0]["loc"]
def test_get_send_message_by_mail_no_messages():
    response = client.post(
        "/api/message/byMail",
        json={"email": "user2@gmail.com"}
    )
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert data["detail"] == "Message not found for the given email"
def test_get_inbox_messages():
    response = client.post(
        "/api/message/inbox",
        json={"email": "user2@gmail.com"}
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "messages" in data
    assert "mailUser" in data
    assert isinstance(data["messages"], list)
    assert len(data["messages"]) > 0  # Assuming at least one message exists
def test_get_inbox_messages_missing_email():
    response = client.post(
        "/api/message/inbox",
        json={}
    )
    assert response.status_code == 422
    data = response.json()
    assert "detail" in data
    assert "email" in data["detail"][0]["loc"]
def test_get_inbox_messages_nonexistent_email():
    response = client.post(
        "/api/message/inbox",
        json={"email": "alice.smithfsdf@example.com"}
    )
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert data["detail"] == "No messages found in the inbox for the given email"
def test_get_inbox_messages_invalid_email():
    response = client.post(
        "/api/message/inbox",
        json={"email": "invalid-email"}
    )
    assert response.status_code == 422
    data = response.json()
    assert "detail" in data
    assert "email" in data["detail"][0]["loc"]
def test_get_inbox_messages_empty_email():
    response = client.post(
        "/api/message/inbox",
        json={"email": ""}
    )
    assert response.status_code == 422
    data = response.json()
    assert "detail" in data
    assert "email" in data["detail"][0]["loc"]
def test_get_unread_inbox_messages():
    response = client.post(
        "/api/message/inboxUnread",
        json={"email": "user2@gmail.com"}
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "messages" in data
    assert "mailUser" in data
    assert isinstance(data["messages"], list)
    assert len(data["messages"]) > 0  # Assuming at least one message exists
def test_get_unread_inbox_messages_missing_email():
    response = client.post(
        "/api/message/inboxUnread",
        json={}
    )
    assert response.status_code == 422
    data = response.json()
    assert "detail" in data
    assert "email" in data["detail"][0]["loc"]
def test_get_unread_inbox_messages_nonexistent_email():
    response = client.post(
        "/api/message/inboxUnread",
        json={"email": "alice.smithdsads@example.com"}
    )   
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert data["detail"] == "No messages found in the inbox for the given email"
def test_get_message_with_all_recipients():
    response = client.get(
        "/api/message/senderDetail/899c237d-3303-4709-b7f4-6473d289ec2b"
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "recipients" in data
    assert isinstance(data["recipients"], list)
    assert len(data["recipients"]) > 0  # Assuming at least one recipient exists
def test_get_message_with_all_recipients_missing_id():
    response = client.get(
        "/api/message/senderDetail/"
    )
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert data["detail"] == "Not Found"
def test_get_message_with_all_recipients_invalid_id():
    response = client.get(
        "/api/message/senderDetail/invalid-id"
    )
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert data["detail"] == "Message not found"
def test_mark_message_as_read():
    response = client.post(
        "/api/message/markAsRead",
        json={
    "message_id": "899c237d-3303-4709-b7f4-6473d289ec2b",
    "recipient_id": "a7ecbe2a-d72d-434a-8dc5-80e1d076a204"
}
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "id" in data
    assert data["id"] == "899c237d-3303-4709-b7f4-6473d289ec2b"
def test_mark_message_as_read_missing_fields():
    response = client.post(
        "/api/message/markAsRead",
        json={
}
    )
    assert response.status_code == 422
    data = response.json()
    assert "detail" in data
    assert "message_id" in data["detail"][0]["loc"]
    assert "recipient_id" in data["detail"][1]["loc"]

