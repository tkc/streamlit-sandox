# Base Python image
FROM python:3.9-slim

# Install uv
RUN pip install uv

# Set working directory
WORKDIR /app

# Copy project files
COPY pyproject.toml ./
COPY README.md ./
COPY uv.lock* ./
COPY src ./src

# Create virtual environment and install dependencies using uv
RUN uv venv /app/.venv && uv pip install -e .

# Set up environment
ENV PYTHONPATH="/app:${PYTHONPATH}"

# Run the Streamlit application
CMD ["/app/.venv/bin/streamlit", "run", "src/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
