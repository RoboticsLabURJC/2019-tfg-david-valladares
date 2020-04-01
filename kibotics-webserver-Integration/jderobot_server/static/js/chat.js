/**
 * @file chat.js
 * Chat script
 **/


/**
 * Get the time
 * @return {String} String with HH:mm format
 **/
function get_time() {
  var date = new Date();
  var hour = date.getHours();
  var minute = date.getMinutes();

  return hour + ":" + minute;
}


/**
 * Displays the messages
 * @param {String} message   Message
 * @param {String} [user=""] User
 **/
function add_message (message, user = "") {
  var text_div = document.createElement("div");
  var p = document.createElement("p");
  var time = document.createElement("span");

  if (user !== "") {
    text_div.className = "container-chat";
    time.className = "time-right";
    p.innerHTML = user.bold() + ": " + message;
  } else {
    text_div.className = "container-chat darker-chat";
    time.className = "time-left";
    p.innerHTML = message;
  }

  text_div.appendChild(p);

  time.innerHTML = get_time();
  text_div.appendChild(time);

  document.querySelector("#messages").appendChild(text_div);
  document.getElementById("messages").scrollTop = document.getElementById("messages").scrollHeight;
}


/**
 * Check the pushed key, call display message function and call send message function.
 * @param  {Object} e Pushed key
 * @return {Boolean}   Return false to skip enter key
 **/
function sendMessage(e) {
  if (e.keyCode == 13) {  // Enter key
    add_message(document.getElementById("chatSend").value);
    sendData(sendChannel, "chat", document.getElementById("chatSend").value);

    document.getElementById("chatSend").value = "";
    return false;
  }
}
