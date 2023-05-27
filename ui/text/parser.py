from ui.actions import UserAction, UserVerb


class InvalidUserActionException(Exception):
    pass


class TextParser:
    def __init__(self, valid_verbs: list[UserVerb]):
        self.verbs = {verb.name: verb for verb in valid_verbs}

    def parse_user_action(self, text: str) -> UserAction:
        try:
            return UserAction(verb=self.verbs[text], object=None)
        except KeyError:
            raise InvalidUserActionException(f"I don't know how to {text}") from None
