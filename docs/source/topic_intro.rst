Introduction to Email
*********************

Email (Electronic Mail) is a store-and-forward method of transmitting digital messages across the Internet. Its
standards are defined by the Internet Engineering Task Force (IETF) in various `RFCs <https://www.rfc-editor.org/>`_ .

Key RFCs include:

- `RFC 5321 <https://datatracker.ietf.org/doc/html/rfc5321>`_ : Simple Mail Transfer Protocol (SMTP), governing
  message transfer between servers.

- `RFC 5322 <https://datatracker.ietf.org/doc/html/rfc5322>`_ : Internet Message Format, defining message headers and
  body syntax.

- `RFC 2045 <https://datatracker.ietf.org/doc/html/rfc2045>`_ to
  `RFC 2049 <https://datatracker.ietf.org/doc/html/rfc2049>`_ : MIME extensions for non-text content.

Email Message Format
====================

According to `RFC 5322 <https://datatracker.ietf.org/doc/html/rfc5322>`_, an Internet
email message consists of header fields followed by a blank line (i.e., two consecutive
CRLF), and then the message body.

Header fields follow the syntax::

    field-name ":" [ws* field-value] CRLF

where ``field-name`` is case-insensitive, and lines may be folded.

Mandatory Headers
-----------------

RFC 5322 specifies the following key originator and destination fields (Sections 3.6.2-3.6.3):

- ``From:`` **REQUIRED** - The mailbox(es) of the author(s) or person(s) responsible for
  the message. A comma-separated list of one or more mailboxes.

- ``Sender:`` (optional, if different from From) - The actual transmitter if not the author.

- ``Date:`` **REQUIRED by some implementations, SHOULD** - Date and time of message
  origination (per RFC 5322 Section 3.6.1).

- ``Message-ID:`` **SHOULD** - Unique identifier for the message.

- ``To:``, ``Cc:``, ``Bcc:`` - Recipient fields; at least one SHOULD be present with
  recipients.


MIME Content-Types
------------------

The format of the message body is determined by the ``Content-Type:`` header field,
introduced by `RFC 2045 <https://datatracker.ietf.org/doc/html/rfc2045>`_ (MIME Part 1).

This header specifies the media type and subtype (e.g., ``text/plain``, ``multipart/mixed``),
plus parameters like ``charset`` or ``boundary``.

The ``Content-Transfer-Encoding:`` header (``7bit``, ``quoted-printable``, ``base64``)
indicates how the body data is encoded for safe transport.

Single-part examples:

**Plain text:**

.. code-block:: 

   Content-Type: text/plain; charset=UTF-8
   
   Content-Transfer-Encoding: 7bit
   
   Hello, this is the message body!

**HTML:**

.. code-block:: 

   Content-Type: text/html; charset=UTF-8
   
   Content-Transfer-Encoding: 8bit
   
   <html><body><h1>Hello</h1></body></html>

Multipart messages (e.g., ``multipart/mixed``) use a boundary to delimit parts:

.. code-block:: 

   Content-Type: multipart/mixed; boundary="frontierABC"

   --frontierABC
   Content-Type: text/plain; charset=UTF-8

   This is the body text.

   --frontierABC
   Content-Type: application/pdf; name="doc.pdf"
   Content-Disposition: attachment; filename="doc.pdf"
   Content-Transfer-Encoding: base64

   JVBERi0xLjQKJcOkw7zDtsO8w7zDtsOkw...

   --frontierABC--