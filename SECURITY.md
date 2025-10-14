# Security Policy 🛡️

## Supported Versions

We release patches for security vulnerabilities in the following versions:

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Security Considerations

### Data Handling
- **Log Data**: GWC-SIEM processes log files that may contain sensitive information
- **Local Storage**: All data is stored locally in SQLite database
- **No Cloud Dependencies**: No data is transmitted to external services by default

### Threat Model
GWC-SIEM is designed for:
- ✅ Home lab environments
- ✅ Educational purposes
- ✅ Small-scale security monitoring
- ✅ Development and testing

GWC-SIEM is **NOT** designed for:
- ❌ Production enterprise environments without additional hardening
- ❌ Processing highly sensitive or classified data
- ❌ Direct internet exposure without proper security controls

## Reporting a Vulnerability

### For Non-Critical Issues
For general security improvements or minor vulnerabilities:
1. Open a GitHub issue with the `security` label
2. Provide a clear description of the potential risk
3. Include steps to reproduce if applicable

### For Critical Security Issues
For severe vulnerabilities that could lead to:
- Remote code execution
- Privilege escalation
- Data exposure
- Authentication bypass

**Please disclose privately:**

📧 **Email**: [security@gwcacademy.com](mailto:security@gwcacademy.com)
🔐 **PGP Key**: Available on request

### What to Include
When reporting security issues, please provide:

1. **Vulnerability Type**: RCE, XSS, SQL injection, etc.
2. **Affected Component**: API, CLI, parsers, etc.
3. **Attack Vector**: How the vulnerability can be exploited
4. **Impact Assessment**: What data/systems are at risk
5. **Proof of Concept**: Steps to reproduce (if safe to share)
6. **Suggested Fix**: If you have ideas for mitigation

### Response Timeline
- **Initial Response**: Within 48 hours
- **Triage**: Within 7 days
- **Fix Development**: Based on severity (1-30 days)
- **Coordinated Disclosure**: After fix is available

## Security Best Practices

### For Users
1. **Network Security**
   - Run GWC-SIEM in isolated network environments
   - Use firewall rules to restrict API access
   - Don't expose the API directly to the internet

2. **Data Protection**
   - Sanitize logs before processing if they contain PII
   - Regularly rotate SQLite database files
   - Use encrypted storage for sensitive log data

3. **Access Control**
   - Limit file system permissions for log directories
   - Run with minimal required privileges
   - Use virtual environments for isolation

### For Developers
1. **Input Validation**
   - All log parsers must validate input data
   - API endpoints should sanitize user input
   - File uploads must be properly validated

2. **Dependency Management**
   - Keep dependencies updated
   - Use `pip audit` to check for known vulnerabilities
   - Pin specific versions in production

3. **Code Review**
   - Security-focused code reviews for all changes
   - Static analysis tools integration
   - Regular dependency audits

## Known Security Considerations

### Current Limitations
1. **No Authentication**: API endpoints have no built-in authentication
2. **File Upload**: Web interface allows log file uploads without strict validation
3. **SQL Injection**: While using SQLite with parameterized queries, custom detections should be carefully reviewed
4. **Path Traversal**: File handling operations need careful validation

### Planned Security Enhancements
- [ ] Optional API authentication (JWT/API keys)
- [ ] File upload restrictions and validation
- [ ] Rate limiting for API endpoints
- [ ] Audit logging for all operations
- [ ] Container security best practices guide

## Security Features

### Current Protections
1. **Local-Only Storage**: No external data transmission
2. **Parameterized Queries**: Protection against SQL injection
3. **Input Sanitization**: Basic validation in parsers
4. **Error Handling**: Prevents information disclosure through error messages

### Planned Features
1. **RBAC**: Role-based access control
2. **Encryption**: Optional database encryption
3. **Sandboxing**: Isolated execution environments
4. **Integrity Checks**: Log file tampering detection

## Compliance and Standards

### Standards Alignment
- **OWASP Top 10**: Regular assessment against web application risks
- **CIS Controls**: Alignment with critical security controls
- **NIST Cybersecurity Framework**: Following framework guidelines

### Privacy Considerations
- **GDPR**: Guidelines for handling EU personal data in logs
- **Data Minimization**: Processing only necessary log fields
- **Retention Policies**: Recommendations for log data lifecycle

## Security Resources

### Documentation
- [OWASP SIEM Security Guide](https://owasp.org/www-community/SIEM_Security)
- [NIST SP 800-92](https://csrc.nist.gov/publications/detail/sp/800-92/final) - Guide to Computer Security Log Management

### Tools and Testing
- **Static Analysis**: Bandit, Semgrep
- **Dependency Scanning**: Safety, pip-audit
- **Container Scanning**: Trivy, Clair
- **Dynamic Testing**: OWASP ZAP for API testing

## Vulnerability Disclosure Policy

### Our Commitment
- We will acknowledge receipt of vulnerability reports
- We will provide regular updates on fix progress
- We will credit researchers in security advisories (unless requested otherwise)
- We will not take legal action against good faith security research

### Safe Harbor
We consider the following activities as authorized:
- Testing on your own installations
- Responsible disclosure of findings
- Avoiding data destruction or privacy violations
- Not performing attacks against other users

## Contact Information

For security-related questions or concerns:

- **Email**: security@gwcacademy.com
- **Discord**: [Security Channel](https://discord.gg/YMJp48qbwR)
- **GitHub**: Use private vulnerability reporting feature

---

**Note**: This is a community-driven open-source project. While we take security seriously, users should evaluate the security posture based on their specific requirements and threat model.