import re


def stands():

    stylized_stand_names = []

    with open('data//stand_names.txt', 'r') as read_file:
        stand_names = read_file.readlines()
        stand_names = [i[:-1] for i in stand_names]

    for i in stand_names:
        stylized_stand_name = "「"
        for j in i:
            stylized_stand_name += j + " "
        stylized_stand_name = stylized_stand_name[:-1]
        stylized_stand_name += "」"
        stylized_stand_names.append(stylized_stand_name)

    def temp(x):

        for sn, ssn in zip(stand_names, stylized_stand_names):
            x = re.sub(sn, ssn, x, flags=re.IGNORECASE | re.MULTILINE)

        return x

    return [temp]


def beginning_b():
    return [
        lambda x: re.sub("^b", "🅱", x, flags=re.IGNORECASE | re.MULTILINE),
        lambda x: re.sub(" b", " 🅱", x, flags=re.IGNORECASE | re.MULTILINE)
    ]


def im_x():
    return [lambda x: re.sub("^.*( |^)i'?m (.+)", r"Hi \2, I'm dad!", x, flags=re.I | re.MULTILINE)]


def shoot_me():
    return [lambda x: re.sub("^.*shoot me.*", ":gun:", x, flags=re.I | re.M)]


def kill_me():
    return [lambda x: re.sub("^.*kill me.*", ":gun:", x, flags=re.I | re.M)]


def stab_me():
    return [lambda x: re.sub("^.*stab me.*", ":dagger:", x, flags=re.I | re.M)]


def nicu():
    return [lambda x: re.sub("^.*nicu.*", "nicu nicu\nvery nicu shiza-chan", x, flags=re.I | re.M)]


def stand():
    return [lambda x: re.sub("^.*stand.*", "What, a stand?", x, flags=re.I | re.M)]


def nullpo():
    return [lambda x: re.sub("^.*nullpo.*", "Gah!", x, flags=re.I | re.M)]