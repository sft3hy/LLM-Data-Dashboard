from sqlalchemy import (
    Column,
    String,
    Text,
    TIMESTAMP,
    create_engine,
    func,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from uuid import uuid4
import os
from sqlalchemy.orm.exc import NoResultFound


Base = declarative_base()

# Database credentials
POSTGRES_USER = "sam"
POSTGRES_PASSWORD = os.getenv("PGSQL_PW")  # Default for testing
POSTGRES_DB = "cos_dash_db"
POSTGRES_HOST = "172.30.11.204"  # Update as needed
POSTGRES_PORT = 31090         # Default PostgreSQL port

# Construct the database URI
DATABASE_URI = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URI, echo=True)

# Create a sessionmaker for interacting with the database
Session = sessionmaker(bind=engine)

# Define the 'users' table
class User(Base):
    __tablename__ = 'users'

    user_id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    user_email = Column(String(100), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())

# Define the 'messages' table
class Message(Base):
    __tablename__ = 'messages'

    message_id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    role = Column(String(100), nullable=False)
    message_contents = Column(Text, nullable=False)
    file_name = Column(Text, nullable=False)
    assistant_code = Column(Text)
    assistant_code_expander = Column(Text)
    assistant_code_top = Column(Text)
    message_timestamp = Column(TIMESTAMP, server_default=func.now())

# Function to create tables
def create_tables():
    Base.metadata.create_all(engine)
    print("Tables created successfully.")

# Function to add a user
def add_user(user_email):
    with Session() as session:
        new_user = User(user_email=user_email)
        session.add(new_user)
        session.commit()
        print(f"User {user_email} added successfully with ID {new_user.user_id}.")

# Function to add a message
def add_message(role, message_contents, file_name, assistant_code=None, assistant_code_expander=None, assistant_code_top=None):
    with Session() as session:
        new_message = Message(
            role=role,
            message_contents=message_contents,
            file_name=file_name,
            assistant_code=assistant_code,
            assistant_code_expander=assistant_code_expander,
            assistant_code_top=assistant_code_top,
        )
        session.add(new_message)
        session.commit()
        print(f"Message added successfully with ID {new_message.message_id}.")


# Function to get messages by file path
def get_file_messages(file_path):
    with Session() as session:
        try:
            # Query messages where the file path matches any of the relevant columns
            results = session.query(Message).filter(
                (Message.assistant_code == file_path) |
                (Message.assistant_code_expander == file_path) |
                (Message.assistant_code_top == file_path)
            ).all()

            # Convert results to a list of dictionaries
            messages = [
                {
                    "message_id": msg.message_id,
                    "role": msg.role,
                    "message_contents": msg.message_contents,
                    "assistant_code": msg.assistant_code,
                    "assistant_code_expander": msg.assistant_code_expander,
                    "assistant_code_top": msg.assistant_code_top,
                    "message_timestamp": msg.message_timestamp
                }
                for msg in results
            ]
            return messages
        except NoResultFound:
            print(f"No messages found for file path: {file_path}")
            return []

# get messages by file path
def update_latest_assistant_message(file_path, assistant_code):
    with Session() as session:
        # Find the most recent assistant message matching the file_path
        latest_message = (
            session.query(Message)
            .filter(
                (Message.role == "assistant") &
                (Message.file_name == file_path)
            )
            .order_by(Message.message_timestamp.desc())
            .first()
        )
        if latest_message:
            # Update the message with the provided values
            latest_message.assistant_code = assistant_code
            session.commit()
            print(f"Updated message with ID {latest_message.message_id}.")
        else:
            print(f"No assistant messages found matching the file path: {file_path}.")
            print()

# Example Usage
if __name__ == "__main__":
    #TODO: COMMENT THIS OUT AFTER FIRST CREATION
    create_tables()  # Create tables

    add_user("user@example.com")  # Add a user
    add_message("assistant", "Hello, how can I help?", "test.py")  # Add a message
    file_messages = get_file_messages("test.py")
    print(file_messages)
    update_latest_assistant_message(file_path="test.py", assistant_code="print('updated this ish')")
    file_messages = get_file_messages("test.py")
    print(file_messages)


