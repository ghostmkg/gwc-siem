# Contributing to GWC-SIEM 🤝

Thank you for your interest in contributing to GWC-SIEM! This project welcomes contributions from developers of all skill levels.

## 🎯 Getting Started

### Prerequisites
- Python 3.8+
- Git
- Basic understanding of security concepts (helpful but not required)

### Development Setup

1. **Fork the repository**
   ```bash
   # Click the "Fork" button on GitHub, then clone your fork
   git clone https://github.com/your-username/gwc-siem.git
   cd gwc-siem
   ```

2. **Set up development environment**
   ```bash
   # Create virtual environment
   python -m venv .venv
   
   # Activate virtual environment
   # On Windows:
   .venv\Scripts\activate
   # On macOS/Linux:
   source .venv/bin/activate
   
   # Install dependencies
   pip install -e .
   pip install pytest black flake8 mypy
   ```

3. **Verify setup**
   ```bash
   # Run tests
   pytest -v
   
   # Start the API server
   uvicorn api.main:app --reload
   ```

## 🔄 Development Workflow

### Creating a Feature Branch
```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/issue-description
```

### Making Changes
1. Write clean, well-documented code
2. Add tests for new functionality
3. Update documentation if needed
4. Follow the existing code style

### Code Quality Checks
```bash
# Format code
black .

# Check linting
flake8 .

# Type checking
mypy core/ api/ cli/

# Run tests
pytest -v --cov=core --cov=api
```

### Submitting Changes
1. Commit your changes with descriptive messages:
   ```bash
   git add .
   git commit -m "feat: add Apache log parser support"
   ```

2. Push to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

3. Create a Pull Request on GitHub

## 🎨 Contribution Guidelines

### Code Style
- Follow PEP 8 for Python code
- Use meaningful variable and function names
- Add docstrings for functions and classes
- Keep functions small and focused

### Commit Messages
Follow conventional commits format:
- `feat:` new features
- `fix:` bug fixes
- `docs:` documentation changes
- `test:` adding tests
- `refactor:` code refactoring

### Testing
- Write unit tests for new functionality
- Ensure all tests pass before submitting PR
- Add integration tests for API endpoints
- Test with sample log data

## 🎯 Areas for Contribution

### 🚀 Good First Issues
- Add new log parsers (Apache, IIS, etc.)
- Improve error handling and logging
- Add more detection rules
- Enhance the web dashboard UI
- Write additional test cases

### 🔥 Advanced Contributions
- Performance optimizations
- Advanced threat detection algorithms
- Integration with external APIs
- Kubernetes deployment manifests
- Real-time log streaming

### 📚 Documentation
- API documentation improvements
- Tutorial videos or blog posts
- Architecture diagrams
- Deployment guides

## 🐛 Bug Reports

When reporting bugs, please include:

1. **Environment details**: OS, Python version, installed packages
2. **Steps to reproduce**: Clear, step-by-step instructions
3. **Expected vs actual behavior**
4. **Error messages**: Full stack traces if applicable
5. **Sample data**: Anonymized log files if relevant

Use the bug report template when creating issues.

## 💡 Feature Requests

For new features:

1. Check existing issues to avoid duplicates
2. Describe the problem your feature solves
3. Provide implementation ideas if you have them
4. Consider contributing the feature yourself!

## 📋 Pull Request Process

1. **Link to an issue**: Reference the issue your PR addresses
2. **Describe changes**: Clear description of what you changed and why
3. **Update docs**: Update README.md or other docs if needed
4. **Add tests**: Include tests for new functionality
5. **Check CI**: Ensure all CI checks pass

### PR Template Checklist
- [ ] Tests added/updated and passing
- [ ] Documentation updated
- [ ] Code follows project style guidelines
- [ ] Commit messages follow conventional format
- [ ] No breaking changes (or clearly documented)

## 🤝 Community Guidelines

- Be respectful and inclusive
- Help newcomers get started
- Provide constructive feedback
- Focus on the code, not the person
- Follow the [Code of Conduct](https://www.contributor-covenant.org/version/2/0/code_of_conduct/)

## 🏆 Recognition

Contributors will be:
- Added to the README.md contributors section
- Mentioned in release notes for significant contributions
- Invited to join the core maintainer team for outstanding ongoing contributions

## 📞 Getting Help

- **Discord**: [Join our community](https://discord.gg/YMJp48qbwR)
- **Telegram**: [GWC Academy](https://t.me/gwcacademy)
- **GitHub Discussions**: For longer form discussions
- **Issues**: For specific bugs or feature requests

## 🎉 Hacktoberfest Participation

This project participates in Hacktoberfest! Look for issues labeled `hacktoberfest` and `good-first-issue` to get started.

Thank you for contributing to GWC-SIEM! 🛡️