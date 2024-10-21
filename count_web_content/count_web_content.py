# coding: utf-8
"""webページのコンテンツをカウントするモジュール"""

import os
from pprint import pprint
from time import sleep
from typing import Tuple

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv


def count_pages(
    root_url: str,
    additional_url: list[str] = [],
    # exclude_url: list[str] = [],
    sleep_sec: int = 0.1,
    is_print_url: bool = False,
    output_url_file_name: str = "",
) -> Tuple[int, int, dict[str, int], list[str]]:
    not_completed = list()
    not_completed.append(root_url)

    completed_list = list()
    page_count = 0
    in_root_page_count = 0

    additional_url_count_dict = dict()
    for key in additional_url:
        additional_url_count_dict[key] = 0

    while len(not_completed) > 0:
        sleep(sleep_sec)
        current_url = not_completed.pop()
        response = requests.get(current_url, timeout=6.0)
        if response.status_code != 200:
            continue

        completed_list.append(current_url)
        page_count += 1
        if is_print_url:
            print("current: " + current_url)

        if not current_url.startswith(root_url):
            continue

        in_root_page_count += 1

        html = BeautifulSoup(response.text, "html.parser")
        a_tags = html.find_all("a", href=True)
        for a_tag in a_tags:
            a_url = a_tag["href"]
            if not a_url.startswith("http") or not a_url.startswith("https"):
                if a_url.startswith("/"):
                    a_url = root_url + a_url[1:]
                else:
                    slash_idx = current_url.rfind("/")
                    a_url = current_url[: slash_idx + 1] + a_url

                # 「..」が含まれているときの処理
                while a_url.find("..") != -1:
                    a_dot_dot_idx = a_url.find("..")
                    a_before_src_from_dot_idx = a_url.rfind("/", 0, a_dot_dot_idx)
                    a_url = (
                        a_url[:a_before_src_from_dot_idx] + a_url[a_dot_dot_idx + 2 :]
                    )

            if (a_url not in completed_list) and (a_url not in not_completed):
                not_completed.append(a_url)
                for key in additional_url:
                    if a_url.startswith(key):
                        additional_url_count_dict[key] += 1

        print("remain: " + str(len(not_completed)))

    if output_url_file_name != "":
        with open(output_url_file_name, "w", encoding="utf-8") as f:
            for url in completed_list:
                print(url, file=f)
    return page_count, in_root_page_count, additional_url_count_dict


if __name__ == "__main__":
    load_dotenv()
    # root_url = os.getenv("SEARCH_ROOT_URL")
    count, in_root_count, add_dict = count_pages(
        "https://mame77.com/",
        is_print_url=True,
        additional_url=["https://mame77.com/posts/"],
        output_url_file_name="output_url.txt",
    )
    print("Unique href url count : " + str(count))
    print("Unique href url count in root url : " + str(in_root_count))
    pprint(add_dict)
    with open("output.txt", "w", encoding="utf-8") as f:
        print("Unique href url count : " + str(count), file=f)
        print("Unique href url count in root url : " + str(in_root_count), file=f)
        pprint(add_dict, stream=f)
