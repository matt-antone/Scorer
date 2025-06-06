import * as gameModule from "./game.js";
import * as gameOverModule from "./gameOver.js";
import * as nameEntryModule from "./nameEntry.js";
import * as noConnectionModule from "./noConnection.js";
import * as splashModule from "./splash.js";

const screens = {
  game: gameModule.game,
  gameOver: gameOverModule.gameOver,
  nameEntry: nameEntryModule.nameEntry,
  noConnection: noConnectionModule.noConnection,
  splash: splashModule.splash,
};

export default screens;
