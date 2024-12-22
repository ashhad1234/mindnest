import streamlit as st
import openai

# Set your OpenAI API key
openai.api_key = "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"

# Define model IDs
fine_tuned_model = "ft:gpt-4o-mini-2024-07-18:personal:friend:AO73jIic:ckpt-step-1002"  # Replace with your fine-tuned model's ID
base_model = "gpt-4o-mini"  # Use the standard model, e.g., GPT-3.5

# Custom CSS for chat layout and switch button
st.markdown(
    """
    <style>
    /* General body style */
    body {
        font-family: Arial, sans-serif;
    }
    
    /* Chat container */
    .chat-container {
        border-radius: 10px;
        padding: 10px;
        margin-bottom: 10px;
    }
    
    /* User messages */
    .user-message {
        background-color: #ECF3F9;
        color: #333;
        padding: 10px;
        border-radius: 10px;
        text-align: left;
        max-width: 80%;
        margin-top: 27px
    }

    /* Assistant messages */
    .assistant-message {
        background-color: #F1F0F0;
        color: #333;
        padding: 10px;
        border-radius: 10px;
        text-align: left;
        max-width: 80%;
    }

    /* Align user messages to the right */
    .user-message-container {
        text-align: right;
    }

    /* Align assistant messages to the left */
    .assistant-message-container {
        text-align: left;
    }

    /* Position the mode switch at the top-right */
    .mode-switch {
        position: fixed;
        top: 280px;
        right: 415px;
        padding: 10px;
        background-color: #31333F;
        border-radius: 10px;
        font-size: 16px;
        color: #FFFFFF;
    }

    
    </style>
    """, 
    unsafe_allow_html=True
)




# Function to get response from OpenAI API with system instructions
def get_openai_response(prompt, model_id, system_instruction):
    response = openai.ChatCompletion.create(
        model=model_id,
        messages=[
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": prompt}
        ],
        max_tokens=180,
        temperature=0.7
    )
    return response.choices[0].message["content"]

# Title
st.title("Mind Nest")

# Initialize session state for chat histories and mode
if "friend_messages" not in st.session_state:
    st.session_state.friend_messages = []
if "therapist_messages" not in st.session_state:
    st.session_state.therapist_messages = []
if "current_mode" not in st.session_state:
    st.session_state.current_mode = "Therapist"

# Mode selector
mode = st.selectbox(
    "Switch Chatbot Mode",
    ["Therapist", "Friend"],
    index=0 if st.session_state.current_mode == "Therapist" else 1,
    key="mode",
    help="Switch between Therapist and Friend mode"
)

# Display current mode on top-right
st.markdown(f'<div class="mode-switch">Mode: {mode}</div>', unsafe_allow_html=True)

# Update current mode if changed
if mode != st.session_state.current_mode:
    st.session_state.current_mode = mode

# Determine the active chat history and system instructions
if st.session_state.current_mode == "Therapist":
    messages_key = "therapist_messages"
    model_id = "gpt-4o-mini"
    system_instruction = (
        "You are a compassionate and supportive AI therapist specializing in addressing common mental health issues, "
        "including anxiety, stress, depression, and daily life challenges. Your role is to provide emotional support, "
        "coping strategies, and guidance in a warm, understanding, and non-judgmental manner. Keep conversations "
        "professional and use formal or clinical language."
    )
else:
    messages_key = "friend_messages"
    model_id = "gpt-4o-mini"
    system_instruction = (
        "You are a friendly and supportive companion. "
        "Respond casually, as a good friend would. "
        "Listen, offer encouragement, and express empathy. "
        "Avoid using overly formal or clinical language. "
        "Keep responses light and supportive, and focus on being a good friend."
    )

# Display chat messages from the active history
for message in st.session_state[messages_key]:
    role = message["role"]
    content = message["content"]
    if role == "user":
        with st.container():
            st.markdown(
                f'<div class="chat-container user-message-container"><div class="user-message">{content}</div></div>',
                unsafe_allow_html=True
            )
    else:
        with st.container():
            st.markdown(
                f'<div class="chat-container assistant-message-container"><div class="assistant-message">{content}</div></div>',
                unsafe_allow_html=True
            )

# Accept user input
if prompt := st.chat_input("What is up?"):
    # Add user message to the current chat history
    st.session_state[messages_key].append({"role": "user", "content": prompt})
    
    # Display user message in chat
    with st.container():
        st.markdown(
            f'<div class="chat-container user-message-container"><div class="user-message">{prompt}</div></div>',
            unsafe_allow_html=True
        )

    # Get assistant response using OpenAI API
    assistant_response = get_openai_response(prompt, model_id, system_instruction)
    with st.container():
        st.markdown(
            f'<div class="chat-container assistant-message-container"><div class="assistant-message">{assistant_response}</div></div>',
            unsafe_allow_html=True
        )

    # Add assistant response to the current chat history
    st.session_state[messages_key].append({"role": "assistant", "content": assistant_response})
