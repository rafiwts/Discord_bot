import time

class Session:
    def __init__(self, 
                 bot_id: str, 
                 user_id: str, 
                 is_active: bool = False, 
                 start_time: int = time.time(), 
                 finish_time: int = 0) -> None:
        self.bot_id = bot_id
        self.user_id = user_id
        self.is_active = is_active
        self.start_time = start_time
        self.finish_time = finish_time

    @property
    def duration_of_session(self) -> int:
        end_time = time.time()
        return end_time - self.start_time