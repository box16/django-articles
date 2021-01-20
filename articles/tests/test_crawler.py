import unittest
import re
from articles.extensions.webcraw import Crawler


class TestWebcraw(unittest.TestCase):
    def setUp(self):
        self.crawler = Crawler()
        self.website = {
            "name": "PaleolithicMan",
            "domain": "https://yuchrszk.blogspot.com/",
            "title_tag": "[class='post-title single-title emfont']",
            "body_tag": "[class='post-single-body post-body']",
            "link_collector": re.compile("^(?=https://yuchrszk.blogspot.com/..../.+?)(?!.*archive)(?!.*label).*$"),
            "link_creater": lambda domestic_url: domestic_url,
        }

    def test_get_page_normal_url(self):
        bs_object = self.crawler.get_bs_object(self.website["domain"])
        self.assertIsNotNone(bs_object)

    def test_get_page_abnormal_url(self):
        bs_object = self.crawler.get_bs_object("")
        self.assertIsNone(bs_object)

    def test_collect_urls_normal_url(self):
        bs_object = self.crawler.get_bs_object(self.website["domain"])
        urls = self.crawler._collect_urls(bs_object,
                                          self.website["link_collector"])
        self.assertGreater(len(urls), 0)

    def test_collect_urls_abnormal_url(self):
        bs_object = self.crawler.get_bs_object("")
        urls = self.crawler._collect_urls(bs_object,
                                          self.website["link_collector"])
        self.assertEqual(len(urls), 0)

    def test_extract_element_normal_url(self):
        bs_object = self.crawler.get_bs_object(
            "https://yuchrszk.blogspot.com/2020/12/20208.html")
        element = self.crawler.extract_element(bs_object,
                                               self.website["title_tag"],
                                               self.website["body_tag"])
        self.assertIsNotNone(element)

    def test_extract_element_abnormal_url(self):
        bs_object = self.crawler.get_bs_object("")
        element = self.crawler.extract_element(bs_object,
                                               self.website["title_tag"],
                                               self.website["body_tag"])
        self.assertIsNone(element)

    def test_extract_element_abnormal_title_tag(self):
        bs_object = self.crawler.get_bs_object(
            "https://yuchrszk.blogspot.com/2020/12/20208.html")
        element = self.crawler.extract_element(bs_object,
                                               "aaaa",
                                               self.website["body_tag"])
        self.assertIsNone(element)

    def test_extract_element_abnormal_body_tag(self):
        bs_object = self.crawler.get_bs_object(
            "https://yuchrszk.blogspot.com/2020/12/20208.html")
        element = self.crawler.extract_element(bs_object,
                                               self.website["title_tag"],
                                               "aaa")
        self.assertIsNone(element)

    def test_format_urls_slash(self):
        urls = ["https://example/"]
        answer_urls = ["https://example"]

        result_urls = self.crawler._format_urls(urls)
        self.assertEqual(result_urls, answer_urls)

    def test_format_urls_duplicate(self):
        urls = ["https://example", "https://example"]
        answer_urls = ["https://example"]

        result_urls = self.crawler._format_urls(urls)
        self.assertEqual(result_urls, answer_urls)

    def test_format_urls_slash_duplicate(self):
        urls = ["https://example/", "https://example/"]
        answer_urls = ["https://example"]

        result_urls = self.crawler._format_urls(urls)
        self.assertEqual(result_urls, answer_urls)

    def test_crawl_normal_url(self):
        urls = self.crawler.crawl_urls(self.website["domain"],
                                       self.website["link_collector"],
                                       times=2)
        self.assertGreater(len(urls), 0)

    def test_crawl_abnormal_url(self):
        urls = self.crawler.crawl_urls("",
                                       self.website["link_collector"],
                                       times=2)
        self.assertEqual(len(urls), 0)

    def test_crawl_abnormal_times(self):
        urls = self.crawler.crawl_urls(self.website["domain"],
                                       self.website["link_collector"],
                                       times=-2)
        self.assertGreater(len(urls), 0)

        urls = self.crawler.crawl_urls(self.website["domain"],
                                       self.website["link_collector"],
                                       times=10000000)
        self.assertGreater(len(urls), 0)
