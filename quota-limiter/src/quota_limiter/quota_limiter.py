import logging
from typing import Any

from llama_stack.distribution.datatypes import Api

from llama_stack.apis.inference import (
    Inference,
    Message,
    UserMessage,
)

from llama_stack.apis.safety import (
    RunShieldResponse,
    Safety,
    SafetyViolation,
    ViolationLevel,
)
from llama_stack.apis.shields import Shield
from llama_stack.providers.utils.inference.prompt_adapter import (
    interleaved_content_as_str,
)

from .config import QuotaLimiterConfig

import tiktoken

log = logging.getLogger(__name__)

class QuotaLimiterSafetyImpl(Safety):
    def __init__(self, config: QuotaLimiterConfig, deps) -> None:
        self.config = config
        self.inference_api = deps[Api.inference]

    async def initialize(self) -> None:
        with open(self.config.db_path, "w") as f:
            f.write(f"{self.config.inital_quota}")

        pass

    async def shutdown(self) -> None:
        pass

    async def register_shield(self, shield: Shield) -> None:
        pass

    async def run_shield(
        self,
        shield_id: str,
        messages: list[Message],
        params: dict[str, Any] = None,
    ) -> RunShieldResponse:
        
        message = messages[-1]
        content_text = interleaved_content_as_str(message.content)

        enc = tiktoken.encoding_for_model("gpt-4-turbo")
        tokens = len(enc.encode(content_text))

        db_path = self.config.db_path

        with open(db_path, "r") as f:
            quota = int(f.read())

        if (tokens > quota):
            violation = SafetyViolation(
                violation_level=(ViolationLevel.ERROR),
                user_message=f"Exceeded quota!\nInput Tokens: {tokens}",
                metadata={},
            )
        else:
            violation = SafetyViolation(
                violation_level=(ViolationLevel.INFO),
                user_message=f"Input Tokens: {tokens}",
                metadata={},
            )

            with open(db_path, "w") as f:
                f.write(f"{quota - tokens}")


        return RunShieldResponse(violation=violation)
