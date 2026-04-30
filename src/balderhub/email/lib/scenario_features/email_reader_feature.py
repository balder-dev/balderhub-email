import time

import balder

from ..utils.email_data_message import EmailDataMessage


class EmailReaderFeature(balder.Feature):
    """
    Represents a feature for reading and managing emails.

    This class provides methods for retrieving emails, waiting for new emails,
    and ensuring a minimum count of emails is reached within a specified time. It serves
    as a base for implementing email-related functionalities.
    """

    @property
    def total_mail_cnt(self) -> int:
        """
        Calculates the total number of mails retrieved by the `get_mails` method.

        :return: The total count of mails
        """
        return len(self.get_mails())

    def get_mails(self) -> list[EmailDataMessage]:
        """
        :return: returns all existing emails
        """
        raise NotImplementedError()

    def wait_for_new_mail(self, timeout_sec: float = 10) -> EmailDataMessage:
        """
        This method waits for a new mail for maximum of `timeout_sec` seconds.

        :param timeout_sec: max time to wait for a new mail in seconds.
        :return: the newly received mail
        """
        mail_cnt_before = len(self.get_mails())
        self.wait_for_min_total_mail_count_of(mail_cnt_before + 1, timeout_sec)
        return self.get_mails()[mail_cnt_before]

    def wait_for_min_total_mail_count_of(self, total_mail_cnt, timeout_sec: float = 10) -> None:
        """
        This method waits for a minimum number of mail count of `total_mail_cnt`. It raises an timeout error if the
        total mail count is not reached within `timeout_sec`.

        :param total_mail_cnt: the expected total mail count
        :param timeout_sec: max time to wait for new mails to come in
        """
        start_time = time.perf_counter()
        while len(self.get_mails()) < total_mail_cnt:
            if time.perf_counter() - start_time > timeout_sec:
                raise TimeoutError(f'did not receive necessary mail within {timeout_sec} seconds')
            time.sleep(.1)
