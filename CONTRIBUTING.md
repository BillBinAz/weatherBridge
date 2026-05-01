# Contributing to WeatherBridge

Thank you for your interest in contributing to WeatherBridge! This document provides guidelines and instructions for contributing.

## Code of Conduct

- Be respectful and professional in all interactions
- Welcome diverse perspectives and experiences
- Focus on constructive feedback
- Report inappropriate behavior to the maintainers

## Getting Started

### Prerequisites
- Python 3.13+
- Git
- Docker (recommended)

### Development Setup

1. **Fork and Clone**
   ```bash
   git clone https://github.com/yourusername/weatherBridge.git
   cd weather-bridge
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Environment Variables**
   ```bash
   export OP_CONNECT_HOST=http://localhost:8080
   export FLASK_ENV=development
   ```

### Making Changes

1. **Create a Feature Branch**
   ```bash
   git checkout -b feature/your-feature-name
   git checkout -b fix/your-bug-fix
   ```

2. **Follow Code Style**
   - Follow PEP 8 guidelines
   - Use meaningful variable and function names
   - Add docstrings to functions and classes
   - Add type hints where appropriate

3. **Write Tests**
   - Add tests for new features
   - Ensure all tests pass: `python -m unittest discover tests/ -v`
   - Maintain or improve code coverage

4. **Commit Messages**
   ```
   [TYPE] Brief description
   
   Detailed explanation of changes (if needed)
   
   - Bullet point 1
   - Bullet point 2
   ```
   
   Types: feat, fix, docs, style, refactor, test, chore

### Testing

Before submitting a pull request, ensure:

```bash
# Run all tests
python -m unittest discover tests/ -v

# Check code style
flake8 . --count --select=E9,F63,F7,F82 --show-source
flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127

# Generate coverage report
coverage run -m unittest discover tests/
coverage report
```

### Docker Testing

```bash
# Build Docker image
docker build -t weatherbridge:test .

# Run container
docker run -p 8080:8080 \
  -e OP_CONNECT_HOST=http://connect-api:8080 \
  weatherbridge:test

# Test API endpoint
curl http://localhost:8080/health
curl http://localhost:8080/weather
```

## Pull Request Process

1. **Update Documentation**
   - Update README.md if needed
   - Update CHANGELOG.md with your changes
   - Add docstrings to new functions

2. **Verify Tests Pass**
   - Run full test suite
   - Ensure coverage doesn't decrease
   - Test on both Python 3.13 and 3.14

3. **Create Pull Request**
   - Use descriptive title
   - Reference related issues (#123)
   - Describe changes in detail
   - Include before/after examples if applicable

4. **Address Feedback**
   - Respond to review comments
   - Make requested changes
   - Re-request review when ready

## Reporting Issues

### Bug Reports
Include:
- Python version and OS
- Steps to reproduce
- Expected vs actual behavior
- Error logs and stack traces
- Screenshots if applicable

### Feature Requests
Include:
- Use case and motivation
- Proposed solution
- Alternative solutions considered
- Examples or mockups

## Documentation

- Keep README.md up-to-date
- Add comments for complex logic
- Update API documentation
- Include examples in docstrings

## Code Review Guidelines

### For Reviewers
- Be constructive and helpful
- Ask questions rather than making demands
- Acknowledge good work
- Suggest improvements, not criticisms

### For Authors
- Remember reviewers are helping you
- Ask clarifying questions
- Be open to feedback
- Don't take comments personally

## Release Process

1. Update CHANGELOG.md
2. Update version numbers
3. Create git tag: `git tag -a v1.x.x -m "Release v1.x.x"`
4. Push tag: `git push origin v1.x.x`
5. GitHub Actions will build and publish

## Development Workflow

```
Main (production)
├── Develop (staging)
│   ├── feature/user-auth
│   ├── feature/data-export
│   ├── fix/timezone-bug
│   └── ...
```

## Questions?

- Check existing GitHub issues
- Review SECURITY.md for security questions
- Check README.md for usage questions
- Create a GitHub Discussion for questions

## License

By contributing, you agree that your contributions will be licensed under the same license as the project.

Thank you for contributing to WeatherBridge! 🌤️

