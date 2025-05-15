FROM python:3.12-slim-bullseye

RUN apt update && apt upgrade -y

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /interactive_study

COPY ./pyproject.toml ./uv.lock ./

RUN uv sync --frozen

COPY . .

# the exposing part does not do anything but gives hint
EXPOSE 8501 

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

CMD ["uv","run","streamlit", "run", "main.py","--server.port=8501", "--server.address=0.0.0.0"]
