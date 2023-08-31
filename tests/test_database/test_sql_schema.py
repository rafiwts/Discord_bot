import pytest
import discord
import peewee
from datetime import datetime
from unittest.mock import Mock, patch

import database
from database.models import DiscordUser, Event, Reaction, Message, BotUser, Command


class TestUser:
    @pytest.mark.parametrize(
        "id, discord_id, username, guildname, created_at",
        [
            (1, 1111, "Rafal", "Guildname", datetime.now()),
            (2, 2222, "Maciek", "Guild", datetime.now()),
            (3, 3333, "Tomasz", "Gildia", datetime.now()),
            (4, 4444, "Maciej", "GildiaMagii", datetime.now()),
        ],
    )
    def test_create_user_with_all_data(
        self, session, id, discord_id, username, guildname, created_at
    ):
        add_user = DiscordUser.create(
            id=id,
            discord_id=discord_id,
            username=username,
            guildname=guildname,
            created_at=created_at,
        )
        add_user.save()

        assert add_user.id == id
        assert add_user.discord_id == discord_id
        assert add_user.username == username
        assert add_user.guildname == guildname
        assert add_user.created_at == created_at

    def test_create_new_user(self, session, mock_time):
        with patch("discord.Member", new_callable=Mock) as user:
            user.id = 1111
            user.name = "Rafał"
            user.created_at = mock_time
            guildname = "NewGuild"

            new_user = DiscordUser.create_new_user(discord.Member, guildname)

            new_user.save()

            assert new_user.discord_id == user.id
            assert new_user.username == user.name
            assert new_user.created_at == user.created_at

    def test_create_new_admin(self, session, mock_time):
        with patch("discord.Member", new_callable=Mock) as user:
            user.id = 1111
            user.name = "Rafał"
            user.created_at = mock_time
            guildname = "NewGuild"
            admin = True

            new_admin = DiscordUser.create_new_admin(discord.Member, guildname, admin)

            new_admin.save()

            assert new_admin.discord_id == user.id
            assert new_admin.username == user.name
            assert new_admin.created_at == user.created_at
            assert new_admin.is_admin == admin

    def test_get_or_create_user_with_all_data(
        self, session, mock_time, mock_discord_user
    ):
        with patch("discord.Member", new_callable=Mock) as member:
            # discord_id of an existing discord user in database
            member.id = 1111

            check_existing_discord_user = DiscordUser.get_or_create_user(discord.Member)

            assert check_existing_discord_user.id == 2
            assert check_existing_discord_user.discord_id == 1111
            assert check_existing_discord_user.username == "Rafiwts"
            assert check_existing_discord_user.guildname == "Gildia"
            assert check_existing_discord_user.created_at == mock_time
            assert check_existing_discord_user.joined_at == mock_time

        with patch("discord.Member", new_callable=Mock) as member:
            # discord_id of an user who is not in a database
            member.id = 2222
            member.name = "Bartosz"
            member.guild = "AnotherGuildname"
            member.created_at = mock_time
            member.joined_at = mock_time

            check_nonexisting_discord_user = DiscordUser.get_or_create_user(
                discord.Member
            )

            assert check_nonexisting_discord_user.id == 1
            assert check_nonexisting_discord_user.discord_id == member.id
            assert check_nonexisting_discord_user.username == member.name
            assert check_nonexisting_discord_user.guildname == member.guild
            assert check_nonexisting_discord_user.created_at == mock_time
            assert check_nonexisting_discord_user.joined_at == mock_time

    def test_create_new_admin(self, session):
        with patch("discord.Member", new_callable=Mock) as admin:
            admin.id = 1111
            admin.name = "Admin"
            admin.created_at = datetime.now()
            guildname = "AnotherGuild"

            create_admin = DiscordUser.create_new_admin(discord.Member, guildname)

            assert create_admin.id == 1
            assert create_admin.discord_id == admin.id
            assert create_admin.username == admin.name
            assert create_admin.created_at == admin.created_at
            assert create_admin.is_admin == True

    def test_update_user_to_admin(self, session, mock_discord_user):
        member_discord_id = mock_discord_user.discord_id
        discord_member = DiscordUser.get(discord_id=member_discord_id)

        assert discord_member.is_admin == False

        update_member_to_admin = DiscordUser.update_user_to_admin(member_discord_id)

        assert update_member_to_admin.is_admin == True

    def test_update_user_data(self, session, mock_discord_user):
        with patch("discord.Member", new_callable=Mock) as member:
            # update a username
            member.id = mock_discord_user.discord_id
            member.name = "Updated name"

            DiscordUser.update_user_data(
                discord.Member, mock_discord_user.guildname, discord.Member
            )

            get_user_with_new_username = DiscordUser.get(
                discord_id=mock_discord_user.discord_id
            )

            assert get_user_with_new_username.username == member.name

            # update the name of a guild
            guild = "Updated guild"

            DiscordUser.update_user_data(discord.Member, guild, discord.Member)

            get_user_with_new_username_and_guildname = DiscordUser.get(
                discord_id=mock_discord_user.discord_id
            )

            assert get_user_with_new_username_and_guildname.username == member.name
            assert get_user_with_new_username_and_guildname.guildname == guild

            # ban user
            banned = True

            DiscordUser.update_user_data(discord.Member, guild, banned=banned)

            get_banned_user = DiscordUser.get(discord_id=mock_discord_user.discord_id)

            assert get_banned_user.banned == True

    def test_discord_id_unique_field(self, session, mock_discord_user):
        with pytest.raises(peewee.IntegrityError):
            create_user_that_exists = DiscordUser.create(
                discord_id=mock_discord_user.discord_id,
                username="New User",
                guildname="New Guildname",
            )

            create_user_that_exists.save()

    def test_username_unique_field(self, session, mock_discord_user):
        with pytest.raises(peewee.IntegrityError):
            create_user_that_exists = DiscordUser.create(
                discord_id="2222",
                username=mock_discord_user.username,
                guildname="New Guildname",
            )

            create_user_that_exists.save()


class TestMessage:
    @pytest.mark.parametrize(
        "id, discord_id, content, created_at, user",
        [
            (1, 1010, "First message", datetime.now(), 1),
            (2, 2020, "Second message", datetime.now(), 2),
            (3, 3030, "Third message", datetime.now(), 3),
            (4, 4040, "Fourth message", datetime.now(), 4),
        ],
    )
    def test_create_message_with_all_data(
        self, session, mock_discord_users, id, discord_id, content, created_at, user
    ):
        add_new_message = Message.create(
            id=id,
            discord_id=discord_id,
            content=content,
            created_at=created_at,
            user=user,
        )

        add_new_message.save()

        assert add_new_message.id == id
        assert add_new_message.discord_id == discord_id
        assert add_new_message.content == content
        assert add_new_message.created_at == created_at
        assert add_new_message.user.id == user

    def test_create_new_message_with_command(
        self, session, mock_time, mock_discord_user, mock_discord_command
    ):
        with patch("discord.Message", new_callable=Mock) as message:
            message.id = 1
            message.content = "content"
            message.created_at = mock_time

            new_message = Message.create_new_message(
                discord.Message, mock_discord_user.id, mock_discord_command.id
            )

            new_message.save()

            assert new_message.id == message.id
            assert new_message.content == message.content
            assert new_message.created_at == mock_time
            assert new_message.user.id == mock_discord_user.id
            assert new_message.command.id == mock_discord_command.id

    def test_message_and_user_relation(self, session, mock_time, mock_discord_user):
        add_new_message = Message.create(
            discord_id=1010, content="New content", created_at=mock_time, user=2
        )

        assert add_new_message.user.id == mock_discord_user.id
        assert add_new_message.user.discord_id == mock_discord_user.discord_id
        assert add_new_message.user.username == mock_discord_user.username

    def test_edit_message_with_new_content(
        self, session, mock_discord_user_and_message
    ):
        with patch("discord.Member", new_callable=Mock) as new_message:
            current_time = datetime.now()
            new_message.content = "New content"
            new_message.edited_at = current_time

            Message.edit_message(discord_id=1010, edited_message=discord.Member)

            edited_message = Message.get(discord_id=1010)

            assert edited_message.content == new_message.content
            assert edited_message.edited_at == new_message.edited_at

    def test_edit_message_with_counter_increment(
        self, session, mock_discord_user_and_message
    ):
        reaction_counter = 1

        Message.edit_message(discord_id=1010, reaction_counter=reaction_counter)

        edited_message = Message.get(discord_id=1010)

        assert edited_message.reaction_counter == reaction_counter

    def test_discord_id_unique_field(self, session, mock_discord_command):
        with pytest.raises(peewee.IntegrityError):
            Message.create(discord_id=1111, content="New content", user=1)

    def test_message_with_fake_user_id(
        self,
        session,
    ):
        with pytest.raises(peewee.IntegrityError):
            Message.create(discord_id="1010", content="New content", user=1)

    def test_message_with_fake_command_id(self, session, mock_discord_user):
        new_message = Message.create(
            discord_id=1010, content="New content", user=mock_discord_user.id
        )

        assert new_message.user.id == mock_discord_user.id

        with pytest.raises(peewee.IntegrityError):
            Message.create(
                discord_id=2020,
                content="Another content",
                user=mock_discord_user.id,
                command=1,
            )


class TestCommand:
    @pytest.mark.parametrize(
        "id, content, user",
        [
            (1, "!firstcommand", 1),
            (2, "!secondcommand", 2),
            (3, "!thirdcommand", 3),
            (4, "!fourthcommand", 4),
        ],
    )
    def test_create_command_with_all_data(
        self, session, mock_discord_users, id, content, user
    ):
        add_command = Command.create(id=id, content=content, user=user)

        add_command.save()

        assert add_command.id == id
        assert add_command.content == content
        assert add_command.user.id == user

    def test_create_new_command(self, session, mock_time, mock_discord_user):
        with patch("discord.Message", new_callable=Mock) as command:
            command.content = "!command"
            command.created_at = mock_time

            new_command = Command.create_new_command(
                discord.Message, mock_discord_user.id
            )

            new_command.save()

            assert new_command.user.id == mock_discord_user.id
            assert new_command.content == command.content
            assert new_command.created_at == command.created_at

    def test_create_command_and_message(self, session, mock_time, mock_discord_user):
        new_command = Command.create(content="!newcommand", user=mock_discord_user.id)

        new_command.save()

        new_message = Message.create(
            discord_id=1010,
            content=new_command.content,
            created_at=mock_time,
            user=mock_discord_user.id,
            command=new_command.id,
        )

        assert new_message.command.id == new_command.id

    def test_edit_command_with_increment_counter_by_one(
        self, session, mock_discord_command, mock_time
    ):
        with patch("discord.Message", new_callable=Mock) as new_command:
            new_command.created_at = mock_time
            new_command.content = mock_discord_command.content
            counter = mock_discord_command.command_counter + 1

            increment_command_counter = Command.increment_counter(
                counter, discord.Message, mock_discord_command.user.id
            )

            increment_command_counter.execute()

            updated_command = Command.get(id=mock_discord_command.id)

            assert updated_command.command_counter == counter

    def test_command_with_fake_user_id(self, session):
        with pytest.raises(peewee.IntegrityError):
            Command.create(content="!newcommand", user=1)


class TestBot:
    @pytest.mark.parametrize(
        "id, discord_id, botname, prefix, owner",
        [
            (1, 1011, "Bot1", "!", 1),
            (2, 2022, "Bot2", "?", 2),
            (3, 3033, "Bot3", "#", 3),
            (4, 4044, "Bot4", "$", 4),
        ],
    )
    def test_create_bot_with_all_data(
        self,
        session,
        mock_discord_users,
        id,
        discord_id,
        botname,
        prefix,
        owner,
    ):
        new_bot = BotUser.create(
            id=id,
            discord_id=discord_id,
            botname=botname,
            command_prefix=prefix,
            owner=owner,
        )

        new_bot.save()

        assert new_bot.id == id
        assert new_bot.discord_id == discord_id
        assert new_bot.owner.id == owner

    def test_create_new_bot(self, session, mock_discord_user):
        with patch("discord.ext.commands.Bot", new_callable=Mock) as bot:
            bot.application_id = 1011
            bot.user = "Bot"
            bot.command_prefix = "!"

            new_bot = BotUser.create_new_bot(
                discord.ext.commands.Bot, mock_discord_user.id
            )

            new_bot.save()

            assert new_bot.discord_id == bot.application_id
            assert new_bot.botname == bot.user
            assert new_bot.owner.id == mock_discord_user.id

    def test_check_user_or_bot(self, session, mock_discord_user, mock_bot_user):
        # check discord user
        get_discord_user = BotUser.check_user_or_bot(mock_discord_user.discord_id)

        assert get_discord_user.discord_id == mock_discord_user.discord_id

        # check bot user
        get_bot_user = BotUser.check_user_or_bot(mock_bot_user.discord_id)

        assert get_bot_user.discord_id == mock_bot_user.discord_id
        assert get_bot_user.owner.id == mock_discord_user.id

    def test_bot_unique_fields(self, session, mock_bot_user):
        # discord_id field
        with pytest.raises(peewee.IntegrityError):
            new_bot = BotUser.create(
                discord_id=mock_bot_user.discord_id,
                botname="AnotherBot",
                command_prefix="!",
                owner=mock_bot_user.id,
            )

            new_bot.save()

        # botname field
        with pytest.raises(peewee.IntegrityError):
            new_bot = BotUser.create(
                discord_id=2022,
                botname=mock_bot_user.botname,
                command_prefix="!",
                owner=mock_bot_user.id,
            )

            new_bot.save()

        # owner field
        with pytest.raises(peewee.IntegrityError):
            new_bot = BotUser.create(
                discord_id=2022,
                botname="AnoterBot",
                command_prefix="!",
                owner=1,
            )

            new_bot.save()


class TestReaction:
    @pytest.mark.parametrize(
        "user_from, user_to, message",
        [(1, 2, 1), (2, 3, 2), (3, 4, 3), (4, 1, 4)],
    )
    def test_create_message_with_all_data(
        self,
        user_from,
        user_to,
        message,
        session,
        mock_discord_users,
        mock_discord_messages,
        mock_time,
    ):
        new_reaction = Reaction.create(
            user_from=user_from,
            user_to=user_to,
            message=message,
            added_at=mock_time,
            edited_at=mock_time,
        )

        new_reaction.save()

        assert new_reaction.user_from.id == user_from
        assert new_reaction.user_to.id == user_to
        assert new_reaction.message.id == message

    def test_create_new_reaction(self, session, mock_discord_user_and_message):
        current_user = DiscordUser.get(discord_id=1111)
        current_message = Message.get(discord_id=1010)

        new_reaction = Reaction.create_new_reaction(current_user.id, current_message)

        assert new_reaction.user_from.id == current_user.id
        assert new_reaction.message.id == current_message.id

    def test_reaction_foreign_keys_validation(
        self, session, mock_discord_user_and_message
    ):
        current_user = DiscordUser.get(discord_id=1111)
        current_message = Message.get(discord_id=1010)

        # incorrect message id
        with pytest.raises(peewee.IntegrityError):
            with patch("database.models.Message", new_callable=Mock) as message:
                message.user.id = current_user.id
                message.id = 2

                new_reaction = Reaction.create_new_reaction(current_user, message)

                new_reaction.save()

        # incorrect user id for `user_to` field
        with pytest.raises(peewee.IntegrityError):
            with patch("database.models.Message", new_callable=Mock) as message:
                message.user.id = 2
                message.id = current_message.id

                new_reaction = Reaction.create_new_reaction(current_user, message)

                new_reaction.save()

        # incorrect user id for `user_from` field
        with pytest.raises(peewee.IntegrityError):
            with patch(
                "database.models.DiscordUser", new_callable=Mock
            ) as discord_user:
                discord_user.id = 2

                new_reaction = Reaction.create_new_reaction(
                    discord_user.id, current_message
                )

                new_reaction.save()


class TestEvent:
    @pytest.mark.parametrize(
        "id, content, created_at, user",
        [
            (1, "message1", datetime.now(), 4),
            (2, "message2", datetime.now(), 3),
            (3, "message3", datetime.now(), 2),
            (4, "message4", datetime.now(), 1),
        ],
    )
    def test_create_event_with_all_data(
        self,
        session,
        mock_discord_users,
        id,
        content,
        created_at,
        user,
    ):
        new_event = Event.create(
            id=id, content=content, created_at=created_at, user=user
        )

        new_event.save()

        assert new_event.id == id
        assert new_event.user.id == user
        assert new_event.content == content
        assert new_event.counter == 1

    def test_create_new_event_with_message(self, session, mock_discord_user, mock_time):
        with patch("discord.Message", new_callable=Mock) as message:
            message.created_at = mock_time
            message.content = "message1"

            new_event = Event.create_new_event(mock_discord_user.id, discord.Message)

            new_event.save()

            assert new_event.content == message.content
            assert new_event.created_at == mock_time

    def test_create_new_event_with_no_message(self, session, mock_discord_user):
        new_event = Event.create_new_event(mock_discord_user.id)

        new_event.save()

        assert new_event.content is None
        assert new_event.user.id == mock_discord_user.id

    def test_increment_counter(self, session, mock_discord_user_and_message):
        current_user = DiscordUser.get(discord_id=1111)
        current_message = Message.get(discord_id=1010)

        with patch("discord.Message", new_callable=Mock) as message:
            message.content = current_message.content

            new_event = Event.create(
                content=current_message.content, user=current_user.id
            )

            new_event.save()

            Event.increment_counter(
                user=current_user.id,
                sent_message=discord.Message,
                counter=new_event.counter + 1,
            ).execute()

            updated_event = Event.get(content=current_message.content)

            assert updated_event.counter == 2

    def test_event_foreign_keys_validations(self, session):
        with pytest.raises(peewee.IntegrityError):
            new_event = Event.create(content="message1", user=1)
            new_event.save()
