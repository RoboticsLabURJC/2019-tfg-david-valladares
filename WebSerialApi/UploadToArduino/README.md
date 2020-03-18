
## Implementation through the avr girl-arduino library

## How to run this example 
Raise a server, two easy ways to do it:
    - For Python 3, run `python -m http.server 3000`
    - For NodeJS, run `npx http-server -p 3000`
You can then navigate to `http://localhost:3000` in Chrome and play with the app from there.

## Requirements
The Web Serial API is currently in development and is only available behind a flag on the stable branch of Chrome. Please enable the #enable-experimental-web-platform-features flag in chrome://flags to run this example.


## For Linux:
Se tienen que dar permisos en /dev
1. dar permiso sudo chmod 777 /dev/ttyUSB0
2. dar permiso a /dev/serial/

## References:
[avrgirl-arduino](https://github.com/noopkat/avrgirl-arduino)
