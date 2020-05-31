import discord,json,asyncio
import fleetyards,embeds

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
                embed=embeds.hangar_diffs(member,diff,bot.api.fleet_value(),bot.api.fleet_auec_value())
                await channel.send(embed=embed)
        print("End of hangar check")
        hangars_backup=new_hangars
        await asyncio.sleep(bot.config["refresh_interval"])

bot.config=open_config()
bot.api=fleetyards.FleetYardsAPI(bot.config["fleetyards_login"],bot.config["fleetyards_password"],bot.config["fleet_id"])


@bot.event
async def on_ready():
    print("Bot ready !")
    bot.loop.create_task(check_hangars())

bot.run(bot.config["token"])