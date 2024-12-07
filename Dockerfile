FROM python:3.7.4-slim

# Install system dependencies
RUN apt-get update && apt-get install -qq -y \
    build-essential \
    libpq-dev \
    curl \
    --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

ENV INSTALL_PATH /katana-nbi
WORKDIR $INSTALL_PATH

# Create directories
RUN mkdir -p /targets

# Copy configuration files first
COPY config/wim_targets.json /targets/wim_targets.json
COPY config/vim_targets.json /targets/vim_targets.json

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Add healthcheck
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/ || exit 1

# Command to run the application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--config", "gunicorn.conf.py", "katana.app:create_app()"]