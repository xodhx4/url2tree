#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `url2tree` package."""

import pytest


from url2tree import url2tree


@pytest.fixture
def randomUrlData():
    # TODO : Add faker for random url test
    from faker import Faker
    fake = Faker()
    domain = fake.url()
    url_logs = [(domain + fake.uri_path(), 1) for _ in range(100)]
    while True:
        domain2 = fake.url()
        if domain2 != domain:
            break
    url_logs += [(domain2 + fake.uri_path(), 1) for _ in range(100)]

    return (domain[:-1], domain2[:-1], url_logs)


def test_url2treeNode_eq():
    assert url2tree.UrlTreeNode("v1") == url2tree.UrlTreeNode("v1")
    assert url2tree.UrlTreeNode("v1") != url2tree.UrlTreeNode("v2")


def test_UrlTreeNode_getChild():
    node = url2tree.UrlTreeNode("v1")
    # check creation
    node2 = node.getChild("v2")
    assert node2.name == "v2"
    assert node2.value == 0
    # check finding
    node2.value += 10
    node3 = node.getChild("v2")
    assert node3.value == 10


def test_UrlTreeNode_getTerminal():
    node = url2tree.UrlTreeNode("v1")
    # check creation
    node2 = node.getTerminal()
    assert node2.name == "END"
    assert node2.value == 0
    # check finding
    node2.value += 10
    node3 = node.getTerminal()
    assert node3.value == 10


def test_addTerminalValue():
    node = url2tree.UrlTreeNode("v1")
    node.addTerminalValue(10)
    node2 = node.getTerminal()

    assert node2.name == "END"
    assert node2.value == 10


def test_UrlTree(randomUrlData):
    tree = url2tree.UrlTree()
    domain_a, domain_b, url_logs = randomUrlData
    for url, value in url_logs:
        tree.addNode(url, value)

    assert tree.root.value == 200
    domain_a_node = tree.root.getChild(domain_a)
    domain_b_node = tree.root.getChild(domain_b)

    assert domain_a_node.value == 100
    assert domain_b_node.value == 100


def test_UrlTree_printTree(randomUrlData):
    tree = url2tree.UrlTree()
    _, _, url_logs = randomUrlData
    for url, value in url_logs:
        tree.addNode(url, value)
    try:
        tree.printTree()
    except Exception as e:
        pytest.fail(str(e))
