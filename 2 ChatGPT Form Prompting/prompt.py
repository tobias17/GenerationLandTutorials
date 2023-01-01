import numpy as np
import re, math

defaults = {
    "theme": "high fantasy, with a Dungeons and Dragons inspiration",
}

base_prompt = """You will help me fill out certain aspects of a video game I am designing. The theme is %%THEME%%. I need your help filling out %%INITIAL_DESC%%.

If you see the phrase `describe()` then you are to fill in a list of physical attributes that describe the object.

If you see `choices=[x, y, z]` then you are to choose one item from that list (x, y, or z in that example). Do not choose more than 1 option. Do not choose something that is not in the list.

If you see something like:
```
Footwear: choices=[sneakers, sandals]
    if (choice == sneakers) {
        Brand: choices=[Nike, Adidas]
    else {
        Brand: choices=[Crocs, Teva]
    }
```
Then you must fill out the items in the if/else block based on the choice you made in the previous item in the form.

I will now provide examples for the following design sheet for a fruit
```
Name: 
Description: describe()
Taste: choices=[sweet, sour]
    if (choice == sweet) {
        Type: choices=[sugary, honeyed]
    else {
        Kick: choices=[acidic, tart]
    }
```

Example 1 shows a good example of a filled out form:
```
Name: Apple
Description: apple with smooth red skin, brown stem with 2 bright green leaves
Taste: sweet
Type: sugary
```

Example 2 shows a bad example of a filled out form:
```
Name: Lemon
Description: brown
Taste: Sour
Kick: acidic
```
This is a bad example because the description both too short and does not describe a lemon

Example 3 shows another bad example of a filled out form:
```
Name: Pear
Description: pear with yellow and orange skin, elongate shape that's narrow at the top and wide at the bottom
Taste: tangy
Kick: tart
```
This is a bad example because the Taste attribute was Tangy, which is not from the list of options to choose from, and breaks the conditional option below it.

Example 4 shows another bad example of a filled out form:
```
Name: Banana
Description: yellow skin with speckles of brown creeping in, peel slightly pulled back at the top for a small portion
Taste: sweet
Kick: acidic
```
This is a bad example because, while `Kick: acidic` is a valid option, it should only be picked when the taste is sour, not sweet.


Please fill out %%COUNT%% form(s) for a %%THEME%% %%FORM_DESC%% in my upcoming video game
%%EXTRA_REQS%%
```
%%FORM%%
```

Please fill out %%COUNT%% form(s) exactly%%SPEC_REQS%%"""


class DistributionManager:
    level_count = 10

    def __init__(self, options, sig):
        self.options = options
        self.sig = sig
    
    def get(self, level):
        mu = ((level-1) / (self.level_count-1)) * (len(self.options) - 1)
        coefs = [1/math.sqrt(2*math.pi*self.sig)*pow(math.e, -1/2*pow((x-mu)/math.sqrt(self.sig), 2)) for x in range(len(self.options))]
        dividend = sum(coefs)
        coefs = [coef/dividend for coef in coefs]
        return np.random.choice(self.options, p=coefs)

character_sizes = ['small animal', 'small humanoid', 'human sized', 'large humanoid', 'large beast']
char_dist_man = DistributionManager(character_sizes, 2)
character = {
    "initial desc": "a character sheet for an enemy that the player will fight",
    "form desc": "enemy that the player will have to fight",
    "extra reqs": """
For the melee attacks:
Claw Swipes is the generic attack for animals, as they can not hold a weapon. Leave the weapon section blank.
Weapon Swing is an attack that has the character swinging the sword from right to left, dealing great damage and knocking the target back slightly.
Weapon Strike is a vertical attack that has the character swinging the sword from above their head to the ground, dealing some damage and stunning the target for some duration.
""",
    "form": f"""Size: choices=[{', '.join(character_sizes)}]
Name:
Description: describe()
Attack Style: choices=[melee, ranged]
    if (choice == melee) {{
        Attack Type: choices=[claw swipes, weapon swing, weapon strike]
        Weapon: describe()
    }} else {{
        Projectile type: choices=[arrow, fireball, magic]
        Projectile: describe()
    }}""",
    "spec reqs": (lambda x:
        " with the following sizes:\n" + "\n".join(f"{i+1}. {char_dist_man.get(level=x['level'])}" for i in range(x['count']))
    ),
}

def fill_prompt(root, inputs):
    prompt = base_prompt
    matches = re.findall(r'%%([A-Z_]+)%%', prompt)
    for match in matches:
        tag = match.lower().replace('_', ' ')
        sub = ""
        if tag in inputs:
            sub = inputs[tag]
        elif tag in root:
            sub = root[tag]
        elif tag in defaults:
            sub = defaults[tag]
        else:
            raise Exception(f"Could not find '{tag}' in inputs, root, or defaults")
        if type(sub) == type(0):
            sub = str(sub)
        elif type(sub) == type(lambda: 0):
            sub = sub(inputs)
        prompt = prompt.replace(f'%%{match}%%', sub)
    return prompt


prompt = fill_prompt(character, {'count': 5, 'level': 7})
print(prompt)
