from dataclasses import dataclass


@dataclass
class Session:
    bot_id: str
    user_id: str
    is_active: bool = False
    start_time: int = 0
    finish_time: int = 0

    def current_user(self, user):
        self.user_id = user
