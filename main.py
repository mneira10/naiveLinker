from hashlib import new
import re
import argparse
from bs4 import BeautifulSoup


def autolink_file(file_path):

    parsed_html = loadHTML(args.file_path)

    section_bodies = parsed_html.find_all("div", {"class": "section_body"})

    for section_body in section_bodies:

        for text in section_body.findAll(text=True):
            if not str.isspace(text):

                matches_iter = re.finditer(r'Section [0-9]+(\.[0-9]+)*', text)
                matches = [match for match in matches_iter]

                if len(matches) > 0:
                    text_parent = text.parent


                    print('#'*20)
                    print('NUM MATCHES', len(matches) )
                    print('PREV', text_parent)
                    last_match_end = 0 
                    raw_text = text.string

                    previous_link = None
                    for match in matches:
                        print('the match:', match)
                        match_start, match_end = match.span()
                        match_content = match.group()

                        section_number = match_content.split(' ')[1]

                        previous_text_tag = parsed_html.new_string(raw_text[last_match_end:match_start])

                        new_link = parsed_html.new_tag('a')
                        new_link.attrs['href'] = "#{}".format(section_number)
                        new_link.string = match_content

                        if last_match_end == 0:
                            text.replace_with(previous_text_tag)

                        else:
                            previous_link.insert_after(previous_text_tag)

                        previous_text_tag.insert_after(new_link)
                        previous_link = new_link

                        last_match_end = match_end
                    print('AFTER', text_parent)
                
                    # print(text)
                    # print('-----')
                # else:
                #     print('$'*10, 'No subs found')
# 
    # print(parsed_html.prettify())

def loadHTML(file_path):
    print('Parsing', file_path)

    with open(file_path) as f:
        file_content = f.read()
        return BeautifulSoup(file_content, 'html.parser')



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Naive autolinker.')
    parser.add_argument('file_path', metavar='file_path', type=str,
                        help='Path to the html file to autolink')
    
    args = parser.parse_args()

    autolink_file(args.file_path)
