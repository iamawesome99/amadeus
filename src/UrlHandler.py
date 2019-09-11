import re
from src import imgur_url
import urllib.request

url = imgur_url.ImgurURL()


def handle(link):

    link = link.split("?")[0]

    if "i.reddit.com" in link:
        return link

    elif "i.redd.it" in link:
        return link

    elif link.endswith(".jpg") or link.endswith(".png"):
        return link

    elif "imgur.com/a/" in link:
        link = url.get_imgur_urls(link)[0]
        return link
        # TODO: Remove imgur_url dependency by implementing own function

    elif "imgur.com" in link:
        link = url.get_single_image_url(link)[0]
        return link

    elif "gfycat.com" in link:
        response = urllib.request.urlopen(link)
        html = str(response.read().decode("utf8"))
        new_link = re.search(r"srcSet=\"([^\"]*)\"", html).group(1)
        if new_link.split(".")[-1] != "gif":
            return None
        return new_link


if __name__ == '__main__':
    print(handle("https://gfycat.com/zealousunfinishedeyra"))
