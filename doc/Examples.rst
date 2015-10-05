Examples
========

.. contents::

Getting Started
---------------

The first step in using the TextMagic Python Client API
is to instantiate a :py:class:`~textmagic.rest.client.TextmagicRestClient` object:

.. code-block:: python

   from textmagic.rest import TextmagicRestClient
   client = TextmagicRestClient("username", "API key")

Now you can use ``client`` to make API calls.
For example, to send a message:

.. code-block:: python

   client.messages.create(phones="comma-separated list of phone numbers", text="message text")

As you can see, working with messages deals with ``client.messages``.
In general, the various resources are accessed via the pattern ``client.<resource-name>``.
For example, operations on catacts go through ``client.contacts``
and operations on lists go through ``client.lists``.

The following table links the resources provided by the Rest API
and their correspondence in the Python API.

==================================================================== ======================
Rest Resource                                                        Python API
==================================================================== ======================
`Messages <https://www.textmagic.com/docs/api/send-sms/>`_           :py:class:`client.messages <textmagic.rest.models.messages.Messages>`
`Contacts <https://www.textmagic.com/docs/api/contacts/>`_           :py:class:`client.contacts <textmagic.rest.models.contacts.Contacts>`
`Custom Fields <https://www.textmagic.com/docs/api/custom-fields/>`_ :py:class:`client.custom_fields <textmagic.rest.models.custom_fields.CustomFields>`
Unsubscribers                                                        :py:class:`client.unsubscribers <textmagic.rest.models.unsubscribers.Unsubscribers>`
`Lists <https://www.textmagic.com/docs/api/lists/>`_                 :py:class:`client.lists <textmagic.rest.models.contacts.Lists>`
Replies                                                              :py:class:`client.replies <textmagic.rest.models.replies.Replies>`
`Templates <https://www.textmagic.com/docs/api/sms-templates/>`_     :py:class:`client.templates <textmagic.rest.models.templates.Templates>`
Bulks                                                                :py:class:`client.bulks <textmagic.rest.models.bulks.Bulks>`
`Chats <https://www.textmagic.com/docs/api/sms-chats/>`_             :py:class:`client.chats <textmagic.rest.models.chats.Chats>`
`Schedules <https://www.textmagic.com/docs/api/schedule-sms/>`_      :py:class:`client.schedules <textmagic.rest.models.schedules.Schedules>`
`Sessions <https://www.textmagic.com/docs/api/sms-sessions/>`_       :py:class:`client.sessions <textmagic.rest.models.sessions.Sessions>`
`Account <https://www.textmagic.com/docs/api/account/>`_             :py:class:`client.user <textmagic.rest.models.user.Users>`
`Numbers <https://www.textmagic.com/docs/api/numbers/>`_             :py:class:`client.numbers <textmagic.rest.models.numbers.Numbers>`
`Sender IDs <https://www.textmagic.com/docs/api/sender-ids/>`_       :py:class:`client.senderids <textmagic.rest.models.numbers.Senderids>`
Sources                                                              :py:class:`client.sources <textmagic.rest.models.numbers.Sources>`
`Sub-Accounts <https://www.textmagic.com/docs/api/sub-accounts/>`_   :py:class:`client.subaccounts <textmagic.rest.models.user.Subaccounts>`
`Invoices <https://www.textmagic.com/docs/api/invoices/>`_           :py:class:`client.invoices <textmagic.rest.models.user.Invoices>`
Tokens                                                               :py:class:`client.tokens <textmagic.rest.models.tokens.Tokens>`
`Statistics <https://www.textmagic.com/docs/api/statistics/>`_       :py:class:`client.stats_messaging <textmagic.rest.models.stats.MessagingStats>`  and  :py:class:`client.stats_spending <textmagic.rest.models.stats.SpendingStats>`
Utils                                                                :py:class:`client.util <textmagic.rest.models.utils.Utils>`
==================================================================== ======================

Working with Contacts
---------------------

Contacts are accessed via the ``client.contacts`` attribute.

To obtain a list of contacts, you can use

.. code-block:: python

   contacts, pager = self.client.contacts.list()

``contacts`` is a list of :py:class:`~textmagic.rest.models.contacts.Contact` objects.
Note that list information is paged by the Rest API.
The example above will fetch the first 10 contacts in your account.
You can change this default behaviour by providing appropriate parameters
to the :py:meth:`~textmagic.rest.models.contacts.Contacts.list` method.
``pager`` is an object that describes the current page.

You can create a new contact with

.. code-block:: python

   contact = client.contacts.create(firstName="First Name"
                                    lastName="Last Name"
                                    phone="Phone Number")


Working with Lists
------------------

``client.lists`` provides access to your contact lists.
You can obtain a list of these as follows:

.. code-block:: python

   lists, pager = self.client.lists.list()

Once again, only 10 lists will be returned by default,
but you can override this behaviour
with the :py:meth:`appropriate parameters <textmagic.rest.models.contacts.Lists.list>`.

Working with Messages
---------------------

``client.messages`` allows you to view and send messages.

To send a message to a particular phone number:

.. code-block:: python

   message = client.messages.create(text="Hi!",
                                    phones="phone number")

To send a message to multiple numbers,
you can provide ``phones`` as a comma-separated string.

Likewise, you can send a message to one or more lists
by providing a ``lists`` parameter:

.. code-block:: python

   message = client.messages.create(text="Hello, list!"
                                    lists=my_list.id)

For a complete list of accepted parameters and their meaning,
see the documentation for :py:meth:`~textmagic.rest.models.messages.Messages.create`.

More Examples and Unit Tests
----------------------------

The ``examples`` directory contains several unit tests
that also serve as concrete examples of common usage patters.
You can run them using Python's ``unittest`` facilities:

.. code-block:: bash

   python -m unittest examples

The ``tests`` directory contains additional unittests,
using mocked versions of library objects.
