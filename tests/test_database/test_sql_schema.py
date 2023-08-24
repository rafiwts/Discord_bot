from datetime import datetime

from database.models import (
            DiscordUser,
            Event,
            Reaction,
            Message,
            BotUser,
            Command
)

class TestDatabase:
    def test_event(self, session):
        event_created = datetime.now()
        user_created = datetime.now()

        add_user = DiscordUser.create(
                                    discord_id = 1299,
                                    discord_user= 1325,
                                    username="Makk",
                                    guildname="GuildName",
                                    created_at=user_created)
        add_user.save()

        add_event = Event.create(name='Event',
                                created=event_created,
                                user=add_user.id,
                                counter=1)
        
        add_event.save()

        assert add_event.user.username == "Makk"

    def test_user(self, session):
        user_created = datetime.now()

        add_model = DiscordUser.create(
                                        discord_id = 12999,
                                        discord_user=12425,
                                        username="Macipopoek",
                                        guildname="GuildName",
                                        created_at=user_created)
        add_model.save()

        assert add_model.discord_id == 12999



