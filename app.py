import streamlit as st
import json
import os
from datetime import datetime
from typing import Sequence
import autogen
from autogen import AssistantAgent, GroupChat, GroupChatManager, ConversableAgent
import openai
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv()

# Configure OpenAI
config_list = [
    {
        'model': 'gpt-4',
        'api_key': os.getenv('OPENAI_API_KEY')
    }
]

# Set wider layout
st.set_page_config(layout="wide")

# Custom CSS for wider components
st.markdown("""
    <style>
    .stTextInput > div > div > input {
        width: 100%;
    }
    .element-container {
        width: 100%;
    }
    .stTextArea > div > div > textarea {
        width: 100%;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state for personas and participants
if 'personas' not in st.session_state:
    st.session_state.personas = []
    # Add default host persona
    st.session_state.personas.append({
        'name': 'Host',
        'description': 'A warm and professional radio show host who guides conversations, asks insightful questions, and ensures balanced participation.',
        'is_host': True,
        'created_at': datetime.now().isoformat()
    })

if 'participants' not in st.session_state:
    st.session_state.participants = []
    # Add host as default participant
    st.session_state.participants.append({
        'role': 'Host',
        'persona': st.session_state.personas[0]
    })

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

def process_name(name):
    """Convert spaces to underscores and remove special characters"""
    return "".join(name.split())

def save_personas():
    """Save personas to a JSON file"""
    with open('personas.json', 'w') as f:
        json.dump([{k: v for k, v in p.items() if k != 'created_at'} 
                  for p in st.session_state.personas], f)

def load_personas():
    """Load personas from JSON file"""
    if os.path.exists('personas.json'):
        with open('personas.json', 'r') as f:
            personas = json.load(f)
            for p in personas:
                p['created_at'] = datetime.now().isoformat()
            st.session_state.personas = personas

def create_agent_configs(participants):
    """Create agent configurations for autogen"""
    configs = {}
    
    # Get list of participant names for host's reference
    participant_names = [p['persona']['name'] for p in participants if not p['persona'].get('is_host')]
    
    # Create config for each participant
    for participant in participants:
        name = participant['persona']['name']
        description = participant['persona']['description']
        
        # Special config for host
        if participant['persona'].get('is_host'):
            system_message = f"""You are the host of 'Starry Night Talks' radio show.
            Available participants: {', '.join(participant_names)}

            Speaking style:
            - Warm and professional tone
            - Precise, brief questions
            - Maximum 2 sentences per response
            
            Dialogue structure:
            1. Opening: Welcome and introduce the topic
            2. Interaction: Ask targeted questions to ONLY the available participants listed above
            3. Summary: Extract key insights from the discussion
            
            Must follow:
            - Only interact with the listed participants
            - Guide discussion between available participants only
            - Keep responses focused and concise"""
        else:
            system_message = f"""You are {name}.
            Background and expertise:
            {description}
            
            Speaking requirements:
            - Maximum 2 sentences per response
            - Must include specific details from your background
            - Share relevant experiences and insights
            
            Interaction rules:
            - Actively resonate with other participants' experiences
            - Stay true to your character and expertise"""
            
        configs[name] = {
            "name": name,
            "system_message": system_message
        }
    
    return configs

def create_group_chat(participants, user_input):
    """Create and configure the group chat with agents"""
    
    # Create agent configurations
    agent_configs = create_agent_configs(participants)
    
    # Create the agents
    agents = []
    for name, config in agent_configs.items():
        agent = AssistantAgent(
            name=config["name"],
            system_message=config["system_message"],
            llm_config={
                "config_list": config_list
            }
        )
        agents.append(agent)
    
    # Create the group chat
    group_chat = GroupChat(
        agents=agents,
        messages=[],
        max_round=12
    )
    
    # Create the manager
    manager = GroupChatManager(
        groupchat=group_chat,
        llm_config={
            "config_list": config_list
        }
    )
    
    return group_chat, manager

def run_chat(user_input, participants):
    """Run the group chat and return messages"""
    try:
        group_chat, manager = create_group_chat(participants, user_input)
        
        # Add user's initial message
        messages = [{
            'role': 'user',
            'content': user_input
        }]
        
        # Set up the initial prompt
        initial_prompt = (
            f"Let's have a panel discussion about: {user_input}\n"
            "The host should start by welcoming everyone and introducing the topic."
        )
        
        # Run the chat
        chat_result = manager.run(message=initial_prompt, max_turns=12)
        
        # Debug print
        st.write("Debug - Chat Result:", chat_result)
        
        # Process the chat result
        if hasattr(chat_result, 'chat_history'):
            history = chat_result.chat_history
            st.write("Debug - Chat History Length:", len(history))
            
            last_role = None
            # Process each message in the chat history
            for msg in history:
                st.write("Debug - Raw Message:", msg)
                
                # Skip system messages and empty messages
                if not msg or (hasattr(msg, 'role') and msg.role == 'system'):
                    continue
                
                # Extract the content and role
                content = None
                role = None
                
                # Try different ways to get content
                if isinstance(msg, str):
                    content = msg
                elif hasattr(msg, 'content'):
                    content = msg.content
                elif isinstance(msg, dict) and 'content' in msg:
                    content = msg['content']
                
                # Try different ways to get role
                if hasattr(msg, 'name'):
                    role = msg.name
                elif hasattr(msg, 'sender'):
                    role = msg.sender
                elif isinstance(msg, dict):
                    role = msg.get('name') or msg.get('sender') or msg.get('role')
                
                # Skip if we couldn't get content or role
                if not content or not role:
                    continue
                
                # Clean up content if it starts with role
                if content.startswith(f"{role}: "):
                    content = content[len(f"{role}: "):]
                
                # Skip duplicate consecutive messages from same role
                if role == last_role:
                    continue
                
                last_role = role
                
                # Add the processed message
                messages.append({
                    'role': role,
                    'content': content
                })
                st.write("Debug - Processed Message:", {
                    'role': role,
                    'content': content
                })
        
        return messages
    except Exception as e:
        st.error(f"Error in run_chat: {str(e)}")
        st.write("Debug - Exception details:", str(e))
        import traceback
        st.write("Debug - Traceback:", traceback.format_exc())
        raise e

def display_messages(messages, message_placeholder):
    """Display messages in a streaming fashion"""
    try:
        full_response = ""
        
        # Debug print
        st.write("Debug - Messages to display:", messages)
        
        # Add user message first
        if messages and messages[0]['role'] == 'user':
            full_response += f"👤 **You asked about:** {messages[0]['content']}\n\n"
            message_placeholder.markdown(full_response)
            time.sleep(1)  # Pause for effect
        
        # Display each message with a delay
        for msg in messages[1:]:  # Skip the first message (user's question)
            st.write("Debug - Processing message:", msg)
            
            # Skip if message is empty or has no content
            if not msg or not msg.get('content'):
                continue
                
            # Skip if content is just a repeat of the user's question
            if msg['content'].endswith(messages[0]['content']):
                continue
            
            # Add appropriate emoji based on role
            emoji = "🎙️" if msg['role'].lower() == "host" else "👥"
            
            # Format the message
            formatted_msg = f"{emoji} **{msg['role']}:** {msg['content']}\n\n"
            
            # Add to full response and display
            full_response += formatted_msg
            message_placeholder.markdown(full_response)
            time.sleep(0.8)  # Add delay between messages
            
    except Exception as e:
        st.error(f"Error in display_messages: {str(e)}")
        st.write("Debug - Display error:", str(e))
        raise e

# Page title
st.title("Multi-Agent Discussion Panel")

# Create two columns for the layout
left_col, right_col = st.columns([1, 1])

with right_col:
    st.header("Persona Management")
    
    # Create new persona
    with st.expander("Create New Persona", expanded=False):
        persona_name = st.text_input("Persona Name", 
            key="persona_name",
            help="Enter the persona's name (spaces will be removed)")
        persona_description = st.text_area("Persona Description", 
            key="persona_description",
            help="Describe the persona's background, personality, and expertise",
            height=150)
        
        if st.button("Add Persona"):
            if persona_name and persona_description:
                processed_name = process_name(persona_name)
                new_persona = {
                    'name': processed_name,
                    'description': persona_description,
                    'is_host': False,
                    'created_at': datetime.now().isoformat()
                }
                st.session_state.personas.append(new_persona)
                save_personas()
                st.success(f"Added persona: {persona_name}")
                st.rerun()
            else:
                st.error("Please fill in both name and description")

    # Display persona gallery
    st.subheader("Available Personas")
    for persona in st.session_state.personas:
        if not persona.get('is_host'):  # Don't show host in gallery
            with st.expander(f"{persona['name']}", expanded=False):
                st.write(persona['description'])
                if st.button("Delete", key=f"del_{persona['name']}"):
                    st.session_state.personas.remove(persona)
                    save_personas()
                    st.rerun()

with left_col:
    st.header("Discussion Setup")
    
    # Participant selection
    st.subheader("Select Participants")
    
    # Get non-host personas for selection
    available_personas = [p for p in st.session_state.personas if not p.get('is_host')]
    
    # Allow selecting up to 3 additional participants
    for i in range(3):
        col1, col2 = st.columns([3, 1])
        with col1:
            if len(available_personas) > 0:
                selected_persona = st.selectbox(
                    f"Participant {i+1}",
                    options=['None'] + [p['name'] for p in available_personas],
                    key=f"participant_{i}"
                )
                
                if selected_persona != 'None':
                    persona = next(p for p in available_personas if p['name'] == selected_persona)
                    # Update participants list
                    participant_entry = {
                        'role': f'Participant {i+1}',
                        'persona': persona
                    }
                    
                    # Update or add participant
                    if i + 1 < len(st.session_state.participants):
                        st.session_state.participants[i + 1] = participant_entry
                    else:
                        st.session_state.participants.append(participant_entry)
            else:
                st.warning("Create some personas first!")

    # Chat interface
    st.subheader("Discussion")
    user_input = st.text_area("Enter your topic or question:", key="user_input", height=100)
    
    if st.button("Start Discussion"):
        if user_input:
            # Get active participants
            active_participants = [p for p in st.session_state.participants 
                                if p['persona']['name'] != 'None']
            
            if len(active_participants) < 2:
                st.error("Please select at least one participant besides the host")
            else:
                # Create a placeholder for the chat
                message_placeholder = st.empty()
                
                with st.spinner("Starting discussion..."):
                    try:
                        # Clear previous chat history
                        st.session_state.chat_history = []
                        
                        # Add user's question
                        st.session_state.chat_history.append({
                            'role': 'user',
                            'content': user_input
                        })
                        
                        # Run the chat
                        messages = run_chat(user_input, active_participants)
                        
                        if messages:
                            # Display messages in streaming fashion
                            display_messages(
                                messages,  # Remove the extra user message since it's already in messages
                                message_placeholder
                            )
                            
                            # Store final messages in session state
                            st.session_state.chat_history = messages  # Store all messages directly
                        else:
                            st.error("No messages were generated from the chat.")
                        
                    except Exception as e:
                        st.error(f"An error occurred: {str(e)}")
                        st.write("Debug - Full error:", e)
                        import traceback
                        st.write("Debug - Traceback:", traceback.format_exc())
        else:
            st.error("Please enter a topic or question") 