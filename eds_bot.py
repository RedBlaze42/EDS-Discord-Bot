import discord,json

bot=discord.Client()

def open_config():
    with open("config.json","r") as config_file:
        config=json.load(config_file)
    return config

def save_config(config):
    with open("config.json","w") as config_file:
        config_file.write(json.dumps(config))

bot.config=open_config()



bot.run(bot.config["token"])