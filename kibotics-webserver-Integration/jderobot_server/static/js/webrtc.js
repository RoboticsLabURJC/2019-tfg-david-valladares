/**
 * @file webrtc.js
 * WebRTC code
 **/

var rmtLoadCode = false;
var lclLoadCode = false;
var isMaster = false;

let token;
let user_name = "";

var sendChannel;
var receiveChannel;


/**
 * WebSocket messages handler
 * @param  {Object} e Message received
 * @return {None}
**/
wsocket.onmessage = function(e) {
  console.log(e);
  var signal = JSON.parse(e.data);
  switch(signal.type) {
    case "requestOpponent":
      if (signal.user == "" && signal.token == "") {
        var alertDiv = document.createElement("div");
        alertDiv.id = "alertDiv";
        alertDiv.className = "alert";
        alertDiv.style.backgroundColor ="lightCoral";
        alertDiv.innerHTML = "El usuario no está disponible.<div class='box' id='acceptDiv'><a href='#' class='btn btn-white btn-animation-1' id='closeAlertBtn' onclick='setConnection(this)'>Cerrar</a></div>"
        $(".navbar").append(alertDiv);
      } else {
        displayRequest(signal.user);
        token = signal.token;
      }
      break;
    case "joinRoom":
      add_message(signal.message, signal.user);
      token = signal.token;
      startStreaming();
      createDatachannelConnection(pc1);
      break;
    case "leaveChat":
      document.getElementById("chat_state").innerHTML = "El otro usuario se ha ido."
      document.getElementById("chat_state").style.backgroundColor = "lightcoral";
      add_message(signal.message, signal.user)
      break;
    case "candidate":
      onAddIceCandidate(signal.candidate);
      break;
    case "RTC-Offer":
      startRemoteStreaming(signal.offer);
      createDatachannelConnection(pc2);
      add_message(signal.message, signal.user);
      break;
    case "RTC-Answer":
      setAnswer(signal.answer);
      break;
    case "stopStream":
      exitStreaming(true);
      add_message(signal.message, signal.user);
      break;
    case "loadCode":
      window.userCode2 = signal.code;
      document.getElementById("chat_state").innerHTML = '<span class="glyphicon glyphicon-ok-sign"></span> Código del otro usuario recibido correctamente.';
      document.getElementById("chat_state").style.backgroundColor = "lightgreen";
      document.getElementById("code2").checked = true;
      rmtLoadCode = true;
      checkLoadCode();
      break;
    case "unloadCode":
      document.getElementById("chat_state").innerHTML = '<span class="glyphicon glyphicon-remove-sign"></span> Código eliminado correctamente.';
      document.getElementById("chat_state").style.backgroundColor = "lightcoral";
      document.getElementById("code2").checked = false;
      rmtLoadCode = false;
      break;
    case "startGame":
      document.getElementById("runbtn").click();
      break;
    case "stopGame":
      document.getElementById("pausebtn").click();
      break;
    default:
      console.log("Conexión WS establecida con el Servidor");
  }
}


/**
 * Search opponent function.
 * @param  {String} e Pushed key
 * @return {Boolean}   Return "flase" to skip "Enter" key
 */
function searchOpponent(e){
  if (e.keyCode == 13) {  // Code(13) = Enter key

    wsocket.send(JSON.stringify({
      type: "searchOpponent",
      user: document.getElementById("userSearch").value,
    }));

    document.getElementById("userSearch").value = "";
    return false;
  }
}


/**
 * Display a meessage to alert the user there's an opponent
 * @param  {String} user Opponent's name
 * @return {None}
 */
function displayRequest(user) {
  var alertDiv = document.createElement("div");
  alertDiv.id = "alertDiv";
  alertDiv.className = "alert";

  user_name = user;

  alertDiv.innerHTML = "El usuario " + user + " quiere competir contigo.<div class='box' id='acceptDiv'><a href='#' class='btn btn-white btn-animation-1' id='connectBtn' onclick='setConnection(this)'>Conectar</a></div>"
  $(".navbar").append(alertDiv);
}


/**
 * Send a "joinRoom" message to the server.
 * @return {None}
 */
function setConnection(cntxt) {
  //document.getElementById("alertDiv").style.display = "none";
  cntxt.parentNode.parentNode.parentNode.removeChild(cntxt.parentNode.parentNode);

  if (user_name != "") {
    wsocket.send(JSON.stringify({
      'type': "joinRoom",
      'user': user_name,
    }));
  }
}


/**
 * Close WebSocket function
 * @return {None}
 **/
function closeWS() {
  console.log("Chat socket closed.");
  wsocket.send(
    JSON.stringify({
      type: "leaveChat",
      token: token,
    })
  )
  wsocket.close();

  document.getElementById("chat_state").innerHTML = "You have leaved the chat."
}


/**
 * Set the connection for the callee. Generates the offer.
 * @return {None}
 **/
async function startStreaming() {
  document.getElementById("searchBar").style.display = "none";
  document.getElementById("online2").checked = true;
  document.querySelector("#chatSend").disabled = false;
  console.log($('#competeButton')[0].style.backgroundColor);
  if ($('#competeButton')[0].style.backgroundColor == "lightgray") {
    document.getElementById("loadRobot").style.display = "inline-block";
    document.getElementById("stopStreamButton").style.display = "inline-block";
  }

  isMaster = true;

  const offerOptions = {
    OfferToReceiveAudio: 1,
    OfferToReceiveVideo: 1
  };
  const constraints = {
    video: {
      mediaSource: "screen", // whole screen sharing
      //mediaSource: "window", // choose a window to share
      //mediaSource: "application", // choose a window to share
      width: {max: '1920'},
      height: {max: '1080'},
      frameRate: {max: '10'}
    }
  };

  pc1 = new RTCPeerConnection(configuration);
  console.log("Starting stream");

  var canvasDiv = $(".a-canvas")[0];
  if (canvasDiv.captureStream) {
    const stream = canvasDiv.captureStream();
    localStream = stream;

    pc1.addEventListener('icecandidate', e => onIceCandidate(e));
    console.log("Added candidates handlers created.");

    console.log(`Streamed tracks added ${localStream.getTracks()[0].label}`);
    localStream.getTracks().forEach(track => pc1.addTrack(track, localStream));

    try{
      const offer = await pc1.createOffer(offerOptions);

      try {
        await pc1.setLocalDescription(offer);
        console.log("Pc1 description created.");
      } catch(error) {
        console.log(`Failed to set session description: ${error.toString()}`);
      }
      console.log("Sending pc1 offer.");
      wsocket.send(
        JSON.stringify({
          type: "RTC-Offer",
          token: token,
          offer: offer,
        })
      );
    } catch(error) {
      console.log(`Failed to create session description: ${error.toString()}`);
    }
  } else {
    document.getElementById('chat_state').innerHTML = "Error capturing WebSim stream.";
  }
}


/**
 * Caller set connection. Generates the answer.
 * @param  {Object} offer Caller session data
 * @return {None}
 **/
async function startRemoteStreaming(offer) {
  document.getElementById("searchBar").style.display = "none";
  document.getElementById("online2").checked = true;
  document.querySelector("#chatSend").disabled = false;
  if ($('#competeButton')[0].style.backgroundColor == "lightgray") {
    document.getElementById("loadRobot").style.display = "inline-block";
    document.getElementById("stopStreamButton").style.display = "inline-block";
  }

  pc2 = new RTCPeerConnection(configuration);
  console.log("Created PC2 RTCPeerConnections");

  pc2.addEventListener('icecandidate', e => onIceCandidate(e));
  console.log("Added candidates handlers created.");

  pc2.ontrack = gotRemoteStream;
  console.log("Received stream handler created");

  try {
    await pc2.setRemoteDescription(offer);
    console.log("Pc2 description set.");
  } catch (error) {
    console.log(`Failed to set session description: ${error.toString()}`);
  }

  try {
    const answer = await pc2.createAnswer();
    try {
      await pc2.setLocalDescription(answer);
      console.log("Pc2 session complete.");
      console.log("Sending Pc2 answer.");
      wsocket.send(
        JSON.stringify({
          type: "RTC-Answer",
          token: token,
          answer: answer,
        })
      );
    } catch (error) {
      console.log(`Failed to set session description: ${error.toString()}`);
    }
  } catch (error) {
    console.log(`Failed to create session description: ${error.toString()}`);
  }
}


/**
 * Function to end the connection.
 * @param  {Boolean} [received=false] Separate Caller & Callee
 * @return {None}
 **/
function exitStreaming(received=false) {
  if (received != true) {
    wsocket.send(
      JSON.stringify({
        type: "stopStream",
        token: token,
      })
    );
  }

  if (pc1 === undefined) {
    pc2.close();
  } else {
    pc1.close();
  }

  if (document.getElementById("streamVideo") !== null) {
    document.getElementById("streamVideo").remove();
  }
  document.getElementById("myIFrame").innerHTML = "Session closed."
  closeWS();
  var url = window.location.href.split('#')[0];
  window.location.replace(url);
}


/**
 * Accept the Caller answer and finish the connection set.
 * @param {Object} answer Callee answer
 **/
async function setAnswer(answer) {
  try {
    await pc1.setRemoteDescription(answer);
    console.log(" Pc1 Session complete.")
  } catch (error) {
    console.log(`Failed to set session description: ${error.toString()}`);
  }
}


/**
 * Accept the candidate.
 * @param  {String} cand Candidato a aceptar
 * @return {None}
 **/
function onAddIceCandidate(cand) {
  var candidate = new RTCIceCandidate(cand)
  if (pc1 === undefined) {
    pc2.addIceCandidate(candidate);
  } else {
    pc1.addIceCandidate(candidate);
  }
}


/**
 * Send the generated candidate to the other user.
 * @param  {Object} event Generated candidate
 * @return {None}
 **/
async function onIceCandidate(event) {
  if (event.candidate != null || event.candidate != undefined) {
    wsocket.send(
      JSON.stringify({
        type: "candidate",
        token: token,
        candidate: event.candidate,
      })
    );
  }
  console.log("Candidate");
}


/**
 * Shows the stream,
 * @param  {Object} e Stream
 * @return {None}
 **/
function gotRemoteStream(e) {
  console.log("Received stream");

  if (divVideo === undefined || divVideo.srcObject !== e.streams[0]) {
    document.getElementById("scene").style.display = "none";
    var divVideo = document.createElement("video");
    divVideo.id = "streamVideo";
    divVideo.style.width = "100%";
    divVideo.style.height = "100%";
    divVideo.autoplay = true;
    divVideo.playsInline = true;
    divVideo.muted = true;
    document.getElementById("myIFrame").appendChild(divVideo);
    divVideo.srcObject = e.streams[0];
  }
}


/**
 * Send the user's code
 * @param  {String} code Codigo del usuario
 * @return {None}
 */
function loadCode() {
  lclLoadCode = true;

  wsocket.send(JSON.stringify({
    'type': "loadCode",
    'token': token,
  }));

  document.getElementById("loadRobot").onclick = unloadCode;
  document.getElementById("loadRobot").title = "Quitar Código";
  document.getElementById("loadRobot").style.backgroundColor = "lightgreen";
  document.getElementById("code1").checked = true;

  if (document.querySelector("#myIFrame").style.display == "inline") {
    checkLoadCode();
  }
}


/**
 * Send a signal to unload it's code
 * @return {None}
 */
function unloadCode() {
  lclLoadCode = false;

  wsocket.send(JSON.stringify({
    'type': "unloadCode",
    'token': token,
  }))

  document.getElementById("loadRobot").title = "Subir Código";
  document.getElementById("loadRobot").style.backgroundColor = "white";
  document.getElementById("loadRobot").onclick = loadCode;
  document.getElementById("code1").checked = false;

  if (document.querySelector("#myIFrame").style.display == "inline") {
    checkLoadCode();
  }
}


/**
 * Check the loaded code's and, if you are the master, display the "Play&Pause" button
 * @return {None}
 */
function checkLoadCode() {
  console.log(isMaster, rmtLoadCode, lclLoadCode);
  if (lclLoadCode && rmtLoadCode && isMaster) {
    document.getElementById("runbtn").style.display = "inline";

    window.setInterval(function(){
      sendData(sendChannel, "update_evaluator");
    }, 1000);

    return true;

  } else if (lclLoadCode && rmtLoadCode && !isMaster) {
    document.getElementById("chat_state").innerHTML = '<span class="glyphicon glyphicon-remove-ok"></span> Códigos cargados. Esperando el inicio.';
    document.getElementById("chat_state").style.backgroundColor = "lightyellow";

    document.getElementById("runbtn").style.display = "none";

    var liDiv = document.createElement("li");
    var aDiv = document.createElement("a");
    aDiv.id = "runRmtBtn";
    aDiv.href = "#";
    aDiv.title = "Ejecutar";
    aDiv.onclick = function () {
      wsocket.send(JSON.stringify({
        'type': "startGame",
        'token': token,
      }));
    }
    var imgDiv = document.createElement("img");
    imgDiv.src = "/static/img/icons/play.png";
    aDiv.appendChild(imgDiv);
    liDiv.appendChild(aDiv);
    $('#exernav-center li:eq(3)').before(liDiv);

    return false;

  } else if (lclLoadCode && !rmtLoadCode) {
    document.getElementById("chat_state").innerHTML = '<span class="glyphicon glyphicon-remove-sign"></span> Esperando el código del otro usuario.';
    document.getElementById("chat_state").style.backgroundColor = "lightyellow";

    document.getElementById("runbtn").style.display = "none";

    return false;

  } else if (!lclLoadCode && rmtLoadCode) {
    document.getElementById("chat_state").innerHTML = '<span class="glyphicon glyphicon-remove-sign"></span> Debes subir tu código.';
    document.getElementById("chat_state").style.backgroundColor = "lightcoral";

    document.getElementById("runbtn").style.display = "none";

    return false;

  } else {
    document.getElementById("chat_state").innerHTML = '<span class="glyphicon glyphicon-remove-sign"></span> Debéis subir vuestro código.';
    document.getElementById("chat_state").style.backgroundColor = "lightcoral";

    document.getElementById("runbtn").style.display = "none";

    return false;

  }
}
