class SmartVADHIS2Exception(Exception):
    """Base Exception"""
    pass


class DbException(SmartVADHIS2Exception):
    """Exceptions for the local database"""
    pass


class FileException(SmartVADHIS2Exception):
    """Exception for mapping file"""
    pass


class DhisApiException(SmartVADHIS2Exception):
    """Exceptions involving DHIS2"""
    pass


class NoODKDataException(SmartVADHIS2Exception):
    """Exception when there is no new data downloaded"""
    pass

