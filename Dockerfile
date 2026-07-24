FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /work

COPY pyproject.toml README.md ./
COPY src ./src
RUN python -m pip install --upgrade pip \
    && python -m pip install --editable ".[dev]"

COPY . .

EXPOSE 8888

CMD ["jupyter", "lab", "--ServerApp.ip=0.0.0.0", "--ServerApp.port=8888", "--ServerApp.root_dir=/work", "--ServerApp.open_browser=False", "--ServerApp.allow_root=True"]
