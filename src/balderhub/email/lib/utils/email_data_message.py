from __future__ import annotations
import dataclasses
import datetime
from typing import Optional, Union

from .email_address import EmailAddress
from .email_header import EmailHeader

try:
    from typing import Self
except ImportError:
    from typing_extensions import Self


# Todo maybe move this message object into an own balderhub project?
@dataclasses.dataclass
class EmailDataMessage:
    """Represents the data part (headers and body) of an email message that can be sent or received.

    It bundles the mandatory ``from_address`` and ``date`` fields with optional additional headers,
    a reply-to address and a textual body. Convenience methods are provided to add the most common
    headers (``To``, ``Cc``, ``Bcc``, ``Subject`` etc.) without having to construct
    :class:`EmailHeader` objects manually.
    """
    from_address: EmailAddress
    date: datetime.datetime
    additional_headers: list[EmailHeader] = dataclasses.field(default_factory=list)

    replyto_address: Optional[EmailAddress] = None
    body_text: Optional[str] = None

    def compare(self, other: EmailDataMessage, ignore_added_headers: bool = False) -> bool:
        """Compare this message with ``other`` and return ``True`` if they are considered equal.

        :param other: The other :class:`EmailDataMessage` to compare against.
        :param ignore_added_headers: If ``True``, the comparison succeeds as long as every header of
            this message is also present in ``other`` (extra headers in ``other`` are ignored).
            If ``False``, both header lists must match exactly.
        :return: ``True`` if the messages are considered equal, otherwise ``False``.
        """
        # TODO optimize this method - sometimes servers change these fields before sending
        if not isinstance(other, EmailDataMessage):
            return False
        if (self.from_address != other.from_address
                or self.date != other.date
                or self.replyto_address != other.replyto_address
                or self.body_text != other.body_text):
            return False

        if not ignore_added_headers:
            return self.additional_headers == self.additional_headers

        for cur_header in self.additional_headers:
            if cur_header not in other.additional_headers:
                return False
        return True

    def add_header(
            self,
            header: EmailHeader,
            allow_multiple: bool = False,
            overwrite: bool = False
    ) -> Self:
        """Add an :class:`EmailHeader` to :attr:`additional_headers`.

        :param header: The header to be added.
        :param allow_multiple: If ``True``, the same header key may exist multiple times.
        :param overwrite: If ``True`` and a header with the same key already exists, replace it.
        :return: This :class:`EmailDataMessage` instance to allow method chaining.
        """
        if self.additional_headers is None:
            self.additional_headers = []

        existing_keys = [existing_header.key for existing_header in self.additional_headers]

        if not allow_multiple and header.key in existing_keys:
            raise ValueError(
                f"header {header.key} already exists, but adding multiple headers is not marked as allowed"
            )
        if overwrite and header.key in existing_keys:
            exist_at_index = existing_keys.index(header.key)
            self.additional_headers[exist_at_index] = header
        else:
            self.additional_headers.append(header)
        return self

    def add_to_addresses(
            self,
            addresses: Union[EmailAddress, list[EmailAddress]],
            allow_multiple: bool = False,
            overwrite: bool = False
    ) -> Self:
        """Add a ``To`` header containing one or many recipient :class:`EmailAddress` objects."""
        mails_as_str = ','.join([str(addr) for addr in addresses]) if isinstance(addresses, list) else str(addresses)
        return self.add_header(
            header=EmailHeader(key='To', value=mails_as_str),
            allow_multiple=allow_multiple, overwrite=overwrite
        )

    def add_cc_addresses(
            self,
            addresses: Union[EmailAddress, list[EmailAddress]],
            allow_multiple: bool = False,
            overwrite: bool = False
    ) -> Self:
        """Add a ``Cc`` header containing one or many copy :class:`EmailAddress` objects."""
        mails_as_str = ','.join([str(addr) for addr in addresses]) if isinstance(addresses, list) else str(addresses)

        return self.add_header(
            header=EmailHeader(key='Cc', value=mails_as_str),
            allow_multiple=allow_multiple, overwrite=overwrite
        )

    def add_bcc_addresses(
            self,
            addresses: Union[EmailAddress, list[EmailAddress]],
            allow_multiple: bool = False,
            overwrite: bool = False
    ) -> Self:
        """Add a ``Bcc`` header containing one or many blind copy :class:`EmailAddress` objects."""
        mails_as_str = ','.join([str(addr) for addr in addresses]) if isinstance(addresses, list) else str(addresses)
        return self.add_header(
            header=EmailHeader(key='Bcc', value=mails_as_str),
            allow_multiple=allow_multiple, overwrite=overwrite
        )

    def add_replyto_address(
            self, address: EmailAddress, allow_multiple: bool = False, overwrite: bool = False
    ) -> Self:
        """Add a ``Reply-To`` header for the given :class:`EmailAddress`."""
        return self.add_header(
            header=EmailHeader(key='Reply-To', value=str(address)),
            allow_multiple=allow_multiple, overwrite=overwrite
        )


    def add_message_id(
            self, message_id: str, allow_multiple: bool = False, overwrite: bool = False
    ) -> Self:
        """Add a ``Message-ID`` header to the email."""
        return self.add_header(
            header=EmailHeader(key='Message-ID', value=message_id),
            allow_multiple=allow_multiple, overwrite=overwrite
        )

    def add_mime_version(
            self, mime_version: str, allow_multiple: bool = False, overwrite: bool = False
    ) -> Self:
        """Add a ``MIME-Version`` header to the email."""
        return self.add_header(
            header=EmailHeader(key='MIME-Version', value=mime_version),
            allow_multiple=allow_multiple, overwrite=overwrite
        )

    def add_content_type(
            self, content_type: str, allow_multiple: bool = False, overwrite: bool = False
    ) -> Self:
        """Add a ``Content-Type`` header to the email."""
        return self.add_header(
            header=EmailHeader(key='Content-Type', value=content_type),
            allow_multiple=allow_multiple, overwrite=overwrite
        )

    def add_content_transfer_encoding(
            self, content_transfer_encoding: str, allow_multiple: bool = False, overwrite: bool = False
    ) -> Self:
        """Add a ``Content-Transfer-Encoding`` header to the email."""
        return self.add_header(
            header=EmailHeader(key='Content-Transfer-Encoding', value=content_transfer_encoding),
            allow_multiple=allow_multiple, overwrite=overwrite
        )

    def add_subject(
            self, subject: str, allow_multiple: bool = False, overwrite: bool = False
    ) -> Self:
        """Add a ``Subject`` header to the email."""
        return self.add_header(
            header=EmailHeader(key='Subject', value=subject),
            allow_multiple=allow_multiple, overwrite=overwrite
        )
