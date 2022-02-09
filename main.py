import argparse
from bs4 import BeautifulSoup


def autolink_file(file_path):

    parsed_html = loadHTML(args.file_path)
    

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
