import openai
import sqlite3

openai.api_key = ''

# Define the model for chat-based completion
model = "gpt-3.5-turbo"

# Function to interact with OpenAI Playground chat
def interact_with_playground(messages):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        max_tokens=250,
    )
    return response.choices[0].message['content']

def create_database():
    conn = sqlite3.connect("chat_history.db")
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT NOT NULL,
            content TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()


# Initialize conversation with system instructions
conversation = [
    {"role": "system", "content": "You are an agent with goals which are reviewed after asking each questions"
                                  "...Start by: Hello! Welcome to headspace. We support young people with mental health, physical health, alcohol and other drug services, as well as work and study support."
                                  "... Your task is to facilitate the admission of a young person to our services."
                                  "Review each task after each conversation"
                                  "Help user through our registration process."
                                  "Ask for name, date of birth and if they have medicare."
                                  "You ONLY know about being a Therapist Receptionist with years of experience."
                                  "Keep conversation formal."
                                  "Inform the user that any information they provide will be confidential."
                                  "... Provide information about headspace: Headspace is an early intervention mental health service for young people. Our services bulk bill to Medicare, which gives young people access to services such as; physical health, sexual health, and mental health care."
                                  "This information will enable our clinicians to decide the most suitable course of action."
                                  "...Service is only accessible for age 12 to 25 years old."
                                  "First name and age is important goals."
                                  "...keep asking for the information until given."
                                  "if the user is over the age of 25 ask them to call headspace."
                                  "...redirect the user to call the mindspace rather than giving mental health advise."
                                  },
]

# Update this function to store messages in the database
def store_message_in_database(conversation, role, content):
    conn = sqlite3.connect("chat_history.db")
    c = conn.cursor()
    c.execute('INSERT INTO conversations (role, content) VALUES (?, ?)', (role, content))
    conn.commit()
    conn.close()

# Initialize the database
create_database()

# Add the system message to the database
store_message_in_database(conversation, conversation[0]["role"], conversation[0]["content"])

print("Hello! Welcome to headspace. We support young people with mental health, physical health, alcohol and other drug services, as well as work and study support.")

while True:
    user_input = input("User: ")

    # Add user input to the conversation
    conversation.append({"role": "user", "content": user_input})

    # Get response from the AI therapist
    ai_response = interact_with_playground(conversation)

    # Add AI response to the conversation
    conversation.append({"role": "assistant", "content": ai_response})

    # Print AI response
    print("AI Therapist Receptionist:", ai_response)

    # Store user and AI responses in the database
    store_message_in_database(conversation, "user", user_input)
    store_message_in_database(conversation, "assistant", ai_response)

