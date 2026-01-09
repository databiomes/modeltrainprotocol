"""
Unit tests for the Protocol class.
"""
from pathlib import Path

import pytest

from model_train_protocol import Protocol, Token, TokenSet, Instruction, ExtendedInstruction, \
    Guardrail, FinalToken
from model_train_protocol.common.instructions.input.InstructionInput import InstructionInput
from model_train_protocol.common.instructions.output.InstructionOutput import InstructionOutput
from model_train_protocol.common.instructions.output.ExtendedResponse import ExtendedResponse
from tests.fixtures.tokens import get_valid_keyless_tokens


class TestProtocol:
    """Test cases for the Protocol class."""

    def test_protocol_initialization_basic(self):
        """Test basic protocol initialization."""
        protocol = Protocol("test_protocol", inputs=3)

        assert protocol.name == "test_protocol"
        assert protocol.instruction_input_snippets == 3
        assert protocol.encrypt is True
        assert protocol.context == []
        assert len(protocol.tokens) == 0
        assert len(protocol.instructions) == 0
        assert protocol.guardrails == {}
        assert protocol.numbers == {}
        assert len(protocol.special_tokens) == 0
        assert len(protocol.used_keys) == 0

    def test_protocol_initialization_encrypted(self):
        """Test protocol initialization with encryption."""
        protocol = Protocol("test_protocol", inputs=3, encrypt=True)

        assert protocol.encrypt is True

        test_tokens: list[Token] = list(get_valid_keyless_tokens().values())
        for token in test_tokens:
            protocol._add_token(token)

        for token in protocol.tokens:
            if token.key is None or token.key == token.value:
                pytest.fail(f"Token {token} was not assigned a hashed key in encrypted protocol.")

    def test_protocol_initialization_unencrypted(self):
        """Test protocol initialization without encryption."""
        protocol = Protocol("test_protocol", inputs=3, encrypt=False)

        assert protocol.encrypt is False

        test_tokens: list[Token] = list(get_valid_keyless_tokens().values())
        for token in test_tokens:
            protocol._add_token(token)

        for token in protocol.tokens:
            if token.key != token.value:
                pytest.fail(
                    f"Token {token} was not assigned its value as key in unencrypted protocol or value was encrypted.")

    def test_protocol_initialization_invalid_instruction_context_snippets(self):
        """Test protocol initialization with invalid context lines."""
        with pytest.raises(ValueError, match="minimum of 2 inputs"):
            Protocol("test_protocol", inputs=1)

        with pytest.raises(ValueError, match="minimum of 2 inputs"):
            Protocol("test_protocol", inputs=0)

        with pytest.raises(ValueError, match="minimum of 2 inputs"):
            Protocol("test_protocol", inputs=-1)

    def test_protocol_initialization_valid_instruction_context_snippets(self):
        """Test protocol initialization with valid context lines."""
        # Should not raise any exception
        Protocol("test_protocol", inputs=2)
        Protocol("test_protocol", inputs=3)
        Protocol("test_protocol", inputs=10)

    def test_protocol_add_context(self):
        """Test adding context to protocol."""
        protocol = Protocol("test_protocol", inputs=3)

        protocol.add_context("Context line 1")
        assert len(protocol.context) == 1
        assert protocol.context[0] == "Context line 1"

        protocol.add_context("Context line 2")
        assert len(protocol.context) == 2
        assert protocol.context[1] == "Context line 2"

    def test_protocol_add_context_multiple(self):
        """Test adding multiple context lines."""
        protocol = Protocol("test_protocol", inputs=3)

        contexts = ["Context 1", "Context 2", "Context 3", "Context 4"]
        for context in contexts:
            protocol.add_context(context)

        assert len(protocol.context) == 4
        assert protocol.context == contexts

    def test_protocol_add_context_empty_string(self):
        """Test adding empty context string."""
        protocol = Protocol("test_protocol", inputs=3)

        protocol.add_context("")
        assert len(protocol.context) == 1
        assert protocol.context[0] == ""

    def test_protocol_add_context_none(self):
        """Test adding None context."""
        protocol = Protocol("test_protocol", inputs=3)

        with pytest.raises(TypeError, match="Context must be a string"):
            protocol.add_context(None)

    def test_protocol_add_token_basic(self):
        """Test adding basic token to protocol."""
        protocol = Protocol("test_protocol", inputs=3)
        token = Token("Test", key="🔑")

        protocol._add_token(token)

        assert token in protocol.tokens
        assert token.key in protocol.used_keys

    def test_protocol_add_token_duplicate_value(self):
        """Test adding token with duplicate value."""
        protocol = Protocol("test_protocol", inputs=3)
        token1 = Token("Test")
        token2 = Token("Test")

        protocol._add_token(token1)

        with pytest.raises(ValueError, match="already used"):
            protocol._add_token(token2)

    def test_protocol_add_token_duplicate_key(self):
        """Test adding token with duplicate key."""
        protocol = Protocol("test_protocol", inputs=3)
        token1 = Token("Test1", key="🔑")
        token2 = Token("Test2", key="🔑")

        protocol._add_token(token1)

        with pytest.raises(ValueError, match="already used"):
            protocol._add_token(token2)

    def test_protocol_add_token_encrypted(self):
        """Test adding token to encrypted protocol."""
        protocol = Protocol("test_protocol", inputs=3, encrypt=True)
        token = Token("Test")  # No key provided

        protocol._add_token(token)

        assert token in protocol.tokens
        assert token.key is not None
        assert token.key in protocol.used_keys

    def test_protocol_add_token_unencrypted(self):
        """Test adding token to unencrypted protocol."""
        protocol = Protocol("test_protocol", inputs=3, encrypt=False)
        token = Token("Test")  # No key provided

        protocol._add_token(token)

        assert token in protocol.tokens
        assert token.key == "Test_"  # Should use value as key
        assert token.key in protocol.used_keys

    def test_protocol_add_token_with_key(self):
        """Test adding token with existing key."""
        protocol = Protocol("test_protocol", inputs=3)
        token = Token("Test", key="🔑")

        protocol._add_token(token)

        assert token in protocol.tokens
        assert token.key == "🔑"
        assert token.key in protocol.used_keys

    def test_protocol_add_instruction_basic(self):
        """Test adding basic instruction to protocol."""
        protocol = Protocol("test_protocol", inputs=2)

        # Create tokens
        token1 = Token("Token1", key="🔑")
        token2 = Token("Token2", key="🔧")
        token3 = Token("Token3", key="🔨")

        # Create token sets
        context_set1 = TokenSet(tokens=(token1,))
        context_set2 = TokenSet(tokens=(token2,))
        response_set = TokenSet(tokens=(token3,))

        # Create instruction
        final_token = FinalToken("Result")
        instruction_input = InstructionInput(tokensets=[context_set1, context_set2], context=None)
        instruction_output = InstructionOutput(tokenset=response_set, final=final_token)
        instruction = Instruction(
            input=instruction_input,
            output=instruction_output,
        )

        # Add samples
        context_snippet1 = context_set1.create_snippet("Context 1")
        context_snippet2 = context_set2.create_snippet("Context 2")
        output_snippet = response_set.create_snippet("Output")

        instruction.add_sample(
            input_snippets=[context_snippet1, context_snippet2],
            output_snippet=output_snippet
        )
        instruction.add_sample(
            input_snippets=[context_snippet1, context_snippet2],
            output_snippet=output_snippet
        )
        instruction.add_sample(
            input_snippets=[context_snippet1, context_snippet2],
            output_snippet=output_snippet
        )
        instruction.add_sample(
            input_snippets=[context_snippet1, context_snippet2],
            output_snippet=output_snippet
        )
        instruction.add_sample(
            input_snippets=[context_snippet1, context_snippet2],
            output_snippet=output_snippet
        )
        instruction.add_sample(
            input_snippets=[context_snippet1, context_snippet2],
            output_snippet=output_snippet
        )
        instruction.add_sample(
            input_snippets=[context_snippet1, context_snippet2],
            output_snippet=output_snippet
        )
        instruction.add_sample(
            input_snippets=[context_snippet1, context_snippet2],
            output_snippet=output_snippet
        )
        instruction.add_sample(
            input_snippets=[context_snippet1, context_snippet2],
            output_snippet=output_snippet
        )

        # Add instruction to protocol
        protocol.add_instruction(instruction)

        assert instruction in protocol.instructions
        assert token1 in protocol.tokens
        assert token2 in protocol.tokens

    def test_protocol_add_instruction_duplicate(self):
        """Test adding duplicate instruction."""
        protocol = Protocol("test_protocol", inputs=2)

        # Create instruction
        token1 = Token("Token1", key="🔑")
        token2 = Token("Token2", key="🔧")
        token3 = Token("Token3", key="🔨")
        context_set1 = TokenSet(tokens=(token1,))
        context_set2 = TokenSet(tokens=(token2,))
        response_set = TokenSet(tokens=(token3,))

        final_token = FinalToken("Result")
        instruction_input = InstructionInput(tokensets=[context_set1, context_set2], context=None)
        instruction_output = InstructionOutput(tokenset=response_set, final=final_token)
        instruction = Instruction(
            input=instruction_input,
            output=instruction_output,
        )

        context_snippet1 = context_set1.create_snippet("Context 1")
        context_snippet2 = context_set2.create_snippet("Context 2")
        output_snippet = response_set.create_snippet("Output")

        instruction.add_sample(
            input_snippets=[context_snippet1, context_snippet2],
            output_snippet=output_snippet
        )
        instruction.add_sample(
            input_snippets=[context_snippet1, context_snippet2],
            output_snippet=output_snippet
        )
        instruction.add_sample(
            input_snippets=[context_snippet1, context_snippet2],
            output_snippet=output_snippet
        )
        instruction.add_sample(
            input_snippets=[context_snippet1, context_snippet2],
            output_snippet=output_snippet
        )
        instruction.add_sample(
            input_snippets=[context_snippet1, context_snippet2],
            output_snippet=output_snippet
        )
        instruction.add_sample(
            input_snippets=[context_snippet1, context_snippet2],
            output_snippet=output_snippet
        )
        instruction.add_sample(
            input_snippets=[context_snippet1, context_snippet2],
            output_snippet=output_snippet
        )
        instruction.add_sample(
            input_snippets=[context_snippet1, context_snippet2],
            output_snippet=output_snippet
        )
        instruction.add_sample(
            input_snippets=[context_snippet1, context_snippet2],
            output_snippet=output_snippet
        )

        protocol.add_instruction(instruction)

        with pytest.raises(ValueError, match="already added"):
            protocol.add_instruction(instruction)

    def test_protocol_add_multiple_instructions_non_conflicting_names(self):
        """Test that adding an instruction with the same name raises an error and stops."""
        protocol = Protocol("test_protocol", inputs=2)

        # Create first instruction
        token1 = Token("Token1", key="🔑")
        token2 = Token("Token2", key="🔧")
        token3 = Token("Token3", key="🔨")
        context_set1 = TokenSet(tokens=(token1,))
        context_set2 = TokenSet(tokens=(token2,))
        response_set = TokenSet(tokens=(token3,))

        final_token = FinalToken("Result")
        instruction_input1 = InstructionInput(tokensets=[context_set1, context_set2], context=None)
        instruction_output1 = InstructionOutput(tokenset=response_set, final=final_token)
        instruction1 = Instruction(
            input=instruction_input1,
            output=instruction_output1,
            name="same_name"
        )

        context_snippet1 = context_set1.create_snippet("Context 1")
        context_snippet2 = context_set2.create_snippet("Context 2")
        output_snippet = response_set.create_snippet("Output")

        for _ in range(3):
            instruction1.add_sample(
                input_snippets=[context_snippet1, context_snippet2],
                output_snippet=output_snippet
            )

        # Create second instruction with the same name
        instruction_input2 = InstructionInput(tokensets=[context_set1, context_set2], context=None)
        instruction_output2 = InstructionOutput(tokenset=response_set, final=final_token)
        instruction2 = Instruction(
            input=instruction_input2,
            output=instruction_output2,
            name="same_name"  # Same name as instruction1
        )

        for _ in range(3):
            instruction2.add_sample(
                input_snippets=[context_snippet1, context_snippet2],
                output_snippet=output_snippet
            )

        # Add first instruction - should succeed
        protocol.add_instruction(instruction1)
        assert len(protocol.instructions) == 1

        # Try to add second instruction with same name - should raise ValueError and stop
        with pytest.raises(ValueError, match="An instruction with name 'same_name' already exists"):
            protocol.add_instruction(instruction2)

        # Verify only the first instruction was added (error stopped execution)
        assert len(protocol.instructions) == 1
        assert instruction1 in protocol.instructions
        assert instruction2 not in protocol.instructions

    def test_protocol_add_multiple_instructions_conflicting_names(self):
        """Test adding multiple instructions with conflicting names raises error."""
        protocol = Protocol("test_protocol", inputs=2)

        # Create first instruction
        token1 = Token("Token1", key="🔑")
        token2 = Token("Token2", key="🔧")
        token3 = Token("Token3", key="🔨")
        context_set1 = TokenSet(tokens=(token1,))
        context_set2 = TokenSet(tokens=(token2,))
        response_set = TokenSet(tokens=(token3,))

        final_token = FinalToken("Result")
        instruction_input1 = InstructionInput(tokensets=[context_set1, context_set2], context=None)
        instruction_output1 = InstructionOutput(tokenset=response_set, final=final_token)
        instruction1 = Instruction(
            input=instruction_input1,
            output=instruction_output1,
            name="conflicting_name"
        )

        context_snippet1 = context_set1.create_snippet("Context 1")
        context_snippet2 = context_set2.create_snippet("Context 2")
        output_snippet = response_set.create_snippet("Output")

        for _ in range(3):
            instruction1.add_sample(
                input_snippets=[context_snippet1, context_snippet2],
                output_snippet=output_snippet
            )

        # Create second instruction with the same name
        token4 = Token("Token4", key="🔩")
        token5 = Token("Token5", key="⚡")
        context_set3 = TokenSet(tokens=(token4,))
        response_set2 = TokenSet(tokens=(token5,))

        instruction_input2 = InstructionInput(tokensets=[context_set1, context_set3], context=None)
        instruction_output2 = InstructionOutput(tokenset=response_set2, final=final_token)
        instruction2 = Instruction(
            input=instruction_input2,
            output=instruction_output2,
            name="conflicting_name"  # Same name as instruction1
        )

        context_snippet3 = context_set3.create_snippet("Context 3")

        for _ in range(3):
            instruction2.add_sample(
                input_snippets=[context_snippet1, context_snippet3],
                output_snippet=response_set2.create_snippet("Output 2")
            )

        # Add first instruction - should succeed
        protocol.add_instruction(instruction1)
        assert len(protocol.instructions) == 1

        # Try to add second instruction with same name - should raise ValueError
        with pytest.raises(ValueError, match="An instruction with name 'conflicting_name' already exists"):
            protocol.add_instruction(instruction2)

        # Verify only the first instruction was added
        assert len(protocol.instructions) == 1
        assert instruction1 in protocol.instructions
        assert instruction2 not in protocol.instructions

    def test_protocol_add_instruction_conflicting_name_after_multiple(self):
        """Test adding instruction with conflicting name after multiple non-conflicting ones."""
        protocol = Protocol("test_protocol", inputs=2)

        # Create tokens
        token1 = Token("Token1", key="🔑")
        token2 = Token("Token2", key="🔧")
        token3 = Token("Token3", key="🔨")
        context_set1 = TokenSet(tokens=(token1,))
        context_set2 = TokenSet(tokens=(token2,))
        response_set = TokenSet(tokens=(token3,))

        context_snippet1 = context_set1.create_snippet("Context 1")
        context_snippet2 = context_set2.create_snippet("Context 2")
        output_snippet = response_set.create_snippet("Output")

        # Add first instruction
        final_token = FinalToken("Result")
        instruction_input1 = InstructionInput(tokensets=[context_set1, context_set2], context=None)
        instruction_output1 = InstructionOutput(tokenset=response_set, final=final_token)
        instruction1 = Instruction(
            input=instruction_input1,
            output=instruction_output1,
            name="first_instruction"
        )

        for _ in range(3):
            instruction1.add_sample(
                input_snippets=[context_snippet1, context_snippet2],
                output_snippet=output_snippet
            )

        protocol.add_instruction(instruction1)

        # Add second instruction with different name
        token4 = Token("Token4", key="🔩")
        context_set3 = TokenSet(tokens=(token4,))

        instruction_input2 = InstructionInput(tokensets=[context_set1, context_set3], context=None)
        instruction_output2 = InstructionOutput(tokenset=response_set, final=final_token)
        instruction2 = Instruction(
            input=instruction_input2,
            output=instruction_output2,
            name="second_instruction"
        )

        context_snippet3 = context_set3.create_snippet("Context 3")

        for _ in range(3):
            instruction2.add_sample(
                input_snippets=[context_snippet1, context_snippet3],
                output_snippet=output_snippet
            )

        protocol.add_instruction(instruction2)

        # Add third instruction with different name
        instruction_input3 = InstructionInput(tokensets=[context_set1, context_set2], context=None)
        instruction_output3 = InstructionOutput(tokenset=response_set, final=final_token)
        instruction3 = Instruction(
            input=instruction_input3,
            output=instruction_output3,
            name="third_instruction"
        )

        for _ in range(3):
            instruction3.add_sample(
                input_snippets=[context_snippet1, context_snippet2],
                output_snippet=output_snippet
            )

        protocol.add_instruction(instruction3)

        # Verify three instructions were added successfully
        assert len(protocol.instructions) == 3

        # Try to add fourth instruction with name that conflicts with first
        instruction_input4 = InstructionInput(tokensets=[context_set1, context_set2], context=None)
        instruction_output4 = InstructionOutput(tokenset=response_set, final=final_token)
        instruction4 = Instruction(
            input=instruction_input4,
            output=instruction_output4,
            name="first_instruction"  # Conflicts with instruction1
        )

        for _ in range(3):
            instruction4.add_sample(
                input_snippets=[context_snippet1, context_snippet2],
                output_snippet=output_snippet
            )

        with pytest.raises(ValueError, match="An instruction with name 'first_instruction' already exists"):
            protocol.add_instruction(instruction4)

        # Verify still only three instructions
        assert len(protocol.instructions) == 3

    def test_protocol_add_instruction_invalid_instruction_context_snippets(self):
        """Test adding instruction with invalid context lines."""
        protocol = Protocol("test_protocol", inputs=3)

        # Create instruction with wrong context lines (2 instead of 3)
        token1 = Token("Token1", key="🔑")
        token2 = Token("Token2", key="🔧")
        token3 = Token("Token3", key="🔨")
        context_set1 = TokenSet(tokens=(token1,))
        context_set2 = TokenSet(tokens=(token2,))
        response_set = TokenSet(tokens=(token3,))

        final_token = FinalToken("Result")
        instruction_input = InstructionInput(tokensets=[context_set1, context_set2], context=None)  # Only 2 context sets, but protocol expects 3
        instruction_output = InstructionOutput(tokenset=response_set, final=final_token)
        instruction = Instruction(
            input=instruction_input,
            output=instruction_output,
        )

        # Add sample with wrong context lines (2 instead of 3)
        context_snippet1 = context_set1.create_snippet("Context 1")
        context_snippet2 = context_set2.create_snippet("Context 2")
        output_snippet = response_set.create_snippet("Output")

        instruction.add_sample(
            input_snippets=[context_snippet1, context_snippet2],
            output_snippet=output_snippet
        )
        instruction.add_sample(
            input_snippets=[context_snippet1, context_snippet2],
            output_snippet=output_snippet
        )
        instruction.add_sample(
            input_snippets=[context_snippet1, context_snippet2],
            output_snippet=output_snippet
        )

        with pytest.raises(ValueError, match="does not match defined inputs count"):
            protocol.add_instruction(instruction)

    def test_protocol_save_basic(self, temp_directory):
        """Test basic protocol saving."""
        protocol = Protocol("test_protocol", inputs=2)

        # Add context
        protocol.add_context("Context line 1")
        protocol.add_context("Context line 2")

        # Create and add instruction
        token1 = Token("Token1", key="🔑")
        token2 = Token("Token2", key="🔧")
        token3 = Token("Token3", key="🔨")
        context_set1 = TokenSet(tokens=(token1,))
        context_set2 = TokenSet(tokens=(token2,))
        response_set = TokenSet(tokens=(token3,))

        final_token = FinalToken("Result")
        instruction_input = InstructionInput(tokensets=[context_set1, context_set2], context=None)
        instruction_output = InstructionOutput(tokenset=response_set, final=final_token)
        instruction = Instruction(
            input=instruction_input,
            output=instruction_output,
        )

        context_snippet1 = context_set1.create_snippet("Context 1")
        context_snippet2 = context_set2.create_snippet("Context 2")
        output_snippet = response_set.create_snippet("Output")

        instruction.add_sample(
            input_snippets=[context_snippet1, context_snippet2],
            output_snippet=output_snippet
        )
        instruction.add_sample(
            input_snippets=[context_snippet1, context_snippet2],
            output_snippet=output_snippet
        )
        instruction.add_sample(
            input_snippets=[context_snippet1, context_snippet2],
            output_snippet=output_snippet
        )

        protocol.add_instruction(instruction)
        
        # Add more context to meet minimum requirement (already has 2, need 8 more for total of 10)
        for i in range(3, 11):
            protocol.add_context(f"Context line {i}")

        # Save protocol
        protocol.save(name="test_save", path=str(temp_directory))

        # Check file was created
        expected_file = temp_directory / "test_save_model.json"
        assert expected_file.exists()
        
        # Clean up
        expected_file.unlink()

    def test_protocol_save_default_name(self, temp_directory):
        """Test protocol saving with default name."""
        protocol = Protocol("test_protocol", inputs=2)

        # Add context and instruction
        protocol.add_context("Context line 1")
        protocol.add_context("Context line 2")

        token1 = Token("Token1", key="🔑")
        token2 = Token("Token2", key="🔧")
        token3 = Token("Token3", key="🔨")
        context_set1 = TokenSet(tokens=(token1,))
        context_set2 = TokenSet(tokens=(token2,))
        response_set = TokenSet(tokens=(token3,))

        final_token = FinalToken("Result")
        instruction_input = InstructionInput(tokensets=[context_set1, context_set2], context=None)
        instruction_output = InstructionOutput(tokenset=response_set, final=final_token)
        instruction = Instruction(
            input=instruction_input,
            output=instruction_output,
        )

        context_snippet1 = context_set1.create_snippet("Context 1")
        context_snippet2 = context_set2.create_snippet("Context 2")
        output_snippet = response_set.create_snippet("Output")

        instruction.add_sample(
            input_snippets=[context_snippet1, context_snippet2],
            output_snippet=output_snippet
        )
        instruction.add_sample(
            input_snippets=[context_snippet1, context_snippet2],
            output_snippet=output_snippet
        )
        instruction.add_sample(
            input_snippets=[context_snippet1, context_snippet2],
            output_snippet=output_snippet
        )

        protocol.add_instruction(instruction)
        
        # Add more context to meet minimum requirement
        for i in range(3, 11):
            protocol.add_context(f"Context line {i}")

        # Save protocol with default name
        protocol.save(path=str(temp_directory))

        # Check file was created with protocol name
        expected_file = temp_directory / "test_protocol_model.json"
        assert expected_file.exists()
        
        # Clean up
        expected_file.unlink()

    def test_protocol_save_default_path(self):
        """Test protocol saving with default path."""
        protocol = Protocol("test_protocol", inputs=2)

        # Add context and instruction
        protocol.add_context("Context line 1")
        protocol.add_context("Context line 2")

        token1 = Token("Token1", key="🔑")
        token2 = Token("Token2", key="🔧")
        token3 = Token("Token3", key="🔨")
        context_set1 = TokenSet(tokens=(token1,))
        context_set2 = TokenSet(tokens=(token2,))
        response_set = TokenSet(tokens=(token3,))

        final_token = FinalToken("Result")
        instruction_input = InstructionInput(tokensets=[context_set1, context_set2], context=None)
        instruction_output = InstructionOutput(tokenset=response_set, final=final_token)
        instruction = Instruction(
            input=instruction_input,
            output=instruction_output,
        )

        context_snippet1 = context_set1.create_snippet("Context 1")
        context_snippet2 = context_set2.create_snippet("Context 2")
        output_snippet = response_set.create_snippet("Output")

        instruction.add_sample(
            input_snippets=[context_snippet1, context_snippet2],
            output_snippet=output_snippet
        )
        instruction.add_sample(
            input_snippets=[context_snippet1, context_snippet2],
            output_snippet=output_snippet
        )
        instruction.add_sample(
            input_snippets=[context_snippet1, context_snippet2],
            output_snippet=output_snippet
        )

        protocol.add_instruction(instruction)
        
        # Add more context to meet minimum requirement
        for i in range(3, 11):
            protocol.add_context(f"Context line {i}")

        # Save protocol with default path
        protocol.save(name="test_save")

        # Check file was created in current directory
        expected_file = Path("test_save_model.json")
        assert expected_file.exists()

        # Clean up
        expected_file.unlink()

    def test_protocol_template_basic(self, temp_directory):
        """Test basic protocol templating."""
        protocol = Protocol("test_protocol", inputs=2)

        # Add context and instruction
        protocol.add_context("Context line 1")
        protocol.add_context("Context line 2")

        token1 = Token("Token1", key="🔑")
        token2 = Token("Token2", key="🔧")
        token3 = Token("Token3", key="🔨")
        context_set1 = TokenSet(tokens=(token1,))
        context_set2 = TokenSet(tokens=(token2,))
        response_set = TokenSet(tokens=(token3,))

        final_token = FinalToken("Result")
        instruction_input = InstructionInput(tokensets=[context_set1, context_set2], context=None)
        instruction_output = InstructionOutput(tokenset=response_set, final=final_token)
        instruction = Instruction(
            input=instruction_input,
            output=instruction_output,
        )

        context_snippet1 = context_set1.create_snippet("Context 1")
        context_snippet2 = context_set2.create_snippet("Context 2")
        output_snippet = response_set.create_snippet("Output")

        instruction.add_sample(
            input_snippets=[context_snippet1, context_snippet2],
            output_snippet=output_snippet
        )
        instruction.add_sample(
            input_snippets=[context_snippet1, context_snippet2],
            output_snippet=output_snippet
        )
        instruction.add_sample(
            input_snippets=[context_snippet1, context_snippet2],
            output_snippet=output_snippet
        )

        protocol.add_instruction(instruction)
        
        # Add more context to meet minimum requirement
        for i in range(3, 11):
            protocol.add_context(f"Context line {i}")

        # Create template
        protocol.template(path=str(temp_directory))

        # Check file was created
        expected_file = temp_directory / "test_protocol_template.json"
        assert expected_file.exists()
        
        # Clean up
        expected_file.unlink()

    def test_protocol_template_default_path(self):
        """Test protocol templating with default path."""
        protocol = Protocol("test_protocol", inputs=2)

        # Add context and instruction
        protocol.add_context("Context line 1")
        protocol.add_context("Context line 2")

        token1 = Token("Token1", key="🔑")
        token2 = Token("Token2", key="🔧")
        token3 = Token("Token3", key="🔨")
        context_set1 = TokenSet(tokens=(token1,))
        context_set2 = TokenSet(tokens=(token2,))
        response_set = TokenSet(tokens=(token3,))

        final_token = FinalToken("Result")
        instruction_input = InstructionInput(tokensets=[context_set1, context_set2], context=None)
        instruction_output = InstructionOutput(tokenset=response_set, final=final_token)
        instruction = Instruction(
            input=instruction_input,
            output=instruction_output,
        )

        context_snippet1 = context_set1.create_snippet("Context 1")
        context_snippet2 = context_set2.create_snippet("Context 2")
        output_snippet = response_set.create_snippet("Output")

        instruction.add_sample(
            input_snippets=[context_snippet1, context_snippet2],
            output_snippet=output_snippet
        )
        instruction.add_sample(
            input_snippets=[context_snippet1, context_snippet2],
            output_snippet=output_snippet
        )
        instruction.add_sample(
            input_snippets=[context_snippet1, context_snippet2],
            output_snippet=output_snippet
        )

        protocol.add_instruction(instruction)
        
        # Add more context to meet minimum requirement
        for i in range(3, 11):
            protocol.add_context(f"Context line {i}")

        # Create template with default path
        protocol.template()

        # Check file was created in current directory
        expected_file = Path("test_protocol_template.json")
        assert expected_file.exists()

        # Clean up
        expected_file.unlink()

    def test_protocol_save_no_instructions(self):
        """Test saving protocol with no instructions."""
        protocol = Protocol("test_protocol", inputs=2)

        # Add context but no instructions
        protocol.add_context("Context line 1")
        protocol.add_context("Context line 2")

        with pytest.raises(ValueError, match="No instructions have been added"):
            protocol.save()

    def test_protocol_template_no_instructions(self):
        """Test templating protocol with no instructions."""
        protocol = Protocol("test_protocol", inputs=2)

        # Add context but no instructions
        protocol.add_context("Context line 1")
        protocol.add_context("Context line 2")

        with pytest.raises(ValueError, match="No instructions have been added"):
            protocol.template()

    def test_protocol_assign_key_encrypted(self):
        """Test key assignment for encrypted protocol."""
        protocol = Protocol("test_protocol", inputs=3, encrypt=True)
        token = Token("Test")  # No key provided

        protocol._assign_key(token)

        assert token.key is not None
        assert token.key != "Test_"  # Should be hashed

    def test_protocol_assign_key_unencrypted(self):
        """Test key assignment for unencrypted protocol."""
        protocol = Protocol("test_protocol", inputs=3, encrypt=False)
        token = Token("Test")  # No key provided

        protocol._assign_key(token)

        assert token.key == "Test_"  # Should use value as key

    def test_protocol_assign_key_existing_key(self):
        """Test key assignment for token with existing key."""
        protocol = Protocol("test_protocol", inputs=3, encrypt=True)
        token = Token("Test", key="🔑")  # Key already provided

        protocol._assign_key(token)

        assert token.key == "🔑"  # Should keep existing key

    def test_protocol_set_guardrails(self):
        """Test setting guardrails in protocol."""
        protocol = Protocol("test_protocol", inputs=2)

        # Create tokens and token sets
        user_token = Token("User", key="👤")
        token1 = Token("Token1", key="🔑")
        token2 = Token("Token2", key="🔧")
        context_set1 = TokenSet(tokens=(user_token,))
        context_set2 = TokenSet(tokens=(token1,))
        user_set = TokenSet(tokens=(user_token,))
        response_set = TokenSet(tokens=(token2,))

        # Create guardrail
        guardrail = Guardrail(
            good_prompt="Good prompt",
            bad_prompt="Bad prompt",
            bad_output="Bad output"
        )
        guardrail.add_sample("Bad sample one")
        guardrail.add_sample("Bad sample two")
        guardrail.add_sample("Bad sample three")

        # Create instruction
        final_token = FinalToken("Result")
        instruction_input = InstructionInput(tokensets=[context_set1, context_set2, user_set], context=None)
        extended_response = ExtendedResponse(final=final_token)
        instruction = ExtendedInstruction(
            input=instruction_input,
            output=extended_response,
        )

        context_snippet1 = context_set1.create_snippet("Context 1")
        context_snippet2 = context_set2.create_snippet("Context 2")
        output_snippet = user_set.create_snippet("Output")

        instruction.add_sample(
            inputs=[context_snippet1, context_snippet2, output_snippet],
            response_string="User prompt"
        )
        instruction.add_sample(
            inputs=[context_snippet1, context_snippet2, output_snippet],
            response_string="User prompt 2"
        )
        instruction.add_sample(
            inputs=[context_snippet1, context_snippet2, output_snippet],
            response_string="User prompt 3"
        )

        # Add guardrail to instruction at tokenset index 2 (user_set)
        instruction.add_guardrail(guardrail, tokenset_index=2)

        protocol.add_instruction(instruction)

        # Verify guardrail was added to instruction
        assert len(instruction.input.guardrails) > 0
        assert 2 in instruction.input.guardrails

    def test_protocol_add_default_special_tokens(self):
        """Test adding default special tokens."""
        protocol = Protocol("test_protocol", inputs=2)

        # Add default special tokens
        protocol._add_default_special_tokens()

        assert len(protocol.special_tokens) >= 4  # BOS, EOS, RUN, PAD

    def test_protocol_add_default_special_tokens_with_guardrails(self):
        """Test adding default special tokens with guardrails."""
        protocol = Protocol("test_protocol", inputs=2)

        # Add guardrails
        protocol.guardrails["test"] = ["bad_output", "bad_prompt", "good_prompt", ["sample1", "sample2", "sample3"]]

        # Add default special tokens
        protocol._add_default_special_tokens()

        assert len(protocol.special_tokens) >= 5  # BOS, EOS, RUN, PAD, UNK

    def test_protocol_prep_protocol(self):
        """Test protocol preparation."""
        protocol = Protocol("test_protocol", inputs=2)

        # Add context and instruction
        protocol.add_context("Context line 1")
        protocol.add_context("Context line 2")

        token1 = Token("Token1", key="🔑")
        token2 = Token("Token2", key="🔧")
        token3 = Token("Token3", key="🔨")
        context_set1 = TokenSet(tokens=(token1,))
        context_set2 = TokenSet(tokens=(token2,))
        response_set = TokenSet(tokens=(token3,))

        final_token = FinalToken("Result")
        instruction_input = InstructionInput(tokensets=[context_set1, context_set2], context=None)
        instruction_output = InstructionOutput(tokenset=response_set, final=final_token)
        instruction = Instruction(
            input=instruction_input,
            output=instruction_output,
        )

        context_snippet1 = context_set1.create_snippet("Context 1")
        context_snippet2 = context_set2.create_snippet("Context 2")
        output_snippet = response_set.create_snippet("Output")

        instruction.add_sample(
            input_snippets=[context_snippet1, context_snippet2],
            output_snippet=output_snippet
        )
        instruction.add_sample(
            input_snippets=[context_snippet1, context_snippet2],
            output_snippet=output_snippet
        )
        instruction.add_sample(
            input_snippets=[context_snippet1, context_snippet2],
            output_snippet=output_snippet
        )

        protocol.add_instruction(instruction)
        
        # Add more context to meet minimum requirement
        for i in range(3, 11):
            protocol.add_context(f"Context line {i}")

        # Prepare protocol
        protocol._prep_protocol()

        # Check that special tokens were added
        assert len(protocol.special_tokens) >= 4

    def test_protocol_prep_protocol_no_instructions(self):
        """Test protocol preparation with no instructions."""
        protocol = Protocol("test_protocol", inputs=2)

        # Add context but no instructions
        protocol.add_context("Context line 1")
        protocol.add_context("Context line 2")

        # _prep_protocol() doesn't validate, so it should succeed
        # Validation happens in save() and template()
        protocol._prep_protocol()
        
        # But validate_protocol() should return False
        valid, error_msg = protocol.validate_protocol()
        assert not valid
        assert "No instructions have been added" in error_msg

    @pytest.mark.parametrize("instruction_context_snippets", [2, 3, 5, 10])
    def test_protocol_various_instruction_context_snippets(self, instruction_context_snippets):
        """Test protocol with various context lines."""
        protocol = Protocol("test_protocol", inputs=instruction_context_snippets)

        assert protocol.instruction_input_snippets == instruction_context_snippets

    @pytest.mark.parametrize("encrypt", [True, False])
    def test_protocol_encryption_settings(self, encrypt):
        """Test protocol with different encryption settings."""
        protocol = Protocol("test_protocol", inputs=3, encrypt=encrypt)

        assert protocol.encrypt == encrypt

    def test_protocol_name_variations(self):
        """Test protocol with various names."""
        names = ["test_protocol", "my_model", "weather_mage", "alice_cat"]

        for name in names:
            protocol = Protocol(name, inputs=3)
            assert protocol.name == name
