/* CUSTOM BLOCKLY BLOCKS MADE FOR PYTHON */

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

    var code = 'console.log(' + value_to_log + ');\n';
    return code;
  };

  Blockly.Python['logs'] = function(block) {
    var value_to_log = Blockly.Python.valueToCode(block, 'TO_LOG', Blockly.Python.ORDER_ATOMIC);

    var code = 'print ' + '(' + value_to_log + ')' + '\r\n';
    return code;
  };
}

function initFollowLineBlock(){
  var followLineBlock = {
    "type": "follow_line",
    "message0": "%1 Follow line with color %2 at speed %3",
    "args0": [
      {
        "type": "field_variable",
        "name": "ROBOT",
        "variable": "myRobot"
      },
      {
        "type": "field_input",
        "name": "COLOUR",
        "text": "white"
      },
      {
        "type": "input_value",
        "name": "INPUT_SPEED"
      }
    ],
    "previousStatement": null,
    "nextStatement": null,
    "colour": "%{BKY_VARIABLES_DYNAMIC_HUE}",
    "tooltip": "Follow line, pass color and speed",
    "helpUrl": ""
  };

  Blockly.Blocks['follow_line'] = {
    init: function() {
      this.jsonInit(followLineBlock);
    }
  };

  Blockly.Python['follow_line'] = function(block) {
    var variable_robot = Blockly.Python.variableDB_.getName(block.getFieldValue('ROBOT'), Blockly.Variables.NAME_TYPE);
    var text_colour = block.getFieldValue('COLOUR');
    var value_speed = Blockly.Python.valueToCode(block, 'INPUT_SPEED', Blockly.Python.ORDER_ATOMIC);

    var code = variable_robot + '.followLine("' + text_colour.toString() + '",' + value_speed + ');\n';
    return code;
  };
}

function initGetAngularSpeedBlock(){
  var getAngular = {
    "type": "getAngularSpeed",
    "message0": "%{BKY_GETANGULARSPEED_TEXT}",
    "args0": [
      {
        "type": "field_variable",
        "name": "ROBOTVAR",
        "variable": "myRobot"
      }
    ],
    "output": null,
    "colour": "%{BKY_ROBOT_MOTORS_HUE}",
    "tooltip": "%{BKY_GETANGULARSPEED_TOOLTIP}",
    "helpUrl": ""
  };

  Blockly.Blocks['getAngularSpeed'] = {
    init: function() {
      this.jsonInit(getAngular);
    }
  };

  Blockly.Python['getAngularSpeed'] = function(block) {
    var variable_robotvar = Blockly.Python.variableDB_.getName(block.getFieldValue('ROBOTVAR'), Blockly.Variables.NAME_TYPE);

    var code = variable_robotvar + '.getW()';

    return [code, Blockly.Python.ORDER_ATOMIC];
  };
}

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

    var code = variable_robotvar + '.getDistance()';

    return [code, Blockly.Python.ORDER_NONE];
  };

  Blockly.Python['get_distance'] = function(block) {
    var variable_robotvar = Blockly.Python.variableDB_.getName(block.getFieldValue('ROBOTVAR'), Blockly.Variables.NAME_TYPE);

    var code = variable_robotvar + '.leerUltrasonido()\r\n';

    return [code, Blockly.Python.ORDER_NONE];
  };
}

function initGetDistancesBlock(){
  var getDistancesBlock = {
    "type": "get_distances",
    "message0": "%{BKY_GET_DISTANCES_TEXT}",
    "args0": [
      {
        "type": "field_variable",
        "name": "ROBOTVAR",
        "variable": "myRobot"
      }
    ],
    "output": null,
    "colour": "%{BKY_ROBOT_SENSORS_HUE}",
    "tooltip": "%{BKY_GET_DISTANCES_TOOLTIP}",
    "helpUrl": ""
  };

  Blockly.Blocks['get_distances'] = {
    init: function() {
      this.jsonInit(getDistancesBlock);

    }
  };

  Blockly.Python['get_distances'] = function(block) {
    var variable_robotvar = Blockly.Python.variableDB_.getName(block.getFieldValue('ROBOTVAR'), Blockly.Variables.NAME_TYPE);

    var code = variable_robotvar + '.getDistances()';

    return [code, Blockly.Python.ORDER_NONE];
  };
}

function initGetImageBlock(){
  var getImageBlock = {
    "type": "get_image",
    "message0": "%{BKY_GET_IMAGE_TEXT}",
    "args0": [
      {
        "type": "field_variable",
        "name": "ROBOTVAR",
        "variable": "myRobot"
      }
    ],
    "output": null,
    "colour": "%{BKY_ROBOT_CAMERA_HUE}",
    "tooltip": "%{BKY_GET_IMAGE_TOOLTIP}",
    "helpUrl": ""
  };

  Blockly.Blocks['get_image'] = {
    init: function() {
      this.jsonInit(getImageBlock);

    }
  };

  Blockly.Python['get_image'] = function(block) {
    var variable_robotvar = Blockly.Python.variableDB_.getName(block.getFieldValue('ROBOTVAR'), Blockly.Variables.NAME_TYPE);

    var code = variable_robotvar.toString() + '.getImage()';

    return [code, Blockly.Python.ORDER_ATOMIC];
  };

  Blockly.Python['get_image'] = function(block) {
    var variable_robotvar = Blockly.Python.variableDB_.getName(block.getFieldValue('ROBOTVAR'), Blockly.Variables.NAME_TYPE);

    var code = variable_robotvar + '.leerIRSigueLineas()\r\n';

    return [code, Blockly.Python.ORDER_ATOMIC];
  };
}

function initGetLateralSpeed(){
  var getLateral = {
    "type": "getLateralSpeed",
    "message0": "%{BKY_GETLATERALSPEED_TEXT}",
    "args0": [
      {
        "type": "field_variable",
        "name": "ROBOTVAR",
        "variable": "myRobot"
      }
    ],
    "output": null,
    "colour": "%{BKY_ROBOT_MOTORS_HUE}",
    "tooltip": "%{BKY_GETLATERALSPEED_TOOLTIP}",
    "helpUrl": ""
  };

  Blockly.Blocks['getLateralSpeed'] = {
    init: function() {
      this.jsonInit(getLateral);
    }
  };

  Blockly.Python['getLateralSpeed'] = function(block) {
    var variable_robotvar = Blockly.Python.variableDB_.getName(block.getFieldValue('ROBOTVAR'), Blockly.Variables.NAME_TYPE);

    var code = variable_robotvar + '.getL()';

    return [code, Blockly.Python.ORDER_ATOMIC];
  };
}

function initGetLinearSpeedBlock(){
  var getLinear = {
    "type": "getLinearSpeed",
    "message0": "%{BKY_GETLINEARSPEED_TEXT}",
    "args0": [
      {
        "type": "field_variable",
        "name": "ROBOTVAR",
        "variable": "myRobot"
      }
    ],
    "output": null,
    "colour": "%{BKY_ROBOT_MOTORS_HUE}",
    "tooltip": "%{BKY_GETLINEARSPEED_TOOLTIP}",
    "helpUrl": ""
  };

  Blockly.Blocks['getLinearSpeed'] = {
    init: function() {
      this.jsonInit(getLinear);
    }
  };

  Blockly.Python['getLinearSpeed'] = function(block) {
    var variable_robotvar = Blockly.Python.variableDB_.getName(block.getFieldValue('ROBOTVAR'), Blockly.Variables.NAME_TYPE);

    var code = variable_robotvar + '.getV()';

    return [code, Blockly.Python.ORDER_ATOMIC];
  };
}

function initGetObjectColorBlock(){
  var getObjectColorBlock = {
    "type": "get_objcolor",
    "message0": "%{BKY_GET_OBJCOLOR_TEXT}",
    "args0": [
      {
        "type": "field_variable",
        "name": "ROBOTVAR",
        "variable": "myRobot"
      },
      {
        "type": "field_dropdown",
        "name": "OPTIONS",
        "options": [
          [
            "centerX",
            "X"
          ],
          [
            "centerY",
            "Y"
          ],
          [
            "area",
            "AREA"
          ]
        ]
      },
      {
        "type": "field_input",
        "name": "COLOUR",
        "text": "blue"
      }
    ],
    "output": null,
    "colour": "%{BKY_ROBOT_CAMERA_HUE}",
    "tooltip": "%{BKY_GET_OBJCOLOR_TOOLTIP}",
    "helpUrl": ""
  };

  Blockly.Blocks['get_objcolor'] = {
    init: function() {
      this.jsonInit(getObjectColorBlock);

    }
  };

  Blockly.Python['get_objcolor'] = function(block) {
    var variable_robotvar = Blockly.Python.variableDB_.getName(block.getFieldValue('ROBOTVAR'), Blockly.Variables.NAME_TYPE);
    var dropdown_options = block.getFieldValue('OPTIONS');
    var text_colour = block.getFieldValue('COLOUR');
    var code = '';

    if(dropdown_options === "X"){
      code = variable_robotvar + '.getObjectColor("' + text_colour +  '").center[0];\n';
    }else if(dropdown_options === "Y"){
      code = variable_robotvar + '.getObjectColor("' + text_colour +  '").center[1];\n';
    }else{
      code = variable_robotvar + '.getObjectColor("' + text_colour +  '").area;\n';
    }

    return [code, Blockly.Python.ORDER_ATOMIC];
  };

  Blockly.Python['get_objcolor'] = function(block) {
    var variable_robotvar = Blockly.Python.variableDB_.getName(block.getFieldValue('ROBOTVAR'), Blockly.Variables.NAME_TYPE);
    var dropdown_options = block.getFieldValue('OPTIONS');
    var text_colour = block.getFieldValue('COLOUR');
    var code = '';

    if(dropdown_options === "X"){
      code = variable_robotvar + '.damePosicionDeObjetoDeColor("' + text_colour +  '")[0][0];\n';
    }else if(dropdown_options === "Y"){
      code = variable_robotvar + '.damePosicionDeObjetoDeColor("' + text_colour +  '")[0][1];\n';
    }else{
      code = variable_robotvar + '.damePosicionDeObjetoDeColor("' + text_colour +  '")[1];\n';
    }

    return [code, Blockly.Python.ORDER_NONE];
  };
}

function initGetPositionBlock(){
  var getPositionBlock = {
    "type": "get_position",
    "message0": "%{BKY_GET_POSITION_TEXT}",
    "args0": [
      {
        "type": "field_dropdown",
        "name": "POSITION_OPTIONS",
        "options": [
          [
            "x",
            "POSX"
          ],
          [
            "y",
            "POSY"
          ],
          [
            "z",
            "POSZ"
          ],
          [
            "theta",
            "ROTATION"
          ]
        ]
      },
      {
        "type": "field_variable",
        "name": "ROBOTVAR",
        "variable": "myRobot"
      }
    ],
    "output": null,
    "colour": "%{BKY_ROBOT_SENSORS_HUE}",
    "tooltip": "%{BKY_GET_POSITION_TOOLTIP}",
    "helpUrl": ""
  };

  Blockly.Blocks['get_position'] = {
    init: function() {
      this.jsonInit(getPositionBlock);

    }
  };

  Blockly.Python['get_position'] = function(block) {
    var dropdown_position_options = block.getFieldValue('POSITION_OPTIONS');
    var variable_robotvar = Blockly.Python.variableDB_.getName(block.getFieldValue('ROBOTVAR'), Blockly.Variables.NAME_TYPE);
    var code = '';

    if(dropdown_position_options === "POSX"){
      code = variable_robotvar + '.getPosition().x';
    }else if(dropdown_position_options === "POSY"){
      code = variable_robotvar + '.getPosition().z';
    }else if(dropdown_position_options === "POSZ"){
      code = variable_robotvar + '.getPosition().y';
    }else{
      code = variable_robotvar + '.getPosition().theta';
    }
    return [code, Blockly.Python.ORDER_ATOMIC];
  };
}

function initGetRotationBlock(){
  var getRotation = {
    "type": "getRotation",
    "message0": "Get Rotation for %1",
    "args0": [
      {
        "type": "field_variable",
        "name": "ROBOTVAR",
        "variable": "myRobot"
      }
    ],
    "output": null,
    "colour": "%{BKY_VARIABLES_DYNAMIC_HUE}",
    "tooltip": "",
    "helpUrl": ""
  };

  Blockly.Blocks['getRotation'] = {
    init: function() {
      this.jsonInit(getRotation);
    }
  };

  Blockly.Python['getRotation'] = function(block) {
    var variable_robotvar = Blockly.Python.variableDB_.getName(block.getFieldValue('ROBOTVAR'), Blockly.Variables.NAME_TYPE);

    var code = variable_robotvar + '.getRotation()';

    return [code, Blockly.Python.ORDER_ATOMIC];
  };
}

function intiLandBlock(){
    var landBlock = {
      "type": "land",
      "message0": "%{BKY_LAND_TEXT}",
      "args0": [
        {
          "type": "field_variable",
          "name": "ROBOT_VAR",
          "variable": "myRobot"
        }
      ],
      "previousStatement": null,
      "nextStatement": null,
      "colour": "%{BKY_ROBOT_MOTORS_HUE}",
      "tooltip": "%{BKY_SET_LAND_TOOLTIP}",
      "helpUrl": ""
    }
  
    Blockly.Blocks['land'] = {
      init: function() {
        this.jsonInit(landBlock);
  
      }
    };
    

     Blockly.Python['land'] = function(block) {
       var robotvar = Blockly.Python.variableDB_.getName(block.getFieldValue('ROBOT_VAR'), Blockly.Variables.NAME_TYPE);

      var code = robotvar + '.setL(-3); \nawait sleep(0.4); \n'+robotvar + '.setL(0);\n';
      return code;
    };
  
  
    Blockly.Python['land'] = function(block) {
      var robotvar = Blockly.Python.variableDB_.getName(block.getFieldValue('ROBOT_VAR'), Blockly.Variables.NAME_TYPE);
      //var value = Blockly.Python.valueToCode(block, 'VALUE', Blockly.Python.ORDER_ATOMIC);
  
      var code = robotvar + '.aterrizar() \r\n' + 'time.sleep(0.5)\r\n';
      return code;
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

    var code = variable_name + '.setV(-' + value_robotvar + '); \n';
    return code;
  };

  Blockly.Python['move_backward'] = function(block) {
    var variable_name = Blockly.Python.variableDB_.getName(block.getFieldValue('NAME'), Blockly.Variables.NAME_TYPE);
    var value_robotvar = Blockly.Python.valueToCode(block, 'ROBOTVAR', Blockly.Python.ORDER_ATOMIC);

    var code = variable_name + '.retroceder(' + value_robotvar + ')\r\n';
    return code;
  };
}

function initMoveBackwardToBlock(){
    var moveBackWardToBlock = {
      "type": "move_backward_to",
      "message0": "%{BKY_MOVE_BACKWARD_TO_TEXT}",
      "args0": [
        {
          "type": "field_variable",
          "name": "NAME",
          "variable": "myRobot"
        },
        {
          "type": "input_value",
          "name": "DISTANCE",
          "check": "Number"
        }
      ],
      "inputsInline": true,
      "previousStatement": null,
      "nextStatement": null,
      "colour": "%{BKY_ROBOT_MOTORS_HUE}",
      "tooltip": "%{BKY_MOVE_BACKWARD_TO_TOOLTIP}",
      "helpUrl": ""
    }
  
    Blockly.Blocks['move_backward_to'] = {
      init: function() {
        this.jsonInit(moveBackWardToBlock);
  
      }
    };
  
    Blockly.Python['move_backward_to'] = function(block) {
      var variable_name = Blockly.Python.variableDB_.getName(block.getFieldValue('NAME'), Blockly.Variables.NAME_TYPE);
      var value_distance = Blockly.Python.valueToCode(block, 'DISTANCE', Blockly.Python.ORDER_ATOMIC);
      var vel = 1;
      var t = value_distance/vel;
      vel  = vel*-1;
      var code = variable_name + '.setV('+vel+'); \nawait sleep('+t+');\n'+variable_name + '.setV(0); \n';
      return code;
    };
  
    Blockly.Python['move_backward_to'] = function(block) {
      var variable_name = Blockly.Python.variableDB_.getName(block.getFieldValue('NAME'), Blockly.Variables.NAME_TYPE);
      var value_distance = Blockly.Python.valueToCode(block, 'DISTANCE', Blockly.Python.ORDER_ATOMIC);
  
      var code = variable_name + '.retroceder_hasta(' + value_distance + ')\r\n';
      return code;
    };
}

function initMoveBlock(){
  var moveBlock = {
    "type": "move_combined",
    "message0": "%{BKY_MOVE_COMBINED_TEXT}",
    "args0": [
      {
        "type": "field_variable",
        "name": "NAME",
        "variable": "myRobot"
      },
      {
        "type": "input_value",
        "name": "LINEARSPEED",
        "check": "Number"
      },
      {
        "type": "input_value",
        "name": "ANGULARSPEED",
        "check": "Number"
      }
    ],
    "inputsInline": true,
    "previousStatement": null,
    "nextStatement": null,
    "colour": "%{BKY_ROBOT_MOTORS_HUE}",
    "tooltip": "%{BKY_MOVE_COMBINED_TOOLTIP}",
    "helpUrl": ""
  }

  Blockly.Blocks['move_combined'] = {
    init: function() {
      this.jsonInit(moveBlock);

    }
  };

  Blockly.Python['move_combined'] = function(block) {
    var variable_name = Blockly.Python.variableDB_.getName(block.getFieldValue('NAME'), Blockly.Variables.NAME_TYPE);
    var value_linear = Blockly.Python.valueToCode(block, 'LINEARSPEED', Blockly.Python.ORDER_ATOMIC);
    var value_angular = Blockly.Python.valueToCode(block, 'ANGULARSPEED', Blockly.Python.ORDER_ATOMIC);

    var code = variable_name + '.move(' + value_linear + ',' + value_angular + ',0); \n';
    return code;
  };

  Blockly.Python['move_combined'] = function(block) {
    var variable_name = Blockly.Python.variableDB_.getName(block.getFieldValue('NAME'), Blockly.Variables.NAME_TYPE);
    var value_linear = Blockly.Python.valueToCode(block, 'LINEARSPEED', Blockly.Python.ORDER_ATOMIC);
    var value_angular = Blockly.Python.valueToCode(block, 'ANGULARSPEED', Blockly.Python.ORDER_ATOMIC);

    var code = "Me han dicho que me mueva a linSpeed --> " + value_linear + ' y angSpeed --> ' + value_angular + '\r\n';
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

    var code = variable_name + '.setV(' + value_robotvar + '); \n';
    return code;
  };

  Blockly.Python['move_forward'] = function(block) {
    var variable_name = Blockly.Python.variableDB_.getName(block.getFieldValue('NAME'), Blockly.Variables.NAME_TYPE);
    var value_robotvar = Blockly.Python.valueToCode(block, 'ROBOTVAR', Blockly.Python.ORDER_ATOMIC);

    var code = variable_name + '.avanzar(' + value_robotvar + ')\r\n';
    return code;
  };
}

function initMoveForwardToBlock(){
    var moveForwardToBlock = {
      "type": "move_forward_to",
      "message0": "%{BKY_MOVE_FORWARD_TO_TEXT}",
      "args0": [
        {
          "type": "field_variable",
          "name": "NAME",
          "variable": "myRobot"
        },
        {
          "type": "input_value",
          "name": "DISTANCE",
          "check": "Number"
        }
      ],
      "inputsInline": true,
      "previousStatement": null,
      "nextStatement": null,
      "colour": "%{BKY_ROBOT_MOTORS_HUE}",
      "tooltip": "%{BKY_MOVE_FORWARD_TO_TOOLTIP}",
      "helpUrl": ""
    }
  
    Blockly.Blocks['move_forward_to'] = {
      init: function() {
        this.jsonInit(moveForwardToBlock);
  
      }
    };
  
    Blockly.Python['move_forward_to'] = function(block) {
      var variable_name = Blockly.Python.variableDB_.getName(block.getFieldValue('NAME'), Blockly.Variables.NAME_TYPE);
      var value_distance = Blockly.Python.valueToCode(block, 'DISTANCE', Blockly.Python.ORDER_ATOMIC);
      var vel = 1;
      var t = value_distance/vel;
      var code = variable_name + '.setV('+vel+'); \nawait sleep('+t+');\n'+variable_name + '.setV(0); \n';
      return code;
    };
  
    Blockly.Python['move_forward_to'] = function(block) {
      var variable_name = Blockly.Python.variableDB_.getName(block.getFieldValue('NAME'), Blockly.Variables.NAME_TYPE);
      var value_distance = Blockly.Python.valueToCode(block, 'DISTANCE', Blockly.Python.ORDER_ATOMIC);
  
      var code = variable_name + '.avanzar_hasta(' + value_distance + ')\r\n';
      return code;
    };
}
  
function initPrintOnCanvasBlock(){
  var imgToCanvasBlock = {
    "type": "imgto_canvas",
    "message0": "%{BKY_IMGTO_CANVAS_TEXT}",
    "args0": [
      {
        "type": "field_input",
        "name": "canvas_id",
        "text": "outputCanvas"
      },
      {
        "type": "input_value",
        "name": "img_input"
      }
    ],
    "previousStatement": null,
    "nextStatement": null,
    "colour": "%{BKY_ROBOT_TOOLS_HUE}",
    "tooltip": "%{BKY_IMGTO_CANVAS_TOOLTIP}",
    "helpUrl": ""
  };

  Blockly.Blocks['imgto_canvas'] = {
    init: function() {
      this.jsonInit(imgToCanvasBlock);
    }
  };

  Blockly.Python['imgto_canvas'] = function(block) {
    var text_canvas_id = block.getFieldValue('canvas_id');
    var value_img_input = Blockly.Python.valueToCode(block, 'img_input', Blockly.Python.ORDER_ATOMIC);
    // ToDo: Assemble Python into code variable.
    var code = 'cv.imshow("' + text_canvas_id + '", ' + value_img_input +');\n';
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
      },
      {
        "type": "field_input",
        "name": "NAME",
        "text": "white"
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
    var value_name = '"'+block.getFieldValue('NAME') +'"';

    var code = variable_robot_var + '.readIR(' + value_name + ')';

    return [code, Blockly.Python.ORDER_ATOMIC];
  };

  Blockly.Python['read_ir'] = function(block) {
    var variable_robot_var = Blockly.Python.variableDB_.getName(block.getFieldValue('ROBOT_VAR'), Blockly.Variables.NAME_TYPE);
    var value_name = Blockly.Python.valueToCode(block, 'NAME', Blockly.Python.ORDER_ATOMIC);

    var code = variable_robot_var + '.leerIRSigueLineas()\r\n';

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
            "PiBot",
            "pibot"
          ],
          [
            "Tello",
            "tello"
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
    return ["myRobot"];
  };
  /*Blockly.Python['robot_instance'] = function(block) {
    var text_robot_id = block.getFieldValue('ROBOT_ID');

    var code = 'new RobotI("' + text_robot_id + '")';

    return [code, Blockly.Python.ORDER_ATOMIC];
  };*/

  Blockly.Python['robot_instance'] = function(block) {
 
    var dropdown_options = Blockly.Python.variableDB_.getName(block.getFieldValue('OPTIONS'), Blockly.Variables.NAME_TYPE)
    
    if(dropdown_options === "pibot"){
      var code = 'PiBot()\r\n';

    }else if(dropdown_options === "tello"){
      var code = 'Tello("",9500)\r\n';
    } 

    return [code];
  };
}

function initSetIntervalBlock(){
  var setIntervalBlock = {
    "type": "set_interval",
    "message0": "%{BKY_SET_INTERVAL_TEXT}",
    "args0": [
      {
        "type": "input_statement",
        "name": "TEXT"
      }
    ],
    "previousStatement": null,
    "colour": "%{BKY_LOOPS_HUE}",
    "tooltip": "%{BKY_SET_INTERVAL_TOOLTIP}",
    "helpUrl": ""
  };

  Blockly.Blocks['set_interval'] = {
    init: function() {
      this.jsonInit(setIntervalBlock);
    }
  };

  Blockly.Python['set_interval'] = function(block) {
    var statements_text = Blockly.Python.statementToCode(block, 'TEXT');

    var code = 'mainInterval = setIntervalSynchronous(async function(){\n' + statements_text + '},66);\n';
    return code;
  };

  Blockly.Python['set_interval'] = function(block) {
    var statements_text = Blockly.Python.statementToCode(block, 'TEXT');

    var code = 'while True:\n' + statements_text + '\ntime.sleep(0.1)\n';
    return code;
  };
}

function initSetLateralSpeedBlock(){
  var setLateralBlock = {
    "type": "set_lateral",
    "message0": "%{BKY_SET_LATERAL_TEXT}",
    "args0": [
      {
        "type": "field_variable",
        "name": "ROBOT_VAR",
        "variable": "myRobot"
      },
      {
        "type": "input_value",
        "name": "VALUE",
        "check": "Number"
      }
    ],
    "previousStatement": null,
    "nextStatement": null,
    "colour": "%{BKY_ROBOT_MOTORS_HUE}",
    "tooltip": "%{BKY_SET_LATERAL_TOOLTIP}",
    "helpUrl": ""
  }

  Blockly.Blocks['set_lateral'] = {
    init: function() {
      this.jsonInit(setLateralBlock);

    }
  };

  Blockly.Python['set_lateral'] = function(block) {
    var robotvar = Blockly.Python.variableDB_.getName(block.getFieldValue('ROBOT_VAR'), Blockly.Variables.NAME_TYPE);
    var value = Blockly.Python.valueToCode(block, 'VALUE', Blockly.Python.ORDER_ATOMIC);

    var code = robotvar + '.setL(' + value + '); \n';
    return code;
  };

}

function initSetTimeoutBlock(){
  var setTimeoutBlock = {
    "type": "set_timeout",
    "message0": "%{BKY_SET_TIMEOUT_TEXT}",
    "args0": [
      {
        "type": "field_number",
        "name": "TIME",
        "value": 0,
        "min": 0
      },
      {
        "type": "input_statement",
        "name": "TEXT"
      }
    ],
    "output": null,
    "colour": "%{BKY_ROBOT_TOOLS_HUE}",
    "tooltip": "%{BKY_SET_TIMEOUT_TOOLTIP}",
    "helpUrl": ""
  };

  Blockly.Blocks['set_timeout'] = {
    init: function() {
      this.jsonInit(setTimeoutBlock);
    }
  };

  Blockly.Python['set_timeout'] = function(block) {
    var number_name = block.getFieldValue('TIME');
    var statements_text = Blockly.Python.statementToCode(block, 'TEXT');

    var code = 'setTimeout(()=>{\n' + statements_text + '},' + number_name + ');\n';
    return [code, Blockly.Python.ORDER_ATOMIC];
  };

  Blockly.Python['set_timeout'] = function(block) {
    var number_name = parseInt(block.getFieldValue('TIME'));
    var statements_text = Blockly.Python.statementToCode(block, 'TEXT');
    var time_secs = number_name / 1000;
    var code = 'time.sleep(' + time_secs + ')\n' + statements_text + "\r\n";
    return code;
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
  
  
    Blockly.Python['start'] = function(block) {
        return "\n";
    };
}

function initStartRaycastersBlock(){
  var startRaycasterBlock = {
    "type": "start_rays",
    "message0": "%1 Start %2 infrared sensors at distance %3",
    "args0": [
      {
        "type": "field_variable",
        "name": "ROBOTVAR",
        "variable": "myRobot"
      },
      {
        "type": "field_number",
        "name": "NUMOFRAYS",
        "value": 0,
        "min": 1,
        "max": 31
      },
      {
        "type": "field_number",
        "name": "RAYDISTANCE",
        "value": 0,
        "min": 1,
        "max": 10
      }
    ],
    "previousStatement": null,
    "nextStatement": null,
    "colour": "%{BKY_VARIABLES_DYNAMIC_HUE}",
    "tooltip": "Start a given number of raycasters with a given distance",
    "helpUrl": ""
  };

  Blockly.Blocks['start_rays'] = {
    init: function() {
      this.jsonInit(startRaycasterBlock);

    }
  };

  Blockly.Python['start_rays'] = function(block) {
    var variable_robotvar = Blockly.Python.variableDB_.getName(block.getFieldValue('ROBOTVAR'), Blockly.Variables.NAME_TYPE);
    var number_numofrays = block.getFieldValue('NUMOFRAYS');
    var number_raydistance = block.getFieldValue('RAYDISTANCE');

    var code = variable_robotvar + '.startRaycasters(' + number_raydistance + ',' + number_numofrays + ');\n';
    return code;
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

    var code = variable_name + '.move(0, 0, 0);\n';
    return code;
  };


  Blockly.Python['stop_robot'] = function(block) {
    var variable_name = Blockly.Python.variableDB_.getName(block.getFieldValue('NAME'), Blockly.Variables.NAME_TYPE);

    var code = variable_name + '.parar()\r\n';
    return code;
  };
}

function initStopRaycastersBlock(){
  var stopRaycastersBlock = {
    "type": "stop_rays",
    "message0": "%1 Stop rays",
    "args0": [
      {
        "type": "field_variable",
        "name": "ROBOTVAR",
        "variable": "myRobot"
      }
    ],
    "previousStatement": null,
    "nextStatement": null,
    "colour": "%{BKY_VARIABLES_DYNAMIC_HUE}",
    "tooltip": "Stop all raycasters.",
    "helpUrl": ""
  };

  Blockly.Blocks['stop_rays'] = {
    init: function() {
      this.jsonInit(stopRaycastersBlock);
    }
  };

  Blockly.Python['stop_rays'] = function(block) {
    var variable_robotvar = Blockly.Python.variableDB_.getName(block.getFieldValue('ROBOTVAR'), Blockly.Variables.NAME_TYPE);
    var code = variable_robotvar + '.stopRaycasters();\n';
    return code;
  };
}

function initTakeOffBlock(){
    var takeOffBlock = {
      "type": "takeoff",
      "message0": "%{BKY_TAKEOFF_TEXT}",
      "args0": [
        {
          "type": "field_variable",
          "name": "ROBOT_VAR",
          "variable": "myRobot"
        }
      ],
      "previousStatement": null,
      "nextStatement": null,
      "colour": "%{BKY_ROBOT_MOTORS_HUE}",
      "tooltip": "%{BKY_TAKEOFF_TOOLTIP}",
      "helpUrl": ""
    }
  
    Blockly.Blocks['takeoff'] = {
      init: function() {
        this.jsonInit(takeOffBlock);
  
      }
    };
  
    Blockly.Python['takeoff'] = function(block) {
      var robotvar = Blockly.Python.variableDB_.getName(block.getFieldValue('ROBOT_VAR'), Blockly.Variables.NAME_TYPE);
  
      var code = robotvar + '.setL(3); \nawait sleep(0.5); \n'+robotvar + '.setL(0);\n';
      return code;
    };
  
  
    Blockly.Python['takeoff'] = function(block) {
      var robotvar = Blockly.Python.variableDB_.getName(block.getFieldValue('ROBOT_VAR'), Blockly.Variables.NAME_TYPE);
  
      var code = robotvar + '.despegar() \r\n' + 'time.sleep(0.5)\r\n';
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

    var code = variable_name + '.setW(' + value_robotvar + '); \n';
    return code;
  };

  Blockly.Python['turn_left'] = function(block) {
    var variable_name = Blockly.Python.variableDB_.getName(block.getFieldValue('NAME'), Blockly.Variables.NAME_TYPE);
    var value_robotvar = Blockly.Python.valueToCode(block, 'ROBOTVAR', Blockly.Python.ORDER_ATOMIC);

    var code = variable_name + '.girarIzquierda(' + value_robotvar + ')\r\n';
    return code;
  };
}

function initTurnLeftToBlock(){
    var turnLeftToBlock = {
      "type": "turn_left_to",
      "message0": "%{BKY_TURN_LEFT_TO_TEXT}",
      "args0": [
        {
          "type": "field_variable",
          "name": "NAME",
          "variable": "myRobot"
        },
        {
          "type": "input_value",
          "name": "DISTANCE",
          "check": "Number"
        }
      ],
      "inputsInline": true,
      "previousStatement": null,
      "nextStatement": null,
      "colour": "%{BKY_ROBOT_MOTORS_HUE}",
      "tooltip": "%{BKY_TURN_LEFT_TO_TOOLTIP}",
      "helpUrl": ""
    }
  
    Blockly.Blocks['turn_left_to'] = {
      init: function() {
        this.jsonInit(turnLeftToBlock);
  
      }
    };
  
    Blockly.Python['turn_left_to'] = function(block) {
      var variable_name = Blockly.Python.variableDB_.getName(block.getFieldValue('NAME'), Blockly.Variables.NAME_TYPE);
      var value_distance = Blockly.Python.valueToCode(block, 'DISTANCE', Blockly.Python.ORDER_ATOMIC);
      //var value_rads = value_distance * 3.14/180;
      //var value_rads = value_distance /425; //el simulador no va en rad/s (Pibot)
      var value_rads = value_distance /620; //el simulador no va en rad/s (Drone)
      var vel = 0.02; // 5 degrees aprox
      var t = value_rads/vel;
      var code = variable_name + '.setW('+vel+'); \nawait sleep('+t+');\n'+variable_name + '.setW(0); \n';
      return code;
    };
  
    Blockly.Python['turn_left_to'] = function(block) {
      var variable_name = Blockly.Python.variableDB_.getName(block.getFieldValue('NAME'), Blockly.Variables.NAME_TYPE);
      var value_distance = Blockly.Python.valueToCode(block, 'DISTANCE', Blockly.Python.ORDER_ATOMIC);
  
      var code = variable_name + '.girar_izquierda_hasta(' + value_distance + ')\r\n';
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

    var code = variable_name + '.setW(-' + value_robotvar + ');\r\n';
    return code;
  };

  Blockly.Python['turn_right'] = function(block) {
    var variable_name = Blockly.Python.variableDB_.getName(block.getFieldValue('NAME'), Blockly.Variables.NAME_TYPE);
    var value_robotvar = Blockly.Python.valueToCode(block, 'ROBOTVAR', Blockly.Python.ORDER_ATOMIC);

    var code = variable_name + '.girarDerecha(' + value_robotvar + ')\r\n';
    return code;
  };
}

function initTurnRightToBlock(){
    var turnRightToBlock = {
      "type": "turn_right_to",
      "message0": "%{BKY_TURN_RIGHT_TO_TEXT}",
      "args0": [
        {
          "type": "field_variable",
          "name": "NAME",
          "variable": "myRobot"
        },
        {
          "type": "input_value",
          "name": "DISTANCE",
          "check": "Number"
        }
      ],
      "inputsInline": true,
      "previousStatement": null,
      "nextStatement": null,
      "colour": "%{BKY_ROBOT_MOTORS_HUE}",
      "tooltip": "%{BKY_TURN_RIGHT_TO_TOOLTIP}",
      "helpUrl": ""
    }
  
    Blockly.Blocks['turn_right_to'] = {
      init: function() {
        this.jsonInit(turnRightToBlock);
  
      }
    };
  
    Blockly.Python['turn_right_to'] = function(block) {
        var variable_name = Blockly.Python.variableDB_.getName(block.getFieldValue('NAME'), Blockly.Variables.NAME_TYPE);
        var value_distance = Blockly.Python.valueToCode(block, 'DISTANCE', Blockly.Python.ORDER_ATOMIC);
        //var value_rads = value_distance * 3.14/180;
        //var value_rads = value_distance /425; //el simulador no va en rad/s (Pibot)
        var value_rads = value_distance /620; //el simulador no va en rad/s (Drone)
        var vel = 0.02; // 5 degrees aprox
        var t = value_rads/vel;
        var code = variable_name + '.setW(-'+vel+'); \nawait sleep('+t+');\n'+variable_name + '.setW(0); \n';
        return code;
    };
  
    Blockly.Python['turn_right_to'] = function(block) {
      var variable_name = Blockly.Python.variableDB_.getName(block.getFieldValue('NAME'), Blockly.Variables.NAME_TYPE);
      var value_distance = Blockly.Python.valueToCode(block, 'DISTANCE', Blockly.Python.ORDER_ATOMIC);
  
      var code = variable_name + '.girar_derecha_hasta(' + value_distance + ')\r\n';
      return code;
    };
}

function initWaitBlock(){
  var waitBlock = {
    "type": "wait_block",
    "message0": "%{BKY_WAIT_BLOCK_TEXT}",
    "args0": [
      {
        "type": "field_number",
        "name": "TIME",
        "value": 0.5,
        "min": 0
      }
    ],
    "previousStatement": null,
    "nextStatement": null,
    "colour": "%{BKY_ROBOT_TOOLS_HUE}",
    "tooltip": "%{BKY_WAIT_BLOCK_TOOLTIP}",
    "helpUrl": ""
  };

  Blockly.Blocks['wait_block'] = {
    init: function() {
      this.jsonInit(waitBlock);

    }
  };

  Blockly.Python['wait_block'] = function(block) {
    var value_time_input = block.getFieldValue('TIME');

    var code = 'await sleep(' + value_time_input + ');\n';
    return code;
  };

  Blockly.Python['wait_block'] = function(block) {
    var value_time_input = block.getFieldValue('TIME');

    var code = 'time.sleep(' + value_time_input + ')\r\n';
    return code;
  };
}

function initLandBlock(){
    var landBlock = {
      "type": "land",
      "message0": "%{BKY_LAND_TEXT}",
      "args0": [
        {
          "type": "field_variable",
          "name": "ROBOT_VAR",
          "variable": "myRobot"
        }
      ],
      "previousStatement": null,
      "nextStatement": null,
      "colour": "%{BKY_ROBOT_MOTORS_HUE}",
      "tooltip": "%{BKY_SET_LAND_TOOLTIP}",
      "helpUrl": ""
    }
  
    Blockly.Blocks['land'] = {
      init: function() {
        this.jsonInit(landBlock);
  
      }
    };
    

     Blockly.Python['land'] = function(block) {
       var robotvar = Blockly.Python.variableDB_.getName(block.getFieldValue('ROBOT_VAR'), Blockly.Variables.NAME_TYPE);

      var code = robotvar + '.setL(-3); \nawait sleep(0.4); \n'+robotvar + '.setL(0);\n';
      return code;
    };
  
  
    Blockly.Python['land'] = function(block) {
      var robotvar = Blockly.Python.variableDB_.getName(block.getFieldValue('ROBOT_VAR'), Blockly.Variables.NAME_TYPE);
      //var value = Blockly.Python.valueToCode(block, 'VALUE', Blockly.Python.ORDER_ATOMIC);
  
      var code = robotvar + '.aterrizar(); \r\n' + 'time.sleep(0.5)\r\n';
      return code;
    };
}
