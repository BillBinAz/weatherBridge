# WeatherBridge

Aggregate residential weather and environmental data from multiple sources (Ecobee, Davis Weather Station, Honeywell Alarm, SensorPush, ThermoWorks) and serve via a unified REST API.

## 🌟 Features

- **Multi-Source Data Aggregation**: Collect data from Ecobee, Davis Weather Stations, Honeywell systems, SensorPush, and ThermoWorks
- **RESTful API**: Simple JSON endpoints for weather data retrieval
- **Containerized**: Production-ready Docker setup with health checks
- **Comprehensive Testing**: 49+ unit tests with full coverage
- **Secure Credential Management**: 1Password integration for secure credentials
- **CI/CD Pipelines**: Automated testing and deployment workflows
- **Environment-Based Configuration**: Flexible setup for different deployment scenarios

## 📋 Prerequisites

- **Docker** & Docker Compose (recommended)
- **Python 3.13+** (for local development)
- **1Password Connect** (for credential management)

## 🚀 Quick Start

### Docker (Recommended)

```bash
# Build the image
docker build -t weatherbridge:latest .

# Run with Docker Compose
docker-compose up -d

# Access the API
curl http://localhost:8080/weather
```

### Manual Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export OP_CONNECT_HOST=http://connect.example.com:8080
export FLASK_APP=get_handler.py

# Run the application
python -m flask run --host=0.0.0.0 --port=8080
```

## 📡 API Endpoints

### GET /weather
Returns aggregated weather data from all configured sources in JSON format.

**Response Example:**
```json
{
  "bedroom_left": { "temp": 72.5 },
  "bedroom_right": { "temp": 71.8 },
  "living_room": { "temp": 73.2 },
  "office": { "temp": 70.5 },
  "master_bedroom": { "temp": 72.0 },
  "hallway_thermostat": { "sensor": { "temp": 71.5 } },
  "whole_house_fan": { "houseTemp": 72.06 }
}
```

### GET /health
Health check endpoint for container orchestration and monitoring.

**Response:**
```json
{ "status": "healthy" }
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `OP_CONNECT_HOST` | 1Password Connect API URL | - | Yes |
| `TZ` | Timezone for the application | `America/Phoenix` | No |
| `PORT` | Flask application port | `8080` | No |
| `FLASK_APP` | Flask application entry point | `get_handler.py` | No |
| `FLASK_ENV` | Flask environment | `production` | No |
| `LOG_FILE` | Log file path | `weather_bridge_rest.log` | No |

### Data Sources Configuration

Each data source requires specific setup in 1Password:

- **Ecobee**: Authorization token in 1Password vault
- **Davis Weather Station**: Network access credentials
- **Honeywell Alarm**: Authentication credentials
- **SensorPush**: API credentials and gateway ID
- **ThermoWorks**: API access credentials

## 🧪 Testing

### Run All Tests

```bash
# Using unittest
python -m unittest discover tests/ -v

# Using pytest
pytest tests/

# With coverage report
coverage run -m unittest discover tests/
coverage report
coverage html  # generates coverage report in htmlcov/
```

### Test Coverage

Current coverage includes:
- Unit tests for all sensor modules (49+ tests)
- Integration tests for data aggregation
- Conversion utility tests
- API endpoint tests
- Mock tests for external API calls

## 📦 Dependencies

- **flask** (3.1.3): Web framework
- **requests** (2.33.0): HTTP client library
- **onepasswordconnectsdk** (2.0.0): 1Password credential management
- **thermoworks-cloud** (0.1.11): ThermoWorks cloud API

## 🐳 Docker Configuration

### Multi-Stage Build Benefits

- Minimal image size using Alpine Linux
- Security health checks with curl
- Automatic service startup with proper signal handling
- Timezone and environment variable support

### Health Check

The container includes a health check that monitors the `/weather` endpoint:
- Interval: 30 seconds
- Timeout: 10 seconds  
- Startup period: 40 seconds (grace period for initialization)
- Retries: 3 attempts before marking unhealthy

## 🔐 Security

For security best practices and vulnerability reporting, see [SECURITY.md](./SECURITY.md).

### Key Security Features

- Secure credential storage via 1Password
- Environment variable isolation
- Health checks for monitoring
- Minimal base image attack surface
- No hardcoded credentials

## 📝 Project Structure

```
weatherBridge/
├── src/                          # Application source code
│   ├── get_handler.py           # Flask API handler
│   ├── stations/                # Data source modules
│   │   ├── home_assistant.py
│   │   ├── sensorPush.py
│   │   ├── wifiLogger.py
│   │   └── thermo_works/
│   ├── utilities/               # Helper modules
│   │   ├── connect.py
│   │   └── conversions.py
│   └── weather/                 # Weather data models
│       ├── data.py
│       └── stations.py
├── tests/                        # Test suite (49+ tests)
├── config/                       # Configuration files
│   └── startup.sh              # Container startup script
├── Dockerfile                    # Container image definition
├── docker-compose.yml           # Multi-container configuration
├── requirements.txt             # Python dependencies
└── SECURITY.md                  # Security policy
```

## 🤝 Contributing

Contributions are welcome! Please ensure:
- All tests pass (`python -m unittest discover tests/`)
- Code follows PEP 8 guidelines
- New features include tests
- Documentation is updated

## 📄 License

See LICENSE file for details.

## 🆘 Troubleshooting

### Application won't start
- Check `OP_CONNECT_HOST` environment variable is set correctly
- Verify 1Password Connect service is running and accessible
- Review logs: `tail -f weather_bridge_rest.log`

### Unhealthy container status
- Check health endpoint: `curl http://localhost:8080/health`
- Review Docker logs: `docker logs weatherbridge`
- Verify port 8080 is accessible

### Data retrieval failures
- Verify all credentials are correctly stored in 1Password
- Check network connectivity to data sources
- Review application logs for specific error messages

## 📞 Support

For issues and questions:
1. Check [SECURITY.md](./SECURITY.md) for security concerns
2. Review application logs
3. Check Docker container health: `docker ps -a`
4. Verify all services are accessible

