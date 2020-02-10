//-- Puerto serie
let port;

//-- Lector del stream de entrada
let reader;

//-- Stream de entrada codificado
let inputDone;

//-- Stream de salida
let outputDone;

//-- Stream de entrada
let inputStream;

//-- Botón de conexion al puerto serie
const butConnect = document.getElementById('butConnect');

//-- LED checkbox
const avance = document.getElementById('avanzar');
const back = document.getElementById('retroceder');
const left = document.getElementById('izquierda');
const right = document.getElementById('derecha');
const stop = document.getElementById('parar');


//-- EStado del boton1
const button1 = document.getElementById('Button');

//------------------------------------------------------
//-- PUNTO DE ENTRADA
//------------------------------------------------------
document.addEventListener('DOMContentLoaded', () => {

  //-- RETROLLAMADA DEL BOTON DE CONEXION
  butConnect.addEventListener('click', clickConnect);

  //-- Comprobar si el navegador soporta puerto serie
  if ('serial' in navigator) {

    //-- Mantener oculto el mensaje de error
    const notSupported = document.getElementById('notSupported');
    notSupported.classList.add('hidden');

    //-- Activar el boton de conectar
    butConnect.disabled = false;
  }
});


//---------------------------------------------------------
//-- SE HA APRETADO EL BOTON DE conectar
//----------------------------------------------------------

async function clickConnect() {

  //-- Si ya estaba abierto el puerto serie
  //-- Lo cerramos
  if (port) {
    await disconnect();

    //-- Cambiar el estado de al interfaz
    butConnect.textContent = '🔌Conectar';

    return;
  }

  //-- Abrir puerto serie y conectarse
  await connect();

  //-- Activar la interfaz
  butConnect.textContent = '🔌Desconectar';

  //-- Estado inicial del checkbutton
  writeToStream('4');

  //-- Retrollamada del Checkbutton para acceder al LED
  avance.onclick = () => {
    if (avance.checked)
      writeToStream('0');
  }
  back.onclick = () => {
    if (back.checked)
      writeToStream('1');
  }
  left.onclick = () => {
    if (left.checked)
      writeToStream('2');
  }
  right.onclick = () => {
    if (right.checked)
      writeToStream('3');
  }
  stop.onclick = () => {
    if (stop.checked)
      writeToStream('4');
  }

}

//--------------------------------
//-- Abrir el puerto serie
//--------------------------------
async function connect() {

  //-- Solicitar puerto serie al usuario
  //-- Se queda esperando hasta que el usuario ha seleccionado uno
  port = await navigator.serial.requestPort();

  // - Abrir el puerto serie. Se espera hasta que este abierto
  await port.open({ baudrate: 9600 });

  //-- Configurar el stream de salida
  //-- Es outputStream. Antes se pasa por un codificador de texto
  //-- y de ahí sale por el puerto serie
  const encoder = new TextEncoderStream();
  outputDone = encoder.readable.pipeTo(port.writable);
  outputStream = encoder.writable;

  //-- Configurar el stream de entrada. Se pasa primero por un
  //-- decodificador de texto y luego se reciben los caracteres
  let decoder = new TextDecoderStream();
  inputDone = port.readable.pipeTo(decoder.writable);

  //-- La informacion se lee desde el lector reader
  reader = decoder.readable.getReader();

  //-- Bucle principal de lectura
  //-- Se procesan los caracteres recibidos
  //-- y se escriben en el estado del boton en la gui
  readLoop();
}


//-----------------------------------
//-- Cerrar el puerto serie
//-----------------------------------
async function disconnect() {

  // -- Cerrar el stream de entrada (lector)
  if (reader) {
    await reader.cancel();
    await inputDone.catch(() => {});
    reader = null;
    inputDone = null;
  }

  // -- Cerrar el stream de salida
  if (outputStream) {
    await outputStream.getWriter().close();
    await outputDone;
    outputStream = null;
    outputDone = null;
  }

  // -- Cerrar el puerto serie
  await port.close();
  port = null;

}


//------------------------------------------
//-- Bucle principal de lectura
//-----------------------------------------
async function readLoop() {

  //-- Se ejecuta indefinidamente
  //-- hasta que stream de entrada desaparezca
  while (true) {

    //-- Leer el valor del stream de entrada
    const { value, done } = await reader.read();

    //-- Hay un valor correcto: Mostrarlo en la gui
    if (value) {
      button1.innerText = value;
      console.log("[RCV] ", value)
    }

    //-- El stream se ha eliminado
    if (done) {
      console.log('[readLoop] DONE', done);
      reader.releaseLock();
      break;
    }
  }
}

//----------------------------------------
//-- Escritura por el puerto serie
//----------------------------------------
function writeToStream(cmd) {

  //-- Obtener el escritor para poder enviar datos de salida
  const writer = outputStream.getWriter();

  //-- Enviar la cadena pasada como parametro
  writer.write(cmd);

  //-- Debug
  console.log('[SEND]', cmd);

  //-- Liberar el stream
  writer.releaseLock();
}
