# encoding: utf-8
"""テストコード"""
from pprint import pprint

from dotenv import load_dotenv

import count_web_content.count_web_content as count_page

if __name__ == "__main__":
    load_dotenv()
    # root_url = os.getenv("SEARCH_ROOT_URL")
    count, in_root_count, add_dict = count_page.count_pages(
        "https://mame77.com/",
        is_print_working=True,
        additional_url=["https://mame77.com/posts/", "https://mame77.com/about"],
        output_url_file_name="output_url.txt",
    )
    print("Unique href url count : " + str(count))
    print("Unique href url count in root url : " + str(in_root_count))
    pprint(add_dict)
    with open("output.txt", "w", encoding="utf-8") as f:
        print("Unique href url count : " + str(count), file=f)
        print("Unique href url count in root url : " + str(in_root_count), file=f)
        pprint(add_dict, stream=f)
