# Azure OpenAI Service: Code of Conduct and Acceptable Use Policy Reference

> **Source:** Microsoft Enterprise AI Services Code of Conduct v4.0 (2026-05-01), Azure Direct Models Data Privacy documentation, and Content Filtering documentation.
>
> **Disclaimer:** This document summarizes publicly available Microsoft policy documentation as of 2026-05-14. It is not legal advice. Consult the original sources and legal counsel for compliance decisions.

## 1. Prohibited Uses (Usage Restrictions)

The Code of Conduct defines 21 usage restrictions. All customers, users, and applications built with Microsoft AI Services must NOT use the services for the following:

### General Prohibitions

| # | Restriction | Summary |
|---|------------|---------|
| 1 | Inconsistent use | Any use inconsistent with the Code of Conduct |
| 2 | Harm to individuals | Any use that can inflict harm on individuals, organizations, or society |
| 3 | Unlawful decisions | Affecting individuals in ways prohibited by law or regulation |
| 4 | Prohibited content | Generating, presenting, monetizing, or interacting with prohibited content |
| 5 | Consequential decisions without oversight | Making decisions without appropriate human oversight that may impact legal/financial position, employment, human rights, or cause physical/psychological harm |

### Deception and Manipulation

| # | Restriction | Summary |
|---|------------|---------|
| 6 | Deception and manipulation | Deceiving, misinforming, or deploying subliminal techniques to manipulate behavior causing harm |
| 7 | Exploiting vulnerabilities | Exploiting age, disability, or socio-economic vulnerabilities to distort behavior |
| 8 | Social scoring | Social scoring or predictive profiling leading to discriminatory treatment |

### Biometric and Identity Restrictions

| # | Restriction | Summary |
|---|------------|---------|
| 9 | Criminality assessment | Assessing criminality risk based solely on profiling or personality traits |
| 10 | **Biometric categorization** | Using biometric data to categorize people or infer race, political opinions, trade union membership, religious/philosophical beliefs, sex life, or sexual orientation |
| 11 | **Sensitive attribute inference** | Inferring gender, race, nationality, religion, or specific age. Exceptions: age range, mouth position (smile/frown), and hair color are permitted |
| 12 | **Emotional state inference** | Inferring emotional states from physical, physiological, or behavioral characteristics |
| 13 | Erotic/romantic chatbots | Creating erotic or romantic chatbots, or personas of specific people without consent |
| 14 | Facial recognition databases | Creating/expanding facial recognition databases via untargeted scraping |
| 15 | **Identity verification** | Identifying or verifying identities based on faces, voices, or biometric characteristics without Microsoft approval |

### Surveillance and Tracking

| # | Restriction | Summary |
|---|------------|---------|
| 16 | Unlawful surveillance | Unlawful tracking, surveillance, stalking, or harassment |
| 17 | **Persistent tracking** | Ongoing surveillance or real-time identification/persistent tracking using personal data (including biometric data) without valid consent |
| 18 | US law enforcement facial recognition | Facial recognition by US state/local police departments |
| 19 | Mobile camera facial recognition | Real-time facial recognition on law enforcement mobile cameras globally |

### Content Integrity and Impersonation

| # | Restriction | Summary |
|---|------------|---------|
| 20 | Content credential tampering | Detecting AI Content Credentials to remove or alter them (except to improve accuracy) |
| 21 | Impersonation | Impersonating any person without explicit consent, including simulating voice/image of politicians or officials |

## 2. Content Filtering Requirements

### Mandatory Content Filter Categories

All Azure OpenAI deployments include default content filtering across four harm categories, each with configurable severity levels (safe, low, medium, high):

| Category | Scope | Examples |
|----------|-------|---------|
| **Hate and Fairness** | Attacks or discriminatory language based on identity attributes | Race, ethnicity, gender identity, sexual orientation, religion, **personal appearance and body size**, disability, harassment |
| **Sexual** | Sexually explicit or exploitative content | Vulgar content, nudity, pornography, abuse, child exploitation |
| **Violence** | Language related to physical harm | Weapons, bullying, terrorism, stalking |
| **Self-Harm** | Content encouraging self-injury | Eating disorders, bullying, self-harm instructions |

### Additional Filter Types

| Filter | Purpose | Default |
|--------|---------|---------|
| Prompt Shields | Detect user prompt attacks and indirect prompt injection | Configurable |
| Protected Material (Text) | Detect known copyrighted text content | Configurable |
| Protected Material (Code) | Detect source code matching public repositories | Configurable (may be required for Copyright Commitment) |
| PII Detection | Filter personally identifiable information from outputs | Configurable |
| Groundedness | Flag ungrounded/non-factual LLM responses | Configurable (streaming only) |
| Task Adherence | Ensure AI Agents align with user instructions | Configurable |

### Configurability

- **Default:** Medium and high severity content is filtered for all four harm categories.
- **Adjustable:** Customers can set thresholds to low/medium/high.
- **Turning off filters:** Requires approval through the [Modified Content Filters application](https://ncv.microsoft.com/uEfCgnITdR) — available only to managed customers.
- **High-Risk Content** safeguards (malicious cyber activity, CBRN weapons) are mandatory and cannot be turned off.

### Prohibited Content Categories

| Category | Description |
|----------|-------------|
| Child sexual exploitation and abuse | Content that describes, features, or promotes CSEA |
| Grooming | Adult building relationship with child for exploitation |
| Non-consensual intimate content | Non-consensual intimate activity content |
| Sexual solicitation | Solicitation of commercial sexual activity |
| Trafficking | Human trafficking recruitment, transport, or promotion |
| Sexually explicit content | Erotic, pornographic, or sexually explicit content |
| Suicide and self-injury | Content that promotes or instructs self-harm |
| Graphic violence and gore | Content promoting graphic violence |
| Terrorism and violent extremism | Content supporting terrorist organizations or ideology |
| Violent threats | Advocating or promoting violence |
| Hate speech and discrimination | Attacks based on protected characteristics |
| Deception and disinformation | Intentionally deceptive content affecting public interest |
| Malicious cyber activity | Malware, DoS attacks, C2 servers (High-Risk) |
| CBRN weapons | Chemical, biological, radiological, nuclear weapons (High-Risk) |

## 3. Biometric and Body-Image Data Policies

### Restrictions Relevant to Body-Image Processing

For applications that process body images or body measurement data (such as clothing fit assessment):

**Prohibited:**

- Using biometric data to categorize people by race, political opinions, trade union membership, religious/philosophical beliefs, sex life, or sexual orientation (restriction #10)
- Inferring sensitive attributes such as gender, race, nationality, religion, or specific age from body images (restriction #11)
- Inferring emotional states from physical characteristics (restriction #12)
- Identifying or verifying individual identities from physical characteristics without Microsoft approval (restriction #15)
- Persistent tracking using biometric data without valid consent (restriction #17)

**Permitted (with appropriate safeguards):**

- Processing body measurements for functional purposes (fit recommendation)
- Inferring age range (explicitly carved out from restriction #11)
- Inferring hair color and mouth position (explicitly carved out from restriction #11)

**Content filter note:** The "Hate and Fairness" category explicitly covers "personal appearance and body size" — applications must ensure outputs do not contain discriminatory language about body size or appearance.

### Responsible AI Requirements for Body-Image Applications

Per the Responsible AI requirements section:

1. Implement technical controls on inputs and outputs to reduce misuse
2. Disclose when outputs are generated by AI
3. Test thoroughly and continuously with appropriate human oversight
4. Establish user feedback channels for reporting abuse
5. Obtain all necessary consents for data processing (for both customer and Microsoft)
6. Implement robust security and access control measures

## 4. Data Processing and Retention Commitments

### Core Data Commitments

| Commitment | Details |
|-----------|---------|
| **No training on customer data** | Prompts, completions, embeddings, and training data are NOT used to train generative AI foundation models without explicit permission or instruction |
| **No cross-customer access** | Customer data is NOT available to other customers |
| **No model provider access** | Customer data is NOT available to OpenAI or other Azure Direct Model providers |
| **No product improvement** | Customer data is NOT used to improve Microsoft or third-party products without explicit permission |
| **Stateless models** | No prompts or completions are stored in the model |
| **Fine-tuned model exclusivity** | Fine-tuned models are available exclusively to the customer whose data was used |

### Data Processing Location

| Deployment Type | Processing Location |
|----------------|-------------------|
| Standard | Within customer-specified Azure geography |
| Global | Any geography where the model is deployed |
| DataZone | Within the specified data zone (e.g., US or EU) |

Data stored at rest always remains in the customer-designated geography, regardless of deployment type.

### Encryption and Security

- **Encryption at rest:** AES-256 by default
- **Customer-managed keys:** Optional (some preview features may not support)
- **Customer deletion:** Data can be deleted at any time

### Content Filtering Data Handling

- Content filtering occurs **synchronously** during processing
- **No prompts or completions are stored** in content classifier models
- Prompts and completions are **not used to train** content filtering models without consent

### Abuse Monitoring

| Mode | Data Storage | Human Review |
|------|-------------|-------------|
| Default | Flagged samples may be stored for review | Microsoft employees via SAWs and JIT access |
| Modified (approved) | No storage for human review | Automated review only; no data retained |

- Automated review does not store customer data
- Human reviewers access data only when flagged by the system
- Data store is logically separated by customer resource
- EEA customers: reviewers are located in the EEA

### Opting Out of Abuse Monitoring Storage

Managed customers can apply to modify abuse monitoring via the [Modified Abuse Monitoring application](https://customervoice.microsoft.com/Pages/ResponsePage.aspx?id=v4j5cvGGr0GRqy180BHbR7en2Ais5pxKtso_Pz4b1_xUOE9MUTFMUlpBNk5IQlZWWkcyUEpWWEhGOCQlQCN0PWcu). Verification is available via the Azure portal (`ContentLogging` capability set to `false`).

## 5. Limited Access Services

- Most Azure OpenAI models are available to all Azure customers without registration
- Registration is required for: (a) models designated as Limited Access Services, or (b) modifying content filters/abuse monitoring
- Modified content filters and abuse monitoring are available only to managed customers or those under eligible programs

## References

- [Microsoft Enterprise AI Services Code of Conduct (v4.0)](https://learn.microsoft.com/en-us/legal/cognitive-services/openai/code-of-conduct) — Last updated 2026-05-01
- [Data, Privacy, and Security for Azure Direct Models](https://learn.microsoft.com/en-us/azure/foundry/responsible-ai/openai/data-privacy) — Last updated 2026-02-28
- [Content Filtering for Microsoft Foundry Models](https://learn.microsoft.com/en-us/azure/foundry-classic/foundry-models/concepts/content-filter) — Last updated 2026-02-28
- [Limited Access for Azure Direct Models](https://learn.microsoft.com/en-us/azure/foundry/responsible-ai/openai/limited-access) — Last updated 2026-02-28
- [Microsoft Product Terms](https://www.microsoft.com/licensing/terms/welcome/welcomepage)
