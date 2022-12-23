# combination script
import os
import cv2
import numpy as np

indir = 'combinations/character'
files = os.listdir(indir)
imgs = [cv2.imread(f'{indir}/{filename}', cv2.IMREAD_UNCHANGED) for filename in files]

global_img = np.zeros(imgs[0].shape)
for img in imgs:
    global_img += img[:,:]/float(len(imgs))

bg_img = np.zeros(imgs[0].shape)
bg_img[:,:] = (127, 127, 127, 0)
for c in range(3):
    bg_img[:,:,c] *= (255-global_img[:,:,3])/float(255)
bg_img[:,:,3] = 255-global_img[:,:,3]

global_img = bg_img + global_img

cv2.imwrite(f'{indir}/output.png', global_img)


# prompts used
prompts = [
    "male wizard, tall and thin with a prominent nose and long white beard, draped in flowing blue robes adorned with intricate silver symbols.",
    "female paladin, short and muscular with short cropped blonde hair, wearing shiny plate armor and carrying a glowing holy sword.",
    "male barbarian, towering and broad-shouldered with a wild mane of red hair, wearing furs and carrying a massive battle-axe.",
    "female ranger, tall and slender with long, flowing brunette hair and piercing green eyes, dressed in leather armor and carrying a sleek longbow.",
    "male monk, short and wiry with a shaved head and sharp features, wearing loose, flowing robes and carrying a pair of nunchucks.",
    "female druid, petite and agile with piercing blue eyes and wild, curly hair, wearing a cloak made of leaves and carrying a staff carved with intricate symbols.",
    "male warlock, tall and gaunt with pale skin and dark, piercing eyes, dressed in black robes and carrying a staff with a glowing crystal at the top.",
    "female cleric, short and plump with rosy cheeks and long, curly red hair, wearing a flowing white robe and carrying a holy symbol.",
    "male fighter, broad-shouldered and muscular with short, cropped hair and a rugged face, dressed in heavy plate armor and carrying a sword and shield.",
    "male warlock, tall and thin with dark, gaunt features and long, black hair, dressed in black robes adorned with glowing runes and carrying a staff topped with a glowing crystal.",
    "female necromancer, short and slight with pale skin and jet black hair styled in intricate braids, wearing dark, flowing robes and carrying a staff topped with a glowing purple crystal.",
    "male sorcerer, tall and lean with piercing green eyes and short, spiky hair, dressed in colorful robes adorned with intricate symbols and carrying a wand topped with a glowing gemstone.",
]
