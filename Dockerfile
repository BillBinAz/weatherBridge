# Use specific Python version for reproducibility
FROM python:3.13-alpine

# Set metadata
LABEL maintainer="weather-bridge"
LABEL description="Weather data aggregation service"
LABEL version="1.0"

WORKDIR /weather-bridge

# Install system dependencies
RUN apk update && apk upgrade && apk add --no-cache bash curl

# Copy application files
COPY requirements.txt .
COPY ./src .
COPY ./config/startup.sh /weather-bridge/startup.sh

# Set permissions and install Python dependencies
RUN chmod 755 /weather-bridge/startup.sh && \
    pip3 install --upgrade pip && \
    pip3 install -r requirements.txt

# Set Flask environment
ENV FLASK_APP=get_handler.py

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8080/weather || exit 1

EXPOSE 8080
ENTRYPOINT ["/weather-bridge/startup.sh"]
