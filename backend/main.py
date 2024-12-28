import os
import datetime
from typing import List, Optional, Dict
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.conditions import TextMentionTermination
from config.agent_configs import AGENT_CONFIGS
from config.dialogue_rules import DIALOGUE_RULES
import PyPDF2
import io

# Load environment variables
load_dotenv()

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("FRONTEND_URL", "http://localhost:3000")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Store for uploaded documents and their content, organized by agent
documents: Dict[str, Dict[str, Dict]] = {
    "elon_musk": {},
    "steve_jobs": {},
    "zhang_yiming": {}
}

class Message(BaseModel):
    content: str
    selected_agents: List[str]
    context: Optional[List[dict]] = []

def create_agent(name: str) -> AssistantAgent:
    """Create an AutoGen agent with specific personality."""
    config = AGENT_CONFIGS.get(name, {})
    display_name = name.replace('_', ' ').title()
    
    # Create a comprehensive system message that combines persona and dialogue rules
    system_message = f"""
{config.get('persona', '')}

INTERACTION GUIDELINES:

1. Response Structure:
- {DIALOGUE_RULES['Response Structure']['Length']}
- Quick Reaction: {DIALOGUE_RULES['Response Structure']['Components']['Quick_Reaction']}
- Main Point: {DIALOGUE_RULES['Response Structure']['Components']['Main_Point']}
- Challenge: {DIALOGUE_RULES['Response Structure']['Components']['Challenge']}

2. Conflict Generation:
- Philosophical Tensions: {', '.join(DIALOGUE_RULES['Conflict Generation']['Philosophical Tensions'])}
- Direct Challenge: {DIALOGUE_RULES['Conflict Generation']['Required Elements']['Direct_Challenge']}
- Counter Example: {DIALOGUE_RULES['Conflict Generation']['Required Elements']['Counter_Example']}
- Technical Correction: {DIALOGUE_RULES['Conflict Generation']['Required Elements']['Technical_Correction']}
- Pointed Question: {DIALOGUE_RULES['Conflict Generation']['Required Elements']['Pointed_Question']}

Remember: Stay true to your core traits and experiences while following these interaction guidelines.
"""
    
    return AssistantAgent(
        name=name,
        model_client=OpenAIChatCompletionClient(
            model="gpt-4-turbo-preview",
            api_key=os.getenv("OPENAI_API_KEY"),
            max_tokens=300
        ),
        system_message=system_message,
        description=f"Agent representing {display_name}"
    )

@app.post("/upload-document")
async def upload_document(
    file: UploadFile = File(...),
    agent_name: str = Form(...)
):
    """Handle document uploads for agents."""
    try:
        content = await file.read()
        
        # Handle different file types
        if file.filename.endswith('.pdf'):
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(content))
            content = ""
            for page in pdf_reader.pages:
                content += page.extract_text()
        elif file.filename.endswith('.txt'):
            content = content.decode()
        else:
            raise HTTPException(status_code=400, detail="Unsupported file type")

        # Store document
        if agent_name not in documents:
            documents[agent_name] = {}
            
        file_id = str(len(documents[agent_name]) + 1)
        documents[agent_name][file_id] = {
            "name": file.filename,
            "content": content,
            "timestamp": datetime.datetime.now().isoformat()
        }

        return {
            "id": file_id,
            "name": file.filename,
            "timestamp": documents[agent_name][file_id]["timestamp"]
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/documents/{agent_name}")
async def get_documents(agent_name: str):
    """Get all documents for a specific agent."""
    if agent_name not in documents:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    return {
        "documents": [
            {
                "id": doc_id,
                "name": doc["name"],
                "timestamp": doc["timestamp"]
            }
            for doc_id, doc in documents[agent_name].items()
        ]
    }

@app.post("/chat")
async def chat(message: Message):
    try:
        # Create agents for selected personalities
        agents = [create_agent(name.lower().replace(' ', '_')) for name in message.selected_agents]
        
        # Create team chat
        termination = TextMentionTermination("TERMINATE")
        agent_team = RoundRobinGroupChat(
            agents,
            termination_condition=termination,
            max_turns=10
        )

        # Run the team chat
        responses = []
        async for response in agent_team.run_stream(task=message.content):
            # Check if it's a message from an agent
            if hasattr(response, 'source') and response.source in [agent.name for agent in agents]:
                # Convert underscore name back to display name
                display_name = response.source.replace('_', ' ').title()
                responses.append({
                    "type": "agent",
                    "speaker": display_name,
                    "content": response.content,
                    "timestamp": datetime.datetime.now().isoformat()
                })

        return {"responses": responses}
    except Exception as e:
        print(f"Error in chat endpoint: {str(e)}")
        return {
            "responses": [{
                "type": "agent",
                "speaker": "System",
                "content": f"Error: {str(e)}",
                "timestamp": datetime.datetime.now().isoformat()
            }]
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)