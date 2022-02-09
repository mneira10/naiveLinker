from hashlib import new
import re
import argparse
from bs4 import BeautifulSoup


def autolink_file(file_path):

    soup = loadHTML(args.file_path)

    find_and_insert_links(soup)

    print(soup.prettify())

def find_and_insert_links(soup):

    section_bodies = soup.find_all("div", {"class": "section_body"})

    for section_body in section_bodies:

        for text in section_body.findAll(text=True):

            find_and_insert_links_in_text(soup, text)
            

def find_and_insert_links_in_text(soup, text):
    
    # a lot of text found by beautiful soup is blank text
    if not str.isspace(text):

        # This is a first approach - it will only get sections of the type:
        # Section <section_number>
        # Next iteration of this would be to also get Sections of the type:
        # Sections 1209.2.1 through/and/or 1209.2.4
        matches_iter = re.finditer(r'Section [A-Z]?[0-9]+(\.[0-9]+)*', text)
        matches = list(matches_iter)

        if len(matches) > 0:

            last_match_end = 0 
            raw_text = text.string
            previous_link = None

            for match in matches:
                match_start, match_end = match.span()
                match_content = match.group()
                section_number = match_content.lstrip('Section ')

                text_before_link = soup.new_string(raw_text[last_match_end:match_start])

                new_link = soup.new_tag('a')
                new_link.attrs['href'] = "#{}".format(section_number)
                new_link.string = match_content

                if last_match_end == 0:
                    text.replace_with(text_before_link)
                else:
                    previous_link.insert_after(text_before_link)

                text_before_link.insert_after(new_link)
                previous_link = new_link

                last_match_end = match_end



            text_after_link = soup.new_string(raw_text[last_match_end:])

            previous_link.insert_after(text_after_link)


def loadHTML(file_path):

    with open(file_path) as f:
        file_content = f.read()
        return BeautifulSoup(file_content, 'html.parser')



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Naive autolinker.')
    parser.add_argument('file_path', metavar='file_path', type=str,
                        help='Path to the html file to autolink')
    
    args = parser.parse_args()

    autolink_file(args.file_path)
