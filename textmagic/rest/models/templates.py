from . import Model, CollectionModel


class Template(Model):
    """
    A Template object model (Message Template)

    .. attribute:: id

    .. attribute:: name

    .. attribute:: content

    .. attribute:: lastModified

    """


class Templates(CollectionModel):
    name = "templates"
    form = "template"
    instance = Template

    def list(self, search=False, **kwargs):
        """
        Returns a list of :class:`Template` objects and a pager dict.

        :Example:

        templates, pager = client.templates.list()

        :param bool search:   If True then search templates using `name` and/or `content`. Default=False
        :param int  page:     Fetch specified results page. Default=1
        :param int  limit:    How many results on page. Default=10
        :param int  name:     Find template by name. Using with `search`=True.
        :param int  content:  Find template by content. Using with `search`=True.
        """
        kwargs["search"] = search
        return self.get_instances(kwargs)

    def create(self, **kwargs):
        """
        Create a new template.
        Returns :class:`Template` object contains id and link to Template.

        :Example:

        template = client.templates.create(name="My Template", body="Template content.")

        :param str name:    Template name. Required.
        :param str content: Template text. May contain tags inside braces. Required.
        """
        return self.create_instance(kwargs)

    def update(self, uid, **kwargs):
        """
        Updates the Template for the given unique id.
        Returns :class:`Template` object contains id and link to Template.

        :Example:

        client.templates.update(uid=1902010, name="My Template", body="Template content.")

        :param int uid:     Unique id of the template to update. Required.
        :param str name:    Template name. Required.
        :param str content: Template text. May contain tags inside braces. Required.
        """
        return self.update_instance(uid, kwargs)

    def delete(self, uid):
        """
        Delete the specified Template from TextMagic.
        Returns True if success.

        :Example:

        client.templates.delete(1902010)

        :param int uid:  Unique id of the template to delete. Required.
        """
        return self.delete_instance(uid)