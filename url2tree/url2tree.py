# -*- coding: utf-8 -*-

"""Main module."""
import re


class UrlTreeNode(object):
    def __init__(self, name, isTerminal=False):
        self.children = []
        self.value = 0
        self.name = name
        self.isTerminal = isTerminal

    def __eq__(self, other):
        """UrlTreeNode is same when there name is same"""
        if isinstance(other, UrlTreeNode):
            return self.name == other.name
        return False

    def getChild(self, name):
        """Return child node by name.

        If not exist, make new child node with name and return it.

        Parameters
        ----------
        name : str
            Name of child node
        """
        for child in self.children:
            if name == child.name:
                return child
        new_child = UrlTreeNode(name)
        self.children.append(new_child)
        return new_child

    def getTerminal(self):
        """Return terminal node with value name in "END".

        It represents url ends with parent url.

        Parameters
        ----------
        value : Number
            value for node.
        """
        TERMINAL_NAME = "END"
        terminal_node = [child for child in self.children if child.isTerminal]
        if terminal_node:
            return terminal_node[0]

        terminal_child = UrlTreeNode(TERMINAL_NAME, isTerminal=True)
        self.children.append(terminal_child)

        return terminal_child

    def addTerminalValue(self, value):
        terminal_node = self.getTerminal()
        terminal_node.value += value

    def _printAll(self, depth, stop,
                  value_filter=None, prefix='', isLast=False):
        """Recursive function for print result of Node with all its child nodes.

        Parameters
        ----------
        depth : int
            Current depth of child node.
        stop : int
            Depth of nodes want to stop print
        value_filter : Number, optional
            UrlTreeNode with value greater than value_filter could be printed,
            by default None
        prefix : str, optional
            Prefix for print single UrlTreeNode, by default ''
        isLast : bool, optional
            Represent whether it is last node to print, by default False
        """
        print_list = []

        name = prefix + "ㄴ" + self.name
        print_list.append(f"{name:50} {self.value}")
        if stop == depth:
            return print_list

        if isLast:
            prefix += '  '
        else:
            prefix += '| '
        depth += 1

        self.children.sort(key=lambda x: -x.value)
        child_nodes = self.children
        if value_filter is not None:
            child_nodes = list(
                filter(lambda x: x.value > value_filter, child_nodes))
        for child in child_nodes[:-1]:
            print_list.extend(child._printAll(
                depth, stop, value_filter, prefix))
        if len(child_nodes) != 0:
            print_list.extend(
                child_nodes[-1]._printAll(
                    depth, stop, value_filter, prefix, True))
        return print_list

    def print(self, stop=-1, value_filter=None):
        """Print UrlTree Tree with root as this.

        Parameters
        ----------
        stop : int, optional
            Depth of nodes want to stop print, by default -1
        value_filter : Number, optional
            UrlTreeNode with value greater than value_filter could be printed,
            by default None
        """
        result = self._printAll(
            depth=0, stop=stop, value_filter=value_filter, isLast=True)
        for line in result:
            print(line)


class UrlTree(object):
    def __init__(self):
        self.root = UrlTreeNode("ROOT")

    def addNode(self, url, value):
        """Add node to the tree."""
        domain_regex = re.compile(
            r'^([\w]+://)?[\w\-\.]+(:[0-9]+)?').match(url)
        domain = ''
        if domain_regex is not None:
            domain = domain_regex.group()
        url = url.replace(domain, '')
        url_tokens = [domain] + url.split("/")
        url_tokens = filter(lambda x: x != '', url_tokens)
        node = self.root
        node.value += value
        for token in url_tokens:
            node = node.getChild(token)
            node.value += value
        node.addTerminalValue(value)

    def printTree(self, stop=-1, value_filter=None):
        """Print the tree result."""
        self.root.print(stop, value_filter)
