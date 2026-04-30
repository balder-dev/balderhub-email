Examples
********

Working with E-Mails
====================

If your scenario needs to work with e-mails, you can use the following feature and add it to your device:

.. code-block:: python

    import balderhub.email.lib.scenario_features

    class ScenarioExample(balder.Scenario):


        class MyDevice(balder.Device):
            mail = balderhub.email.lib.scenario_features.EmailReaderFeature()

        def test_example(self):
            new_mail = self.MyDevice.mail.wait_for_new_mail()
            assert new_mail.body_text == "Hello World"

This feature can be used to retrieve mails independent if your test setup captures the output of a outgoing SMTP server
(usually as a simulated test server) or is connected with a real POP3/IMAP server.

All BalderHub packages for these protocols provide an implementation of this feature:

+----------------------------------------------------------------------+-------------------------------------------------------------------------------------------------------------------------------+
| BalderHub Package                                                    | Description / Setup-Level Feature Implementations                                                                             |
+======================================================================+===============================================================================================================================+
| `balderhub-smtp <https://hub.balder.dev/projects/smtp>`_             | **BalderHub Package providing SMTP server for outgoing mails - specially for simulating smtp servers**                        |
|                                                                      |                                                                                                                               |
|                                                                      | * :class:`balderhub.smtp.lib.setup_features.LocalSmtpReader` for reading mails from a SMTP server within the assigned device  |
|                                                                      | * :class:`balderhub.smtp.lib.setup_features.ProxySmtpReader` for reading mails from a SMTP server of another connected device |
+----------------------------------------------------------------------+-------------------------------------------------------------------------------------------------------------------------------+

.. note::
    There are no balderhub packages for IMAP/POP3 yet. If you're interested in developing such a package, feel free to reach out.
