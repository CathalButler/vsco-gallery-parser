import os
import time

import requests
from requests import Session

from config import USERNAME

VSCO_URL = 'https://vsco.co'
VSCO_COOKIE_URL = 'https://vsco.co/content/Static/userinfo'
VSCO_PHOTO_DIR = 'vsco_photos/'


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
        Function to get all images from user account and add it to the list the following fields:
        responsive_url: This is the URL where the post image is stored.
        upload_date: This is the date when the photo was uploaded to VSCO
        description: This is the description you set on the image, I am filtering this as I only want to save the
        hashtags used in the description.
        :return: filtered posts
        """

        # Todo - Need to re-think the size and page count
        results = self.session.get(self.media_url, params={"size": 300}).json()["media"]
        posts = []

        for post in results:
            posts.append(
                [
                    "https://%s" % post["responsive_url"],  # Grab the Image URL
                    str(post["upload_date"])[:-3],  # Grab the upload date
                    self.filter_tags(str(post["description"]))  # Grab the tags from post, if none: null
                ]
            )

        return posts

    def download_images(self, posts):
        """
        Function handles downloading images from the URL collected in the get_all_image_data() function.
        This function will also check if the image already exists in storage, if so it skips.
        The file name is made up of the desc_tags and upload_date
        :param posts - dictionary of posts
        :return: complete - Returns True when complete unless it fails
        """

        for post in posts:
            # Create file name from 'desc_tags_upload_date'
            filename = str(post[2]) + str(post[1])
            # Check is the file exists in storage already
            if "%s.jpg" % filename in os.listdir(VSCO_PHOTO_DIR):
                print(filename + " in storage. Skipping...")
                continue
            print("Downloading: " + filename)
            with open(VSCO_PHOTO_DIR + "%s.jpg" % filename, "wb") as file:
                file.write(requests.get(post[0], stream=True).content)

        return True

    def filter_tags(self, desc_tag):
        """
        Function is used to filter the description tags inside a post due to the possibility of there being None, one
        or many.The tags are going to make up the image name when downloaded.
        Ref: https://www.geeksforgeeks.org/python-extract-hashtags-from-text/

        :param desc_tag:
        :return: tag_string
        """
        tag_string = ""

        for word in desc_tag.split():
            # Check the first character of every word
            if word[0] == '#':
                tag_string += word[1:] + "_"

        return tag_string.lower()

    # def get_image_by_tag(self, tag):
    #     """
    #     This function gathers all images with the matching tag provided
    #
    #     :param tag: User defined
    #     :return:
    #     """


def main():
    parser = VscoParser(username=USERNAME)
    data = parser.get_all_image_data()
    # TODO - needed to add a progress updater
    parser.download_images(data)


if __name__ == "__main__":
    main()
