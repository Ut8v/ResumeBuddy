from openai import OpenAI
from app.configs.config import settings

CLIENT = OpenAI(api_key=settings.OPENAI_API_KEY)


def __unscape(s: str) -> str:
    return s.replace("\\n", "\n")


def call_agent(text: str, description: str) -> str:
    resume_txt = text or ""
    jd = description or ""

    SYSTEM_PROMPT = __unscape(settings.PROMPT_SYSTEM).strip()
    USER_PROMPT = __unscape(settings.PROMPT_ATS_USER_TEMPLATE).format(
        resume_text=resume_txt,
        job_description=jd
    ).strip()

    agent_response = CLIENT.responses.create(
        model=settings.OPENAI_MODEL,
        instructions=SYSTEM_PROMPT,
        input=USER_PROMPT,
        max_output_tokens=settings.MAX_OPENAI_TOKENS,
        temperature=0.2,
    )

    return __unscape(agent_response.output_text).strip()
