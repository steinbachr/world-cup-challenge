from bs4 import BeautifulSoup
from lxml import etree
import requests


class XPathOps():
    def __init__(self, url):
        self.url = url

    def get_val_at_xpath(self, xpath=''):
        """
        :param xpath: the xpath to use for selecting an iterable we can use to create the rows of data we'll eventually
        use for creating model instances. Note: when this xpath is applied to the element tree, it should return a list
        """
        resp = requests.get(self.url)
        soup = BeautifulSoup(resp.content, "lxml")
        html = soup

        root = etree.fromstring(html.prettify())
        xpath = etree.XPath(xpath)
        target_nodes = xpath(root)

        for row in target_nodes:
            creation_dict = static_fields
            for field_name, xpath_to_field in field_mapping.items():
                col_el = row.find(xpath_to_field)
                col_val = BeautifulSoup(etree.tostring(col_el)).get_text(strip=True)
                creation_dict[field_name] = col_val
                # if a parse function exists for this field, then apply the parse function with the column value
                if parse_functions and parse_functions.get(field_name):
                    creation_dict[field_name] = parse_functions[field_name](col_val)

        return True

    def get_nodes_at_xpath(self, xpath=''):
        """
        :param xpath: ``str`` the path to retrieve lxml nodes from

        :return: ``list`` of lxml nodes at the specified xpath
        """
        pass
