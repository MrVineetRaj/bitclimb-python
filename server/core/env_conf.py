from dotenv import load_dotenv
load_dotenv()
from pydantic import BaseModel
import os

class EnvConf(BaseModel):
    # PORT:int
    DATABASE_URL: str
    DATABASE_USER: str
    DATABASE_PASS: str

    GITHUB_CLIENT_SECRET: str
    GITHUB_CLIENT_ID: str


def get_env_conf() -> EnvConf:
    return EnvConf(
        # PORT=int(os.environ["PORT"]),
        DATABASE_URL=os.environ["DATABASE_URL"],
        DATABASE_USER=os.environ["DATABASE_USER"],
        DATABASE_PASS=os.environ["DATABASE_PASS"],
        GITHUB_CLIENT_SECRET=os.environ["GITHUB_CLIENT_SECRET"],
        GITHUB_CLIENT_ID=os.environ["GITHUB_CLIENT_ID"],
    )

env_conf = get_env_conf()
