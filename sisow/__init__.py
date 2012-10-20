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
import hashlib

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


class WebshopURLs(object):
    """\ """
    def __init__(self, returnurl, cancelurl='', notifyurl='', callbackurl=''):
        """Constructor """
        self.returnurl = returnurl
        self.cancelurl = cancelurl
        self.notifyurl = notifyurl
        self.callbackurl = callbackurl


class Transaction(object):
    """\
    
    """
    def __init__(self, purchaseid, amount, issuerid, entrancecode, description=''):
        """TODO: validation """
        self.shopid = ''
        self.payment = '' # Empty string indicates iDeal
        self.purchaseid = purchaseid
        self.amount = amount
        self.issuerid = issuerid
        self.entrancecode = entrancecode
        self.description = description
        # Will be set in SisowAPI.start_transaction
        self.merchantid = ''
        self.testmode = False
    
    def sha1(self, merchantkey):
        """\
        Return SHA1 value for:
        purchaseid/entrancecode/amount/shopid/merchantid/merchantkey
        """
        key = "%(purchaseid)s%(entrancecode)s%(amount)s%(shopid)s%(merchantid)s"
        sha1 = hashlib.sha1(key % self.__dict__)
        sha1.update(merchantkey)
        return sha1.hexdigest()
        
    def __str__(self):
        return str(self.__dict__)

class SisowAPI(object):
    """Sisow API abstraction """
    _url_api = 'https://www.sisow.nl/Sisow/iDeal/RestHandler.ashx/'
    _xmlns = 'https://www.sisow.nl/Sisow/REST'
    
    def __init__(self, merchantid, merchantkey, testmode=False):
        self.merchantid = merchantid
        self.merchantkey = merchantkey
        self._testmode = testmode
    
    @property
    def providers(self):
        call = 'DirectoryRequest'
        xml = _xml_request(self._url_api+call, data={'test': self._testmode})
        for issuer in xml.iter('{%s}issuer'%SisowAPI._xmlns):
            yield {'id': issuer[0].text, 'name': issuer[1].text}
    
    def start_transaction(self, transaction, urls):
        call = 'TransactionRequest'
        assert isinstance(transaction, Transaction)
        # Testmode
        transaction.testmode = 'true' if self._testmode else ''
        # Add additional attributes
        transaction.merchantid = self.merchantid
        # Extract query parameters, a bit hacky
        data = {}
        data.update(transaction.__dict__)
        data.update(urls.__dict__)
        # SHA encoding!
        data['sha1'] = transaction.sha1(self.merchantkey)
        # Cleanup
        for key in data.keys():
            if data[key] is '':
                del(data[key])
        xml = _xml_request(self._url_api+call, data)
        return TransactionResponse(xml)


class Response(object):
    """General response base class """
    def __init__(self, xml):
        """ """
        self.sha1 = ''
        self._signature = '' # Define in subclass
        # Detect errorresponse
        root = xml.getroot()
        if root.tag == "{%s}errorresponse" % SisowAPI._xmlns:
            raise ErrorResponse(xml)
        # Process XML (second level)
        offset = 2 + len(SisowAPI._xmlns)
        for element in xml.findall(".//*/*"):
            tag = element.tag[offset:]
            if tag in self.__dict__:
                self.__dict__[tag] = element.text
            
    def is_valid(self, merchantid, merchantkey):
        """\
        Validate the response using our merchantid and secret merchantkey
        """
        data = dict(merchantid=merchantid, merchantkey=merchantkey)
        data.update(self.__dict__)
        sha1 = hashlib.sha1(self._signature % data)
        return sha1.hexdigest() == self.sha1
    
class TransactionResponse(Response):
    """Specific transaction respons.
    
    <?xml version="1.0" encoding="UTF-8"?>
    <transactionresponse xmlns="https://www.sisow.nl/Sisow/REST" version="1.0.0">
        <transaction>
            <issuerurl>IssuerURL</issuerurl>
            <trxid>TransactionID</trxid>
        </transaction>
        <signature>
            <sha1>SHA1 trxid + merchantid + merchantkey</sha1>
        </signature>
    </transactionresponse>
    
    TODO: Sisow server is returning a transactionrequest!
    """
    def __init__(self, xml):
        """Constructor  """
        self.issuerurl = ''
        self.trxid = ''
        # Superclass
        super(TransactionResponse, self).__init__(xml)
        # Validation of type
        root = xml.getroot()
        # TODO: Sisow server is returning a transactionrequest!
        if not root.tag == "{%s}transactionrequest" % SisowAPI._xmlns:  # transactionresponse
            raise ValueError('Root node not "transactionrequest".\n\n'+etree.tostring(xml))
        # Validation signature
        # <sha1>SHA1 trxid + issuerurl + merchantid + merchantkey</sha1>
        self._signature = "%(trxid)s%(issuerurl)s%(merchantid)s%(merchantkey)s"

class ErrorResponse(Exception):
    def __init__(self, xml):
        # Extract info from XML
        ns = SisowAPI._xmlns
        code = xml.find(".//{%s}errorcode"%ns).text
        message = xml.find(".//{%s}errormessage"%ns).text
        super(ErrorResponse, self).__init__("%s %s"%(code, message))
        self.code = code
        self.message = message

def sisow_account(filename):
    with file(filename) as f:
        return f.readline().strip(), f.readline().strip()

if __name__ == "__main__":
    
    (id_, key) = sisow_account('../account-sisow.secret')
    api = SisowAPI(id_, key, False)
    # Request banks
    for i in api.providers:
        print i
    # Build transaction
    t = Transaction('test', 1302, '09', 'xtr1234z', 'Blubber')
    
    #Send transaction
    urls = WebshopURLs('http://test.nl/ok/')
    result = api.start_transaction(t, urls)
    print result.is_valid(id_, key)
    print urllib.url2pathname(result.issuerurl)
    
    