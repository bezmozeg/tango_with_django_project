from django.test import TestCase
from django.test import TestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from django.core.urlresolvers import reverse
import os
import socket

# Create your tests here.
class navigationTests(StaticLiveServerTestCase):
    def test_navigate_from_index_to_about(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('headless')
        self.browser = webdriver.Chrome(chrome_options = chrome_options)
        self.browser.implicitly_wait(3)
        # Go to rango main page
        url = self.live_server_url
        url = url.replace('localhost', '127.0.0.1')
        print(url)
        print("hello")
        self.browser.get(url + reverse('index'))

        # Search for a link to About page
        about_link = self.browser.find_element_by_partial_link_text("About")
        about_link.click()

        # Check if it goes back to the home page
        self.assertIn(url + reverse('about'), self.browser.current_url)

    def test_navigate_from_about_to_index(self):
        # Go to rango main page
        self.client.get(reverse('index'))
        url = self.live_server_url
        url = url.replace('localhost', '127.0.0.1')
        self.browser.get(url + reverse('about'))

        # Check if there is a link back to the home page
        # link_to_home_page = self.browser.find_element_by_tag_name('a')
        link_to_home_page = self.browser.find_element_by_link_text('Index')
        link_to_home_page.click()

        # Check if it goes back to the home page
        self.assertEqual(url + reverse('index'), self.browser.current_url)
