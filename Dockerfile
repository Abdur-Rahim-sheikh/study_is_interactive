FROM python:3.13.3-alpine3.21

WORKDIR /app
COPY . .
RUN pip install uv
RUN uv sync

CMD ["uv","run", "main.py"]