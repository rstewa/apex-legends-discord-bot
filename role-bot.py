import os

import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# NAMES
B = 'Bronze'
S = 'Silver'
G = 'Gold'
P = 'Platinum'
D = 'Diamond'
M = 'Master'
AP = 'ApexPredator'

# IDs

# GUILDS
GUILD_ID = 981367539860914247

# CHANNELS
GET_RANKED_ROLE = 1016541235751702638

# ROLES
BRONZE_ROLE = 1016541451603165264
SILVER_ROLE = 1016543606204543097
GOLD_ROLE = 1016543996635529308
PLATINUM_ROLE = 1016544185219829790
DIAMOND_ROLE = 1016544507254276196
MASTER_ROLE = 1016544760212762655
APEX_PREDATOR_ROLE = 1016545014102364181

ROLE_IDS = {
    BRONZE_ROLE,
    SILVER_ROLE,
    GOLD_ROLE,
    PLATINUM_ROLE,
    DIAMOND_ROLE,
    MASTER_ROLE,
    APEX_PREDATOR_ROLE
}

# EMOJIS
BRONZE_EMOJI_ID = 1016557459294400522
SILVER_EMOJI_ID = 1016557460238118912
GOLD_EMOJI_ID = 1016557461265715262
PLATINUM_EMOJI_ID = 1016557462956019792
DIAMOND_EMOJI_ID = 1016557464444997672
MASTER_EMOJI_ID = 1016557464931536937
APEX_PREDATOR_EMOJI_ID = 1016557466353401936

ROLE_EMOJIS = {
    B: f'<:{B}:{BRONZE_EMOJI_ID}>',
    S: f'<:{S}:{SILVER_EMOJI_ID}>',
    G: f'<:{G}:{GOLD_EMOJI_ID}>',
    P: f'<:{P}:{PLATINUM_EMOJI_ID}>',
    D: f'<:{D}:{DIAMOND_EMOJI_ID}>',
    M: f'<:{M}:{MASTER_EMOJI_ID}>',
    AP: f'<:{AP}:{APEX_PREDATOR_EMOJI_ID}>'
}

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = discord.Client(intents=intents)


async def send_message(message: str, interaction: discord.Interaction):
    embed = discord.Embed(description=message, color=discord.Color.blurple())
    await interaction.response.send_message(embed=embed, ephemeral=True)

    print(message)


async def add_or_remove_role(interaction: discord.Interaction, role_id):
    guild = client.get_guild(GUILD_ID)
    if guild is None:
        # Check if we're still in the guild, and it's cached.
        return

    role = guild.get_role(role_id)
    if role is None:
        # Make sure the role still exists and is valid.
        return

    cur_role_ids = [role.id for role in interaction.user.roles]
    try:
        if role_id in cur_role_ids:
            # remove the role.
            await interaction.user.remove_roles(role)
            await send_message(f'Removed **{role.name}** {ROLE_EMOJIS[role.name]}  role from user **{interaction.user.name}**', interaction)

        elif any(x in ROLE_IDS for x in cur_role_ids):
            # remove the other rank role before adding the new one
            role_to_remove = next(x for x in interaction.user.roles if x.id in ROLE_IDS)

            await interaction.user.remove_roles(role_to_remove)
            await interaction.user.add_roles(role)

            message = f'Removed **{role_to_remove.name}** {ROLE_EMOJIS[role_to_remove.name]}  role from user **{interaction.user.name}**\n'\
                      f'Added **{role.name}** {ROLE_EMOJIS[role.name]}  role to user **{interaction.user.name}**'
            await send_message(message, interaction)

        else:
            # add the role.
            await interaction.user.add_roles(role)
            await send_message(f'Added **{role.name}** {ROLE_EMOJIS[role.name]}  role to user **{interaction.user.name}**', interaction)

    except discord.HTTPException:
        # If we want to do something in case of errors we'd do it here.
        pass


class Buttons(discord.ui.View):
    def __init__(self, *, timeout=None):
        super().__init__(timeout=timeout)

    @discord.ui.button(label=B, style=discord.ButtonStyle.gray, emoji=ROLE_EMOJIS[B])
    async def bronze_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await add_or_remove_role(interaction, BRONZE_ROLE)

    @discord.ui.button(label=S, style=discord.ButtonStyle.gray, emoji=ROLE_EMOJIS[S])
    async def silver_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await add_or_remove_role(interaction, SILVER_ROLE)

    @discord.ui.button(label=G, style=discord.ButtonStyle.gray, emoji=ROLE_EMOJIS[G])
    async def gold_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await add_or_remove_role(interaction, GOLD_ROLE)

    @discord.ui.button(label=P, style=discord.ButtonStyle.gray, emoji=ROLE_EMOJIS[P])
    async def platinum_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await add_or_remove_role(interaction, PLATINUM_ROLE)

    @discord.ui.button(label=D, style=discord.ButtonStyle.gray, emoji=ROLE_EMOJIS[D])
    async def diamond_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await add_or_remove_role(interaction, DIAMOND_ROLE)

    @discord.ui.button(label=M, style=discord.ButtonStyle.gray, emoji=ROLE_EMOJIS[M])
    async def master_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await add_or_remove_role(interaction, MASTER_ROLE)

    @discord.ui.button(label=AP, style=discord.ButtonStyle.gray, emoji=ROLE_EMOJIS[AP])
    async def apex_predator_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await add_or_remove_role(interaction, APEX_PREDATOR_ROLE)


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

    await purge_channel()

    channel = client.get_channel(GET_RANKED_ROLE)
    text = "Click on your current rank"
    client.role_message_id = await channel.send(text, view=Buttons())


async def purge_channel():
    print('purging get-ranked-role channel')
    channel = client.get_channel(GET_RANKED_ROLE)
    await channel.purge()


# todo: create function to create ranked roles
# todo: create function to create ranked roles emojis


client.run(TOKEN)
