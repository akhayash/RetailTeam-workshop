# Subagent Research: Azure OpenAI Code of Conduct and Acceptable Use Policy

## Research Questions

1. What are the prohibited uses of Azure OpenAI Service?
2. What are the content filtering requirements?
3. What usage policies apply to processing biometric or body-image data?
4. What are the data processing and retention commitments?

## Sources Consulted

- Microsoft Enterprise AI Services Code of Conduct (v4.0, 2026-05-01): https://learn.microsoft.com/en-us/legal/cognitive-services/openai/code-of-conduct
- Data, privacy, and security for Azure Direct Models in Microsoft Foundry: https://learn.microsoft.com/en-us/azure/foundry/responsible-ai/openai/data-privacy
- Content filtering for Microsoft Foundry Models: https://learn.microsoft.com/en-us/azure/foundry-classic/foundry-models/concepts/content-filter
- Limited access for Azure Direct Models: https://learn.microsoft.com/en-us/azure/foundry/responsible-ai/openai/limited-access

## Key Discoveries

### 1. Prohibited Uses (Usage Restrictions)

The Code of Conduct (v4.0, effective 2026-05-01) lists 21 usage restrictions. Key prohibitions relevant to the clothing fit assessment scenario include:

- **Biometric categorization (restriction #10):** Prohibits using biometric data to categorize people or to deduce/infer race, political opinions, trade union membership, religious/philosophical beliefs, sex life, or sexual orientation.
- **Sensitive attribute inference (restriction #11):** Prohibits inferring sensitive attributes such as gender, race, nationality, religion, or specific age (age range is permitted). Does NOT prohibit inferring hair color, mouth position (smile/frown), or age range.
- **Emotional state inference (restriction #12):** Prohibits inferring emotional states from physical, physiological, or behavioral characteristics.
- **Identity verification without approval (restriction #15):** Prohibits identifying or verifying individual identities based on faces, voices, or other biometric characteristics without Microsoft approval for modified content filtering/abuse monitoring.
- **Surveillance (restriction #17):** Prohibits ongoing surveillance or real-time identification/persistent tracking using personal data including biometric data without valid consent.
- **Harm to individuals (restriction #2):** Prohibits any use that can inflict harm on individuals, organizations, or society.
- **Consequential decisions without oversight (restriction #5):** Prohibits making decisions without appropriate human oversight that may have consequential impact on legal position, finances, employment, human rights, or may cause physical/psychological harm.

### 2. Content Filtering Requirements

Four primary content filter categories with configurable severity levels:

| Category | Description |
|----------|-------------|
| Hate and Fairness | Content attacking/discriminating based on identity attributes including personal appearance and body size |
| Sexual | Sexually explicit language, nudity, pornography, abuse |
| Violence | Physical harm language, weapons, stalking |
| Self-Harm | Self-injury, eating disorders, bullying |

Additional filters:
- Prompt shields (user prompt attacks, indirect attacks)
- Protected material detection (text and code)
- PII detection
- Groundedness detection
- Task adherence (for AI agents)

Default safety settings are applied to all models. Severity thresholds are configurable (low/medium/high). Turning filters off requires approval through the Limited Access program.

### 3. Biometric / Body-Image Data Policies

**Directly relevant to clothing fit assessment:**

- Restriction #10 explicitly addresses biometric data processing. The system must NOT use body measurements to categorize people by protected characteristics.
- Restriction #11 prohibits inferring sensitive attributes. Body measurement data must not be used to infer gender, race, nationality, religion, or specific age. However, inferring age range is permitted.
- The "Hate and Fairness" content filter category explicitly includes "personal appearance and body size" as a protected attribute.
- Restriction #12 prohibits inferring emotional states from physical characteristics, so body-image analysis must not include emotional inference.

**What is permitted:**
- Processing body measurements for functional purposes (fit assessment) is not explicitly prohibited, provided the data is not used for prohibited categorization or inference.
- Age range inference is explicitly carved out as permitted.
- Mouth position and hair color inference are explicitly permitted.

### 4. Data Processing and Retention Commitments

Key commitments from the Data Privacy documentation:

- **No training on customer data:** Prompts, completions, embeddings, and training data are NOT used to train generative AI foundation models without explicit permission.
- **No sharing:** Customer data is NOT available to other customers, OpenAI, or other model providers.
- **No product improvement:** Customer data is NOT used to improve Microsoft or third-party products without explicit permission.
- **Stateless models:** Models are stateless; no prompts or completions are stored in the model.
- **Geography-bound processing:** Data is processed within the customer-specified geography (except Global/DataZone deployments).
- **Encryption at rest:** AES-256 encryption by default, with customer-managed key option.
- **Customer deletion:** Customer can delete stored data at any time.
- **Content filtering is synchronous:** No prompts or generated content are stored in the content classifier models.
- **Abuse monitoring:** System may store samples of flagged prompts/completions for human review. Can be turned off with approval. Automated review does not store data.

## Follow-on Questions (Directly Relevant)

- What specific consent requirements apply when processing user-submitted body images through Azure OpenAI vision models?
- Does the Florence-2 model (Azure AI Foundry) fall under the same Code of Conduct as Azure OpenAI models?

## Clarifying Questions

- The Code of Conduct v4.0 was updated 2026-05-01 with a new "High-Risk Content" section. The team should verify they are reviewing the latest version before finalizing compliance.
- The distinction between "biometric data" (restricted) and "body measurement data for functional purposes" (potentially permitted) may require legal review for the clothing fit assessment use case.
