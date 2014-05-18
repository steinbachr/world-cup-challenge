from bs4 import BeautifulSoup
from lxml import etree
import requests
import pdb


class XPathOps():
    def __init__(self, url=None, html=None, xpath='', **kwargs):
        self.url = url
        self.xpath = xpath
        self.css_class_root = kwargs.pop('css_class_root', None)
        if html:
            self.html = self._make_beautiful_soup(html)

    def _apply_xpath_to_el(self, xpath, el):
        """
        :param xpath: ``str`` the xpath to apply to el
        :param el: ``lxml`` element to apply xpath to
        :return: the result of ``xpath`` applied to ``el``
        """
        compiled_x = etree.XPath(xpath)
        return compiled_x(el)

    def _make_beautiful_soup(self, html):
        """
        :param html: the html to make beautiful soup from
        :return: ``BeautifulSoup`` instance
        """
        soup = BeautifulSoup(html, "lxml")
        return soup.find(class_=self.css_class_root)

    def _get_xpath_target(self):
        """
        :return: result of applying ``xpath`` to the content of self.url
        """
        if not self.html:
            resp = requests.get(self.url)
            self.html = self._make_beautiful_soup(resp.content)

        root = etree.fromstring(self.html.prettify())
        return self._apply_xpath_to_el(self.xpath, root)

    def get_val_at_xpath(self):
        target_list = self._get_xpath_target()
        if target_list:
            target = target_list[0]
            return self.get_val_from_node(target)
        else:
            return None

    def get_nodes_at_xpath(self, from_node=None, xpath=None):
        """
        :param from_node: ``lxml`` node if given. If not given, use self.html
        :param xpath: if given, use this xpath rather then self.xpath to find the node
        :return: ``list`` of lxml nodes at the specified xpath
        """
        pdb.set_trace()
        root = from_node if from_node else etree.fromstring(self.html.prettify())
        nodes = list(self._apply_xpath_to_el(xpath, root))
        return nodes

    def get_node_at_xpath(self, from_node=None, xpath=None):
        """
        :param from_node: ``lxml`` node if given. If not given, use self.html
        :param xpath: if given, use this xpath rather then self.xpath to find the node
        :return: ``lxml`` node at the specified xpath if given, else using self.xpath
        """
        root = from_node if from_node else etree.fromstring(self.html.prettify())
        return self._apply_xpath_to_el(xpath, root)

    def get_val_from_node(self, node):
        """
        :param node: ``lxml`` node
        :return: ``str`` the text in the passed node
        """
        return BeautifulSoup(etree.tostring(node)).get_text(strip=True)

    def change_xpath(self, new_xpath):
        """
        :param new_xpath: ``str`` new xpath to use for xpath operations
        :return: self for chaining purposes
        """
        self.xpath = new_xpath
        return self

    @classmethod
    def classlist_contains(cls, css_class):
        """
        :param css_class: ``str`` the css class to use in the xpath expression
        :return: ``str`` xpath for selecting elements containing css_class as a css class
        """
        return "div[contains(concat(' ',normalize-space(@class),' '),' {css} '".format(css=css_class)
