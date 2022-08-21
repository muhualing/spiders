import pprint

from googleapiclient.discovery import build


def main():
    # Build a service object for interacting with the API. Visit
    # the Google APIs Console <http://code.google.com/apis/console>
    # to get an API key for your own application.
    service = build(
        "customsearch", "v1", developerKey="AIzaSyA2HvtTC23IsDg1FppxnSyO4GxiHXve0jA"
    )

    res = (
        service.cse()
        .list(
            q="合同 filetype:doc OR filetype:docx",
            cx="017576662512468239146:omuauf_lfve",
        )
        .execute()
    )
    pprint.pprint(res)


if __name__ == "__main__":
    main()