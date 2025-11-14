from authlib.integrations.starlette_client import OAuth
from core.env_conf import env_conf

oauth = OAuth()

oauth.register(
    name="github",
    client_id=env_conf.GITHUB_CLIENT_ID,
    client_secret=env_conf.GITHUB_CLIENT_SECRET,
    access_token_url="https://github.com/login/oauth/access_token",
    authorize_url="https://github.com/login/oauth/authorize",
    api_base_url="https://api.github.com/",
    client_kwargs={"scope": "read:user user:email"}
)
