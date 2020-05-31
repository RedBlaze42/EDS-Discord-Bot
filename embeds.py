import discord
from datetime import datetime

class EDS_Embeds():

    def __init__(self,bot):
        self.bot = bot
        self.api = bot.api

    def hangar_diffs(self,username,diffs):
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
        embed.add_field(name="Nouvelle valeur de la flotte de {} vaisseaux:".format(len(self.api.get_corp_hangar())), value="{}$\n{} aUEC (provisoire)".format(self.api.fleet_value(),self.api.fleet_auec_value()), inline=False)
    embed.set_footer(text="EDS Bot par RedBlaze")
    embed.timestamp=diffs[0][0].updated_at if len(diffs[0])>0 else diffs[1][0].updated_at
    return embed