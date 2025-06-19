from typing import Any

from .config import QuotaLimiterConfig

async def get_provider_impl(config: QuotaLimiterConfig, deps: dict[str, Any]):
    from .quota_limiter import QuotaLimiterSafetyImpl

    impl = QuotaLimiterSafetyImpl(config, deps)
    await impl.initialize()
    return impl
