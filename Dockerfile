# Use the official Python image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Install system dependencies and Rust compiler
RUN apt-get update && \
    apt-get install -y \
    build-essential \
    libjpeg-dev \
    libfreetype6-dev \
    zlib1g-dev \
    liblcms2-dev \
    libopenjp2-7-dev \
    libimagequant-dev \
    libtiff-dev \
    libwebp-dev \
    libharfbuzz-dev \
    libfribidi-dev \
    libxcb1-dev \
    curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y && \
    export PATH="$HOME/.cargo/bin:$PATH"

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port your application runs on
EXPOSE 5000

# Run the application
CMD ["python", "app.py"]
