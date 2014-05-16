from bs4 import BeautifulSoup
from lxml import etree
import requests
import pdb


class XPathOps():
    def __init__(self, url, xpath='', **kwargs):
        self.url = url
        self.xpath = xpath
        self.css_class_root = kwargs.pop('css_class_root', None)

        self.html = None

    def _get_xpath_target(self):
        """
        :return: result of applying ``xpath`` to the content of self.url
        """
        if not self.html:
            resp = requests.get(self.url)
            soup = BeautifulSoup(resp.content, "lxml")
            self.html = soup.find(class_=self.css_class_root)

        root = etree.fromstring(self.html.prettify())
        xpath = etree.XPath(self.xpath)
        return xpath(root)

    def get_val_at_xpath(self):
        target_list = self._get_xpath_target()
        if target_list:
            target = target_list[0]
            return self.get_val_from_node(target)
        else:
            return None

    def get_nodes_at_xpath(self):
        """
        :return: ``list`` of lxml nodes at the specified xpath
        """
        nodes = list(self._get_xpath_target())
        return nodes

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
