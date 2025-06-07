from datetime import datetime
from sqlalchemy.exc import IntegrityError
from . import models  # Assuming your User model is in models.py
from . import db
import uuid
from dotenv import load_dotenv
import os

load_dotenv()


SessionLocal = db.connect_to_postgresql(user='postgres', password='postgres', host=os.getenv("HOST"), port=5432, database = 'postgres').get('SessionLocal')
engine = db.connect_to_postgresql(user='postgres', password='postgres', host=os.getenv('HOST'), port=5432, database = 'postgres').get('engine')

# Create tables if they don't exist
models.Base.metadata.create_all(bind=engine)

def get_list_users():
    """
    Retrieve a list of all users from the users table.

    :return: List of User objects or an empty list if no users found
    """
    models.Base.metadata.create_all(bind=engine)
    session = SessionLocal()
    try:
        users = session.query(models.User).all()
        return users
    except Exception as e:
        print(f"Error retrieving users: {e}")
        return []
    finally:
        session.close()
        
def create_user(email, name, created_at = datetime.utcnow()):
    """
    Create a new user in the users table.

    :param email: Email of the user (must be unique)
    :param name: Name of the user
    :return: UUID of the newly created user or None if an error occurred
    """
    models.Base.metadata.create_all(bind=engine)
    session = SessionLocal()
    try:
        new_user = models.User(
            id=uuid.uuid4(),  # Generate a new UUID for the user
            email=email,
            name=name,
            created_at = created_at
        )
        session.add(new_user)
        session.commit()
        session.refresh(new_user)  # Refresh to get the updated user object with ID
        print(f"User  created with id: {new_user.id}")
        return new_user
    except IntegrityError:
        session.rollback()
        print("Error: A user with this email already exists.")
        return None
    except Exception as e:
        session.rollback()
        print(f"Error creating user: {e}")
        return None
    finally:
        session.close()

def find_user_by_mail(email):
    """
    Find a user by their email address.

    :param email: Email of the user to find
    :return: User object if found, None otherwise
    """
    models.Base.metadata.create_all(bind=engine)
    session = SessionLocal()
    try:
        user = session.query(models.User).filter(models.User.email == email).first()
        return user
    except Exception as e:
        print(f"Error finding user by email: {e}")
        return None
    finally:
        session.close()

def update_user(user_id, email=None, name=None):
    """
    Update an existing user in the users table.

    :param user_id: UUID of the user to update
    :param email: New email for the user (optional)
    :param name: New name for the user (optional)
    :return: Updated User object or None if an error occurred
    """
    models.Base.metadata.create_all(bind=engine)
    session = SessionLocal()
    try:
        user = session.query(models.User).filter(models.User.id == user_id).first()
        if not user:
            print("User not found")
            return None
        
        if email:
            user.email = email
        if name:
            user.name = name
        
        session.commit()
        return user
    except Exception as e:
        session.rollback()
        print(f"Error updating user: {e}")
        return None
    finally:
        session.close()

def create_message(sender, recipients, subject, content):
    """Create a new message and associate it with the sender and recipients.
    :param sender: User object representing the sender
    :param recipients: List of User objects representing the recipients
    :param subject: Subject of the message
    :param content: Content of the message
    :return: Message object if created successfully, None otherwise
    """
    """Create a new message and associate it with the sender and recipients.
    :param sender: User object representing the sender
    :param recipients: List of User objects representing the recipients
    :param subject: Subject of the message
    :param content: Content of the message
    :return: Message object if created successfully, None otherwise
    """
    models.Base.metadata.create_all(bind=engine)
    session = SessionLocal()
    try:
        new_message = models.Message(
            id=uuid.uuid4(),
            sender_id=sender.id,
            subject=subject,
            content=content,
            timestamp=datetime.utcnow()
        )
        session.add(new_message)
        session.commit()

        # Add recipients
        for recipient in recipients:
            message_recipient = models.MessageRecipient(
                id=uuid.uuid4(),
                message_id=new_message.id,
                recipient_id=recipient.id
            )
            session.add(message_recipient)

        session.commit()

        session.refresh(new_message)
        return {
            "id": new_message.id,
            "sender": sender.email,
            "subject": new_message.subject,
            "content": new_message.content,
            "timestamp": new_message.timestamp,
            "recipients": [recipient.email for recipient in recipients]
        }

    except IntegrityError:
        session.rollback()
        print("Error: A message with this ID already exists.")
        return None

    except Exception as e:
        session.rollback()
        print(f"Error creating message: {e}")
        return None
    finally:
        session.close()

def find_message_by_mail(email):
    """Retrieve messages sent by a user with a given email address.
    :param email: Email of the sender
    :return: List of Message objects if found, empty list otherwise
    """
    """Retrieve messages sent by a user with a given email address.
    :param email: Email of the sender
    :return: List of Message objects if found, empty list otherwise
    """
    models.Base.metadata.create_all(bind=engine)
    session = SessionLocal()
    try:
        user = session.query(models.User).filter(models.User.email == email).first()
        if not user:
            print("Sender user not found")
            return []
        
        messages = session.query(models.Message).filter(models.Message.sender_id == user.id).all()
        if not messages:
            print("No messages found for this user")
            return []
        return messages
    except Exception as e:
        print(f"Error retrieving message by email: {e}")
        return []
    finally:
        session.close()

def find_message_inbox(email):
    """Retrieve inbox messages for a given email address.
    :param email: Email of the recipient
    :return: List of MessageRecipient objects if found, empty list otherwise
    """
    """Retrieve inbox messages for a given email address.
    :param email: Email of the recipient
    :return: List of MessageRecipient objects if found, empty list otherwise
    """
    """Retrieve inbox messages for a given email address.
    :param email: Email of the recipient
    :return: List of MessageRecipient objects if found, empty list otherwise
    """
    models.Base.metadata.create_all(bind=engine)
    session = SessionLocal()
    try:
        user = session.query(models.User).filter(models.User.email == email).first()
        if not user:
            print("Recipient user not found")
            return []
        
        message_recipients = session.query(models.MessageRecipient).filter(models.MessageRecipient.recipient_id == user.id).all()
        # messages = [recipient.message for recipient in message_recipients]

        if message_recipients:
            message_recipients = [{
                "id": recipient.message.id,
                "sender": recipient.message.sender.email,
                "subject": recipient.message.subject,
                "content": recipient.message.content,
                "timestamp": recipient.message.timestamp,
                # "recipients": [recipient.recipient.email for recipient in message.recipients],
                "read": recipient.read if recipient.read else False,
                "read_at": recipient.read_at
            } for recipient in message_recipients]
            
        return message_recipients
    except Exception as e:
        print(f"Error retrieving inbox messages: {e}")
        return []
    finally:
        session.close()

def find_message_inbox_unread(email):
    """Retrieve unread messages in the inbox for a given email address.
    :param email: Email of the recipient
    :return: List of unread Message objects if found, empty list otherwise
    """
    """Retrieve unread messages in the inbox for a given email address.
    :param email: Email of the recipient
    :return: List of unread Message objects if found, empty list otherwise
    """
    models.Base.metadata.create_all(bind=engine)
    session = SessionLocal()
    try:
        user = session.query(models.User).filter(models.User.email == email).first()
        if not user:
            print("Recipient user not found")
            return []
        
        message_recipients = session.query(models.MessageRecipient).filter(
            models.MessageRecipient.recipient_id == user.id,
            models.MessageRecipient.read == False
        ).all()

        if message_recipients:
            message_recipients = [{
                "id": recipient.message.id,
                "sender": recipient.message.sender.email,
                "subject": recipient.message.subject,
                "content": recipient.message.content,
                "timestamp": recipient.message.timestamp,
                # "recipients": [recipient.recipient.email for recipient in message.recipients],
                "read": recipient.read if recipient.read else False,
                "read_at": recipient.read_at
            } for recipient in message_recipients]
            
        return message_recipients
    except Exception as e:
        print(f"Error retrieving unread inbox messages: {e}")
        return []
    finally:
        session.close()

def find_message_sender_detail(message_id):
    """Retrieve detailed information about a specific message by message ID.
    :param message_id: UUID of the message
    :return: Message detail with sender and recipient information if found, None otherwise
    """
    """Retrieve detailed information about a specific message by message ID.
    :param message_id: UUID of the message
    :return: Message detail with sender and recipient information if found, None otherwise
    """
    models.Base.metadata.create_all(bind=engine)
    session = SessionLocal()
    try:
        message = session.query(models.Message).filter(models.Message.id == message_id).first()
        if not message:
            print("Message not found")
            return None
        
        recipients = []
        for recipient in message.recipients:
            recipient_data = {
                "recipient_email": recipient.recipient.email,
                "recipient_name": recipient.recipient.name,
                "read": recipient.read if recipient.read else False,
                "read_at": recipient.read_at
            }
            recipients.append(recipient_data)


        message_detail = {
            "id": message.id,
            "sender": message.sender.email,
            "subject": message.subject,
            "content": message.content,
            "timestamp": message.timestamp,
            "recipients": recipients
        }

        return message_detail
    except Exception as e:
        print(f"Error retrieving message detail: {e}")
        return None
    finally:
        session.close()

def find_message_recipient_detail(message_id, recipient_id):
    """Retrieve detailed information about a specific message for a recipient by message ID and recipient ID.
    :param message_id: UUID of the message
    :param recipient_id: UUID of the recipient
    :return: Message detail with recipient information if found, None otherwise
    """
    """Retrieve detailed information about a specific message for a recipient by message ID and recipient ID.
    :param message_id: UUID of the message
    :param recipient_id: UUID of the recipient
    :return: Message detail with recipient information if found, None otherwise
    """
    models.Base.metadata.create_all(bind=engine)
    session = SessionLocal()
    try:
        message = session.query(models.Message).filter(models.Message.id == message_id).first()
        if not message:
            print("Message not found")
            return None
        user = session.query(models.User).filter(models.User.id == recipient_id).first()
        if not user:
            print("Recipient user not found")
            return None
        message_recipient = session.query(models.MessageRecipient).filter(
            models.MessageRecipient.message_id == message.id,
            models.MessageRecipient.recipient_id == user.id
        ).first()
        if not message_recipient:
            print("Message recipient not found")
            return None
        
        if(message_recipient.read == False):
            message_recipient.read = True
            message_recipient.read_at = datetime.utcnow()
            session.commit()
            # Refresh the message_recipient to get the updated values
            # This is necessary to ensure that the read and read_at fields are updated in the response
            session.refresh(message_recipient)
        
        recipients = []
        for recipient in message.recipients:
            recipient_data = {
                "recipient_email": recipient.recipient.email,
                "recipient_name": recipient.recipient.name,
                "read": recipient.read if recipient.read else False,
                "read_at": recipient.read_at
            }
            recipients.append(recipient_data)


        message_detail = {
            "id": message.id,
            "sender": message.sender.email,
            "subject": message.subject,
            "content": message.content,
            "timestamp": message.timestamp,
            "recipients": recipients,
            "read": message_recipient.read,
            "read_at": message_recipient.read_at
        }

        return message_detail
    except Exception as e:
        print(f"Error retrieving message detail: {e}")
        return None
    finally:
        session.close()