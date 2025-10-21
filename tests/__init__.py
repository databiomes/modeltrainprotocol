"""
Test package for Model Train Protocol.

tests/
├── __init__.py
├── unit/                          # Unit tests for individual components
│   ├── __init__.py
│   ├── test_protocol/             # Protocol class tests
│   │   ├── __init__.py
│   │   └── test_protocol.py
│   ├── test_tokens/               # Token-related tests
│   │   ├── __init__.py
│   │   ├── test_token.py          # Basic Token tests
│   │   ├── test_num_token.py      # NumToken tests
│   │   └── test_token_set.py      # TokenSet tests
│   ├── test_tokensets/            # TokenSet tests
│   │   ├── __init__.py
│   │   └── test_token_set.py
│   ├── test_instructions/         # Instruction-related tests
│   │   ├── __init__.py
│   │   ├── test_simple_instruction.py
│   │   └── test_user_instruction.py
│   ├── test_guardrails/           # Guardrail tests
│   │   ├── __init__.py
│   │   └── test_guardrail.py
│   └── test_protocol_json/         # Internal module tests
│       ├── __init__.py
│       └── test_protocol_json.py
├── integration/                   # Integration tests
│   ├── __init__.py
│   ├── test_protocol_workflow.py  # End-to-end protocol creation
│   └── test_file_operations.py   # Save/load operations
├── fixtures/                      # Test data and fixtures
│   ├── __init__.py
│   ├── correct_protocol_utils.py       # Correct protocol examples
│   ├── sample_protocols.py        # Sample protocol data
│   └── tokens.py            # Sample token data

To run tests:

# Install the package in development mode with test dependencies
pip install -e ".[test]"

# Run all tests
pytest

# Run specific test categories
pytest tests/unit/                 # Unit tests only
pytest tests/integration/          # Integration tests only
pytest tests/unit/test_tokens/     # Token tests only
pytest tests/unit/test_instructions/  # Instruction tests only
pytest tests/unit/test_guardrails/ # Guardrail tests only
"""


