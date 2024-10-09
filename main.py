import os
import streamlit as st
import requests
import time

# Set the base URL of your server API
API_URL = "https://fuprechatbot-fed3b2c7d4d0bce2.northcentralus-01.azurewebsites.net/ask"


#def main():
# Custom CSS for animations
custom_css = """
    <style>
    /* Center the content */
    .center {
        display: flex;
        justify-content: center;
        align-items: center;
        flex-direction: column;
        min-height: 200px;
    }

    /* Sliding animation for the logo */
    @keyframes slide-in {
        0% {
            transform: translateY(-100px);
            opacity: 0;
        }
        100% {
            transform: translateY(0);
            opacity: 1;
        }
    }

    /* Apply the animation to the logo */
    .logo {
        animation: slide-in 2s ease-out;
        max-width: 200px; /* Adjust logo size */
        margin-bottom: 10px;
    }

    /* Fading and italic animation for the slogan */
    @keyframes fade-in {
        0% {
            opacity: 0;
        }
        100% {
            opacity: 1;
        }
    }

    .slogan {
        animation: fade-in 3s ease-in;
        font-style: italic;
        font-size: 1.5rem;
        color: grey;
        text-align: center;
    }

    /* Optional: Add space and style for the main title */
    .main-title {
        font-size: 2rem;
        margin-top: 20px;
        text-align: center;
    }

    /* Ensure proper scaling and layout for mobile */
    @media (max-width: 760px) {
        .center {
            min-height: auto; /* Adjust height for mobile */
            padding: 20px; /* Add padding around the content */
            margin: 20px; /* Add margin to create space outside the container */
        }

        .logo {
            max-width: 150px; /* Adjust logo size for mobile */
        }

        .slogan {
            font-size: 1.2rem; /* Adjust slogan size for mobile */
        }

        .main-title {
            font-size: 1.5rem; /* Adjust main title size for mobile */
        }

        /* Chat message styling */
        .chat-message {
            max-width: 150%; /* Ensure messages don't stretch too wide */
            margin: 5px auto; /* Center messages and add spacing */
            padding: 10px;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }

        .chat-message.user {
            background-color: #e1ffc7; /* Light green for user messages */
            align-self: flex-start; /* Align user messages to the left */
        }

        .chat-message.assistant {
            background-color: #f1f0f0; /* Light grey for assistant messages */
            align-self: flex-end; /* Align assistant messages to the right */
        }

        /* Chat input styling */
        .stChatInput {
            width: 100%; /* Ensure input field is responsive */
            margin: 10 auto; /* Center input field */
            padding: 10px;
            box-sizing: border-box; /* Include padding and border in element's total width and height */
        }
    }
    </style>
    """

# Inject custom CSS into Streamlit
st.markdown(custom_css, unsafe_allow_html=True)

# Load the local image (FUPRE logo)
fupre_logo_path = "https://media.licdn.com/dms/image/v2/C4D0BAQGjGJd6c2gRRw/company-logo_200_200/company-logo_200_200/0/1630504443001?e=1733961600&v=beta&t=jOpzGzPMaAWuGcpKPxdVaC-vPSiQ3nYCeiOfyZOZXx0"  # Path to your uploaded image

# Use HTML to structure the logo with a CSS class
html_logo = f"""
    <div class="center">
        <div class="logo-container">
            <img src="{fupre_logo_path}" class="logo" alt="FUPRE Logo"/>
        </div>
        <div class="slogan">Excellence and Relevance</div>
    </div>
    <h1 class="main-title">Fupre Chatbot</h1>
"""

# Display the logo, slogan, and title
st.markdown(html_logo, unsafe_allow_html=True)

# Store the last interaction time globally
last_interaction_time = time.time()
bot_intro_displayed = False  # Flag to check if the bot's introduction has been displayed

# Function to show citations in an expander
def show_citation(citations):
    unique_citations = {}
        
    # Collect unique citations by URL
    for c in citations:
        if c['url'] not in unique_citations:
            unique_citations[c['url']] = c['title']
        
    # Display citations with clickable titles
    with st.expander("Reference"):
        for url, title in unique_citations.items():
            st.markdown(f"[**{title}**]({url})")

# Function to introduce the bot
def introduce_bot():
    bot_intro = "Hi, I'm Frida. How can I help you today?"
    st.chat_message("assistant").markdown(bot_intro)

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


# Display chat history (with citations for previous responses)
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        #st.markdown(f'<div class="chat-message {message["role"]}">{message["content"]}</div>', unsafe_allow_html=True)
        if message["role"] == "assistant" and message.get("citations"):
            show_citation(message["citations"])

# Input field for user's message
user_prompt = st.chat_input("Ask me about FUPRE...")

if user_prompt:
    last_interaction_time = time.time()  # Reset last interaction time

    # Add user's message to chat and display it
    #st.chat_message("user").markdown(f'<div class="chat-message user">{user_prompt}</div>', unsafe_allow_html=True)
    st.chat_message("user").markdown(user_prompt)
    st.session_state.chat_history.append({"role": "user", "content": user_prompt})

    # Prepare the payload for your server API
    payload = {"question": user_prompt}
    headers = {}

    try:
        # Make the API call to get the bot's response
        response = requests.post(API_URL, json=payload, headers=headers)
        response.raise_for_status()  # Raise an exception for 4XX/5XX errors
        data = response.json()

        # Extract the response content and citations
        bot_response = data.get("response", "No response received.")
        citations = data.get("citations", [])

        # Add the bot's response and citations to the chat history
        st.session_state.chat_history.append({"role": "assistant", "content": bot_response, "citations": citations})

        # Display bot's response
        with st.chat_message("assistant"):
            #st.markdown(f'<div class="chat-message assistant">{bot_response}</div>', unsafe_allow_html=True)
            st.markdown(bot_response)
            if citations:
                show_citation(citations)

    except requests.exceptions.RequestException as e:
        # Handle any errors during the API call
        error_message = f"Error: Unable to get a response. {str(e)}"
        st.session_state.chat_history.append({"role": "assistant", "content": error_message})
        st.chat_message("assistant").markdown(error_message)

# Check for inactivity every second
if not user_prompt and not bot_intro_displayed:
    while True:
        time.sleep(1)  # Pause for 1 second
        if time.time() - last_interaction_time > 10:  # 10 seconds of inactivity
            introduce_bot()
            bot_intro_displayed = True  # Set the flag to prevent repeated introductions
            break  # Exit the loop after introducing the bot