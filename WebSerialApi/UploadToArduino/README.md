
## Implementation through the avr girl-arduino library

## How to run this example 
Raise a server, two easy ways to do it:
    - For Python 3, run `python -m http.server 3000`
    - For NodeJS, run `npx http-server -p 3000`
You can then navigate to `http://localhost:3000` in Chrome and play with the app from there.   

## Analysis   
Analysis in different operating systems in order to make it work without installing anything.   

| S.O | Arduino | Mbot |
| --- | ---: | :---: |
| MacOs | Yes | Yes |
| Ubuntu 16.04| Yes | Yes |
| Ubuntu 18.04 | Yes | Yes |
| Windows 7 | Yes | No |
| Windows 8 | Yes | Yes |
| Windows 10 | Yes | Yes |    
    
   * Results:    
        . MacOS => No additional action is necessary, both Mbot and Arduino are recognized.   
        . Windows:   
            - 10 => No additional action is necessary, both Mbot and Arduino are recognized.   
            - 8 => When the board is inserted through the widows update, the drivers are downloaded automatically, so it is necessary to do it manually.   
            - 7 => In the case of arduino windows update if the driver is downloaded automatically. But in the case of Mbot it does not detect it, so here it would be required to manually download the drivers for operation.   
        . Unbuntu 16.04 or 18.04:
            1. We need to add dialout to user group. If we did not do this every time the command is restarted we would need to do the following steps to always give permissions.     
            ```
            sudo usermod -a -G dialout $USER   
            ```   
            * For Arduino => Once the arduino is connected we need to give permissions to /dev/ttyACM0.    
            ```   
            sudo chmod +x /dev/ttyACM0   
            ```  
             *For Mbot => Once the Mbot is connected we need to give permissions to /dev/ttyUSB0.  
            ```
            sudo chmod +x /dev/ttyUSB0
            ```   
            It would only take this task, but nothing needed to be installed.
            
   * Conclusion:   
        - With this implementation we could load programs to mbot or arduino from any s.o, without the need to install anything additional (**zero-installation**), simply using chrome and WebSerialApi.  
     
## References:
[avrgirl-arduino](https://github.com/noopkat/avrgirl-arduino)
