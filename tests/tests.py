"""\

Voorbeeld van een TransactionRequest (GET):
https://www.sisow.nl/Sisow/iDeal/RestHandler.ashx/TransactionRequest?shopid=&merchantid
=0123456&purchaseid=123456789&amount=1000&payment=ecare&entrancecode=uniqueentrance&descriptio
n=Bestelling
webshop.nl&returnurl=http%3a%2f%2fwww.webshop.nl&callbackurl=http%3a%2f%2fwww.webshop.nl%2f/ca
llback&sha1=cb2461bd40ed1a77a6d837a560bfcbc3e03d6c3c

De waarde voor sha1 wordt als volgt bepaald:
sha1("123456789uniqueentrance10000123456b36d8259346eaddb3c03236b37ad3a1d7a67cec6")


Transaction response
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

<?xml version="1.0" encoding="UTF-8"?>
<transactionrequest xmlns="https://www.sisow.nl/Sisow/REST" version="1.0.0">
<transaction>
<issuerurl>https%3a%2f%2fbetalen.rabobank.nl%2fide%2fide.cgi%3fX009%3dBETAAL%26X010%3d2
0%26X015%3d%26V020%3d0050000513599081%26V022%3d01%26V021%3d9470173121213998</issuerurl>
<trxid>0050000513599081</trxid>
</transaction>
<signature>
<sha1>10bc163e9cb2050297514ad4db320ec1a16074d4</sha1>
</signature>
</transactionrequest>

"""

