import time

from requests import Session

from config import USERNAME

VSCO_URL = 'https://vsco.co'
VSCO_COOKIE_URL = 'https://vsco.co/content/Static/userinfo'


class VscoParser(object):
    def __init__(self, username):
        self.username = username
        self.session = Session()
        self.session.get(VSCO_COOKIE_URL + "?callback=jsonp_%s_0" % (str(round(time.time() * 1000))))

        # Get session cookie:
        self.session_cookie = self.session.cookies.get_dict()["vs"]
        # Get Session ID
        self.site_id = self.get_vsco_session_id()
        self.get_vsco_session_id()
        # Set Media URL
        self.media_url = self.media_url = VSCO_URL + "/ajxp/%s/2.0/medias?site_id=%s" % (
            self.session_cookie,
            self.site_id,
        )

    def get_vsco_session_id(self):
        """
        This function gathers a the 'id' field from the site, this is required to allow another requests gather
        all the 'medias' data for that site_id.

        Endpoint: https://vsco.co/ajxp/{vs_session_cookie}/2.0/sites?subdomain={account_username}
        :params: none
        :return: returns the site id for the user account specified
        """

        results = self.session.get(VSCO_URL + "/ajxp/%s/2.0/sites?subdomain=%s" % (self.session_cookie, self.username))

        # Get id from json data
        site_id = results.json()["sites"][0]["id"]

        return site_id

    def get_all_image_data(self):
        """
        Function to get all images from user account
        :return:
        """
        # Todo - Need to re-think the size and page count
        results = self.session.get(self.media_url, params={"size": 300}).json()["media"]
        posts = []

        for post in results:
            # print(post)
            posts.append(
                [
                    "https://%s" % post["responsive_url"],  # Grab the Image URL
                    str(post["upload_date"])[:-3],  # Grab the update date
                    post.get("tags", "null")  # Grab the tags from post, if none: null
                ]
            )

        # Test print
        print(len(posts))

        for post in posts:
            print(post)

        return posts

    def download_images(self, posts):
        """
        Function handles downloading images from the URL collected in the get_all_image_data() function
        :param posts - dictionary of posts
        :return:
        """

    # with open("%s.jpg" % str(post[1]), "wb") as file:
    #     file.write(requests.get())

    def get_image_by_tag(self, tag):
        """
        This function gathers all images with the matching tag provided

        :param tag: User defined
        :return:
        """


def main():
    parser = VscoParser(username=USERNAME)
    parser.get_all_image_data()


if __name__ == "__main__":
    main()
