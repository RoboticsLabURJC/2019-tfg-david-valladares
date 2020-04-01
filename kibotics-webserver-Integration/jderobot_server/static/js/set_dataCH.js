/**
 * @file synch_evaluator.js
 * WebRTC DataChannels Script
 */


/**
 * create the DataChannel connection
 * @param  {[type]} pc agent
 * @return {None}
 */
 function createDatachannelConnection(pc) {
   var dataConstraint;
   sendChannel = pc.createDataChannel('sendDataChannel', dataConstraint);
   pc.ondatachannel = receiveChannelCallback;
 }


/**
 * Send the data via DataChannel
 * @param  {[type]} sendChannel  [description]
 * @param  {[type]} type         [description]
 * @param  {String} [message=""] [description]
 * @return {[type]}              [description]
 */
function sendData(sendChannel, type, message="") {
  if (type == "chat") {
    var data = JSON.stringify({
      "type": type,
      "message": message,
      "user": nameUser
    });

  } else if (type == "update_evaluator") {
    var data = JSON.stringify({
      "type": type,
      "progress1": document.getElementById('a-car1bar').innerHTML,
      "progress2": document.getElementById('a-car2bar').innerHTML
    });

  }
  sendChannel.send(data);
  console.log('Sent Data: ' + data);
}


/**
 * Close the DataChannel
 * @return {None}
 */
function closeDataChannels() {
  console.log('Closing data channels');
  sendChannel.close();
  receiveChannel.close();
  console.log('Closed peer connections');
}


/**
 * Callback for DataChannel receiver
 * @param  {Object} event Meesage received
 * @return {None}
 */
function receiveChannelCallback(event) {
  console.log('Receive Channel Callback');
  receiveChannel = event.channel;
  receiveChannel.onmessage = onReceiveMessageCallback;
}


/**
 * Received messages handler
 * @param  {Object} event Message received
 * @return {None}
 */
function onReceiveMessageCallback(event) {
  console.log(`Received datachannel message: ${event.data}`);

  var msg = JSON.parse(event.data);
  if (msg.type == "update_evaluator") {
    document.getElementById('a-car1bar').innerHTML = msg.progress1;
    document.getElementById('a-car1bar').style.width = msg.progress1;
    document.getElementById('a-car2bar').innerHTML = msg.progress2;
    document.getElementById('a-car2bar').style.width = msg.progress2;
  } else if (msg.type == "chat") {
    add_message(msg.message, msg.user);
  }
}
