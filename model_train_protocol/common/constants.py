from model_train_protocol.common.tokens import SpecialToken

NON_TOKEN: SpecialToken = SpecialToken(value="<NON>", key="<NON>", special="none")
BOS_TOKEN: SpecialToken = SpecialToken(value="<BOS>", key="<BOS>", special="start")
EOS_TOKEN: SpecialToken = SpecialToken(value="<EOS>", key="<EOS>", special="end")
RUN_TOKEN: SpecialToken = SpecialToken(value="<RUN>", key="<RUN>", special="infer")
PAD_TOKEN: SpecialToken = SpecialToken(value="<PAD>", key="<PAD>", special="pad")
UNK_TOKEN: SpecialToken = SpecialToken(value="<UNK>", key="<UNK>", special="unknown")

# TODO: Remove this code when emoji dependency is removed
"""Assign default emoji keys to special tokens for backward compatibility."""
special_token_emoji_map = {
    NON_TOKEN.value: "🫙",
    BOS_TOKEN.value: "🏁",
    EOS_TOKEN.value: "🎬",
    RUN_TOKEN.value: "🏃",
    PAD_TOKEN.value: "🗒",
    UNK_TOKEN.value: "🛑"
}
for token in [NON_TOKEN, BOS_TOKEN, EOS_TOKEN, RUN_TOKEN, PAD_TOKEN, UNK_TOKEN]:
    token.key = special_token_emoji_map[token.value]
