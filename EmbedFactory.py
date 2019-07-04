import discord

def reddit_default(data):

    embed = discord.Embed()
    embed.set_author(name=data['title'], url="https://www.reddit.com" + data['permalink'])
    embed.set_footer(text="by u/" + data['author'])
    embed.colour = 16747360

    return embed


def reddit_selfpost(data):

    embed = reddit_default(data)
    embed.description = data['selftext']

    return embed


def reddit_link_post(data):

    embed = reddit_default(data)
    embed.description = data['selftext']

    return embed


def reddit_image_post(data, image_link):

    embed = reddit_default(data)
    embed.set_image(url=image_link)

    return embed


def nhentai_gallery(_id, url, title, pages, tags, languages, artists, categories, parodies, characters, groups,
                    cover_url):

    embed = discord.Embed()
    embed.colour = 15476564

    embed.set_author(name=_id, url=url)

    embed.title = title

    embed.set_thumbnail(url=cover_url)

    embed.add_field(name="Pages", value=pages)

    tag_string = nhentai_tag_formatter(tags)
    if tag_string:
        embed.add_field(name="Tags", value=tag_string)

    language_string = nhentai_tag_formatter(languages)
    if language_string:
        embed.add_field(name="Languages", value=language_string)

    artist_string = nhentai_tag_formatter(artists)
    if artist_string:
        embed.add_field(name="Artists", value=artist_string)

    categories_string = nhentai_tag_formatter(categories)
    if categories_string:
        embed.add_field(name="Categories", value=categories_string)

    parodies_string = nhentai_tag_formatter(parodies)
    if parodies_string:
        embed.add_field(name="Parodies", value=parodies_string)

    characters_string = nhentai_tag_formatter(characters)
    if characters_string:
        embed.add_field(name="Characters", value=characters_string)

    groups_string = nhentai_tag_formatter(groups)
    if groups_string:
        embed.add_field(name="Groups", value=groups_string)

    return embed


def nhentai_tag_formatter(tags):
    j = len(tags)
    if tags:
        tags_string = ""
        for i in tags:

            j -= 1
            if len(tags_string) + len(str(j)) + sum([len(x) for x in i]) > 990:
                tags_string += "+" + str(j) + " more"
                break


            tags_string += "[" + i[0] + "](https://nhentai.net" + i[2] + ") (" + str(i[1]) + ")\n"


        return tags_string
    return None


def blank(message):

    embed = discord.Embed()
    embed.description = message

    return embed


def nhentai_gallery_list(query, results):

    embed = discord.Embed()
    embed.colour = 15476564

    embed.set_author(name="Search results for: " + query)

    if results:
        description = ""

        for i in results:

            if len(description) + len(i) > 2048:
                break

            description += "**" + i[0] + "** - " + i[1]
            description += "\n"

    else:
        description = "No results found."

    embed.description = description

    return embed
