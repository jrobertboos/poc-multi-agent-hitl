from .agent_instance import HitlChatAgent
from llama_stack.providers.inline.agents.meta_reference.persistence import AgentInfo

from llama_stack.providers.inline.agents.meta_reference.agents import (
    MetaReferenceAgentsImpl,
)

from llama_stack.apis.inference import Inference
from llama_stack.apis.safety import Safety
from llama_stack.apis.tools import ToolGroups, ToolRuntime
from llama_stack.apis.vector_io import VectorIO

from .config import HitlAgentsImplConfig


class HitlAgentsImpl(MetaReferenceAgentsImpl):
    def __init__(
        self,
        config: HitlAgentsImplConfig,
        inference_api: Inference,
        vector_io_api: VectorIO,
        safety_api: Safety,
        tool_runtime_api: ToolRuntime,
        tool_groups_api: ToolGroups,
    ):
        super().__init__(
            config,
            inference_api,
            vector_io_api,
            safety_api,
            tool_runtime_api,
            tool_groups_api,
        )
        self.config = config

    async def _get_agent_impl(self, agent_id: str) -> HitlChatAgent:
        agent_info_json = await self.persistence_store.get(
            key=f"agent:{agent_id}",
        )
        if not agent_info_json:
            raise ValueError(f"Could not find agent info for {agent_id}")

        try:
            agent_info = AgentInfo.model_validate_json(agent_info_json)
        except Exception as e:
            raise ValueError(f"Could not validate agent info for {agent_id}") from e

        return HitlChatAgent(
            agent_id=agent_id,
            agent_config=agent_info,
            inference_api=self.inference_api,
            safety_api=self.safety_api,
            vector_io_api=self.vector_io_api,
            tool_runtime_api=self.tool_runtime_api,
            tool_groups_api=self.tool_groups_api,
            persistence_store=(
                self.persistence_store
                if agent_info.enable_session_persistence
                else self.in_memory_store
            ),
            created_at=agent_info.created_at,
            hil_endpoint=self.config.hil_endpoint
        )
