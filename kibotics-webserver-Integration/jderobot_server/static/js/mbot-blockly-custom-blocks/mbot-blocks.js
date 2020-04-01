/* CUSTOM BLOCKLY BLOCKS MADE FOR MBOT THROUGH PYTHON */

function initConsoleLogBlock(){
  var consoleLogBlock = {
    "type": "logs",
    "message0": "%{BKY_LOGS_TEXT}",
    "args0": [
      {
        "type": "input_value",
        "name": "TO_LOG"
      }
    ],
    "previousStatement": null,
    "nextStatement": null,
    "colour": "%{BKY_ROBOT_TOOLS_HUE}",
    "tooltip": "%{BKY_LOGS_TOOLTIP}",
    "helpUrl": ""
  };

  Blockly.Blocks['logs'] = {
    init: function() {
      this.jsonInit(consoleLogBlock);
    }
  };

  Blockly.Python['logs'] = function(block) {
    var value_to_log = Blockly.Python.valueToCode(block, 'TO_LOG', Blockly.Python.ORDER_ATOMIC);

    var code = 'print ' + '(' + value_to_log + ')' + '\r\n';
    return code;
  };
}

/*function initFollowLineBlock(){
  var followLineBlock = {
    "type": "follow_line",
    "message0": "Detectar la línea negra con el IR de %1",
    "args0": [
      {
        "type": "field_variable",
        "name": "ROBOT",
        "variable": "myRobot"
      },
    ],
    "output": null,
    "colour": "%{BKY_VARIABLES_DYNAMIC_HUE}",
    "tooltip": "Detectar la línea de color negro a través del IR",
    "helpUrl": ""
  };

  Blockly.Blocks['follow_line'] = {
    init: function() {
      this.jsonInit(followLineBlock);
    }
  };

  Blockly.Python['follow_line'] = function(block) {
    var variable_robot = Blockly.Python.variableDB_.getName(block.getFieldValue('ROBOT'), Blockly.Variables.NAME_TYPE);

    var code = variable_robot + '.get_line_follow_value()\n';
    return code;
  };
}*/


function initGetDistanceBlock(){
  var getDistanceBlock = {
    "type": "get_distance",
    "message0": "%{BKY_GET_DISTANCE_TEXT}",
    "args0": [
      {
        "type": "field_variable",
        "name": "ROBOTVAR",
        "variable": "myRobot"
      }
    ],
    "output": null,
    "colour": "%{BKY_ROBOT_SENSORS_HUE}",
    "tooltip": "%{BKY_GET_DISTANCE_TOOLTIP}",
    "helpUrl": ""
  };

  Blockly.Blocks['get_distance'] = {
    init: function() {
      this.jsonInit(getDistanceBlock);

    }
  };

  Blockly.Python['get_distance'] = function(block) {
    var variable_robotvar = Blockly.Python.variableDB_.getName(block.getFieldValue('ROBOTVAR'), Blockly.Variables.NAME_TYPE);

    var code = variable_robotvar + '.get_us()\n';

    return [code, Blockly.Python.ORDER_NONE];
  };
}


  
function initMoveBackwardBlock(){
  var moveBackwardBlock = {
    "type": "move_backward",
    "message0": "%{BKY_MOVE_BACKWARD_TEXT}",
    "args0": [
      {
        "type": "field_variable",
        "name": "NAME",
        "variable": "myRobot"
      },
      {
        "type": "input_value",
        "name": "ROBOTVAR",
        "check": "Number"
      }
    ],
    "previousStatement": null,
    "nextStatement": null,
    "colour": "%{BKY_ROBOT_MOTORS_HUE}",
    "tooltip": "%{BKY_MOVE_BACKWARD_TOOLTIP}",
    "helpUrl": ""
  }

  Blockly.Blocks['move_backward'] = {
    init: function() {
      this.jsonInit(moveBackwardBlock);

    }
  };

  Blockly.Python['move_backward'] = function(block) {
    var variable_name = Blockly.Python.variableDB_.getName(block.getFieldValue('NAME'), Blockly.Variables.NAME_TYPE);
    var value_robotvar = Blockly.Python.valueToCode(block, 'ROBOTVAR', Blockly.Python.ORDER_ATOMIC);

    var code = variable_name + '.retroceder(' + value_robotvar + ')\n';
    return code;
  };
}



function initMoveForwardBlock(){
  var moveForwardBlock = {
    "type": "move_forward",
    "message0": "%{BKY_MOVE_FORWARD_TEXT}",
    "args0": [
      {
        "type": "field_variable",
        "name": "NAME",
        "variable": "myRobot"
      },
      {
        "type": "input_value",
        "name": "ROBOTVAR",
        "check": "Number"
      }
    ],
    "previousStatement": null,
    "nextStatement": null,
    "colour": "%{BKY_ROBOT_MOTORS_HUE}",
    "tooltip": "%{BKY_MOVE_FORWARD_TOOLTIP}",
    "helpUrl": ""
  }

  Blockly.Blocks['move_forward'] = {
    init: function() {
      this.jsonInit(moveForwardBlock);

    }
  };

  Blockly.Python['move_forward'] = function(block) {
    var variable_name = Blockly.Python.variableDB_.getName(block.getFieldValue('NAME'), Blockly.Variables.NAME_TYPE);
    var value_robotvar = Blockly.Python.valueToCode(block, 'ROBOTVAR', Blockly.Python.ORDER_ATOMIC);

    var code = variable_name + '.avanzar(' + value_robotvar + ')\n';
    return code;
  };
}

function initReadIRBlock(){
  var readIRBlock = {
    "type": "read_ir",
    "message0": "%{BKY_READ_IR_TEXT}",
    "args0": [
      {
        "type": "field_variable",
        "name": "ROBOT_VAR",
        "variable": "myRobot"
      }
    ],
    "output": null,
    "colour": "%{BKY_ROBOT_SENSORS_HUE}",
    "tooltip": "%{BKY_READ_IR_TOOLTIP}",
    "helpUrl": ""
  };

  Blockly.Blocks['read_ir'] = {
    init: function() {
      this.jsonInit(readIRBlock);
    }
  };

  Blockly.Python['read_ir'] = function(block) {
    var variable_robot_var = Blockly.Python.variableDB_.getName(block.getFieldValue('ROBOT_VAR'), Blockly.Variables.NAME_TYPE);

    var code = variable_robot_var + '.get_message()\n';

    return [code, Blockly.Python.ORDER_ATOMIC];
  };
}

function initRobotInstanceBlock(){
  var robotInstanceBlock = {
    "type": "robot_instance",
    "message0": "Create robot %1",
    "args0": [
      /*{
        "type": "field_variable",
        "name": "ROBOT_VAR",
        "variable": "myRobot"
      },*/
      {
        "type": "field_dropdown",
        "name": "OPTIONS",
        "options": [
          [
            "MBot",
            "mbot"
          ]
        ]
      }
    ],
    "output": null,
    "tooltip": "",
    "colour": "%{BKY_ROBOT_MOTORS_HUE}",
    "helpUrl": ""
  };

  Blockly.Blocks['robot_instance'] = {
    init: function() {
      this.jsonInit(robotInstanceBlock);
    }
  };

  Blockly.Python['robot_instance'] = function(block) {
 
    var dropdown_options = Blockly.Python.variableDB_.getName(block.getFieldValue('OPTIONS'), Blockly.Variables.NAME_TYPE)
    
    if(dropdown_options === "mbot"){
      var code = 'halduino\n';

    }else {
      var code = 'myRobot\n';
    } 

    return [code];
  };
}

function initStartBlock(){
    var startBlock = {
      "type": "start",
      "message0": "%{BKY_START_TEXT}",
      "nextStatement": null,
      "colour": "%{BKY_ROBOT_START_HUE}",
      "tooltip": "%{BKY_START_TOOLTIP}",
      "helpUrl": ""
    }
  
    Blockly.Blocks['start'] = {
      init: function() {
        Blockly.BlockSvg.START_HAT = true; 
        this.jsonInit(startBlock);
  
      }
    };
  
    Blockly.Python['start'] = function(block) {
        return "\n";
    };
}

function initStopBlock(){
  var stopBlock = {
    "type": "stop_robot",
    "message0": "%{BKY_STOP_ROBOT_TEXT}",
    "args0": [
      {
        "type": "field_variable",
        "name": "NAME",
        "variable": "myRobot"
      }
    ],
    "inputsInline": true,
    "previousStatement": null,
    "nextStatement": null,
    "colour": "%{BKY_ROBOT_MOTORS_HUE}",
    "tooltip": "%{BKY_STOP_ROBOT_TOOLTIP}",
    "helpUrl": ""
  };

  Blockly.Blocks['stop_robot'] = {
    init: function() {
      this.jsonInit(stopBlock);
    }
  };

  Blockly.Python['stop_robot'] = function(block) {
    var variable_name = Blockly.Python.variableDB_.getName(block.getFieldValue('NAME'), Blockly.Variables.NAME_TYPE);

    var code = variable_name + '.parar()\n';
    return code;
  };
}
  
function initTurnLeftBlock(){
  var turnLeftBlock = {
    "type": "turn_left",
    "message0": "%{BKY_TURN_LEFT_TEXT}",
    "args0": [
      {
        "type": "field_variable",
        "name": "NAME",
        "variable": "myRobot"
      },
      {
        "type": "input_value",
        "name": "ROBOTVAR",
        "check": "Number"
      }
    ],
    "previousStatement": null,
    "nextStatement": null,
    "colour": "%{BKY_ROBOT_MOTORS_HUE}",
    "tooltip": "%{BKY_TURN_LEFT_TOOLTIP}",
    "helpUrl": ""
  }

  Blockly.Blocks['turn_left'] = {
    init: function() {
      this.jsonInit(turnLeftBlock);

    }
  };

  Blockly.Python['turn_left'] = function(block) {
    var variable_name = Blockly.Python.variableDB_.getName(block.getFieldValue('NAME'), Blockly.Variables.NAME_TYPE);
    var value_robotvar = Blockly.Python.valueToCode(block, 'ROBOTVAR', Blockly.Python.ORDER_ATOMIC);

    var code = variable_name + '.set_speed_engines(' + -value_robotvar/2 + ', ' + value_robotvar + ')\n';
    return code;
  };
}


function initTurnRightBlock(){
  var turnRightBlock = {
    "type": "turn_right",
    "message0": "%{BKY_TURN_RIGHT_TEXT}",
    "args0": [
      {
        "type": "field_variable",
        "name": "NAME",
        "variable": "myRobot"
      },
      {
        "type": "input_value",
        "name": "ROBOTVAR",
        "check": "Number"
      }
    ],
    "previousStatement": null,
    "nextStatement": null,
    "colour": "%{BKY_ROBOT_MOTORS_HUE}",
    "tooltip": "%{BKY_TURN_RIGHT_HUE}",
    "helpUrl": ""
  }

  Blockly.Blocks['turn_right'] = {
    init: function() {
      this.jsonInit(turnRightBlock);

    }
  };

  Blockly.Python['turn_right'] = function(block) {
    var variable_name = Blockly.Python.variableDB_.getName(block.getFieldValue('NAME'), Blockly.Variables.NAME_TYPE);
    var value_robotvar = Blockly.Python.valueToCode(block, 'ROBOTVAR', Blockly.Python.ORDER_ATOMIC);

    var code = variable_name + '.set_speed_engines(' + -value_robotvar + ', ' + value_robotvar/2 + ')\n';
    return code;
  };
}


function initSetLedsBlock(){
  var setLedsBlock = {
    "type": "set_leds",
    "message0": "%{BKY_SET_LEDS_TEXT}",
    "args0": [
      {
        "type": "field_variable",
        "name": "NAME",
        "variable": "myRobot"
      },
      {
        "type": "field_dropdown",
        "name": "OPTIONS",
        "options": [
          [
            "Red",
            "red"
          ],
          [
            "Green",
            "green"
          ],
          [
            "Blue",
            "blue"
          ]
        ]
      }
    ],
    "inputsInline": true,
    "previousStatement": null,
    "nextStatement": null,
    "colour": "%{BKY_ROBOT_SENSORS_HUE}",
    "tooltip": "%{BKY_SET_LEDS_TOOLTIP}",
    "helpUrl": ""
  }

  Blockly.Blocks['set_leds'] = {
    init: function() {
      this.jsonInit(setLedsBlock);

    }
  };

  Blockly.Python['set_leds'] = function(block) {
    var variable_name = Blockly.Python.variableDB_.getName(block.getFieldValue('NAME'), Blockly.Variables.NAME_TYPE);
    var dropdown_options = Blockly.Python.variableDB_.getName(block.getFieldValue('OPTIONS'), Blockly.Variables.NAME_TYPE)
    var r, g, b;
    if(dropdown_options === "red"){
      r = 255;
      g = 0;
      b = 0;
    }else if(dropdown_options === "green"){
      r = 0;
      g = 255;
      b = 0;
    } else if (dropdown_options === "blue") {
      r = 0;
      g = 0;
      b = 255;
    } else {
      r = 255;
      g = 255;
      b = 255;
    }

    var code = variable_name + '.set_leds(1, ' + r + ', ' + g + ', ' + b + ')\n';
    return code;
  };
}

function initLightSensorBlock(){
  var lightSensorBlock = {
    "type": "light_sensor",
    "message0": "%{BKY_GET_LIGHT_SENSOR_TEXT}",
    "args0": [
      {
        "type": "field_variable",
        "name": "ROBOTVAR",
        "variable": "myRobot"
      }
    ],
    "output": null,
    "colour": "%{BKY_ROBOT_SENSORS_HUE}",
    "tooltip": "%{BKY_GET_LIGHT_SENSOR_TOOLTIP}",
    "helpUrl": ""
  };

  Blockly.Blocks['light_sensor'] = {
    init: function() {
      this.jsonInit(lightSensorBlock);

    }
  };

  Blockly.Python['light_sensor'] = function(block) {
    var variable_robotvar = Blockly.Python.variableDB_.getName(block.getFieldValue('ROBOTVAR'), Blockly.Variables.NAME_TYPE);

    var code = variable_robotvar + '.get_light_sensor()\n';

    return [code, Blockly.Python.ORDER_NONE];
  };
}

function initIsButtonPressedBlock(){
  var isButtonPressedBlock = {
    "type": "button_pressed",
    "message0": "%{BKY_IS_BUTTON_PRESSED_TEXT}",
    "args0": [
      {
        "type": "field_variable",
        "name": "ROBOTVAR",
        "variable": "myRobot"
      }
    ],
    "output": null,
    "colour": "%{BKY_ROBOT_SENSORS_HUE}",
    "tooltip": "%{BKY_IS_BUTTON_PRESSED_TOOLTIP}",
    "helpUrl": ""
  };

  Blockly.Blocks['button_pressed'] = {
    init: function() {
      this.jsonInit(isButtonPressedBlock);

    }
  };

  Blockly.Python['button_pressed'] = function(block) {
    var variable_robotvar = Blockly.Python.variableDB_.getName(block.getFieldValue('ROBOTVAR'), Blockly.Variables.NAME_TYPE);

    var code = variable_robotvar + '.is_button_pressed()\n';

    return [code, Blockly.Python.ORDER_NONE];
  };
}

function initIsButtonReleasedBlock(){
  var isButtonReleasedBlock = {
    "type": "button_released",
    "message0": "%{BKY_IS_BUTTON_RELEASED_TEXT}",
    "args0": [
      {
        "type": "field_variable",
        "name": "ROBOTVAR",
        "variable": "myRobot"
      }
    ],
    "output": null,
    "colour": "%{BKY_ROBOT_SENSORS_HUE}",
    "tooltip": "%{BKY_IS_BUTTON_RELEASED_TOOLTIP}",
    "helpUrl": ""
  };

  Blockly.Blocks['button_released'] = {
    init: function() {
      this.jsonInit(isButtonReleasedBlock);

    }
  };

  Blockly.Python['button_released'] = function(block) {
    var variable_robotvar = Blockly.Python.variableDB_.getName(block.getFieldValue('ROBOTVAR'), Blockly.Variables.NAME_TYPE);

    var code = variable_robotvar + '.is_button_released()\n';

    return [code, Blockly.Python.ORDER_NONE];
  };
}

function initPlayBuzzerBlock(){
  var playBuzzerBlock = {
    "type": "play_buzzer",
    "message0": "%{BKY_PLAY_BUZZER_TEXT}",
    "args0": [
      {
        "type": "field_variable",
        "name": "ROBOTVAR",
        "variable": "myRobot"
      },
      {
        "type": "input_value",
        "name": "TONE",
        "check": "Number"
      },
      {
        "type": "input_value",
        "name": "LENGTH",
        "check": "Number"
      }
    ],
    "inputsInline": true,
    "previousStatement": null,
    "nextStatement": null,
    "colour": "%{BKY_ROBOT_SENSORS_HUE}",
    "tooltip": "%{BKY_PLAY_BUZZER_TOOLTIP}",
    "helpUrl": ""
  };

  Blockly.Blocks['play_buzzer'] = {
    init: function() {
      this.jsonInit(playBuzzerBlock);

    }
  };

  Blockly.Python['play_buzzer'] = function(block) {
    var variable_robotvar = Blockly.Python.variableDB_.getName(block.getFieldValue('ROBOTVAR'), Blockly.Variables.NAME_TYPE);
    var value_tone = Blockly.Python.valueToCode(block, 'TONE', Blockly.Python.ORDER_ATOMIC);
    var value_length = Blockly.Python.valueToCode(block, 'LENGTH', Blockly.Python.ORDER_ATOMIC);

    var code = variable_robotvar + '.play_buzzer(' + value_tone + ', ' + value_length + ')\n';

    return code;
  };
}

function initDrawStringBlock(){
  var drawStringBlock = {
    "type": "draw_string",
    "message0": "%{BKY_DRAW_STRING_TEXT}",
    "args0": [
      {
        "type": "field_variable",
        "name": "ROBOTVAR",
        "variable": "myRobot"
      },
      {
        "type": "field_input",
        "name": "TODRAW",
        "text": "hola"
      }
    ],
    "inputsInline": true,
    "previousStatement": null,
    "nextStatement": null,
    "colour": "%{BKY_ROBOT_TOOLS_HUE}",
    "tooltip": "%{BKY_DRAW_STRING_TOOLTIP}",
    "helpUrl": ""
  };

  Blockly.Blocks['draw_string'] = {
    init: function() {
      this.jsonInit(drawStringBlock);

    }
  };

  Blockly.Python['draw_string'] = function(block) {
    var variable_robotvar = Blockly.Python.variableDB_.getName(block.getFieldValue('ROBOTVAR'), Blockly.Variables.NAME_TYPE);
    var text = block.getFieldValue('TODRAW');

    var code = variable_robotvar + '.draw_string("' + text + '")\n';

    return code;
  };
}

