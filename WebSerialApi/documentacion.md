#                   WEB SERIAL API EN KIBOTICS
#### Introducción
- Esta api proporciona una forma para que los sitios web se pueden comunicar con el puerto serie del ordenador. Uniendo asi la web con el mundo físco. Permitiendo la comunicación con dispositivos como microcontroladoras, impresoras 3D...   
- Es una api proporcionada por el navegador Chrome, que todavía no esta integrada, por lo que para activarla, necesitamos ir a chrome://flags/ y habilitar *Experimental Web Platform features*.   
- El objetivo que hemos llevado a cabo, es que actualmente Kibotics para el robot real Mbot, solo funcionaba en linux. Y con esta api, nos brinda una oportunidad de que la carga del programa al robot funcione tanto en MacOs, Windows y Linux, incluso sin necesidad de realizar ninguna instalación o descarga de ficheros.   

### Desarrollo
- En cuanto al desarrollo realizado, consiste en que el usuario una vez que desea cargar el programa, pulsará el botón para ello, esto desencadenará una serie de acciónes por debajo, y el programa se cargará al robot. Este proceso que se realiza por debajo sigue los siguientes pasos: 
    - Primero se comprobará si hubiera algun puerto abierto para cerrarlo. Después al llamar a navigator.serial.requestPort() se abrirá un panel para selecionar el puerto que queremos abrir para la comunicación y una vez seleccionado se abrirá el puerto.   
        ```
        async function clickConnect() {
            progress.style.width = '0%';
            alertError.style.visibility = 'hidden';
            //-- Abrir puerto serie y conectarse
            if (portPrev) {
                await disconnect();
            }
            await connect();
            activeProgress.style.visibility = 'visible';
            progress.style.width = '25%';
            if(document.getElementById('uploadMbot').value == 'python'){
                send_code_to_mbot()
            }else{
                convert_and_send_code_to_mbot();
            }

        }
        async function connect() {
    
            //-- Solicitar puerto serie al usuario
            //-- Se queda esperando hasta que el usuario ha seleccionado uno
            portPrev = await navigator.serial.requestPort();
    
            // - Abrir el puerto serie. Se espera hasta que este abierto
            await portPrev.open({ baudrate: 115200 });
    
        }
       
       async function disconnect() {
            // -- Cerrar el puerto serie
            await portPrev.close();
            portPrev = null;
        }
       ```     
    - Una vez abierto el puerto, se llamará a la función correspondiente, en función de si el código es python o scratch, la principal diferencia es que para scratch primero necesitamos hacer una conversión a python. Esta función realizara una petición al servidor enviándole el código del programa y esperando como respuesta el *.hex, que es fichero que entiende la placa.     
    ```   
      function convert_and_send_code_to_mbot() {
        var pythoncode = Blockly.Python.workspaceToCode(editor.ui);
        console.log(pythoncode);

        var enc = new TextEncoder();
        const message = {
            method: "GET"
        };
        url = '/get_python_to_arduino_binary?python_code=' + JSON.stringify(pythoncode);
        fetch(url, message)
            .....
            .....
            .....
        // Una vez enviada la peticion al servidor, esperara la respuesta
    ```   
    - En el lado del servidor, cuando recibe la petición con el código, se encarga de generar el *.hex y enviarlo en la respuesta.     
    ```   
    def get_python_to_arduino_code_binary(request):
                ........
                ........
                ........
        
        # Extraemos el binario
        f_binary = open(exercise_dir + 'build-uno/output.hex', 'r')
        binary = f_binary.read()
        f_binary.close()

        print('Python code: ' + python_code)
    
        response = HttpResponse(binary, content_type='text/plain')
        response['Content-Length'] = len(response.content)
        return response
    ```   
  
    - Una vez recibida la respuesta con el *.hex, lo convertimos a un arraybuffer, y se llama a la función que permite cargar el *.hex al robot.  
    ```   
      function convert_and_send_code_to_mbot() {
            .....
            .....
            .....
        fetch(url, message)
        // Una vez erecibida la respuesta.
            .then(function(response) {
                if(response.ok){
                    responseOk = true
                }else{
                    responseOk = false
                }
                return response.text();
            })
            .then(function(data) {

               if(responseOk){
                    var dataBuffer = enc.encode(data);
                    upload_to_mbot(dataBuffer)
                    progress.style.width = '99%';
                    alertError.style.visibility = 'hidden';

                }else{
                    console.log("Fallo al compilar el programa")
                    infoError.innerHTML = "¡Upss!. Hay un error en el programa, revisalo"
                    alertError.style.visibility = 'visible';
                    activeProgress.style.visibility = 'hidden';
                }

            })
            .catch(function(err) {

                console.error(err);
            });

    }
        
    ```   
  - Para la carga del *.hex, hacemos uso de una librería, realizada en javascript, llamada [avrgirl](https://github.com/noopkat/avrgirl-arduino), que implementa el protocolo stk500 para el proceso de carga a la placa del mbot, que esta basada en arduino uno.   
     - Hemos tenido que ajustar esta librería a nuestras necesidades, ya que ella también implementaba la parte de abrir el puerto con webserial, y por seguridad, para abrir el puerto serie se requiere una acción del usuario, como la de pulsar el botón, pero tiene un tiempo limitado. Entonces cuando llamábamos a la funciónn de la librería que carga el programa, a veces fallaba y otras no. Esto se debía al tiempo que se tardaba desde esa acción del usuario hasta la llamada de la función, puesto que antes de llamar a esta función, necesitamos conseguir el *.hex y esta acción requiere de un tiempo. Por lo que hemos adaptado la librería eliminado la parte de abrir el puerto.
     - Si la carga ha ido bien, la función de la librería utilizada (**avrgirl.flash(dataBuffer,(error)**) , cerrará el puerto serie.
     ```   
      function upload_to_mbot(dataBuffer){
            let avrgirl = new AvrgirlArduino({
                board: "uno"
            });
    
            avrgirl.flash(dataBuffer,(error) =>  {
                if (error) {
                    console.error(error);
                    portPrev = null;
                    infoError.innerHTML = "¡Upss!. Se ha producio un error al cargar el programa, intentelo de nuevo!"
                    alertError.style.visibility = 'visible';
                    activeProgress.style.visibility = 'hidden';
    
                } else {
                    console.info('done correctly.');
                    portPrev = null
                    alertError.style.visibility = 'hidden';
                    activeProgress.style.visibility = 'hidden';
                }
            });
      }
        
     ```   
     
  * Condiciones de mensajes de errores que pueden darse:
    - Si el programa realizado por el usuario no esta bien, por lo que fallará la generación del *.hex. Entonces se parará el proceso de carga y se mostrará un mensaje de error.
    - Si falla al cargase a la placa, se mostrara también un mensaje de error indicándolo.
   
    
    
  