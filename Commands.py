from RedditBot import RedditBot
import discord
import UrlHandler
import json

with open('config.json') as json_data_file:
    r_data = json.load(json_data_file)['reddit']

    r_bot = RedditBot(r_data['username'], r_data['password'],
                      r_data['client-id'], r_data['secret-id'],
                      "DiscordScraper/v1.0")

r_bot.authorize()


class Commands:

    @staticmethod
    async def general(message, bot):

        content = message.content

        for substitution in bot.substitutions:

            content = substitution(content)

            if not bot.stack and content != message.content:
                break

        if content != message.content:

            await bot.send(content, message.channel)

    @staticmethod
    async def help(message, bot):
        pass

    @staticmethod
    async def get_post(message, bot):
        command = message.content.split(" ")
        channel = message.channel

        try:
            if len(command) == 2:
                posts = r_bot.get_posts(command[1], "top", 1)

            elif len(command) == 3:

                try:
                    posts = r_bot.get_posts(command[1], "top", int(command[2]))
                except ValueError:
                    posts = r_bot.get_posts(command[1], command[2], 1)

            elif len(command) == 4:
                posts = r_bot.get_posts(command[1], command[2], int(command[3]))

            else:
                await channel.send("too many/too little arguments")
                return

        except KeyError:
            await channel.send("reddit api error; one of the arguments is wrong")
            return

        if not posts:
            await channel.send("no posts found")

        post = posts[-1]

        try:
            if post['data']['is_self']:
                await Commands.handle_selfposts(post, channel, bot)
            else:
                await Commands.handle_image_posts(post, channel, bot)
        
        except KeyError:
            await channel.send("no posts found")

    @staticmethod
    async def handle_image_posts(post, channel, bot):
        try:
            link = post['data']['url']
        except KeyError:
            await bot.send("Something went wrong!", channel)
            return

        link = UrlHandler.handle(link)

        if not link:
            await Commands.handle_link_posts(post, channel, bot)
            return

        embed = discord.Embed()
        embed.set_author(name=post['data']['title'], url="https://www.reddit.com" + post['data']['permalink'])
        embed.set_footer(text="by u/" + post['data']['author'])
        embed.set_image(url=link)
        embed.colour = 16747360

        await bot.send("", channel, embed=embed)

    @staticmethod
    async def handle_selfposts(post, channel, bot):

        embed = discord.Embed()
        embed.set_author(name=post['data']['title'], url="https://www.reddit.com" + post['data']['permalink'])
        embed.set_footer(text="by u/" + post['data']['author'])
        embed.description = post['data']['selftext']
        embed.colour = 16747360

        await bot.send("", channel, embed=embed)

    @staticmethod
    async def handle_link_posts(post, channel, bot):

        embed = discord.Embed()
        embed.set_author(name=post['data']['title'], url="https://www.reddit.com" + post['data']['permalink'])
        embed.set_footer(text="by u/" + post['data']['author'])
        embed.description = post['data']['url']
        embed.colour = 16747360

        await bot.send("", channel, embed=embed)

    @staticmethod
    async def get_multi_post(message, bot):
        command = message.content.split(" ")
        channel = message.channel

        try:
            if len(command) == 2:
                posts = r_bot.get_posts(command[1], "top", 1)

            elif len(command) == 3:
                posts = r_bot.get_posts(command[1], command[2], 1)

            elif len(command) == 4:
                posts = r_bot.get_posts(command[1], command[2], int(command[3]))

            else:
                await channel.send("too many/too little arguments")
                return

        except KeyError:
            await channel.send("reddit api error; one of the arguments is wrong")
            return

        if not posts:
            await channel.send("no posts found")

        for post in posts:
            if post['data']['is_self']:
                await Commands.handle_selfposts(post, channel, bot)
            else:
                await Commands.handle_image_posts(post, channel, bot)

    @staticmethod
    async def stack(message, bot):
        arg = message.content.split(" ")

        try:
            if arg[1].lower() in ("yes", "true", "t", "1"):
                bot.stack = True
            else:
                bot.stack = False

        except IndexError:
            bot.stack = not bot.stack

        await bot.send("Changed `stack` to `" + str(bot.stack) + "`", message.channel)
        bot.update_subs()

    @staticmethod
    async def handle_command(command, message, bot):

        try:
            method = command_list[command]
        except KeyError:
            method = default_command

        await method(message, bot)

    @staticmethod
    async def handle_message(message, bot):

        if message.content.startswith(trigger):

            command = message.content.strip(trigger).split()[0]
            await Commands.handle_command(command, message, bot)

        else:
            await Commands.general(message, bot)


command_list = {
    'stack': Commands.stack,
    'p': Commands.get_post,
    'help': Commands.help,
    'pm': Commands.get_multi_post,
}

default_command = Commands.help

trigger = "/"
