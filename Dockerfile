FROM python:3.12.10-slim-bookworm

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /interactive_study

COPY ./pyproject.toml ./uv.lock ./
RUN uv sync --frozen

COPY . .
ENV PATH="/study_is_interactive/.venv/bin:$PATH"

CMD ["streamlit","run", "main.py"]