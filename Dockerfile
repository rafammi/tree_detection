FROM ghcr.io/astral-sh/uv:python3.13-bookworm

WORKDIR /app

ENV UV_LINK_MODE=copy
ENV UV_HTTP_TIMEOUT=120


COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --no-dev

COPY . .

CMD ["uv", "run", "tree_detect_kd.py"]
