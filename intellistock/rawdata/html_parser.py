#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging
from lxml import etree


logger = logging.getLogger(__name__)


class HtmlParser(object):
    def __init__(self):
        pass

    @classmethod
    def dumpElement(cls,node):
        logger.debug("dumpping node type :{}".format(type(node)))
        if not isinstance(node,etree._Element):
            logger.error("get type {} expected type {}".format(type(node),type(etree._Element)))
            return

        for el in node.iter():
            logger.debug("%s - %s",el.tag,el.text)


    @classmethod
    def dumpElements(cls,nodes):
        for node in nodes:
            cls.dumpElement(node)