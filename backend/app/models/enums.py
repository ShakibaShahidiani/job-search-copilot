import enum


class WorkModel(str, enum.Enum):
    REMOTE = "remote"
    HYBRID = "hybrid"
    ONSITE = "onsite"


class EmploymentType(str, enum.Enum):
    FULL_TIME = "full_time"
    PART_TIME = "part_time"
    CONTRACT = "contract"
    INTERNSHIP = "internship"


class JobStatus(str, enum.Enum):
    ACTIVE = "active"
    CLOSED = "closed"
    EXPIRED = "expired"


class CompanyType(str, enum.Enum):
    PRODUCT = "product"
    CONSULTANCY = "consultancy"


class SeniorityLevel(str, enum.Enum):
    JUNIOR = "junior"
    MEDIOR = "medior"
    SENIOR = "senior"


class FeedbackAction(str, enum.Enum):
    LIKE = "LIKE"
    REJECT = "REJECT"
    SHORTLIST = "SHORTLIST"
    APPLY = "APPLY"
    INTERVIEW = "INTERVIEW"
    OFFER = "OFFER"


class RejectReason(str, enum.Enum):
    TOO_SENIOR = "too_senior"
    TOO_JUNIOR = "too_junior"
    CONSULTING = "consulting"
    COMPANY = "company"
    DOMAIN = "domain"
    COMPENSATION = "compensation"
    LOCATION = "location"
    TECHNOLOGY = "technology"
    ROLE_CONTENT = "role_content"
    LANGUAGE = "language"
    VISA = "visa"
    OTHER = "other"


class FeatureType(str, enum.Enum):
    ROLE_FAMILY = "role_family"
    TECHNOLOGY = "technology"
    DOMAIN = "domain"
    COMPANY_TYPE = "company_type"
    SENIORITY = "seniority"
    LOCATION = "location"
    WORK_MODEL = "work_model"


class Confidence(str, enum.Enum):
    OBSERVATION = "observation"
    WEAK = "weak"
    MEDIUM = "medium"
    STRONG = "strong"


class GapSeverity(str, enum.Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    BLOCKER = "BLOCKER"
