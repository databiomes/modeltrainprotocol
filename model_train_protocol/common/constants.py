from model_train_protocol.common.tokens import SpecialToken, Token, NumToken, FinalToken, FinalNumToken, NumListToken
from model_train_protocol.common.tokens.SpecialFinalToken import SpecialFinalToken

NON_TOKEN: SpecialFinalToken = SpecialFinalToken(value="<NON>", key="<NON>", special="none")
BOS_TOKEN: SpecialToken = SpecialToken(value="<BOS>", key="<BOS>", special="start")
EOS_TOKEN: SpecialFinalToken = SpecialFinalToken(value="<EOS>", key="<EOS>", special="end")
RUN_TOKEN: SpecialToken = SpecialToken(value="<RUN>", key="<RUN>", special="infer")
PAD_TOKEN: SpecialToken = SpecialToken(value="<PAD>", key="<PAD>", special="pad")
UNK_TOKEN: SpecialToken = SpecialToken(value="<UNK>", key="<UNK>", special="unknown")

MINIMUM_TOTAL_CONTEXT_LINES = 10
PER_FINAL_TOKEN_SAMPLE_MINIMUM = 3

TokenTypeEnum: dict = {
    "Token": Token,
    "SpecialToken": SpecialToken,
    "SpecialFinalToken": SpecialFinalToken,
    "NumToken": NumToken,
    "FinalToken": FinalToken,
    "FinalNumToken": FinalNumToken,
    "NumListToken": NumListToken
}
