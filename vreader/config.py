import os


def get_env(key, default=None, required=False) -> str | None:
    """Wrapper for gathering env vars."""
    if required:
        assert key in os.environ, "Missing Environment Variable: %s" % key
    env = os.environ.get(key, default)
    return str(env) if env is not None else None


class Config:
    """Wrap application configurations

    Attributes
    ----------
    DATA_PATH : str
        The path where to store any resources (default: ./)
    OPENAI_API_KEY : str
        OpenAI API Key - Required
    """

    DATA_PATH: str | None = get_env("DATA_PATH", required=False)
    OPENAI_API_KEY: str | None = get_env("OPENAI_API_KEY", required=True)
