async def link_account(user, epic_id):
    await user.edit(nick=epic_id)