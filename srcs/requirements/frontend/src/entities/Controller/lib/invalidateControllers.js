import { CONTROL_KEYS } from 'entities/Controller/config/constants.js';
import {
  CONTROLLED_BY_INPUT_NAME,
  CONTROLLED_BY_PLAYER,
  CONTROLS_INPUT_NAME,
  NAME_INPUT_NAME,
  SIDE_INPUT_NAME,
} from 'entities/Game/config/constants.js';

function invalidateControllers(controllers = []) {
  let playerIndex = 0;
  let cpuIndex = 0;
  let leftPlayers = 0;
  let rightPlayers = 0;

  return controllers
    .filter((controller) => controller?.side === 'left' || controller?.side === 'right')
    .map((controller) => {
      const { [CONTROLLED_BY_INPUT_NAME]: controlledBy, [SIDE_INPUT_NAME]: side } = controller;

      if (controlledBy.key === CONTROLLED_BY_PLAYER.key) {
        return {
          ...controller,
          [CONTROLS_INPUT_NAME]:
            side === 'left'
              ? CONTROL_KEYS[side][leftPlayers++]
              : CONTROL_KEYS[side][rightPlayers++],
          [NAME_INPUT_NAME]: `PLAYER ${++playerIndex}`,
        };
      } else {
        return {
          ...controller,
          [CONTROLS_INPUT_NAME]: null,
          [NAME_INPUT_NAME]: `CPU ${++cpuIndex}`,
        };
      }
    });
}

export default invalidateControllers;
