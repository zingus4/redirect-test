import os
import re
import argparse
import requests as r
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
from tqdm import tqdm


load_dotenv()
# url песочницы
BASE_URL = os.getenv("BASE_URL")
# Логин пароль для входа на песочницу
HTTP_LOGIN = os.getenv("HTTP_LOGIN")
HTTP_PASSWORD = os.getenv("HTTP_PASSWORD")
basic = HTTPBasicAuth(HTTP_LOGIN, HTTP_PASSWORD)


class CustomSession(r.Session):
    def rebuild_auth(self, prepared_request, response):
        return


s = CustomSession()
s.auth = basic


def try_open_file(file_name, option):
    try:
        with open(file_name, option) as file:
            pass
    except Exception:
        print(f'Something gone wrong with {file_name} file!')
        exit(1)
    return file


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "-input_file",
                        help="Название входного txt файла",
                        default="redirect.txt")
    parser.add_argument("-o", "-output_file",
                        help="Название выходного txt файла",
                        default="output.txt")
    return parser.parse_args()


def check_input_file(redirects):
    for redirect in redirects:
        if re.fullmatch(r'Redirect 301 .+[ \t].+[\n]$', redirect) is None:
            print("The input file contains an invalid format.",
                  "You can look at the input file format in file README.txt",
                  sep='\n')
            exit(1)


def get_info_from_redirect(redirect):
    _, status_code, from_url, to_url = redirect.split()
    response = s.get(f"{BASE_URL}{from_url}")
    first_request = response.history[0]
    is_redirect = first_request.status_code == int(status_code) and first_request.url.endswith(from_url)
    result_url = response.url.replace(BASE_URL, "")
    # Происходит ли редирект; Финальный статус;
    # Совпадает ли конечная ссылка с задуманной; Начальный url;
    # Куда должно перейти url; Где в итоге оказались url
    answer = f"{is_redirect}, {response.status_code}, {result_url==to_url}, {from_url}, {to_url}, {result_url}\n"
    return answer


def main(redirect_file, output_file):
    file_with_redirects = try_open_file(redirect_file, 'r')
    out_file = try_open_file(output_file, 'w+')

    redirects = file_with_redirects.readlines()
    check_input_file(redirects)

    for redirect in tqdm(redirects):
        out_file.write(get_info_from_redirect(redirect))


if __name__ == "__main__":
    args = get_arguments()
    main(args.i, args.o)
