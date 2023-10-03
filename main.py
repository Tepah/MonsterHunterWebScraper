import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient


def createData(url, monster_link_list):
    response = requests.get(url)

    if response.status_code == 200:
        print("Success!")
        soup = BeautifulSoup(response.content, 'html.parser')
    else:
        print("Failure!")
        return None

    paragraphs = soup.find_all(['a'])
    found = False
    # List of things to exclude from the list of monsters since they are not monsters or are from other games
    excludeList = (
    "Afflicted Monsters", "Apex Monsters (MHRise)", "Black Blight", "Frenzy Virus", "Fish", "Fishman Oni", "Goocoo",
    "Halk", "Moofy", "Poogie", "Tempered State", "Boaboa", "Gear REX", "Grimalkyne", "Miyamoa", "Mysterious Mi Ru",
    "Oltura")
    for paragraph in paragraphs:
        if paragraph.string == "Giaprey" or paragraph.string == "Seltas": found = True
        if found and paragraph.string != None and paragraph.string not in excludeList:
            print(paragraph.string)
            monster_link_list.append((paragraph.string, paragraph['href']))
        if paragraph.string == "Size":
            found = True
        if paragraph.string == "Giaorugu" \
                or paragraph.string == "Seething Bazelgeuse" \
                or paragraph.string == "Zorah Magdaros":
            found = False

def getMonsterData(link, monster_data):
    url = "https://monsterhunter.fandom.com" + link

    response = requests.get(url)

    if response.status_code == 200:
        print("Success!")
        soup = BeautifulSoup(response.content, 'html.parser')
    else:
        print("Failure!")
        return None

    monster_data['mainPic'] = get_monster_profile_picture(soup)
    monster_data['description'] = get_monster_description(soup)
    monster_data['weakness'] = get_monster_weakness(soup)
    monster_data['icon'] = get_monster_icon(soup)



def get_monster_description(soup):
    # Finds the first <p> tag after the first <h2> tag with the text 'Physiology'
    physiology_h2 = soup.find('h2', string='Physiology')
    physiology_span = soup.find('span', string='Physiology')
    appearance_h2 = soup.find('h2', string='Appearance')
    appearance_span = soup.find('span', string='Appearance')
    physiology_span_parent = None
    appearance_span_parent = None
    if physiology_span:
        physiology_span_parent = physiology_span.parent
    elif appearance_span:
        appearance_span_parent = appearance_span.parent
    summary = physiology_h2.find_next('p') if physiology_h2 else \
        appearance_h2.find_next('p') if appearance_h2 else \
        appearance_span.find_next('p') if appearance_span_parent else \
        physiology_span.find_next('p') if physiology_span_parent else None
    return summary.text if summary else ''


def get_monster_profile_picture(soup):
    # Finds the first <img> tag with the class 'pi-image-thumbnail' and sends back the link for the image
    imgs = soup.find(class_='pi-image-thumbnail')
    img_url = imgs['src']
    return img_url


def get_monster_weakness(soup):
    weaknesses_h3 = soup.find('h3', string='Weakest to')
    weaknesses_div = weaknesses_h3.find_next('div')
    weaknesses_small = weaknesses_div.find_all('small')
    if not weaknesses_small:
        return ['None']
    weakness_list = []
    for smalls in weaknesses_small:
        weaknesses = smalls.find_all('a')
        if len(weaknesses) > 1:
            weakness_list.append(weaknesses[1].text)
    print(weakness_list)
    return weakness_list


def get_monster_icon(soup):
    icon_img = soup.find('img', alt=lambda alt: alt and 'Icon' in alt)
    return icon_img['src'] if icon_img else None

def main():
    all_monster_links = ["https://monsterhunter.fandom.com/wiki/Category:Monsters",
                         "https://monsterhunter.fandom.com/wiki/Category:Monsters?from=Giaprey",
                         "https://monsterhunter.fandom.com/wiki/Category:Monsters?from=Seltas"]
    monster_list_links = []
    for link in all_monster_links:
        createData(link, monster_list_links)
    print(monster_list_links)

    for name, link in monster_list_links:
        print(name)
        monster_data = {}
        monster_data['name'] = name
        getMonsterData(link, monster_data)
        print(monster_data)



if __name__ == "__main__":
    main()
