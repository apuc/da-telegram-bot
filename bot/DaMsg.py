import emoji

class DaMsg:

    def __init__(self, telegram_message):
        self.telegram_message = telegram_message
        self.text = self.telegram_message.text
        self.caption = self.telegram_message.caption
        self.stylizedText = self.telegram_message.text
        self.stylizedCaption = self.telegram_message.caption
        self.m = Markdown()
        self.add_styles()

    @staticmethod
    def get_msg(data=None) -> str:
        pass

    def add_styles(self):
        if self.telegram_message.entities:
            self.stylizedText = self.m.add_entities_to_text(self.text, self.telegram_message.entities)

        if self.telegram_message.caption_entities:
            self.stylizedCaption = self.m.add_entities_to_text(self.caption, self.telegram_message.caption_entities)


class Markdown:

    def __init__(self):
        pass

    def add_entities_to_text(self, text: str, entities_list):
        offset_correction = 0
        for ent in entities_list:
            ent.offset += offset_correction
            if ent.type == "bold":
                text = self.bold(text, ent)
                offset_correction += 7
            if ent.type == "italic":
                text = self.italic(text, ent)
                offset_correction += 7
            if ent.type == "underline":
                text = self.underline(text, ent)
                offset_correction += 7
            if ent.type == "strikethrough":
                text = self.strikethrough(text, ent)
                offset_correction += 7

        return text

    @staticmethod
    def bold(text: str, entities):
        start = entities.offset - Markdown.get_emoji_offset(text)
        text = text[:start] + "<b>" + text[start:]
        end = entities.offset + entities.length - Markdown.get_emoji_offset(text) + 3
        text = text[:end] + "</b>" + text[end:]

        return text

    @staticmethod
    def italic(text: str, entities):
        start = entities.offset - Markdown.get_emoji_offset(text)
        text = text[:start] + "<i>" + text[start:]
        end = entities.offset + entities.length - Markdown.get_emoji_offset(text) + 3
        text = text[:end] + "</i>" + text[end:]

        return text

    @staticmethod
    def underline(text: str, entities):
        start = entities.offset - Markdown.get_emoji_offset(text)
        text = text[:start] + "<u>" + text[start:]
        end = entities.offset + entities.length - Markdown.get_emoji_offset(text) + 3
        text = text[:end] + "</u>" + text[end:]

        return text

    @staticmethod
    def strikethrough(text: str, entities):
        start = entities.offset - Markdown.get_emoji_offset(text)
        text = text[:start] + "<s>" + text[start:]
        end = entities.offset + entities.length - Markdown.get_emoji_offset(text) + 3
        text = text[:end] + "</s>" + text[end:]

        return text

    @staticmethod
    def get_emoji_offset(text: str):
        offset = 0
        emoji_list = emoji.distinct_emoji_list(text)
        for em in emoji_list:
            if em in Markdown.exclude_slim_emoji_pool():
                continue
            if len(em) >= 2:
                offset += 2
            else:
                offset += 1

        return offset

    @staticmethod
    def exclude_slim_emoji_pool():
        return [
            '\u2757',
            '\u2764\ufe0f',
        ]
