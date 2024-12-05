# AI-Powered Smart Contract Security Testing System

An innovative system that combines artificial intelligence with dynamic analysis tools to automate and enhance smart contract security testing, making it more accessible and cost-effective for developers.

## Overview

This system addresses the critical challenge of smart contract security in blockchain applications by automating the generation and execution of security tests. Using a combination of artificial intelligence and established testing tools, particularly Echidna, the system provides comprehensive security analysis while maintaining accessibility and cost-effectiveness.

## Key Features

- Automated generation of property-based security tests
- Integration with static analysis tools for enhanced contract understanding
- AI-driven test case generation using Claude 3.5 Sonnet
- Comprehensive five-stage analysis pipeline
- User-friendly web interface built with Gradio
- Cost-effective alternative to traditional security audits

## System Architecture

The system implements a five-stage pipeline for thorough smart contract analysis:

1. Input Processing: Validates and preprocesses Solidity smart contracts
2. Static Analysis: Employs Slither to identify potential vulnerabilities
3. Use Case Generation: Leverages AI to analyze contract structure
4. Test Generation: Creates comprehensive Echidna test files
5. Dynamic Analysis: Executes property-based fuzzing tests

## Technical Requirements

- Python 3.8+
- Anthropic Claude API access
- Gradio (for web interface)
- Slither
- Echidna

## Getting Started

First, install the required dependencies:

```bash
pip install -r requirements.txt
```

Next, create a `prompts` directory in the project root and add the required prompt files:

```bash
mkdir prompts
touch prompts/prompt_generate_test.txt
touch prompts/prompt_guideline.txt
```

Add your system prompt to these files. The quality of the generated tests heavily depends on these prompts, and we encourage the community to share and iterate on improved versions. Better prompts lead to better security testing!

To run the system, use the following command from the project root directory:

```bash
python3 main.py
```

If you're running the script on Windows, you can also use:

```bash
python main.py
```

## Community Contributions

I strongly believe in the power of community collaboration, especially for improving the system's prompts. You can help by:

- Sharing your optimized prompts that produce better test results
- Documenting successful prompt patterns and techniques
- Reporting prompt effectiveness for different types of smart contracts
- Contributing to a collection of proven prompt templates

The effectiveness of AI-generated tests largely depends on the quality of our prompts. Together, we can create a robust library of prompts that enhances the security testing process for everyone.

## Usage Considerations

While this system provides valuable security insights, users should be aware of the following:

- The system complements but does not replace professional security audits
- Generated tests should be reviewed and validated by developers
- Multiple analysis runs may be needed due to the statistical nature of AI-driven testing
- Regular testing throughout the development cycle is recommended

## Cost Benefits

The system is designed to be highly cost-effective:

- Requires only two AI model calls per analysis
- Significantly more affordable than traditional smart contract audits
- Makes security testing accessible to individual developers and small projects

## Future Development

Planned enhancements include:

- Development of a specialized model for smart contract testing
- Creation of a comprehensive labeled dataset of smart contracts and test cases
- Implementation of smart contract-specific evaluation metrics
- Fine-tuning of language models for improved test generation
- Building a community-driven repository of effective prompts

## License

All rights reserved. Any version of this code is protected by copyright law. Any use, reproduction, distribution, or modification of this code without explicit written permission from the author is strictly prohibited.

## Author

Simone Orsi

## Academic Supervision

- Advisor: Prof. Michele Amoretti
- Co-advisor: Ing. Stefano Cavalli

## Institution

Department of Engineering and Architecture
University of Parma
Academic Year 2023/2024
