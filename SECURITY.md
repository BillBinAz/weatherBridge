# Security Policy

## Supported Versions

Current version support for security updates:

| Version | Supported          | Status      |
|---------|------------------|-------------|
| 1.x     | :white_check_mark: | Current     |
| 0.x     | :x:                | End of Life |

## Security Considerations

### Dependencies
- All dependencies are regularly scanned for known vulnerabilities using GitHub's dependabot
- Dependencies are kept up-to-date with security patches
- Pinned versions in `requirements.txt` ensure reproducible builds

### API Security
- The `/weather` endpoint provides read-only access to aggregated data
- No authentication required for data retrieval
- Deploy behind a reverse proxy (nginx, Traefik) for production use
- Consider implementing rate limiting for public deployments

### Credential Management
- 1Password integration is used for secure credential storage
- Never commit credentials to version control
- Use environment variables for sensitive configuration
- The `OP_CONNECT_HOST` environment variable should point to a secure 1Password Connect instance

### Docker Security
- Uses minimal Alpine Linux base image for reduced attack surface
- Non-root user execution recommended (can be added to Dockerfile)
- Regular base image updates via CI/CD pipeline
- Health checks enabled for container orchestration

### Container Deployment
- Run containers with read-only root filesystem where possible
- Use resource limits (CPU, memory) to prevent DoS
- Deploy behind a load balancer with rate limiting
- Use secrets management instead of passing credentials in environment

## Reporting a Vulnerability

If you discover a security vulnerability, please email: [security@weatherbridge.local](mailto:security@weatherbridge.local)

**Please do not create a public GitHub issue for security vulnerabilities.**

### Reporting Process
1. Email the security team with vulnerability details
2. Include proof-of-concept or steps to reproduce if possible
3. Allow 7 days for initial response
4. Security patches are released within 30 days for critical issues

### Expectations
- Acknowledgment of report within 48 hours
- Regular updates on remediation progress
- Credit in release notes (unless you prefer anonymity)
- CVE assignment for critical vulnerabilities
