import discord

def hangar_diffs(username,diffs,fleet_value,fleet_auec_value):#TODO Put that in a class with bot object and add fleet logo in the embed
    embed=discord.Embed(title=username, url="https://fleetyards.net/hangar/{}".format(username), color=0x00fffb)
    embed.set_author(name="Changement de hangar !")

    if len(diffs[0]) > 0:
        ships=str()
        for ship in diffs[0]:
            ships+="+ __**{}** {}__\n".format(ship.brand_name,ship.model_name)
        embed.add_field(name="**__Ajouts__**", value=ships, inline=False)

    if len(diffs[1]) > 0:
        ships=str()
        for ship in diffs[1]:
            ships+="- __**{}** {}__\n".format(ship.brand_name,ship.model_name)
        embed.add_field(name="**__Suppressions__**", value=ships, inline=False)
    embed.add_field(name="Nouvelle valeur de la flotte:", value="{}$\n{} aUEC (provisoire)".format(fleet_value,fleet_auec_value), inline=False)
    embed.set_footer(text="EDS Bot par RedBlaze")
    embed.timestamp=diffs[0][0].updated_at if len(diffs[0])>0 else diffs[1][0].updated_at
    return embed