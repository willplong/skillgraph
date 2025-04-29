import traceback
import uuid

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from skillgraph.config import ALLOWED_ORIGINS
from skillgraph.graph import Graph, Skill
from skillgraph.llm import AnthropicModel
from skillgraph.utils import load_prompt, parse_json_response


# Define request and response models
class GraphRequest(BaseModel):
    skill_level: str
    topic: str
    id: str | None = None


class GraphResponse(BaseModel):
    id: str
    graph_text: str
    num_skills: int


class ErrorResponse(BaseModel):
    error: str
    traceback: str | None = None


# Initialize FastAPI app
app = FastAPI(title="Skill Graph Generator API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Store generated graphs
graphs: dict[str, dict] = {}


def generate_prerequisites(
    skill: Skill, llm: AnthropicModel, user_skill_level: str, max_retries: int = 3
) -> list[Skill]:
    prompt = load_prompt("generate_prerequisites").format(
        name=skill.name, description=skill.description, level=user_skill_level
    )
    prerequisites_data = parse_json_response(llm, prompt, max_retries)
    prerequisites = [
        Skill(name=prereq["name"], description=prereq["description"])
        for prereq in prerequisites_data
    ]
    return prerequisites


@app.get("/api/health")
async def health_check():
    return {"status": "healthy"}


@app.post("/api/generate", response_model=GraphResponse)
async def generate_graph(request: GraphRequest):
    # Use provided ID or generate new one
    graph_id = request.id or str(uuid.uuid4())

    try:
        # Create root skill from the topic
        root_skill = Skill(
            name=request.topic, description=f"Learning about {request.topic}"
        )

        # Initialize LLM with system prompt
        system_prompt = load_prompt("system").format(
            root_skill=root_skill.name,
            root_skill_description=root_skill.description,
            user_skill_level=request.skill_level,
        )
        llm = AnthropicModel(system_prompt=system_prompt)

        # Generate graph
        graph = Graph(root=root_skill)
        skill_queue = [root_skill]
        processed_skills = set()

        while skill_queue:
            current_skill = skill_queue.pop(0)
            if current_skill.id in processed_skills:
                continue

            # Generate prerequisites for current skill
            prerequisites = generate_prerequisites(
                current_skill, llm, request.skill_level
            )
            processed_skills.add(current_skill.id)

            for prerequisite in prerequisites:
                graph.add_prerequisite(current_skill, prerequisite)
                skill_queue.append(prerequisite)

        # Generate text representation of the graph
        graph_text = []

        def build_text_representation(skill_id: str, level: int = 0):
            node = graph._nodes[skill_id]
            indent = "  " * level
            graph_text.append(f"{indent}- {node.skill.name}")
            for child_id in node.child_ids:
                build_text_representation(child_id, level + 1)

        build_text_representation(root_skill.id)

        # Store the result
        result = {
            "graph_text": "\n".join(graph_text),
            "num_skills": len(processed_skills),
        }
        graphs[graph_id] = result

        return GraphResponse(id=graph_id, **result)

    except Exception as e:
        # Get detailed error information
        error_details = traceback.format_exc()
        print(f"ERROR: {str(e)}")
        print(f"TRACEBACK: {error_details}")
        raise HTTPException(
            status_code=500, detail={"error": str(e), "traceback": error_details}
        ) from e


@app.post("/api/test-post")
async def test_post(request: dict):
    print("Test-post endpoint called")
    print(f"Received test data: {request}")
    return {"status": "ok", "received": request}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
