from world.action import UserAction, UserVerbDictionary


class InvalidUserActionException(Exception):
    pass


class TextParser:
    def __init__(self, verbs: UserVerbDictionary):
        self.verbs = verbs

    def parse_user_action(self, text: str) -> UserAction:
        try:
            return UserAction(verb=self.verbs[text], object=None)
        except KeyError:
            raise InvalidUserActionException(f"I don't know how to {text}") from None
