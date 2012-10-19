"""\
iDeal implementation in Python for the Sisow Payment provider


1. DirectoryRequest
het opvragen van de aangesloten iDEAL banken (alleen voor iDEAL);
2. TransactionRequest
het opvragen van de URL voor het starten van een transactie;
3. StatusRequest
het opvragen van de status van een transactie;
4. RefundRequest: 
retourneer een iDEAL transactie, geheel of gedeeltelijk;

NOT IMPLEMENTED
5. CancelReservation: annuleren van een Sisow ecare reservering;
6. InvoiceRequest: aanmaken van de Sisow ecare factuur;
7. CreditInvoiceRequest: aanmaken van een Sisow ecare creditnota;

Test the service using:
merchantid=0123456
merchantkey=b36d8259346eaddb3c03236b37ad3a1d7a67cec6

"""
from lxml import etree

import urllib
import urllib2

def _xml_request(url, data=None):
    if data is not None:
        data = urllib.urlencode(data)
        req = urllib2.Request(url, data)
    else:
        req = urllib2.Request(url)
    stream = urllib2.urlopen(req)
    return etree.parse(stream)


class Transaction(object):
    """\
    
    """
    def __init__(self, purchaseid, amount, issuerid, entrancecode, description=''):
        self.shopid = ''
        self.payment = '' # Empty string indicates iDeal
        self.purchaseid = purchaseid
        self.amount = amount
        self.issuerid = issuerid
        self.entrancecode = entrancecode
        self.description = description
        self.testmode = False
        self.sha1 = None
        # Will be set in SisowAPI.start_transaction
        self.merchantid = None
        self.returnurl = ''
        self.cancelurl = ''
        self.notifyurl = ''
        self.callbackurl = ''
    
    def __str__(self):
        return str(self.__dict__)

class SisowAPI(object):
    """Sisow API abstraction """
    _url_api = 'https://www.sisow.nl/Sisow/iDeal/RestHandler.ashx/'
    _xmlns = 'https://www.sisow.nl/Sisow/REST'
    
    def __init__(self, merchantid, merchantkey):
        self.merchantid = merchantid
        self.merchantkey = merchantkey
        
    @property
    def providers(self, test=False):
        call = 'DirectoryRequest'
        xml = _xml_request(self._url_api+call)
        for issuer in xml.iter('{%s}issuer'%SisowAPI._xmlns):
            yield {'id': issuer[0].text, 'name': issuer[1].text}
    
    def start_transaction(self, transaction, returnurl, cancelurl='',
                          notifyurl='', callbackurl=''):
        call = 'TransactionRequest'
        assert isinstance(transaction, Transaction)
        transaction.merchantid = self.merchantid
        transaction.returnurl = returnurl
        transaction.cancelurl = cancelurl
        transaction.notifyurl = notifyurl
        transaction.callbackurl = callbackurl
        xml = _xml_request(self._url_api+call) #, transaction.__dict__)
        return etree.tostring(xml)

class SisowTestAPI(SisowAPI):
    def __init__(self):
        """Test API constructor """
        key = 'b36d8259346eaddb3c03236b37ad3a1d7a67cec6'
        super(SisowTestAPI, self).__init__('0123456', key)
    
    @property
    def providers(self, test=False):
        call = 'DirectoryRequest'
        xml = _xml_request(self._url_api+call, data={'test': True})
        for issuer in xml.iter('{%s}issuer'%SisowAPI._xmlns):
            yield {'id': issuer[0].text, 'name': issuer[1].text}
    
    def start_transaction(self, transaction, returnurl, cancelurl='',
                          notifyurl='', callbackurl=''):
        transaction.testmode = True
        super(SisowTestAPI, self).start_transaction(transaction, returnurl,
                                                    cancelurl='', notifyurl='',
                                                    callbackurl='')
    
if __name__ == "__main__":
    api = SisowTestAPI()
    #api = SisowAPI(1, 2)
    #for i in api.providers:
    #    print i
    t = Transaction('test', 12301, 99, 'xtr123z', 'Bitcoins')
    print api.start_transaction(t, 'http://www.bitbank.nl/yes/')