from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="gwc-siem",
    version="1.0.0",
    author="GWC Academy",
    author_email="contact@gwcacademy.com",
    description="A lightweight Security Information and Event Management (SIEM) system for home labs and education",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Shubham11440/gwc-siem",
    project_urls={
        "Bug Tracker": "https://github.com/Shubham11440/gwc-siem/issues",
        "Documentation": "https://github.com/Shubham11440/gwc-siem/wiki",
        "Source Code": "https://github.com/Shubham11440/gwc-siem",
        "Discord": "https://discord.gg/YMJp48qbwR",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Intended Audience :: Education",
        "Topic :: Security",
        "Topic :: System :: Logging",
        "Topic :: System :: Monitoring",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
        "Environment :: Web Environment",
        "Framework :: FastAPI",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.4.3",
            "pytest-asyncio>=0.21.1",
            "pytest-cov>=4.1.0",
            "black>=23.11.0",
            "flake8>=6.1.0",
            "mypy>=1.7.1",
            "pre-commit>=3.6.0",
        ],
        "docs": [
            "mkdocs>=1.5.3",
            "mkdocs-material>=9.4.8",
        ],
        "geoip": [
            "geoip2>=4.7.0",
            "maxminddb>=2.2.0",
        ],
        "notifications": [
            "jinja2>=3.1.2",
            "aiosmtplib>=2.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "gwc-siem=cli.app:main",
            "gwc-siem-api=api.main:start_server",
        ],
    },
    include_package_data=True,
    package_data={
        "gwc-siem": [
            "config/*.yaml",
            "web/*.html",
            "web/static/*",
            "sample_data/*",
        ],
    },
    keywords=[
        "siem",
        "security",
        "logging",
        "monitoring",
        "threat-detection",
        "cybersecurity",
        "log-analysis",
        "intrusion-detection",
        "security-monitoring",
        "fastapi",
        "sqlite",
        "homelab",
        "education",
        "hacktoberfest",
    ],
    zip_safe=False,
)