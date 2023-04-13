
"use strict";

let GetProgramState = require('./GetProgramState.js')
let IsInRemoteControl = require('./IsInRemoteControl.js')
let Load = require('./Load.js')
let IsProgramSaved = require('./IsProgramSaved.js')
let AddToLog = require('./AddToLog.js')
let RawRequest = require('./RawRequest.js')
let GetLoadedProgram = require('./GetLoadedProgram.js')
let GetRobotMode = require('./GetRobotMode.js')
let GetSafetyMode = require('./GetSafetyMode.js')
let IsProgramRunning = require('./IsProgramRunning.js')
let Popup = require('./Popup.js')

module.exports = {
  GetProgramState: GetProgramState,
  IsInRemoteControl: IsInRemoteControl,
  Load: Load,
  IsProgramSaved: IsProgramSaved,
  AddToLog: AddToLog,
  RawRequest: RawRequest,
  GetLoadedProgram: GetLoadedProgram,
  GetRobotMode: GetRobotMode,
  GetSafetyMode: GetSafetyMode,
  IsProgramRunning: IsProgramRunning,
  Popup: Popup,
};
