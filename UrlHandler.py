import re
import imgur_url
import urllib.request

url = imgur_url.ImgurURL()


def handle(link):

    print(link)

    if "i.reddit.com" in link:
        return link

    if "i.redd.it" in link:
        return link

    elif "i.imgur.com" in link:
        return link

    elif "imgur.com/a" in link:
        link = url.get_imgur_urls('link')[0]
        return link
        # TODO: Remove imgur_url dependency by implement own function

    elif "gfycat.com" in link:
        response = urllib.request.urlopen(link)
        html = str(response.read().decode("utf8"))
        new_link = re.search(r"srcSet=\"([^\"]*)\"", html).group(1)
        if new_link.split(".")[-1] != "gif":
            return None
        return new_link


if __name__ == '__main__':
    print(handle("https://gfycat.com/zealousunfinishedeyra"))
