"""Payment file for the bank's batch upload. Format: docs/bankfile.md."""


def export_bank_file(payments, company_id, file_date, sequence):
    """Return the file contents as a str.

    payments: list of ledger.models.BankPayment
    company_id: our 10-character company id at the bank
    file_date: datetime.date
    sequence: int, the file's sequence number for that day
    """
    raise NotImplementedError
