function displayTheory() {
  setExerciseBar("theory");

  document.getElementById("theory_column").style.display = "inline";
  document.getElementById("theoryButton").style.backgroundColor = "lightgray";
}


function displayEditor() {
  setExerciseBar("editor");

  document.getElementById('editor').style.width = "100%";
  document.getElementById('editor').style.display = "inline";
  document.getElementById("editorButton").style.backgroundColor = "lightgray";

  resizeEditor();
}


function displaySimulator() {
  if (document.getElementById('myIFrame')) {
    setExerciseBar("simulate");
    document.getElementById('myIFrame').style.width = "100%";
    document.getElementById('myIFrame').style.display = "inline";
    resizeSimulator();

  } else {
    setExerciseBar("simulate_real");
    document.getElementById('download_guide_column').style.width = "100%";
    document.getElementById("download_guide_column").style.display = "inline";

  }
  document.getElementById("simulateButton").style.backgroundColor = "lightgray";
}


function displayDual() {
  if (document.getElementById('myIFrame')) {
    setExerciseBar("dual");

    document.getElementById('editor').style.width = "50%";
    document.getElementById('editor').style.display = "inline";
    resizeEditor();

    document.getElementById('myIFrame').style.width = "50%";
    document.getElementById('myIFrame').style.display = "inline";
    resizeSimulator();

  } else {
    setExerciseBar("dual_real");

    document.getElementById('editor').style.width = "50%";
    document.getElementById('editor').style.display = "inline";
    resizeEditor();

    document.getElementById('download_guide_column').style.width = "50%";
    document.getElementById("download_guide_column").style.display = "inline";

  }

  document.getElementById("dualButton").style.backgroundColor = "lightgray";
}


function displayCompete() {
  setExerciseBar("compete");

  document.getElementById('chat_column').style.width = "20%";
  document.getElementById("chat_column").style.display = "inline";
  document.getElementById('myIFrame').style.width = "80%";
  document.getElementById('myIFrame').style.display = "inline";
  resizeSimulator();

  document.getElementById("competeButton").style.backgroundColor = "lightgray";
  document.querySelector("#searchBar").style.display ="inline";
  document.querySelector("#checkStatus").style.display = "inline";
}


function displayNoteBook() {
  setExerciseBar("notebook");

  document.getElementById('editor').style.width = "100%";
  document.getElementById('editor').style.display = "inline";
  document.getElementById("notebookButton").style.backgroundColor = "lightgray";

  resizeEditor();
}


function displayTheoryTH() {
  setExerciseBar("theory");

  document.getElementById("loading_page").style.display = "none";
  document.getElementById('editor').style.display = 'none';
  document.getElementById('theory_column').style.display = 'inline';
  document.getElementById("dualButton").style.display = "none";
}

/**
 * Resize the editor window to load its content
 * @return {None}
 */
async function resizeEditor() {
  var elem = $("#editor")[0];
  if (elem.requestFullscreen) {
    await elem.requestFullscreen();
    await document.exitFullscreen();
  }
}


/**
 * Reload the Simulator window to load its content.
 * @return {None}
 */
async function resizeSimulator() {
  var elem = $( ".a-canvas")[0];
  if (elem && elem.requestFullscreen) {
    await elem.requestFullscreen();
    await document.exitFullscreen();
  }
}


function clearBar(clear=false) {
  var nodes = document.getElementById("exernav-center").childNodes;
  for (var i = 0; i < nodes.length; i++) {
    if (nodes[i].childNodes.length > 0) {
      nodes[i].childNodes[0].style.display = "none";
    }
  }
  var childs = document.getElementById("navcenter").childNodes;
  for (var i = 0; i < childs.length; i++) {
    if (childs[i].childNodes.length > 0) {
      childs[i].childNodes[0].style.backgroundColor = "white";
    }
  }
  document.querySelectorAll(".col-xs-6").forEach(element => element.style.display = "none");

  if (document.getElementById("loading_page") && !clear) {
    document.getElementById("loading_page").style.display = "inline";
  }
}


function setExerciseBar(mode) {
  var dict_mode = {"theory": ["exitbtn"],
                  "editor": ["firstRobot", "saveCode", "exitbtn"],
                  "simulate": ["runbtn", "cambtn", "resetRobot", "exitbtn"],
                  "dual": ["firstRobot", "saveCode", "runbtn", "cambtn", "resetRobot", "exitbtn"],
                  "compete": ["loadRobot", "runbtn", "resetRobot", "stopStreamButton" ,"exitbtn"],
                  "simulate_real": ["loadRobot", "send_tello", "send_mbot", "exitbtn"],
                  "dual_real": ["saveCode", "loadRobot", "send_tello", "send_mbot", "exitbtn"],
                  "notebook": ["saveCode", "runBtn", "exitbtn"]}

  clearBar(true);

  for (var i = 0; i < dict_mode[mode].length; i++) {
    if (synch) {
      if (mode == "compete") {
        checkLoadCode();
        if (pc1 == undefined && pc2 == undefined ) {
          if (dict_mode[mode][i] == "exitbtn")  {
            document.getElementById(dict_mode[mode][i]).style.display = "inline-block";
          }
        } else {
          if (dict_mode[mode][i] != "runbtn" || dict_mode[mode][i] != "pausebtn") {
            document.getElementById(dict_mode[mode][i]).style.display = "inline-block";
          }
        }
      } else {
        if (lenguage == "Python" && dict_mode[mode][i] != "firstRobot") {
          document.getElementById(dict_mode[mode][i]).style.display = "inline-block";
        } else if (lenguage == "Scratch") {
          document.getElementById(dict_mode[mode][i]).style.display = "inline-block";
        }
      }
    } else {
      if (mode == "simulate_real" || mode == "dual_real") {
        if (exercise_name.includes("Tello") && dict_mode[mode][i] != "send_mbot") {
          document.getElementById(dict_mode[mode][i]).style.display = "inline-block";
        } else if (exercise_name.includes("MBot") && dict_mode[mode][i] != "send_tello") {
          document.getElementById(dict_mode[mode][i]).style.display = "inline-block";
        }
      } else {
        if (lenguage == "Python" && dict_mode[mode][i] != "firstRobot") {
          document.getElementById(dict_mode[mode][i]).style.display = "inline-block";
        } else if (lenguage == "Scratch") {
          document.getElementById(dict_mode[mode][i]).style.display = "inline-block";
        }
      }
    }
  }
}
