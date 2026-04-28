async def create_team(guild, name):
    role = await guild.create_role(name=name)
    category = await guild.create_category(name)

    await guild.create_text_channel("chat", category=category)
    await guild.create_voice_channel("vc", category=category)
