FROM python:3.11-slim

# Keep Python output unbuffered for container logs
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install system packages required to compile or handle gettext files
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc gettext libgettextpo-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . /app

# Compile translations (if .po files are present)
RUN python scripts/compile_translations.py || true

# Create data dir (mounted at runtime)
RUN mkdir -p /app/data

# Default entrypoint: run a python module/file. Override with `docker run image python your_bot.py`
ENTRYPOINT ["python", "-u"]
CMD ["bot_example.py"]
