<h1>AdxSuds</h1>

Suds Module for the Brocade Adx Loadbalancer SOAP based Api.

The Module uses the ADX Wsdl file to dynamically create and implement all methods supported by the Adx device connected to.

The Adx programmers guide can be found below;  

     http://www.brocade.com/content/html/en/programmers-guide/SI_12502_XMLAPI/wwhelp/wwhimpl/js/html/wwhelp.htm

This will show you a list of the available methods as well as the input structures and output structures of the methods.

<h3>Installation</h3>

You can install this module through pip with the following Command; 

     sudo pip install git+https://github.com/Flexin1981/AdxSuds
     
Currently this is tested on linux but should work on Windows, although this will require a tweak for the cache file location.

<h3>Usage</h3>

<h4>Importing</h4>

     import adxsuds

<h4>Transport</h4>

By default the module will use https as the transport to the ADX as this is the most secure, however this can be overridden should you wish as below. At this time custom ports are not supported.
 
    adx = Adx(<host/ip>, username, password, protocol="http")

It is also possible to turn off the ssl certificate verification on the https connection by adding the below option although again this is not recommended for secure communication to the device.

    adx = Adx(<host/ip>, username, password, protocol="https", verify_ssl=False)

<h4>NameSpaces</h4>

The Adx currently supports the following namespaces;

    sys, network, slb, gslb, security

These Namespaces can be accessed through the normal python method as below;
  
    adx = Adx(<host/ip>, username, password)
    adx.slb.XXXX

<h4>Simple Methods</h4>

     adx = Adx(<host/ip>, username, password)

     adx.slb.getAllVirtualServers()
     
<h4>Simple inputs</h4>

     adx = Adx(<host/ip>, username, password)
     
     adx.sys.getTacacsServersConfiguration("<IP Address>")

<h4>Complex objects inputs</h4>

There is two ways to create the input structures to the device the simplest is to create a dictionary structure that matches the structure in the documentation, see below for an example.

    adx = Adx(<host/ip>, username, password)
    
    ArrayOfVirtualServerConfigurationSequence = {
        "VirtualServerConfigurationSequence": [
            {
                "virtualServer": {
                    "Name": "test_server_with_config",
                    "IP": "192.168.100.22"
                },
                "trackPort": {
                    "NameOrNumber": "http"
                }
            }
        ]
    }

    ServerPort = {
        "srvr": {
            "Name": "test_server_with_config"
        },
        "port": {
            "NameOrNumber": "http"
        }
    }

    adx.slb.createVirtualServerWithConfiguration(ArrayOfVirtualServerConfigurationSequence)
    adx.slb.createVirtualServerPort(ServerPort)
    
    
The second is to use the factory method to create the objects before passing these to the methods, this technique though can get a little complex if you have to create structures that are nested X levels deep. See below for an example of this method.     

    adx = Adx(<host/ip>, username, password)

    server = adx.slb_service.factory.create('Server')

    server.name = "Test_server"
    server.ip = "192.168.0.1"
    server.description "Testing_server"

    adx.slb.createVirtualServers(server)

<h3>Outputs</h4>

The output of the module is a dictionary like object and can be interacted with by the common dict operators, you can also cast the output to a dict should you wish to do so.


<h3>Help</h3>

Some of the API documentation types do not match up to the complex types that you need to create within the complex object structures of the WSDL file. To find the correct input structures you can call the "get_method_in" method in correct namespace for that call and pass the method name in as a string. This method will return you a list of the parameter types that you need to send in.

    adx = Adx(<host/ip>, username, password)
    
    print adx.network.get_method_in("createVlan")
    
Output:

    ['ArrayOfPortVlanSequence vlanList', ' ']
    
Note that there is two parts to the type "ArrayOfPortVlanSequence" & "vlanList" only the first part of the type string is the required type structure that you need to pass to the relevant method using the complex object structure above. The second part is used internally to name the soap structure so can be ignored in this case.


<h3>Debuging</h3>

The module allows for debugging the soap packets that are being sent to and received from the ADX device. To turn this on increase the debug integer when creating the ADX device object.
 
    adx = Adx(<host/ip>, username, password, verify_ssl=False, debug=2)
    
<h4>Output</h4>
    ====================Begin Reply Packet======================
    <?xml version="1.0"?>
    <s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
     <s:Body><tns:createVirtualServerPortResponse xmlns:tns="urn:webservicesapi">
    </tns:createVirtualServerPortResponse>
    </s:Body>
    </s:Envelope>
    =====================End Reply Packet=======================
    