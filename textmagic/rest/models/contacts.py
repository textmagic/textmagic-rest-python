from . import Model, CollectionModel


class Contact(Model):
    """
    A Contact object model

    .. attribute:: id

    .. attribute:: phone

    .. attribute:: email

    .. attribute:: firstName

    .. attribute:: lastName

    .. attribute:: companyName

    .. attribute:: country

        Dictionary like this:
        ::
            {
                "id": "US",
                "name": "United States"
            }

    .. attribute:: customFields

        List of dictionaries, each looks like this:
        ::
            {
                "value": "30",
                "id": "1044",
                "name": "Age",
                "createdAt": "2015-04-27T09:29:46+0000"
            }
    """


class Contacts(CollectionModel):
    name = "contacts"
    instance = Contact

    def list(self, search=False, **kwargs):
        """
        Returns a list of :class:`Contact` objects and a pager dict.

        :Example:

        contacts, pager = client.contacts.list()

        :param bool search:   If True then search contacts using `query`, `ids` and/or `group_id`. Default=False
        :param int  page:     Fetch specified results page. Default=1
        :param int  limit:    How many results on page. Default=10
        :param int  shared:   Should shared contacts to be included. Default=0
        :param str  ids:      Find contact by ID(s). Using with `search`=True.
        :param int  listId:   Find contact by List ID. Using with `search`=True.
        :param str  query:    Find contact by specified search query. Using with `search`=True.
        """
        kwargs["search"] = search
        return self.get_instances(kwargs)

    def create(self, **kwargs):
        """
        Create a new contact.
        Returns :class:`Contact` object contains id and link to Contact.

        :Example:

        c = client.contacts.create(firstName="John", lastName="Doe", phone="19025555555", lists="1901901")

        :param str firstName:
        :param str lastName:
        :param str phone:       Contact's phone number. Required.
        :param str email:
        :param str companyName:
        :param str country:     2-letter ISO country code.
        :param str lists:       String of Lists separated by commas to assign contact. Required.
        """
        return self.create_instance(kwargs)

    def update(self, uid, **kwargs):
        """
        Updates the existing Contact for the given unique id.
        Returns :class:`Contact` object contains id and link to Contact.

        :Example:

        client.contacts.update(uid=7981278, firstName="John", lastName="Doe", phone="19025555555", lists="1901901")

        :param int uid:         The unique id of the Contact to update. Required.
        :param str firstName:
        :param str lastName:
        :param str phone:       Contact's phone number. Required.
        :param str email:
        :param str companyName:
        :param str lists:       String of Lists separated by commas to assign contact. Required.
        """
        return self.update_instance(uid, kwargs)

    def delete(self, uid):
        """
        Delete the specified Contact from TextMagic.
        Returns True if success.

        :Example:

        client.contacts.delete(1901010)

        :param int uid: The unique id of the Contact to delete.
        """
        return self.delete_instance(uid)

    def lists(self, uid=0, **kwargs):
        """
        Returns a list of :class:`List` objects (lists which Contact belongs to) and a pager dict.

        :Example:

        lists, pager = client.contacts.lists(uid=1901010)

        :param int uid:   The unique id of the Contact to update. Required.
        :param int page:  Fetch specified results page. Default=1
        :param int limit: How many results on page. Default=10
        """
        lists = Lists(self.base_uri, self.auth)
        return self.get_subresource_instances(uid, instance=lists,
                                              resource="lists", params=kwargs)


class List(Model):
    """
    A List object model

    .. attribute:: id

    .. attribute:: name

    .. attribute:: description

    .. attribute:: membersCount

    .. attribute:: shared
    """


class Lists(CollectionModel):
    name = "lists"
    instance = List

    def list(self, search=False, **kwargs):
        """
        Returns a list of :class:`List` objects and a pager dict.

        :Example:

        lists, pager = client.lists.list()

        :param bool search: If True then search lists using `ids` and/or `query`. Default=False
        :param int  page:   Fetch specified results page. Default=1
        :param int  limit:  How many results on page. Default=10
        :param str  ids:    Find lists by ID(s). Using with `search`=True.
        :param str  query:  Find lists by specified search query. Using with `search`=True.
        """
        kwargs["search"] = search
        return self.get_instances(kwargs)

    def create(self, **kwargs):
        """
        Create a new list.
        Returns :class:`List` object contains id and link to List.

        :Example:

        list = client.lists.create(name="My List")

        :param str name:        List name. Required.
        :param str description: List description.
        :param int shared:      Should this list be shared with sub-accounts. Can be 1 or 0. Default=0.
        """
        return self.create_instance(kwargs)

    def update(self, uid, **kwargs):
        """
        Updates the List for the given unique id.
        Returns :class:`List` object contains id and link to List.

        :Example:

        list = client.lists.update(uid=1901010, name="My List")

        :param int uid:         The unique id of the List to update. Required.
        :param str name:        List name. Required.
        :param str description: List description.
        :param int shared:      Should this list be shared with sub-accounts. Can be 1 or 0. Default=0.
        """
        return self.update_instance(uid, kwargs)

    def delete(self, uid):
        """
        Delete the specified List from TextMagic.
        Returns True if success.

        :Example:

        client.lists.delete(1901010)

        :param int uid: The unique id of the List to delete. Required.
        """
        return self.delete_instance(uid)

    def contacts(self, uid=0, **kwargs):
        """
        Fetch user contacts by given group id.
        A useful synonym for "contacts/search" command with provided `groupId` parameter.

        :Example:

        lists = client.lists.contacts(1901010)

        :param int uid:   The unique id of the List. Required.
        :param int page:  Fetch specified results page. Default=1
        :param int limit: How many results on page. Default=10
        """
        contacts = Contacts(self.base_uri, self.auth)
        return self.get_subresource_instances(uid, instance=contacts,
                                              resource="contacts", params=kwargs)

    def put_contacts(self, uid, **kwargs):
        """
        Assign contacts to the specified list.

        :Example:

        client.lists.put_contacts(uid=1901010, contacts="1723812,1239912")

        :param int uid:      The unique id of the List. Required.
        :param str contacts: Contact ID(s), separated by comma. Required.
        """
        return self.update_subresource_instance(uid,
                                                body=kwargs,
                                                subresource=None,
                                                slug="contacts")

    def delete_contacts(self, uid, **kwargs):
        """
        Unassign contacts from the specified list.
        If contacts assign only to the specified list, then delete permanently.
        Returns True if success.

        :Example:

        client.lists.delete_contacts(uid=1901010, contacts="1723812,1239912")

        :param int uid:      The unique id of the List. Required.
        :param str contacts: Contact ID(s), separated by comma. Required.
        """
        uri = "%s/%s/contacts" % (self.uri, uid)
        response, instance = self.request("DELETE", uri, data=kwargs)
        return response.status == 204