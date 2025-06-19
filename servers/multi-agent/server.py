from mcp.server.fastmcp import FastMCP
from llama_stack_client import LlamaStackClient
from llama_stack_client.lib.agents.agent import Agent
from llama_stack_client.lib.agents.event_logger import EventLogger

mcp = FastMCP(name="mcp-lance")

TOOL_STACK_URL = 'http://localhost:8003'
BIOLOGY_CONTENT = "You are a biology expert assistant. You answer university-level biology questions clearly, using equations and theory where appropriate. You refuse to answer non-biology questions."
PHYSICS_CONTENT = "You are a physics expert assistant. You answer university-level physics questions clearly, using equations and theory where appropriate. You refuse to answer non-physics questions."

tool_stack_client = LlamaStackClient(base_url=TOOL_STACK_URL)
tool_stack_client.shields.register(shield_id="quota-limiter-shield", provider_shield_id="quota-limiter")

def create_agent(client: LlamaStackClient, CONTENT) -> Agent:
    return Agent(
        client=client,
        model=client.models.list()[0].identifier,
        instructions=CONTENT,
        input_shields=["quota-limiter-shield"],
    )

biology_agent = create_agent(tool_stack_client, BIOLOGY_CONTENT)
biology_session_id = biology_agent.create_session("bio-session")

physics_agent = create_agent(tool_stack_client, PHYSICS_CONTENT)
physics_session_id = physics_agent.create_session("phy-session")


@mcp.tool()
def biology(text: str) -> str:
    """Answer Biology questions."""
    response = biology_agent.create_turn(
        messages=[
            {
                "role": "user",
                "content": text,
            }
        ],
        session_id=biology_session_id,
    )
        
    acc = ""
    for log in EventLogger().log(response):
        if log.role:
            print(log.role)
        acc += log.content

    return acc


@mcp.tool()
def physics(text: str) -> str:
    """Answer Physics questions."""
    response = physics_agent.create_turn(
        messages=[
            {
                "role": "user",
                "content": text,
            }
        ],
        session_id=physics_session_id,
    )
        
    acc = ""
    for log in EventLogger().log(response):
        if log.role:
            print(log.role)
        acc += log.content

    return acc


if __name__ == "__main__":
    mcp.run(transport="sse")
