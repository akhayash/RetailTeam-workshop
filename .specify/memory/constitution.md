<!--
Sync Impact Report:
- Version change: 1.0.0 → 1.1.0
- Modified principles:
  - II. Security First → expanded with enterprise compliance frameworks
  - IV. API-First Architecture → added enterprise integration patterns
  - V. Test-Driven Development → expanded with enterprise quality gates
  - VI. Observability → expanded with enterprise SLA/SLO requirements
- Added principles:
  - VIII. Enterprise Change Management
  - IX. Resilience & Business Continuity
  - X. Infrastructure as Code & Environment Parity
- Added sections:
  - Enterprise Compliance & Certification (new section)
  - Expanded Security & Compliance Requirements
  - Expanded Development Workflow & Quality Gates
- Removed sections: None
- Templates requiring updates:
  - .specify/templates/plan-template.md ✅ (Constitution Check compatible)
  - .specify/templates/spec-template.md ✅ (User Scenarios compatible)
  - .specify/templates/tasks-template.md ✅ (Phase structure compatible)
- Follow-up TODOs: None
-->

# VirtualMirror AI Constitution

## Core Principles

### I. Privacy by Design (NON-NEGOTIABLE)

- All user photo data MUST be treated as biometric/sensitive personal
  data under enterprise data classification policies
- Photo processing MUST occur in-memory where possible; persistent
  storage requires explicit user consent and encryption at rest
- No user images MUST be used for model training without anonymization
  and informed opt-in consent
- All PII MUST be separated from analytics and telemetry data
- GDPR, CCPA, and applicable regional privacy regulations MUST be
  satisfied by default — not as an afterthought
- Users MUST have the ability to request deletion of all their data
  (right to erasure) with automated fulfillment within 30 days
- Data Protection Impact Assessments (DPIA) MUST be conducted before
  processing new categories of personal data

### II. Security First

- OWASP Top 10 MUST be addressed in every component
- All API endpoints MUST require authentication and authorization
- Input validation MUST occur at every system boundary — uploaded
  images MUST be validated for type, size, and content before processing
- Secrets and credentials MUST never appear in source code, logs, or
  error messages; enterprise secret management (e.g., Azure Key Vault,
  HashiCorp Vault) MUST be used
- All data in transit MUST use TLS 1.2+; data at rest MUST use
  AES-256 encryption or equivalent
- Dependencies MUST be scanned for known vulnerabilities on every
  build; critical CVEs MUST be patched within 48 hours
- File upload handling MUST prevent path traversal, code injection,
  and denial-of-service via oversized payloads
- Penetration testing MUST be performed at least annually and before
  major releases
- Zero-trust network architecture MUST be assumed — every service
  call MUST be authenticated regardless of network boundary
- Container images MUST be scanned and signed; only approved base
  images from the enterprise registry MUST be used

### III. AI Responsibility & Governance

- The AI model MUST be evaluated for bias across body types, skin
  tones, genders, and age groups before deployment
- Model accuracy metrics MUST be published and tracked per demographic
  segment to detect disparity
- Users MUST be informed they are interacting with an AI system and
  shown confidence levels for fit recommendations
- Model versions MUST be immutable and auditable — every prediction
  MUST be traceable to a specific model version
- A human escalation path MUST exist for disputed or low-confidence
  results
- The system MUST NOT make body-shaming or judgmental statements in
  any output
- An AI Ethics Review Board or designated authority MUST approve new
  model deployments that materially change prediction behavior
- Model cards MUST be maintained documenting intended use, limitations,
  training data provenance, and known biases

### IV. API-First Architecture

- The fit assessment engine MUST be a standalone service with a
  well-defined REST/gRPC integration layer
- API contracts MUST be defined via OpenAPI 3.x (REST) or Protocol
  Buffers (gRPC) before implementation begins
- The service MUST be stateless — session state belongs to the
  consuming frontend
- Backward-compatible versioning MUST be used; breaking changes
  require a new major API version with minimum 6-month deprecation
  period and consumer migration support
- The integration layer MUST support health checks, rate limiting,
  circuit-breaker patterns, and graceful degradation
- API gateway MUST enforce enterprise cross-cutting concerns:
  authentication, throttling, request correlation, and payload
  validation
- Service contracts MUST include SLA definitions (availability,
  latency, throughput) agreed with consuming teams
- Event-driven integration MUST use enterprise message broker
  (e.g., Kafka, Azure Service Bus) for async workflows

### V. Test-Driven Development

- Unit tests MUST be written before implementation (Red-Green-Refactor)
- Integration tests MUST cover all API contract endpoints
- ML model tests MUST validate accuracy thresholds, latency budgets,
  and regression against baseline metrics
- Security tests (SAST, DAST, dependency scanning) MUST run in CI
  on every pull request
- Load tests MUST validate the system handles expected concurrent
  image processing workloads
- Contract tests MUST verify backward compatibility with all known
  consumers before deployment
- Chaos engineering experiments SHOULD be conducted quarterly to
  validate resilience assumptions
- Code coverage MUST meet minimum 80% for business logic; critical
  paths (image processing, prediction serving) MUST have 90%+
- End-to-end tests MUST validate the full user journey in a
  production-like environment before release

### VI. Observability & Model Monitoring

- Structured logging MUST be implemented across all services using
  enterprise-standard correlation IDs
- Model prediction drift MUST be monitored with automated alerting
  when accuracy degrades beyond defined thresholds
- API latency, error rates, and throughput MUST be tracked via
  metrics dashboards with defined SLOs:
  - Availability: 99.9% uptime (measured monthly)
  - Latency: p95 < 2 seconds for fit assessment responses
  - Error rate: < 0.1% 5xx responses under normal load
- Image processing pipelines MUST emit tracing spans for
  end-to-end request correlation (OpenTelemetry standard)
- All anomalies MUST trigger alerts — silent failures are not
  acceptable
- Runbooks MUST exist for every alert with clear escalation paths
- Business metrics (assessment accuracy, return rate correlation)
  MUST be tracked alongside technical metrics
- Log retention MUST comply with enterprise retention policies
  (minimum 90 days hot, 1 year cold storage)

### VII. Data Minimization & Retention

- Only the minimum data required for fit assessment MUST be collected
- Processed images MUST be purged after assessment unless the user
  explicitly opts in to storage for future comparisons
- Retention policies MUST be enforced automatically — manual deletion
  is not a valid strategy
- Audit logs MUST record access to user data with immutable timestamps
- Third-party integrations MUST NOT receive raw user images without
  explicit consent and a data processing agreement
- Data classification labels (Public, Internal, Confidential,
  Restricted) MUST be applied to all data stores and pipelines
- Cross-border data transfer MUST comply with applicable regulations
  (EU SCCs, data residency requirements)

### VIII. Enterprise Change Management

- All production changes MUST follow a formal change management
  process: request → review → approve → implement → validate
- Feature flags MUST be used for progressive rollouts; new
  capabilities MUST NOT be exposed to all users simultaneously
- Rollback procedures MUST be documented and tested for every
  deployment; rollback MUST be achievable within 15 minutes
- Change Advisory Board (CAB) review MUST be obtained for
  infrastructure changes affecting multiple teams or services
- Post-implementation reviews MUST be conducted within 5 business
  days for all significant changes
- Emergency changes MUST follow a streamlined approval path but
  still require post-hoc documentation and review

### IX. Resilience & Business Continuity

- The service MUST be designed for multi-availability-zone deployment
  with automatic failover
- Recovery Point Objective (RPO): < 1 hour for all persistent data
- Recovery Time Objective (RTO): < 30 minutes for service restoration
- Disaster recovery plans MUST be tested at least semi-annually
- Graceful degradation MUST be implemented — if the AI model is
  unavailable, the system MUST return a helpful fallback (e.g.,
  size chart guidance) rather than an error
- Dependency failure MUST NOT cascade; bulkhead and timeout patterns
  MUST isolate failures to individual components
- Capacity planning MUST account for 3x peak load with documented
  auto-scaling policies

### X. Infrastructure as Code & Environment Parity

- All infrastructure MUST be defined as code (Terraform, Bicep, or
  equivalent) and versioned alongside application code
- Environment promotion MUST follow: dev → staging → production
  with identical configurations (differing only in scale and secrets)
- No manual configuration changes MUST be made to any environment;
  drift detection MUST alert on unauthorized modifications
- Container orchestration (Kubernetes or equivalent) MUST be used
  for service deployment with declarative manifests
- Infrastructure changes MUST pass the same review and CI gates as
  application code

## Security & Compliance Requirements

- **Authentication**: OAuth 2.0 / OpenID Connect for API consumers;
  short-lived tokens (< 1 hour) with refresh rotation; service-to-
  service authentication via managed identities or mTLS
- **Authorization**: Role-based access control (RBAC) with
  least-privilege defaults; attribute-based access control (ABAC)
  for fine-grained data access decisions
- **Image Upload**: Max 10 MB per image; allowed formats restricted
  to JPEG/PNG/WebP; MIME type validation beyond file extension;
  malware scanning on all uploaded content
- **Rate Limiting**: Per-consumer throttling to prevent abuse and
  resource exhaustion; adaptive rate limiting under load
- **Audit Trail**: All data access, model invocations, and admin
  actions MUST be logged immutably in a tamper-evident store
- **Incident Response**: Security incidents MUST be triaged within
  4 hours; user notification within 72 hours per GDPR Article 33;
  post-incident reviews within 5 business days
- **Supply Chain**: All dependencies MUST be pinned to exact versions;
  SBOM generated on each release (SPDX or CycloneDX format);
  provenance attestation for build artifacts
- **Vulnerability Management**: Critical vulnerabilities patched
  within 48 hours; high within 7 days; medium within 30 days

## Enterprise Compliance & Certification

- **SOC 2 Type II**: The system MUST maintain controls supporting
  SOC 2 Trust Service Criteria (Security, Availability, Processing
  Integrity, Confidentiality, Privacy)
- **ISO 27001**: Information security management practices MUST
  align with ISO 27001 Annex A controls
- **PCI DSS**: If payment data flows through the system (even
  indirectly), PCI DSS compliance MUST be maintained
- **Accessibility**: WCAG 2.1 AA compliance for all user-facing
  components including photo upload interfaces
- **Regulatory Monitoring**: A designated compliance owner MUST
  track evolving AI regulations (EU AI Act, state-level privacy
  laws) and flag impacts within 30 days of publication

## Development Workflow & Quality Gates

- **Code Review**: Every PR MUST have at least one approval;
  security-sensitive changes require a second reviewer; automated
  code quality gates (complexity, duplication, coverage) MUST pass
- **CI/CD Pipeline**: Lint → Unit Tests → Integration Tests →
  Contract Tests → Security Scan (SAST + SCA) → Build → DAST →
  Deploy to staging → Smoke Tests → Production (all gates must pass)
- **Model Deployment**: New model versions MUST pass A/B validation
  against the current production model before full rollout; canary
  deployment with automated rollback on metric degradation
- **Branch Strategy**: Trunk-based development with short-lived
  feature branches (< 2 days); no direct pushes to `main`; squash
  merge enforced
- **Documentation**: API changes MUST update OpenAPI specs; model
  changes MUST update the model card; architecture decisions MUST
  be recorded as ADRs (Architecture Decision Records)
- **Versioning**: Semantic versioning (MAJOR.MINOR.PATCH) for the
  service; model versions use date-based tags (YYYY-MM-DD-vN)
- **Release Management**: Production releases MUST follow a defined
  release calendar; hotfixes follow an expedited path with mandatory
  post-release review
- **Dependency Management**: Dependencies MUST be updated monthly;
  major version upgrades require a dedicated spike and risk assessment
- **Definition of Done**: Feature is not done until it is deployed
  to production, monitored, documented, and validated against
  acceptance criteria

## Governance

- This constitution supersedes all other development practices for
  the VirtualMirror AI project
- Amendments require: (1) written proposal with business justification,
  (2) team review with minimum 3 business days comment period, and
  (3) documented rationale and impact analysis before merge
- All pull requests and code reviews MUST verify compliance with
  these principles
- Exceptions MUST be documented with justification, risk assessment,
  compensating controls, and an expiration date (max 90 days)
- Constitution version follows semantic versioning: MAJOR for principle
  removals/redefinitions, MINOR for additions, PATCH for clarifications
- Quarterly compliance audits MUST verify adherence to this
  constitution; findings MUST be tracked to resolution
- Architecture Review Board MUST approve deviations from stated
  architectural principles (IV, IX, X)
- New team members MUST review this constitution as part of onboarding

**Version**: 1.1.0 | **Ratified**: 2025-05-13 | **Last Amended**: 2025-05-13
