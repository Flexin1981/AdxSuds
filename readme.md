<h1>AdxSuds</h1>

Suds Module for the Brocade Adx Loadbalancer SOAP based Api.

The Module uses the ADX Wsdl file to dynamically create and implement all methods supported by the Adx device connected to.

The Adx programmers guide can be found @    

     http://www.brocade.com/content/html/en/programmers-guide/SI_12502_XMLAPI/wwhelp/wwhimpl/js/html/wwhelp.htm

This will show you a list of the available methods and the input structures and output structures of the methods.

<h3>Usage</h3>

<h4>Simple Methods</h4>

     adx = Adx(<host/ip>, username, password)

     adx.slb_service.wsdl.service.getAllVirtualServers()
     
<h4>Simplple inputs</h4>

     adx = Adx(<host/ip>, username, password)
     
     adx.slb_service.wsdl.service.getTacacsServersConfiguration("input")

<h4>Complex objects inputs</h4>

    adx = Adx(<host/ip>, username, password)

    server = adx.slb_service.factory.create('Server')

    server.name = "Test_server"
    server.ip = "192.168.0.1"
    server.description "Testing_server"

    adx.slb_service.wsdl.service.createVirtualServers(server)
