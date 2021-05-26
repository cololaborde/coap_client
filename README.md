# Coap client

Coap client using coapthon library to connect with z1 rest-server motes

Parameters: 

python client.py method [-g | -p] minimal_ipv6_server nodes_quantity endpoint [/endpoint | endpoint] timeinterval [int seconds](OPCIONAL)

Use mode: 

python client.py -p aaaa::c30c:0:0:3 3 /leds/blue 10    
  
  ==>    make POST request to [aaaa::c30c:0:0:3]/leds/blue [aaaa::c30c:0:0:4]/leds/blue [aaaa::c30c:0:0:5]/leds/blue every 10 seconds 
  
  
python client.py -p aaaa::c30c:0:0:3 1 /leds/blue
  
  ==>    make POST request to [aaaa::c30c:0:0:3]/leds/blue just one time
  
 
python client.py -g aaaa::c30c:0:0:3 1 position 5

  ==>    make GET request to [aaaa::c30c:0:0:3]/position every 5 seconds

