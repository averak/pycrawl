import re
import unittest
from pycrawl import PyCrawl


class TestAPI(unittest.TestCase):
    def setUp(self):
        self.sample_url: str = "http://example.com/"
        self.sample_html: str
        with open("tests/sample.html", "r") as f:
            self.sample_html = f.read()

    def tearDown(self):
        pass

    def test_create_with_url(self):
        spider = PyCrawl(self.sample_url)
        self.assertEqual(self.sample_url, spider.url)

    def test_create_with_node(self):
        import lxml.html
        node = lxml.html.fromstring(self.sample_html)
        spider = PyCrawl(node=node)
        self.assertEqual(
            re.sub(r"[\n ]", "", self.sample_html),
            re.sub(r"[\n ]", "", spider.outer_text())
        )

    def test_create_with_html(self):
        spider = PyCrawl(html=self.sample_html)
        self.assertEqual(self.sample_html, spider.html)

    def test_create_error(self):
        with self.assertRaises(Exception):
            PyCrawl()

    def test_send_params(self):
        spider = PyCrawl(html=self.sample_html)
        spider.send(id="test id", value="hello")
        spider.send(id="test id", check=True)
        spider.send(id="test id", file_name="tests/sample.html")
        self.assertEqual(3, len(spider.params))

    def test_find_node_with_css(self):
        spider = PyCrawl(html=self.sample_html)
        self.assertEqual(6, len(spider.css("p")))

    def test_find_node_with_xpath(self):
        spider = PyCrawl(html=self.sample_html)
        self.assertEqual(4, len(spider.xpath("/html/body/p")))

    def test_find_node_with_attr(self):
        spider = PyCrawl(html=self.sample_html)
        self.assertEqual("sample text 3", spider.css("#test_id").inner_text())
        self.assertEqual("sample text 4", spider.css(".test_class").inner_text())

    def test_find_deep_node(self):
        spider = PyCrawl(html=self.sample_html)
        self.assertEqual("sample text 5", spider.css("div").css("p").inner_text())
        self.assertEqual("sample text 5", spider.css("div").css("p")[0].inner_text())
        self.assertEqual("sample text 6", spider.css("div").css("p")[1].inner_text())

    def test_find_node_attr(self):
        spider = PyCrawl(html=self.sample_html)
        self.assertEqual(self.sample_url, spider.css("a").attr("href"))

    def test_extract_table(self):
        spider = PyCrawl(html=self.sample_html)
        self.assertEqual("Alice", spider.table["name"])
        self.assertEqual("20", spider.table["age"])


