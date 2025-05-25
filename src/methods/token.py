class Token:
    def __init__(self, string, emoji, user=False, num=False, desc=None, special=None):
        self.string = string
        self.emoji = emoji
        self.user = user
        self.num = num
        self.desc = desc
        self.special = special

    def __str__(self):
        return f"Token(String: '{self.string}', Emoji: '{self.emoji}', User: {self.user}, Num: {self.num}, Desc: {self.desc}, Special: {self.special})"

    def to_dict(self):
        return {'string': self.string, 'emoji': self.emoji, 'user': self.user, 'num': self.num, 'desc': self.desc, 'special': self.special}
