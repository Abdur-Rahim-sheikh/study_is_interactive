FROM python:3.12-slim-bullseye


RUN apt update && apt upgrade -y
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /interactive_study

COPY ./pyproject.toml ./uv.lock ./
RUN uv sync --frozen

COPY . .

EXPOSE 8501
CMD ["streamlit","run", "main.py"]