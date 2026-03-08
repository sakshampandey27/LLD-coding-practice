from enum import Enum

class IssueType(Enum):
    PAYMENT_FAILED = 1
    REFUND = 2
    KYC = 3
    FRAUD = 4