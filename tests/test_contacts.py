# -*- coding: utf-8 -*-

import unittest
from mock import patch
from textmagic.rest.models import Contacts, Lists


class TestContact(unittest.TestCase):

    def setUp(self):
        self.resource = Contacts("uri", ("username", "token"))

    def test_list(self):
        with patch.object(self.resource, 'get_instances') as mock:
            self.resource.list(
                limit=10,
                page=2,
            )
            mock.assert_called_with({
                'limit': 10,
                'page': 2,
                'search': False,
            })

    def test_list_search(self):
        with patch.object(self.resource, 'get_instances') as mock:
            self.resource.list(
                limit=25,
                page=5,
                search=True,
                shared=1,
                ids="190,112,123",
                listId=123,
                query="abc"
            )
            mock.assert_called_with({
                "limit": 25,
                "page": 5,
                "search": True,
                "shared": 1,
                "ids": '190,112,123',
                "listId": 123,
                "query": 'abc'
            })

    def test_create(self):
        with patch.object(self.resource, 'create_instance') as mock:
            self.resource.create(
                phone="4479999999",
                firstName="John",
                lastName="Smith",
                email="john.smith@gmail.com",
                lists="123"
            )
            mock.assert_called_with({
                "phone": "4479999999",
                "firstName": "John",
                "lastName": "Smith",
                "email": "john.smith@gmail.com",
                "lists": "123"
            })

    def test_update(self):
        with patch.object(self.resource, 'update_instance') as mock:
            self.resource.update(
                uid=123,
                phone="4479999999",
                firstName="John",
                lastName="Smith",
                email="john.smith@gmail.com",
                lists="123"
            )
            mock.assert_called_with(123, {
                "phone": "4479999999",
                "firstName": "John",
                "lastName": "Smith",
                "email": "john.smith@gmail.com",
                "lists": "123"
            })

    def test_delete(self):
        with patch.object(self.resource, 'delete_instance') as mock:
            self.resource.delete(123)
            mock.assert_called_with(123)