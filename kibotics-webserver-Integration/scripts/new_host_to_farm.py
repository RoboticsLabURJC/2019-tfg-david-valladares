#!/bin/python

hosts = {"212.128.254.97":  "epsilon01.kibotics.org",
"212.128.254.98":  "epsilon02.kibotics.org",
"212.128.254.99":  "epsilon03.kibotics.org",
"212.128.254.100": "epsilon04.kibotics.org",
"212.128.254.101": "epsilon05.kibotics.org",
"212.128.254.102": "epsilon06.kibotics.org",
"212.128.254.103": "epsilon07.kibotics.org",
"212.128.254.104": "epsilon08.kibotics.org",
"212.128.254.105": "epsilon09.kibotics.org",
"212.128.254.106": "epsilon10.kibotics.org",
"212.128.254.107": "epsilon11.kibotics.org",
"212.128.254.108": "epsilon12.kibotics.org",
"212.128.254.109": "epsilon13.kibotics.org",
"212.128.254.110": "epsilon14.kibotics.org",
"212.128.254.111": "epsilon15.kibotics.org",
"212.128.254.112": "epsilon16.kibotics.org",
"212.128.254.113": "epsilon17.kibotics.org",
}


for key, value in hosts.iteritems():
    maquina = Host.objects.create(host=value, 
                                    ip=key, 
                                    max_simulations=1, 
                                    running_simulations=0, 
                                    priority=1, 
                                    main_server=False,
									active=False)

