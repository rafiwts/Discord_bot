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
                
    def test_if_discord_id_is_unique(
        self,
        session,
        mock_discord_user
    ):
        with pytest.raises(peewee.IntegrityError):
            create_user_that_exists = DiscordUser.create(discord_id=mock_discord_user.discord_id,
                                                         username="New User",
                                                         guildname="New Guildname")  
            create_user_that_exists.save()        