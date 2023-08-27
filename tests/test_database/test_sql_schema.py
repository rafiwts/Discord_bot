import pytest
import discord
import peewee
from datetime import datetime
from unittest.mock import Mock, patch

from database.models import (
            DiscordUser,
            Event,
            Reaction,
            Message,
            BotUser,
            Command
)

class TestUserTable:
    #FIXME: how to save the whole for records 
    @pytest.mark.parametrize(
        "id, discord_id, username, guildname, created_at",
        [(1 ,1111, "Rafal", "Guildname", datetime.now()),
         (2, 2222, "Maciek", "Guild", datetime.now()),
         (3, 3333, "Tomasz", "Gildia", datetime.now()),
         (4, 4444, "Maciej", "GildiaMagii", datetime.now())]
    )
    def test_create_user_with_all_data(
        self, 
        session,
        id,
        discord_id,
        username,
        guildname, 
        created_at
    ):
       
        add_user = DiscordUser.create(id=id,
                                      discord_id=discord_id,
                                      username=username,
                                      guildname=guildname,
                                      created_at=created_at)
        add_user.save()
    
        assert add_user.id == id
        assert add_user.discord_id == discord_id
        assert add_user.username == username
        assert add_user.guildname == guildname
        assert add_user.created_at == created_at

    def test_get_or_create_user_with_all_data(
            self,
            session, 
            mock_time, 
            mock_discord_user
    ):
        with patch('discord.Member', new_callable=Mock) as member:
            # discord_id of an existing discord user in database
            member.id = 1111
        
            check_existing_discord_user = DiscordUser.get_or_create_user(discord.Member)

            assert check_existing_discord_user.id == 2
            assert check_existing_discord_user.discord_id == 1111
            assert check_existing_discord_user.username == "Rafiwts"
            assert check_existing_discord_user.guildname == "Gildia"
            assert check_existing_discord_user.created_at == mock_time
            assert check_existing_discord_user.joined_at == mock_time

        with patch('discord.Member', new_callable=Mock) as member:
            
            # discord_id of an user who is not in a database
            member.id = 2222
            member.name = "Bartosz"
            member.guild = "AnotherGuildname"
            member.created_at = mock_time
            member.joined_at = mock_time

            check_nonexisting_discord_user = DiscordUser.get_or_create_user(discord.Member)

            assert check_nonexisting_discord_user.id == 1
            assert check_nonexisting_discord_user.discord_id == member.id
            assert check_nonexisting_discord_user.username == member.name
            assert check_nonexisting_discord_user.guildname == member.guild
            assert check_nonexisting_discord_user.created_at == mock_time
            assert check_nonexisting_discord_user.joined_at == mock_time
             
    def test_create_new_admin(
        self,
        session 
    ):
        with patch('discord.Member', new_callable=Mock) as admin:
            admin.id = 1111
            admin.name = "Admin"
            admin.created_at = datetime.now()
            guildname = "AnotherGuild"

            create_admin = DiscordUser.create_new_admin(discord.Member,
                                                        guildname)

            assert create_admin.id == 1
            assert create_admin.discord_id == admin.id
            assert create_admin.username == admin.name
            assert create_admin.created_at == admin.created_at
            assert create_admin.is_admin == True

    def test_update_user_to_admin(
        self,
        session,
        mock_discord_user
    ):
        member_discord_id = mock_discord_user.discord_id
        discord_member = DiscordUser.get(discord_id=member_discord_id)
    
        assert discord_member.is_admin == False

        update_member_to_admin = DiscordUser.update_user_to_admin(member_discord_id)

        assert update_member_to_admin.is_admin == True
    
    def test_update_user_data(
        self,
        session,
        mock_discord_user
    ):
        with patch('discord.Member', new_callable=Mock) as member:
            # update a username
            member.id = mock_discord_user.discord_id  
            member.name = "Updated name"

            DiscordUser.update_user_data(discord.Member,
                                         mock_discord_user.guildname,
                                         discord.Member)
            
            get_user_with_new_username = DiscordUser.get(discord_id=mock_discord_user.discord_id)

            assert get_user_with_new_username.username == member.name
                
            # update the name of a guild
            guild = "Updated guild"

            DiscordUser.update_user_data(discord.Member,
                                         guild,
                                         discord.Member)
            
            get_user_with_new_username_and_guildname = DiscordUser.get(discord_id=mock_discord_user.discord_id)

            assert get_user_with_new_username_and_guildname.username == member.name
            assert get_user_with_new_username_and_guildname.guildname == guild

            # ban user
            banned = True

            DiscordUser.update_user_data(discord.Member,
                                         guild,
                                         banned=banned)
            
            get_banned_user = DiscordUser.get(discord_id=mock_discord_user.discord_id)

            assert get_banned_user.banned == True
                
    def test_discord_id_unique_field(
        self,
        session,
        mock_discord_user
    ):
        with pytest.raises(peewee.IntegrityError):
            create_user_that_exists = DiscordUser.create(discord_id=mock_discord_user.discord_id,
                                                         username="New User",
                                                         guildname="New Guildname")  

            create_user_that_exists.save()        
    
    def test_username_unique_field(
        self,
        session,
        mock_discord_user
    ):
        with pytest.raises(peewee.IntegrityError):
            create_user_that_exists = DiscordUser.create(discord_id="2222",
                                                         username=mock_discord_user.username,
                                                         guildname="New Guildname")
            
            create_user_that_exists.save()

    
    class TestMessageTable:
        @pytest.mark.parametrize(
           "id, discord_id, content, created_at, user",
            [(1, 1010, "First message", datetime.now(), 1),
            (2, 2020, "Second message", datetime.now(), 2),
            (3, 3030, "Third message", datetime.now(), 3),
            (4, 4040, "Fourth message", datetime.now(), 4)]
        )
        def test_create_message_with_all_data(
            self,
            session,
            mock_discord_users,
            id,
            discord_id,
            content,
            created_at,
            user
        ):
            add_new_message = Message.create(id=id,
                                             discord_id=discord_id,
                                             content=content,
                                             created_at=created_at,
                                             user=user)
            add_new_message.save()

            assert add_new_message.id == id
            assert add_new_message.discord_id == discord_id
            assert add_new_message.content == content
            assert add_new_message.created_at == created_at
            assert add_new_message.user.id == user

        def test_message_and_user_relation(
            self,
            session,
            mock_time,
            mock_discord_user
        ):
            add_new_message = Message.create(discord_id=1010,
                                             content="New content",
                                             created_at=mock_time,
                                             user=2)
            
            assert add_new_message.user.id == mock_discord_user.id
            assert add_new_message.user.discord_id == mock_discord_user.discord_id
            assert add_new_message.user.username == mock_discord_user.username
        
        def test_edit_message_with_new_content(
            self,
            session,
            mock_discord_user_and_message
        ):
            with patch('discord.Member', new_callable=Mock) as new_message:
                current_time = datetime.now()
                new_message.content = "New content"
                new_message.edited_at = current_time

                Message.edit_message(discord_id=1010,
                                     edited_message=discord.Member)
                
                edited_message = Message.get(discord_id=1010)

                assert edited_message.content == new_message.content
                assert edited_message.edited_at == new_message.edited_at
        
        def test_edit_message_with_counter_increment(
            self,
            session,
            mock_discord_user_and_message
        ):
            reaction_counter = 1

            Message.edit_message(discord_id=1010,
                                 reaction_counter=reaction_counter)
                
            edited_message = Message.get(discord_id=1010)

            assert edited_message.reaction_counter == reaction_counter

        def test_message_with_no_user_id(
            self,
            session,
        ): 
            with pytest.raises(peewee.IntegrityError):
                Message.create(discord_id="1010",
                               content="New content",
                               user=1)
                                                                
        def test_message_with_no_command_id(
            self,
            session,
            mock_discord_user
        ):
            new_message = Message.create(discord_id=1010,
                                         content="New content",
                                         user=mock_discord_user.id)
            
            assert new_message.user.id == mock_discord_user.id

            with pytest.raises(peewee.IntegrityError):
                Message.create(discord_id=2020,
                               content="Another content",
                               user=mock_discord_user.id,
                               command=1)
                
        class TestCommandTable:
            @pytest.mark.parametrize(
                "id, content, user",
                [(1, "!firstcommand", 1),
                (2, "!secondcommand", 2),
                (3, "!thirdcommand", 3),
                (4, "!fourthcommand", 4)]
            )
            def test_create_command_with_all_data(
                self,
                session,
                mock_discord_users,
                id,
                content,
                user
            ):
                add_command = Command.create(id=id,
                                             content=content,
                                             user=user)
                
                add_command.save()

                assert add_command.id == id
                assert add_command.content == content
                assert add_command.user.id == user