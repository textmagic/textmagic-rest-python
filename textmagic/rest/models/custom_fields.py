from . import Model, CollectionModel, Contacts


class CustomField(Model):
    """
    A CustomField object model

    .. attribute:: id

    .. attribute:: name

    .. attribute:: createdAt
    """


class CustomFields(CollectionModel):
    name = "customfields"
    instance = CustomField

    def list(self, **kwargs):
        """
        Returns a list of :class:`CustomField` objects and a pager dict.

        :Example:

        custom_fields, pager = client.custom_fields.list()

        :param int page:  Fetch specified results page. Default=1
        :param int limit: How many results on page. Default=10
        """
        kwargs["search"] = False
        return self.get_instances(kwargs)

    def create(self, **kwargs):
        """
        Create a new custom field.
        Returns :class:`CustomField` object contains id and link to CustomField.

        :Example:

        custom_field = client.custom_fields.create(name="My Custom Field")

        :param str name: Name of custom field. Required.
        """
        return self.create_instance(kwargs)

    def update(self, uid, **kwargs):
        """
        Updates the CustomField for the given unique id.
        Returns :class:`CustomField` object contains id and link to CustomField.

        :Example:

        client.custom_fields.update(uid=1900901, name="New Name")

        :param int uid:  The unique id of the CustomField to update. Required.
        :param str name: Name of custom field. Required.
        """
        return self.update_instance(uid, kwargs)

    def update_value(self, uid, **kwargs):
        """
        Updates contact's custom field value.
        Returns :class:`Contact` object contains id and link to Contact.

        :Example:

        client.custom_fields.update_value(uid=1900901, contact_id=192012, value="abc")

        :param int uid:        The unique id of the CustomField to update a value. Required.
        :param int contactId:  The unique id of the Contact to update value. Required.
        :param str value:      Value of CustomField. Required.
        """
        contacts = Contacts(self.base_uri, self.auth)
        return self.update_subresource_instance(uid, body=kwargs,
                                                subresource=contacts,
                                                slug="update")

    def delete(self, uid):
        """
        Delete the specified CustomField from TextMagic.
        Returns True if success.

        :Example:

        client.custom_fields.delete(19019010)

        :param int uid: The unique id of the CustomField to delete.
        """
        return self.delete_instance(uid)