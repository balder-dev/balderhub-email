import dataclasses



@dataclasses.dataclass
class EmailAddress:
    """Represents an email address with an associated display ``name`` and the actual ``mail_address``."""
    name: str
    mail_address: str

    def __str__(self):
        """Return the formatted email address (see :meth:`to_string`)."""
        return self.to_string()

    def to_string(self):
        """Return the email address formatted as ``"<name> <<mail_address>>"``."""
        return f'{self.name} <{self.mail_address}>'
