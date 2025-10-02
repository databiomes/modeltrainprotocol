"""
Test package for Model Train Protocol.

tests/
├── __init__.py
├── unit/                          # Unit tests for individual components
│   ├── __init__.py
│   ├── test_protocol.py          # Protocol class tests
│   ├── test_tokens/               # Token-related tests
│   │   ├── __init__.py
│   │   ├── test_token.py          # Basic Token tests
│   │   ├── test_user_token.py     # UserToken tests
│   │   ├── test_num_token.py      # NumToken tests
│   │   └── test_token_set.py      # TokenSet tests
│   ├── test_instructions/         # Instruction-related tests
│   │   ├── __init__.py
│   │   ├── test_simple_instruction.py
│   │   └── test_user_instruction.py
│   ├── test_guardrails/           # Guardrail tests
│   │   ├── __init__.py
│   │   └── test_guardrail.py
│   └── test_internal/             # Internal module tests
│       ├── __init__.py
│       ├── test_protocol_file.py
│       └── test_template_file.py
├── integration/                   # Integration tests
│   ├── __init__.py
│   ├── test_protocol_workflow.py  # End-to-end protocol creation
│   └── test_file_operations.py   # Save/load operations
├── fixtures/                      # Test data and fixtures
│   ├── __init__.py
│   ├── sample_protocols.py        # Sample protocol data
│   └── test_tokens.py            # Sample token data
└── utils/                         # Test utilities
    ├── __init__.py
    └── helpers.py                 # Test helper functions

To run tests

# Install the package in development mode with test dependencies
pip install -e ".[test]"

pytest
"""


