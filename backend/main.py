import os
import datetime
from typing import Sequence
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import SelectorGroupChat
from autogen_agentchat.messages import AgentEvent, ChatMessage
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.conditions import TextMentionTermination
from config.agent_configs import AGENT_CONFIGS
from fastapi.responses import StreamingResponse
import json
import asyncio

# Load environment variables
load_dotenv()

# OpenAI API configuration
model_client = OpenAIChatCompletionClient(
    model="gpt-4",
    api_key=os.getenv('OPENAI_API_KEY')
)

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("FRONTEND_URL", "http://localhost:3000")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Message(BaseModel):
    content: str

@app.post("/chat")
async def chat(message: Message):
    async def generate():
        try:
            # Create host
            host = AssistantAgent(
                name="Host",
                description="Late-night radio show host guiding conversations",
                system_message=AGENT_CONFIGS["Host"]["persona"],
                model_client=model_client
            )
            
            # Create guests
            handel = AssistantAgent(
                name="Handel",
                description="Baroque composer specializing in religious music",
                system_message=AGENT_CONFIGS["Handel"]["persona"],
                model_client=model_client
            )
            
            sultan = AssistantAgent(
                name="SultanMehmed",
                description="Ottoman ruler who conquered Constantinople",
                system_message=AGENT_CONFIGS["SultanMehmed"]["persona"],
                model_client=model_client
            )
            
            scott = AssistantAgent(
                name="Scott",
                description="Pioneer of Antarctic exploration",
                system_message=AGENT_CONFIGS["Scott"]["persona"],
                model_client=model_client
            )

            def selector_func(messages: Sequence[AgentEvent | ChatMessage]) -> str | None:
                # If no messages, host starts
                if not messages:
                    return "Host"
                    
                # Get last message's sender and content
                last_message = messages[-1]
                last_speaker = last_message.source
                last_content = last_message.content if hasattr(last_message, 'content') else ''
                
                # After user message, host responds
                if last_speaker == "user":
                    return "Host"
                
                # If host invites specific guest, they must speak next
                if last_speaker == "Host":
                    guests = {
                        "Handel": ["handel", "composer"],
                        "SultanMehmed": ["sultan", "mehmed", "mehmet"],
                        "Scott": ["scott", "explorer"]
                    }
                    
                    for guest, keywords in guests.items():
                        if any(keyword.lower() in last_content.lower() for keyword in keywords):
                            return guest
                    return None  # If no specific invitation, let model choose next speaker
                
                # Every 3-4 turns, let host guide conversation
                if len(messages) % 4 == 0 and last_speaker != "Host":
                    return "Host"
                    
                return None  # Let model choose speaker in other cases

            # Create team chat
            agent_team = SelectorGroupChat(
                participants=[host, handel, sultan, scott],
                selector_func=selector_func,
                model_client=model_client,
                termination_condition=TextMentionTermination("Thank you for listening"),
                max_turns=12
            )

            initial_message = f"Host: Midnight strikes, welcome to 'Starry Night Talks'. Tonight, we received a listener's concern: {message.content}"
            
            async for response in agent_team.run_stream(task=initial_message):
                if hasattr(response, 'source') and response.content:
                    data = {
                        "type": "message",
                        "speaker": response.source,
                        "content": response.content,
                        "timestamp": datetime.datetime.now().isoformat()
                    }
                    yield f"data: {json.dumps(data)}\n\n"
                    await asyncio.sleep(0.1)  # Small delay between messages
                    
        except Exception as e:
            error_data = {
                "type": "error",
                "content": str(e)
            }
            yield f"data: {json.dumps(error_data)}\n\n"

    return StreamingResponse(
        generate(),
        media_type="text/event-stream"
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)