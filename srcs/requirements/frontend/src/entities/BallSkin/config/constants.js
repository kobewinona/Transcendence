import ballSkin1 from 'assets/ballSkins/regular/skin1.png';
import ballSkin2 from 'assets/ballSkins/regular/skin2.png';
import ballSkin3 from 'assets/ballSkins/regular/skin3.png';
import ballSkin4 from 'assets/ballSkins/regular/skin4.png';
import ballSkin5 from 'assets/ballSkins/regular/skin5.png';
import ballSkin6 from 'assets/ballSkins/regular/skin6.png';
import pixarSkin from 'assets/ballSkins/special/pixarSkin.png';

export const BALL_REGULAR_TYPE_SKIN_KEY = 'regular';
export const BALL_SPECIAL_TYPE_SKIN_KEY = 'special';

export const BALL_SKINS = {
  [BALL_REGULAR_TYPE_SKIN_KEY]: [ballSkin1, ballSkin2, ballSkin3, ballSkin4, ballSkin5, ballSkin6],
  [BALL_SPECIAL_TYPE_SKIN_KEY]: [pixarSkin],
};

export const BALL_COLORS = [
  '--primary-color',
  '--secondary-color',
  '--complementary-1-color',
  '--complementary-2-color',
  '--complementary-3-color',
  '--complementary-4-color',
];

export const BALL_SPECIAL_SKINS_COLORS = ['#0061a6'];
