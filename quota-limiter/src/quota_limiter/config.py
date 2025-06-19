from typing import Any

from pydantic import BaseModel

class QuotaLimiterConfig(BaseModel):
    inital_quota: int = 100
    db_path: str = "quota.txt"
    
    @classmethod
    def sample_run_config(cls, __distro_dir__: str, **kwargs: Any) -> dict[str, Any]:
        return {
            "inital_quota": 100,
            "db_path": "quota.txt",
        }
