class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __repr__(self):
        return f"Token(type={self.type}, value={self.value})"


class HeaderToken(Token):
    def __init__(self, level, value):
        super().__init__('HEADER', value)
        self.level = level

    def __repr__(self):
        return f"HeaderToken(level={self.level}, value={self.value})"


class BoldToken(Token):
    def __init__(self, value):
        super().__init__('BOLD', value)


class LinkToken(Token):
    def __init__(self, text, url):
        super().__init__('LINK', text)
        self.url = url

    def __repr__(self):
        return f"LinkToken(text={self.value}, url={self.url})"


class TextToken(Token):
    def __init__(self, value):
        super().__init__('TEXT', value)


class ListToken(Token):
    def __init__(self, value, ordered):
        super().__init__('LIST', value)
        self.ordered = ordered

    def __repr__(self):
        return f"ListToken(ordered={self.ordered}, value={self.value})"

class BlockquoteToken(Token):
    def __init__(self, value):
        super().__init__('BLOCKQUOTE', value)

    def __str__(self):
        return f"BlockquoteToken(text={self.value})"

class NewLineToken(Token):
    def __init__(self):
        super().__init__('NEWLINE', '\n')
