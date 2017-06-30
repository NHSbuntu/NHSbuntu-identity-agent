from smartcard.CardType import AnyCardType
from smartcard.CardRequest import CardRequest
from smartcard.Exceptions import CardRequestTimeoutException
from smartcard.util import toHexString

class SmartCardReader(object):
    def __init__(self):
        self.cardtype = AnyCardType()

    def is_card_inserted(self, timeout=1):
        self.cardrequest = CardRequest( timeout=timeout, cardType=self.cardtype )
        try:
            self.cardservice = self.cardrequest.waitforcard()
        except CardRequestTimeoutException:
            return False
        return True 

