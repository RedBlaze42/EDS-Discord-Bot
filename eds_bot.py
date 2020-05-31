import discord,json,asyncio
import fleetyards,embeds
from datetime import datetime,timedelta

bot=discord.Client()

def open_config():
    with open("config.json","r") as config_file:
        config=json.load(config_file)
    return config

def save_config(config):
    with open("config.json","w") as config_file:
        config_file.write(json.dumps(config))

async def check_hangars():
    hangars_backup=bot.api.get_all_corp_hangars()
    channel=bot.get_channel(bot.config["fleet_channel"])
    if channel is None: raise Exception("No channel found")
    while True:
        new_hangars=bot.api.get_all_corp_hangars()
        for member,hangar in new_hangars.items():
            if member not in hangars_backup.keys(): continue
            diff=bot.api.compare_hangars(hangars_backup[member], hangar)
            if diff!=([],[]):
                embed=bot.embeds.hangar_diffs(member,diff)
                await channel.send(embed=embed)
        #print("End of hangar check")
        hangars_backup=new_hangars
        await asyncio.sleep(bot.config["refresh_interval"])

async def check_members():
    previous_members=bot.api.members
    channel=bot.get_channel(bot.config["fleet_channel"])#TODO Separate channels ?
    if channel is None: raise Exception("No channel found")

    while True:
        new_members=bot.api.members
        diffs=bot.api.compare_members(previous_members, new_members)
        if diffs!=([],[]):
            for new_member in diffs[0]:
                embed=bot.embeds.new_member(new_member)
                await channel.send(embed=embed)

            for kicked_member in diffs[1]:
                embed=bot.embeds.member_leeaving(kicked_member)
                await channel.send(embed=embed)
        #print("End of members check")
        previous_members=new_members
        await asyncio.sleep(bot.config["refresh_interval"])

bot.config=open_config()
bot.api=fleetyards.FleetYardsAPI(bot.config["fleetyards_login"],bot.config["fleetyards_password"],bot.config["fleet_id"])
bot.embeds=embeds.EDS_Embeds(bot)

async def delete_old_messages():
    while True:
        if bot.config["expires"]<=0: return
        channels=[bot.get_channel(bot.config["fleet_channel"])]
        time_limit=datetime.utcnow()-timedelta(days=bot.config["expires"])
        count=0
        for channel in channels:
            async for message in channel.history(before=time_limit):
                if message.author==bot.user:
                    await message.delete()
                    count+=1
        print("Deleted",count,"messages with time limit on",time_limit)
        await asyncio.sleep(86400)


@bot.event
async def on_ready():
    print("Bot ready !")
    bot.loop.create_task(check_hangars())
    bot.loop.create_task(check_members())
    bot.loop.create_task(delete_old_messages())
bot.run(bot.config["token"])