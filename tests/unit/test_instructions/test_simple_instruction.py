"""
Unit tests for the Instruction class.
"""
import pytest

from model_train_protocol.common.instructions.Instruction import Instruction
from model_train_protocol.common.instructions.input.InstructionInput import InstructionInput
from model_train_protocol.common.instructions.output.InstructionOutput import InstructionOutput
from model_train_protocol.common.tokens.TokenSet import TokenSet
from model_train_protocol.common.tokens.FinalToken import FinalToken
from tests.fixtures.tokens import SIMPLE_TOKENSET, USER_TOKENSET, \
    SIMPLE_NUMTOKEN_TOKENSET


class TestSimpleInstruction:
    """Test cases for the Instruction class."""

    def test_simple_tokenset(self):
        """Test creating a simple instruction with basic tokens."""
        token_continue = FinalToken("Continue")
        instruction_input = InstructionInput(tokensets=[SIMPLE_TOKENSET, SIMPLE_TOKENSET])
        instruction_output = InstructionOutput(tokenset=SIMPLE_TOKENSET, final=token_continue)
        instruction: Instruction = Instruction(input=instruction_input, output=instruction_output)

        assert len(instruction.input.tokensets) == 2
        assert instruction.output.tokenset == SIMPLE_TOKENSET
        assert instruction.output.final == [token_continue]

    def test_user_tokenset(self):
        """Test that adding a user token in the final tokenset succeeds"""
        token_continue = FinalToken("Continue")
        instruction_input = InstructionInput(tokensets=[USER_TOKENSET, SIMPLE_TOKENSET])
        instruction_output = InstructionOutput(tokenset=USER_TOKENSET, final=token_continue)
        # Should not raise error since UserToken validation is no longer required
        instruction = Instruction(input=instruction_input, output=instruction_output)
        assert instruction is not None

    def test_num_tokensset(self):
        """Test creating an instruction with numeric tokens."""
        token_continue = FinalToken("Continue")
        instruction_input = InstructionInput(tokensets=[SIMPLE_NUMTOKEN_TOKENSET, SIMPLE_TOKENSET])
        instruction_output = InstructionOutput(tokenset=SIMPLE_TOKENSET, final=token_continue)
        instruction: Instruction = Instruction(input=instruction_input, output=instruction_output)

        assert len(instruction.input.tokensets) == 2
        assert instruction.output.tokenset == SIMPLE_TOKENSET
        assert instruction.output.final == [token_continue]

    def test_num_and_numlist_tokenset(self):
        """Test creating an instruction with both numeric and numeric list tokens."""
        from tests.fixtures.tokens import SIMPLE_NUMTOKEN_NUMLISTTOKEN_TOKENSET

        token_continue = FinalToken("Continue")
        instruction_input = InstructionInput(tokensets=[SIMPLE_NUMTOKEN_NUMLISTTOKEN_TOKENSET, SIMPLE_TOKENSET])
        instruction_output = InstructionOutput(tokenset=SIMPLE_TOKENSET, final=token_continue)
        instruction: Instruction = Instruction(input=instruction_input, output=instruction_output)

        assert len(instruction.input.tokensets) == 2
        assert instruction.output.tokenset == SIMPLE_TOKENSET
        assert instruction.output.final == [token_continue]

    def test_multiple_num_tokensets(self):
        """Test creating an instruction with multiple numeric tokens."""
        from tests.fixtures.tokens import SIMPLE_NUMTOKEN_TOKENSET

        token_continue = FinalToken("Continue")
        instruction_input = InstructionInput(tokensets=[SIMPLE_NUMTOKEN_TOKENSET, SIMPLE_NUMTOKEN_TOKENSET])
        instruction_output = InstructionOutput(tokenset=SIMPLE_TOKENSET, final=token_continue)
        instruction: Instruction = Instruction(input=instruction_input, output=instruction_output)

        assert len(instruction.input.tokensets) == 2
        assert instruction.output.tokenset == SIMPLE_TOKENSET
        assert instruction.output.final == [token_continue]

    def test_wrong_tokenset_snippet(self):
        """Test that creating a snippet with wrong tokenset raises an error."""
        token_continue = FinalToken("Continue")
        instruction_input = InstructionInput(tokensets=[SIMPLE_TOKENSET, SIMPLE_TOKENSET])
        instruction_output = InstructionOutput(tokenset=SIMPLE_TOKENSET, final=token_continue)
        instruction: Instruction = Instruction(input=instruction_input, output=instruction_output)

        # Create snippet with wrong tokenset (USER_TOKENSET instead of SIMPLE_TOKENSET)
        wrong_snippet = USER_TOKENSET.create_snippet("Wrong snippet")
        correct_snippet = SIMPLE_TOKENSET.create_snippet("Correct snippet")

        with pytest.raises(ValueError, match="does not match expected token set"):
            instruction.add_sample(
                input_snippets=[wrong_snippet, correct_snippet],
                output_snippet=correct_snippet
            )
    def test_wrong_number_of_snippets(self):
        """Test that creating a snippet with wrong tokenset raises an error."""
        token_continue = FinalToken("Continue")
        instruction_input = InstructionInput(tokensets=[SIMPLE_TOKENSET, SIMPLE_TOKENSET])
        instruction_output = InstructionOutput(tokenset=SIMPLE_TOKENSET, final=token_continue)
        instruction: Instruction = Instruction(input=instruction_input, output=instruction_output)

        # Create snippet with wrong tokenset (USER_TOKENSET instead of SIMPLE_TOKENSET)
        correct_snippet = SIMPLE_TOKENSET.create_snippet("Correct snippet")

        with pytest.raises(ValueError):
            instruction.add_sample(
                input_snippets=[correct_snippet],
                output_snippet=correct_snippet
            )