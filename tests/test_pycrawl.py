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
            self.sample_html.replace("\n", ""),
            spider.outer_text().replace("\n", ""),
        )

    def test_create_with_html(self):
        spider = PyCrawl(html=self.sample_html)
        self.assertEqual(self.sample_html, spider.html)

    def test_send_params(self):
        spider = PyCrawl(html=self.sample_url)
        spider.send(id="test id", value="hello")
        spider.send(id="test id", check=True)
        spider.send(id="test id", file_name="tests/sample.html")
        self.assertEqual(3, len(spider.params))
