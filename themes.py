"""
THEMES  -  one dict per book concept.  Add a new concept by copying a block and editing it.
Everything in the book (words, riddles, hints, code phrases, colours, mascot, icons) is
built from these entries, so changing the theme changes ALL puzzles.

Required keys
  name        short name used in file names / on the cover ribbon
  edition     text for the cover ribbon
  tagline     one line under the cover title
  palette     5 RGB colours  (orange-ish first; used for cards, bars, section colours)
  bg          RGB page background tint
  mascot      dict(name, hat)  hat in {"pirate","space","wizard"}
  icons       margin doodle names (see ICON_FUNCS in word_games_book.py)
  says        short mascot sayings
  categories  {CATEGORY NAME: [WORDS]}  UPPERCASE letters only, 3-11 letters
              (used for anagrams, missing letters, vowels, word search, code phrases,
               odd-one-out, word building, ladders, sentences)
  riddles     [(riddle, ANSWER)]   one-word answers
  synonyms    [(WORD, SAME-MEANING WORD)]   themed pairs (a generic pool is added automatically)
"""

THEMES = {}

THEMES["pirates"] = dict(
    name="Pirates", edition="PIRATE ADVENTURE EDITION",
    tagline="Sail the seven seas of words!",
    palette=[(255, 110, 40), (60, 200, 110), (60, 160, 255), (255, 70, 130), (150, 80, 240)],
    bg=(255, 250, 235),
    mascot=dict(name="Captain Doodle", hat="pirate"),
    icons=["anchor", "xmark", "wave", "star", "ship"],
    says=["Ahoy, matey!", "Shiver me timbers!", "X marks the spot!", "Yo ho ho!", "Hoist the sails!"],
    categories={
        "ON THE SHIP": "SAIL MAST DECK ANCHOR CANNON RUDDER HULL STERN CABIN GALLEY PLANK ROPE FLAG CREW BARREL LANTERN COMPASS TELESCOPE HAMMOCK SPYGLASS HARBOR BUOY KNOT WHEEL".split(),
        "TREASURE": "GOLD COINS JEWEL RUBY PEARL EMERALD DIAMOND CHEST MAP CROWN GOBLET DOUBLOON LOOT RING NECKLACE SILVER TREASURE SAPPHIRE TRINKET RELIC GEM BRACELET LOCKET".split(),
        "SEA CREATURES": "SHARK WHALE OCTOPUS CRAB DOLPHIN TURTLE SQUID JELLYFISH EEL SEAL STARFISH LOBSTER SEAHORSE CLAM OYSTER PORPOISE WALRUS BARRACUDA KRAKEN SEAGULL CORAL".split(),
        "PIRATE CREW": "CAPTAIN SAILOR PARROT BUCCANEER PIRATE LOOKOUT COOK NAVIGATOR MATEY SKIPPER GUNNER EXPLORER SMUGGLER ADMIRAL VILLAIN MERMAID CASTAWAY ROGUE".split(),
        "ISLAND AND SEA": "ISLAND BEACH PALM COCONUT LAGOON REEF WAVE TIDE STORM CAVE JUNGLE VOLCANO HORIZON SUNSET SAND SHELL BAY COVE CLIFF FOG BREEZE HURRICANE SHORE OCEAN".split(),
    },
    riddles=[
        ("I point north wherever you go, but I am no bird. What am I?", "COMPASS"),
        ("I am a map's best friend and I show where treasure lies. Look for me marked with an X. What am I?", "TREASURE"),
        ("I repeat what pirates say, and I sit on a shoulder. What am I?", "PARROT"),
        ("I have a hull and many sails, and I float on the sea. What am I?", "SHIP"),
        ("I am heavy and drop down to keep the ship from drifting. What am I?", "ANCHOR"),
        ("I have eight arms but no hands to wave. What am I?", "OCTOPUS"),
        ("Pirates walk off me, but I am not a path. I am a long flat board. What am I?", "PLANK"),
        ("I flap and fly at the top of the mast, and I show who you are. What am I?", "FLAG"),
        ("I am a ship's bed. I swing and sway while you sleep. What am I?", "HAMMOCK"),
        ("I make a boom when I am fired from the side of the ship. What am I?", "CANNON"),
        ("You look through me to spot land far away. What am I?", "TELESCOPE"),
        ("I am a big fish with a famous fin and lots of sharp teeth. What am I?", "SHARK"),
    ],
    synonyms=[("LOOT", "PLUNDER"), ("ISLAND", "ISLE"), ("BOAT", "VESSEL"), ("TRIP", "VOYAGE"),
              ("CHIEF", "CAPTAIN"), ("SHORE", "COAST"), ("SEA", "OCEAN"), ("CHART", "MAP")],
)

THEMES["space"] = dict(
    name="Space", edition="SPACE EXPLORER EDITION",
    tagline="Blast off into a universe of words!",
    palette=[(255, 140, 40), (80, 210, 160), (80, 150, 255), (255, 80, 160), (160, 90, 255)],
    bg=(238, 240, 255),
    mascot=dict(name="Captain Zorp", hat="space"),
    icons=["planet", "rocket", "moon", "star", "wave"],
    says=["3, 2, 1, blast off!", "Houston, we have a puzzle!", "To infinity!", "Zoom zoom!", "Out of this world!"],
    categories={
        "PLANETS AND STARS": "MERCURY VENUS EARTH MARS JUPITER SATURN URANUS NEPTUNE PLUTO SUN MOON STAR COMET ASTEROID GALAXY NEBULA METEOR ORBIT CRATER ECLIPSE UNIVERSE SOLAR LUNAR COSMOS".split(),
        "SPACE GEAR": "ROCKET SHUTTLE SATELLITE TELESCOPE HELMET SPACESUIT CAPSULE PROBE ROVER ANTENNA RADAR THRUSTER ENGINE LANDER STATION FUEL BOOSTER CONTROLS MISSION LAUNCH COUNTDOWN PLATFORM".split(),
        "SPACE PEOPLE": "ASTRONAUT ALIEN PILOT COMMANDER ENGINEER SCIENTIST EXPLORER CREW ROBOT ANDROID MARTIAN CADET CAPTAIN NAVIGATOR TRAVELER INVENTOR DOCTOR GENIUS HERO VISITOR PROFESSOR DROID LEADER".split(),
        "ENERGY AND FORCES": "GRAVITY ENERGY LIGHT SPEED POWER PLASMA ATOM LASER BEAM SPARK FLARE MAGNET VACUUM SIGNAL RADIO FUSION FORCE OXYGEN DARKNESS SILENCE RING".split(),
        "ALIEN WORLDS": "CRYSTAL TENTACLE SLIME TUNNEL VOLCANO DESERT GLACIER CANYON JUNGLE OCEAN MOUNTAIN CAVERN SAUCER PORTAL FOREST SWAMP ISLAND RIVER".split(),
    },
    riddles=[
        ("I am a big ball of fire that makes your day bright. What am I?", "SUN"),
        ("I change shape every night, from a thin curve to a full circle. What am I?", "MOON"),
        ("I am a trail of ice and dust with a glowing tail. What am I?", "COMET"),
        ("I am a ship that blasts upward with fire, then leaves the Earth. What am I?", "ROCKET"),
        ("I wear a helmet and float without weight. What am I?", "ASTRONAUT"),
        ("I am the planet with famous rings. What am I?", "SATURN"),
        ("I orbit the Earth and send signals back down. What am I?", "SATELLITE"),
        ("You look through me to see far-off stars. What am I?", "TELESCOPE"),
        ("I am a rolling robot that explores the red planet. What am I?", "ROVER"),
        ("I keep your feet on the floor and make apples fall. What am I?", "GRAVITY"),
        ("I am a giant swirl of stars, and your home is inside one of me. What am I?", "GALAXY"),
        ("I am a bowl-shaped dent in the Moon's face. What am I?", "CRATER"),
    ],
    synonyms=[("SPACESHIP", "STARSHIP"), ("MOON", "SATELLITE"), ("SHINE", "TWINKLE"), ("TRAVEL", "JOURNEY"),
              ("ENORMOUS", "COSMIC"), ("GLOW", "BEAM"), ("EXPLORE", "DISCOVER"), ("ROUND", "SPHERICAL")],
)

THEMES["wizards"] = dict(
    name="Wizards", edition="WIZARD ACADEMY EDITION",
    tagline="Cast a spell on your vocabulary!",
    palette=[(255, 120, 60), (70, 200, 120), (90, 150, 255), (255, 80, 150), (150, 80, 240)],
    bg=(250, 242, 255),
    mascot=dict(name="Merlo the Wizard", hat="wizard"),
    icons=["wand", "potion", "star", "moon", "wave"],
    says=["Abracadabra!", "Magic time!", "Poof! Puzzle!", "Spell it out!", "Wand at the ready!"],
    categories={
        "SPELLS AND MAGIC": "SPELL CHARM WAND POTION CURSE MAGIC RUNE WISH ENCHANT CAULDRON SPELLBOOK SCROLL AMULET TALISMAN ELIXIR ILLUSION SORCERY TRICK MIRACLE SPARKLE SHADOW POWER".split(),
        "MAGICAL CREATURES": "DRAGON UNICORN GRIFFIN PHOENIX TROLL GOBLIN GIANT FAIRY ELF DWARF OGRE CENTAUR PIXIE GHOST TOAD RAVEN SPRITE SERPENT WEREWOLF WYVERN".split(),
        "CASTLE AND PLACES": "CASTLE TOWER DUNGEON FOREST CAVERN PALACE LIBRARY GARDEN BRIDGE MOAT GATE THRONE CHAMBER CELLAR ATTIC VILLAGE MOUNTAIN SWAMP LAKE HALL COURTYARD KINGDOM REALM VALLEY".split(),
        "PEOPLE OF THE REALM": "WIZARD WITCH KNIGHT QUEEN KING PRINCE PRINCESS SORCERER APPRENTICE HERO ARCHER JESTER BARD HERMIT SQUIRE GUARD PROPHET HEALER DRUID MAGE ROGUE PAGE LORD".split(),
        "WIZARD STUFF": "BROOM CROWN SWORD SHIELD ARMOR CLOAK ROBE BOOK CANDLE LANTERN MIRROR CRYSTAL KEY MAP RING BOTTLE TREASURE FEATHER BANNER ARROW LOCKET TORCH GOBLET".split(),
    },
    riddles=[
        ("I am a stick that can make sparks fly when you wave me. What am I?", "WAND"),
        ("I bubble and brew, and every witch has one. What am I?", "CAULDRON"),
        ("I breathe fire and guard a pile of gold. What am I?", "DRAGON"),
        ("I am a horse with a horn on my head. What am I?", "UNICORN"),
        ("I have pages full of spells, and I am very, very old. What am I?", "SPELLBOOK"),
        ("I have towers and a moat, and a king may live inside me. What am I?", "CASTLE"),
        ("I fly through the night and wizards sweep with me. What am I?", "BROOM"),
        ("I am a drink that can turn you into a frog. What am I?", "POTION"),
        ("I say hoot at night and carry messages. What am I?", "OWL"),
        ("I am a small winged person who sprinkles dust. What am I?", "FAIRY"),
        ("I rise from the ashes in a burst of flame. What am I?", "PHOENIX"),
        ("I wear a pointy hat and a long robe, and I know many spells. What am I?", "WIZARD"),
    ],
    synonyms=[("SPELL", "CHARM"), ("WIZARD", "SORCERER"), ("MAGIC", "SORCERY"), ("BREW", "CONCOCT"),
              ("FOREST", "WOODS"), ("TRICK", "ILLUSION"), ("HOME", "CASTLE"), ("FRIGHTENING", "SPOOKY")],
)


# =====================================================================
# AUTO-THEME GENERATOR
# =====================================================================
# Large word banks grouped by broad topic. When a user types any theme
# name, we hash it to pick palette colours and mascot style, then pull
# words from whichever bank(s) best match the name. If no bank matches
# we fall back to a general-purpose vocabulary so the engine always has
# enough words to build every puzzle type.
# =====================================================================


import hashlib

# =====================================================================
# THEME-SPECIFIC WORD BANKS
# Each key is a theme name (or keyword). Words are UPPERCASE, 3-11 chars.
# =====================================================================
_THEME_WORDS = {

    # ── Sports ────────────────────────────────────────────────────────
    "cricket": {
        "CRICKET GEAR":    "BAT BALL WICKET STUMP BAIL HELMET GLOVE PAD JERSEY CAP BOOT GUARD CHEST THIGH VISOR GRIP HANDLE BLADE CREASE PITCH".split(),
        "CRICKET ROLES":   "BATSMAN BOWLER FIELDER CAPTAIN KEEPER UMPIRE SPINNER PACER OPENER ALLROUNDER COACH SELECTOR SCORER COMMENTATOR WICKETKEEPER".split(),
        "CRICKET SHOTS":   "DRIVE PULL HOOK SWEEP CUT GLANCE FLICK LOFT BLOCK NUDGE SLOG SCOOP RAMP REVERSE PADDLE HELICOPTER".split(),
        "CRICKET TERMS":   "OVER WICKET CENTURY FIFTY DUCK BOUNDARY SIXSIX FOUR MAIDEN WIDE NOBALL LBW CAUGHT STUMPED RUNOUT REVIEW POWERPLAY INNINGS".split(),
        "CRICKET PLACES":  "OVAL GROUND OUTFIELD BOUNDARY PAVILION DRESSING CREASE PITCH SQUARE LEG SLIP GULLY MIDWICKET LONGON COVER MIDOFF".split(),
    },
    "football": {
        "FOOTBALL ROLES":  "GOALKEEPER DEFENDER MIDFIELDER STRIKER WINGER CAPTAIN REFEREE LINESMAN COACH MANAGER SUBSTITUTE SWEEPER FULLBACK CENTREBACK LIBERO".split(),
        "FOOTBALL GEAR":   "BOOT JERSEY SHORTS GLOVES SHIN GUARD CLEAT SOCK CAPTAIN ARMBAND WHISTLE BALL FLAG GOALPOST NET CROSSBAR".split(),
        "FOOTBALL ACTIONS":"KICK PASS DRIBBLE SHOOT TACKLE HEADER VOLLEY CROSS CHEST TRAP BLOCK SAVE SLIDE SPRINT TURN JINK CURL CHIP".split(),
        "FOOTBALL TERMS":  "GOAL PENALTY FREEKICK CORNER OFFSIDE FOUL CARD THROW KICKOFF HALFTIME OVERTIME SHOOTOUT AGGREGATE ASSIST FORMATION PRESSING COUNTER".split(),
        "FOOTBALL PLACES": "STADIUM PITCH GOALMOUTH PENALTY BOX MIDFIELD TOUCHLINE DUGOUT TUNNEL STAND TERRACE SCOREBOARD FLOODLIGHT CHANGING TROPHY BOOTH".split(),
    },
    "basketball": {
        "BASKETBALL ROLES": "GUARD FORWARD CENTER POINT SHOOTING POWER SMALL COACH REFEREE CAPTAIN STARTER BENCHER PLAYMAKER REBOUNDER BLOCKER".split(),
        "BASKETBALL MOVES": "DRIBBLE PASS SHOOT LAYUP DUNK PIVOT SCREEN REBOUND BLOCK STEAL ALLEYOOP FADEAWAY HOOK CROSSOVER PULLUP FLOATER POSTUP".split(),
        "BASKETBALL TERMS": "BASKET HOOP COURT FOUL ZONE PRESS TIMEOUT QUARTER OVERTIME ASSIST TURNOVER TRIPLE DOUBLE SLAM BUZZER BACKBOARD FREETHROW".split(),
        "BASKETBALL GEAR":  "BALL JERSEY SHORTS SNEAKER HEADBAND WRISTBAND MOUTHGUARD KNEPAD ANKLEBRACE UNIFORM SCOREBOARD SHOT CLOCK".split(),
        "BASKETBALL PLACES":"ARENA COURT HALFCOURT PAINT LANE PERIMETER BASELINE MIDCOURT LOCKER BENCH BLEACHER HARDWOOD SIDELINE ENDLINE".split(),
    },
    "tennis": {
        "TENNIS SHOTS":    "SERVE VOLLEY FOREHAND BACKHAND SMASH LOB DROP SLICE TOPSPIN FLAT ACE RETURN PASSING APPROACH HALFVOLLEY".split(),
        "TENNIS TERMS":    "LOVE DEUCE ADVANTAGE SET MATCH BREAK HOLD ACE FAULT RALLY NET LET TIEBREAK GRAND SLAM WILDCARD SEED RANKING".split(),
        "TENNIS PLACES":   "COURT BASELINE TRAMLINE SERVICE NET DEUCE ADVANTAGE CENTRE UMPIRE CHAIR LINESMAN BALLBOY AUDIENCE CLUBHOUSE".split(),
        "TENNIS GEAR":     "RACKET BALL STRING GRIP FRAME HEAD BEAM SHOULDER WRISTBAND HEADBAND SHOE SKIRT SHORTS JERSEY VISOR".split(),
        "TENNIS PEOPLE":   "PLAYER CHAMPION SEED QUALIFIER UMPIRE LINESMAN BALLKID COACH OPPONENT WILDCARD VETERAN PRODIGY LEGEND RIVAL".split(),
    },
    "swimming": {
        "SWIMMING STROKES": "FREESTYLE BACKSTROKE BREASTSTROKE BUTTERFLY CRAWL SIDESTROKE ELEMENTARY MEDLEY RELAY SPRINT DISTANCE OPEN WATER".split(),
        "SWIMMING GEAR":   "GOGGLES SWIMSUIT CAP FINS FLOAT KICKBOARD PULL BUOY PADDLES NOSECLIP EARPLUGS WETSUIT JAMMERS COSTUME TOWEL".split(),
        "SWIMMING TERMS":  "LAP LANE STROKE TURN FLIP DIVE START FINISH TOUCH SPLIT PERSONAL BEST RECORD HEAT FINAL SEMI QUALIFIER HEAT".split(),
        "SWIMMING PLACES": "POOL LANE GUTTER BLOCK WALL CEILING SHALLOW DEEP INDOOR OUTDOOR OLYMPIC FIFTY TWENTYFIVE METRE YARD".split(),
        "SWIMMING PEOPLE": "SWIMMER COACH LIFEGUARD TIMEKEEPER REFEREE STARTER OFFICIAL CHAMPION OLYMPIAN RECORD HOLDER MEDALIST".split(),
    },

    # ── Animals / Nature ──────────────────────────────────────────────
    "animals": {
        "WILD ANIMALS":    "LION TIGER WOLF BEAR ELEPHANT GIRAFFE ZEBRA CHEETAH LEOPARD RHINO HIPPO GORILLA PANDA PANTHER JAGUAR LYNX COUGAR BISON BUFFALO MOOSE".split(),
        "SEA ANIMALS":     "SHARK WHALE DOLPHIN OCTOPUS JELLYFISH SEAHORSE STARFISH LOBSTER CRAB TURTLE SEAL WALRUS PENGUIN ORCA STINGRAY SQUID BARRACUDA EEL CLAM OYSTER".split(),
        "BIRDS":           "EAGLE PARROT TOUCAN FLAMINGO PEACOCK OSTRICH PENGUIN SWAN CRANE FALCON HAWK OWL RAVEN CROW ROBIN SPARROW HERON STORK PELICAN ALBATROSS".split(),
        "REPTILES":        "SNAKE LIZARD CROCODILE ALLIGATOR TORTOISE GECKO IGUANA CHAMELEON COBRA PYTHON VIPER MONITOR SKINK TUATARA KOMODO".split(),
        "BABY ANIMALS":    "CUB KITTEN PUPPY FOAL CALF LAMB CHICK FAWN JOEY PIGLET DUCKLING GOSLING EAGLET TADPOLE CATERPILLAR LEVERET COLT FILLY PUP KID".split(),
    },
    "dinosaurs": {
        "DINOSAUR TYPES":  "TREX RAPTOR STEGOSAURUS TRICERATOPS BRACHIOSAURUS ANKYLOSAURUS PTERODACTYL SPINOSAURUS ALLOSAURUS DIPLODOCUS VELOCIRAPTOR IGUANODON PARASAUROLOPHUS PACHYCEPHALOSAURUS CARNOTAURUS".split(),
        "DINOSAUR TRAITS": "HORN CLAW FANG SCALE PLATE SPIKE CREST BEAK WING FEATHER TAIL ARMOR FRILL THUMB TUSK NECK SKULL JAW SPINE RIB".split(),
        "DINOSAUR ERA":    "JURASSIC CRETACEOUS TRIASSIC PREHISTORIC FOSSIL BONE LAYER ROCK SEDIMENT AMBER EXCAVATE PALEONTOLOGY MUSEUM DISCOVERY EXTINCT EVOLUTION".split(),
        "DINOSAUR PLACES": "JUNGLE SWAMP FOREST PLAIN DESERT VOLCANO CAVE ISLAND CRATER VALLEY RIVER MARSH COAST HIGHLAND CANYON LAGOON".split(),
        "PALEONTOLOGY":    "FOSSIL BONE SKULL EXCAVATE PALEONTOLOGIST MUSEUM LAYER ROCK SEDIMENT AMBER CAST MOLD SPECIMEN ARTIFACT DISCOVERY EXPEDITION".split(),
    },
    "ocean": {
        "SEA CREATURES":   "SHARK WHALE DOLPHIN OCTOPUS JELLYFISH SEAHORSE STARFISH LOBSTER CRAB TURTLE SEAL WALRUS STINGRAY SQUID BARRACUDA EEL CLAM OYSTER CORAL ANEMONE".split(),
        "OCEAN FEATURES":  "WAVE TIDE CURRENT REEF TRENCH ABYSS SHELF CANYON SEAMOUNT ATOLL LAGOON ESTUARY COAST SHORE BEACH CLIFF BAY COVE INLET DELTA".split(),
        "OCEAN GEAR":      "SUBMARINE SCUBA WETSUIT FLIPPER MASK TANK SNORKEL HARPOON SONAR ANCHOR BUOY LIGHTHOUSE COMPASS CHART DEPTH GAUGE DIVER".split(),
        "OCEAN ACTIONS":   "DIVE SWIM FLOAT DRIFT SINK SURFACE EXPLORE NAVIGATE ANCHOR TRAWL HARVEST MIGRATE SPAWN HUNT CAMOUFLAGE ECHO LOCATE BREACH".split(),
        "OCEAN PLACES":    "PACIFIC ATLANTIC INDIAN ARCTIC CORAL BARRIER DEEP SEA OPEN OCEAN COASTAL POLAR TROPICAL TEMPERATE ABYSSAL PELAGIC BENTHIC".split(),
    },
    "jungle": {
        "JUNGLE ANIMALS":  "JAGUAR PARROT TOUCAN MONKEY GORILLA SLOTH ANACONDA PANTHER TIGER TAPIR CAPYBARA PIRANHA IGUANA CHAMELEON LEMUR OCELOT PUMA ARMADILLO GIBBON".split(),
        "JUNGLE PLANTS":   "VINE FERN ORCHID BAMBOO MOSS LICHEN BROMELIAD MANGROVE MAHOGANY RUBBER KAPOK CEIBA PALM PITCHER STRANGLER EPIPHYTE LIANA REED SEDGE".split(),
        "JUNGLE FEATURES": "CANOPY UNDERSTORY FLOOR RIVER WATERFALL CLEARING TRAIL CAVE HOLLOW ROOT BRANCH TRUNK LEAF BARK SOIL MUD STREAM MARSH SWAMP".split(),
        "JUNGLE PEOPLE":   "EXPLORER GUIDE TRACKER SCIENTIST RANGER INDIGENOUS NATIVE TRIBE HUNTER PHOTOGRAPHER BIOLOGIST CONSERVATIONIST ADVENTURER BOTANIST".split(),
        "JUNGLE WEATHER":  "RAIN HUMIDITY STORM MIST FOG DOWNPOUR THUNDER LIGHTNING HEAT CANOPY SHADE DAMP TROPICAL MONSOON DRIZZLE DELUGE SUNLIGHT".split(),
    },

    # ── Fantasy / Adventure ───────────────────────────────────────────
    "dragons": {
        "DRAGON TYPES":    "FIRE ICE LIGHTNING EARTH WATER SHADOW CRYSTAL FOREST STONE ELECTRIC WIND POISON METAL COSMIC ANCIENT ELDER WYVERN DRAKE SERPENT BASILISK".split(),
        "DRAGON PARTS":    "WING SCALE CLAW FANG TAIL HORN SPIKE CREST BREATH FLAME SNOUT EYE JAW NECK TALON BARB RIDGE FRINGE MEMBRANE NOSTRIL".split(),
        "DRAGON MAGIC":    "FLAME FROST SPARK ACID VENOM THUNDER SHADOW ILLUSION ROAR HYPNOSIS CURSE SHIELD SUMMON TRANSFORM REGENERATE BREATHE CHARGE SOAR RAMPAGE".split(),
        "DRAGON PLACES":   "CAVE MOUNTAIN VOLCANO FOREST LAKE CASTLE RUIN ISLAND DUNGEON PEAK RIDGE CRATER LAIR NEST HOARD TREASURE AERIE CITADEL STRONGHOLD REALM".split(),
        "DRAGON LORE":     "TREASURE HOARD LEGEND MYTH ELDER ANCIENT PROPHECY RIDER BOND TAME HUNT SLAY KNIGHT HERO QUEST BATTLE GUARDIAN PROTECTOR DESTROYER MASTER".split(),
    },
    "magic": {
        "SPELLS":          "FIREBALL LIGHTNING FREEZE CHARM HEAL SHIELD CURSE SUMMON BANISH TRANSFORM LEVITATE TELEPORT INVISIBLE SHRINK GROW CLONE BLIND SILENCE REFLECT ABSORB".split(),
        "MAGIC ITEMS":     "WAND STAFF ORB AMULET SCROLL POTION CRYSTAL RING CLOAK GRIMOIRE TOME TALISMAN RUNE SIGIL CHARM PENDANT BROOCH SCEPTRE CROWN DIADEM".split(),
        "MAGIC PEOPLE":    "WIZARD WITCH SORCERER MAGE ENCHANTER WARLOCK ALCHEMIST DRUID SHAMAN ORACLE PROPHET SAGE MYSTIC ILLUSIONIST CONJURER NECROMANCER BARD HEALER SUMMONER".split(),
        "MAGIC CREATURES": "DRAGON UNICORN GRIFFIN PHOENIX SPRITE FAIRY ELEMENTAL GOLEM DEMON ANGEL FAMILIAR IMP WRAITH SPECTER BANSHEE DJINN NYMPH SATYR CENTAUR HYDRA".split(),
        "MAGIC PLACES":    "TOWER ACADEMY LIBRARY DUNGEON PORTAL REALM DIMENSION SANCTUM ALTAR CIRCLE NEXUS LEYLINE GROVE CRYPT LABYRINTH VAULT FORGE OBSERVATORY GARDEN SHRINE".split(),
    },
    "superheroes": {
        "POWERS":          "FLIGHT SPEED STRENGTH INVISIBILITY TELEPATHY TELEKINESIS HEALING SHIELD LASER FIRE ICE LIGHTNING EARTH WATER MIND TECH STEALTH AGILITY ENDURANCE BLAST".split(),
        "HERO GEAR":       "CAPE MASK SUIT GLOVE BOOT BELT SHIELD GADGET WEAPON COMMUNICATOR VEHICLE JET COMPUTER LAB HEADQUARTERS BASE ARMOR VISOR GRAPPLE JETPACK".split(),
        "VILLAINS":        "VILLAIN NEMESIS MASTERMIND OVERLORD TYRANT MERCENARY ASSASSIN CYBORG ANDROID MUTANT ALIEN SORCERER CRIMINAL TERRORIST CORRUPT RUTHLESS MENACE THREAT SABOTEUR INFILTRATOR".split(),
        "HERO TYPES":      "SPEEDSTER FLYER TELEPATH BRAWLER GADGETEER MYSTIC ARCHER SOLDIER SCIENTIST TITAN VIGILANTE AGENT GUARDIAN CHAMPION DEFENDER AVENGER PALADIN SENTINEL RANGER CRUSADER".split(),
        "HERO PLACES":     "GOTHAM METROPOLIS SHIELD HELICARRIER FORTRESS WATCHTOWER SANCTUM LAB CAVE BUNKER ROOFTOP ALLEY STREET DOWNTOWN SPACE STATION DIMENSION ISLAND MOUNTAIN UNDERWATER".split(),
    },

    # ── Food ──────────────────────────────────────────────────────────
    "food": {
        "FRUIT":           "APPLE ORANGE MANGO BANANA GRAPE LEMON LIME STRAWBERRY BLUEBERRY CHERRY PEACH PEAR PLUM MELON KIWI PINEAPPLE COCONUT POMEGRANATE APRICOT PAPAYA".split(),
        "VEGETABLES":      "CARROT POTATO ONION TOMATO BROCCOLI SPINACH LETTUCE CELERY PEPPER CUCUMBER PUMPKIN EGGPLANT MUSHROOM GARLIC GINGER CORN PEAS BEANS CABBAGE BEET".split(),
        "MEALS":           "PIZZA PASTA BURGER SALAD SOUP SANDWICH STEW CURRY RICE BREAD CAKE PIE TACOS SUSHI NOODLES PANCAKE WAFFLE OMELETTE STEAK ROAST".split(),
        "TASTES":          "SWEET SALTY SOUR BITTER SPICY TANGY MILD RICH CREAMY CRUNCHY CRISPY JUICY FRESH WARM CHEWY STICKY SMOOTH FLUFFY SAVOURY UMAMI".split(),
        "KITCHEN":         "OVEN STOVE FRIDGE BLENDER WHISK SPATULA LADLE KNIFE BOWL PLATE FORK SPOON CUP TRAY RACK TIMER GRATER COLANDER STEAMER TOASTER".split(),
    },
    "cooking": {
        "COOKING METHODS": "BOIL BAKE FRY ROAST GRILL STEAM POACH SIMMER SAUTE BLANCH BRAISE STIR WHIP BLEND FOLD MARINATE SMOKE CURE FERMENT FLAMBE".split(),
        "INGREDIENTS":     "FLOUR SUGAR BUTTER SALT PEPPER OIL CREAM EGG MILK YEAST VINEGAR HONEY GARLIC GINGER LEMON HERBS SPICE STOCK SAUCE PASTE".split(),
        "KITCHEN TOOLS":   "WHISK SPATULA LADLE TONGS GRATER PEELER SIEVE COLANDER MORTAR ROLLING PASTRY THERMOMETER TIMER SCALES MEASURING CHOPPING MIXING BAKING ROASTING FRYING".split(),
        "DISHES":          "SOUP STEW CURRY PASTA RISOTTO PAELLA QUICHE SOUFFLE CASSEROLE PILAF TAGINE BIRYANI SHAKSHUKA GOULASH RAMEN PHO LAKSA TEMPURA FRITTATA CREPE".split(),
        "TASTES":          "SWEET SALTY SOUR BITTER UMAMI SPICY TANGY SMOKY EARTHY RICH FRESH MILD BOLD DELICATE ROBUST FRUITY NUTTY HERBY CREAMY CRISPY".split(),
    },

    # ── Science / Technology ──────────────────────────────────────────
    "space": {
        "PLANETS":         "MERCURY VENUS EARTH MARS JUPITER SATURN URANUS NEPTUNE PLUTO MOON SUN STAR COMET ASTEROID GALAXY NEBULA METEOR ORBIT CRATER ECLIPSE".split(),
        "SPACE GEAR":      "ROCKET SHUTTLE SATELLITE TELESCOPE HELMET SPACESUIT CAPSULE PROBE ROVER ANTENNA RADAR THRUSTER ENGINE LANDER STATION FUEL BOOSTER CONTROLS MISSION LAUNCH".split(),
        "SPACE PEOPLE":    "ASTRONAUT ALIEN PILOT COMMANDER ENGINEER SCIENTIST EXPLORER CREW ROBOT ANDROID MARTIAN CADET CAPTAIN NAVIGATOR TRAVELER INVENTOR GENIUS HERO VISITOR PROFESSOR".split(),
        "SPACE SCIENCE":   "GRAVITY ENERGY LIGHT SPEED PLASMA ATOM LASER BEAM SPARK FLARE MAGNET VACUUM SIGNAL RADIO FUSION FORCE OXYGEN DARKNESS UNIVERSE COSMOS".split(),
        "ALIEN WORLDS":    "CRYSTAL TENTACLE SLIME TUNNEL VOLCANO DESERT GLACIER CANYON JUNGLE OCEAN MOUNTAIN CAVERN SAUCER PORTAL FOREST SWAMP ISLAND RIVER CRATER ABYSS".split(),
    },
    "robots": {
        "ROBOT PARTS":     "CIRCUIT WIRE SENSOR MOTOR GEAR CHIP BATTERY SCREEN CAMERA LASER ARM CLAW WHEEL TRACK JOINT SERVO ANTENNA SPEAKER MICROPHONE DISPLAY".split(),
        "ROBOT TYPES":     "ANDROID DRONE CYBORG AUTOMATON HUMANOID INDUSTRIAL MEDICAL MILITARY EXPLORER COMPANION GUARDIAN WARRIOR BUILDER CLEANER SURGEON TEACHER HELPER SOLDIER SCOUT SENTINEL".split(),
        "ROBOT ACTIONS":   "COMPUTE SCAN DETECT NAVIGATE BUILD ASSEMBLE WELD SORT LIFT CARRY COMMUNICATE TRANSMIT RECEIVE PROCESS ANALYSE LEARN ADAPT PATROL DEFEND RESCUE".split(),
        "TECH TERMS":      "CODE PROGRAM ALGORITHM BINARY PROCESSOR MEMORY STORAGE NETWORK WIRELESS SIGNAL DIGITAL ANALOG VOLTAGE CURRENT FREQUENCY BANDWIDTH ENCRYPTION INTERFACE OUTPUT INPUT".split(),
        "ROBOT PLACES":    "FACTORY LAB WAREHOUSE SPACE UNDERWATER HOSPITAL BATTLEFIELD SCHOOL HOME CITY MARS MINE OCEAN FLOOR VOLCANO DEEP SPACE STATION SATELLITE PROBE".split(),
    },
    "science": {
        "PHYSICS":         "GRAVITY FORCE ENERGY MASS VELOCITY MOMENTUM FRICTION PRESSURE DENSITY TEMPERATURE LIGHT SOUND WAVE CIRCUIT MAGNET CHARGE PROTON NEUTRON ELECTRON NUCLEUS".split(),
        "CHEMISTRY":       "ATOM MOLECULE ELEMENT COMPOUND MIXTURE REACTION ACID ALKALI CATALYST SOLUTION CRYSTAL POLYMER METAL CARBON OXYGEN HYDROGEN NITROGEN IRON COPPER ZINC".split(),
        "BIOLOGY":         "CELL ORGAN TISSUE MUSCLE BONE BRAIN HEART LUNG KIDNEY LIVER BLOOD NERVE SKIN GENE CHROMOSOME DNA PROTEIN ENZYME HORMONE MEMBRANE MITOSIS".split(),
        "EXPERIMENTS":     "MICROSCOPE TELESCOPE THERMOMETER RULER BALANCE BEAKER FLASK PIPETTE FORCEPS SCALPEL COMPASS MAGNET CIRCUIT BATTERY PRISM LENS CALCULATOR BURETTE STOPWATCH CRUCIBLE".split(),
        "SCIENTISTS":      "EINSTEIN NEWTON DARWIN CURIE TESLA GALILEO HAWKING FEYNMAN BOHR HEISENBERG FARADAY MAXWELL PASTEUR MENDEL LOVELACE TURING SAGAN HUBBLE LYELL KEPLER".split(),
    },

    # ── Arts & Creativity ─────────────────────────────────────────────
    "music": {
        "INSTRUMENTS":     "GUITAR PIANO VIOLIN DRUMS TRUMPET SAXOPHONE FLUTE CLARINET CELLO BASS HARP TROMBONE OBOE KEYBOARD BANJO UKULELE ACCORDION MANDOLIN SITAR DJEMBE".split(),
        "GENRES":          "POP ROCK JAZZ BLUES CLASSICAL OPERA REGGAE COUNTRY FOLK HIPHOP ELECTRONIC SOUL FUNK DISCO PUNK METAL INDIE GOSPEL AMBIENT TECHNO".split(),
        "MUSIC TERMS":     "MELODY HARMONY RHYTHM TEMPO BEAT NOTE CHORD SCALE OCTAVE PITCH TUNE LYRICS VERSE CHORUS BRIDGE REFRAIN CADENCE CLEF SHARP FLAT".split(),
        "MUSIC PEOPLE":    "SINGER COMPOSER CONDUCTOR MUSICIAN DRUMMER GUITARIST PIANIST VIOLINIST BASSIST PRODUCER SONGWRITER LYRICIST SOLOIST CHORISTER MAESTRO VIRTUOSO ARRANGER".split(),
        "MUSIC ACTIONS":   "SING PLAY PERFORM RECORD COMPOSE CONDUCT REHEARSE IMPROVISE STRUM PLUCK BLOW BEAT PRACTICE HARMONISE TUNE ACCOMPANY AUDITION COLLABORATE TOUR BROADCAST".split(),
    },
    "art": {
        "ART TOOLS":       "BRUSH PENCIL CANVAS PALETTE CHISEL EASEL CHARCOAL PASTEL INK PEN MARKER CRAYON SPRAY SPONGE KNIFE ROLLER STAMP STENCIL RULER COMPASS".split(),
        "ART STYLES":      "PORTRAIT LANDSCAPE ABSTRACT REALISTIC IMPRESSIONIST CUBIST SURREAL MINIMALIST EXPRESSIONIST BAROQUE RENAISSANCE GOTHIC MODERN CONTEMPORARY DIGITAL GRAFFITI".split(),
        "COLOURS":         "RED BLUE GREEN YELLOW ORANGE PURPLE PINK BROWN BLACK WHITE GREY SILVER GOLD TURQUOISE CRIMSON VIOLET INDIGO SCARLET MAROON CREAM TEAL".split(),
        "ART PLACES":      "GALLERY MUSEUM STUDIO WORKSHOP EXHIBITION AUCTION COLLECTION ARCHIVE RESTORATION LAB CLASSROOM STREET MARKET ATELIER PRINT FRAMING INSTALLATION PERFORMANCE MURAL".split(),
        "ART PEOPLE":      "PAINTER SCULPTOR ILLUSTRATOR PHOTOGRAPHER DESIGNER ANIMATOR CERAMICIST PRINTMAKER CALLIGRAPHER MURALIST GRAFFITI CURATOR COLLECTOR CRITIC PATRON DIRECTOR ARCHIVIST".split(),
    },

    # ── School / Everyday ─────────────────────────────────────────────
    "school": {
        "SUBJECTS":        "MATHS SCIENCE ENGLISH HISTORY GEOGRAPHY MUSIC ART DRAMA PHYSICS CHEMISTRY BIOLOGY COMPUTING FRENCH SPANISH LATIN DESIGN TECHNOLOGY ECONOMICS PHILOSOPHY SOCIOLOGY".split(),
        "PEOPLE":          "TEACHER STUDENT PRINCIPAL LIBRARIAN COUNSELLOR JANITOR SECRETARY GOVERNOR COACH MENTOR PREFECT VOLUNTEER PARENT INSPECTOR TUTOR EXAMINER CARETAKER ASSISTANT VISITOR ADVISOR".split(),
        "STATIONERY":      "PENCIL RULER ERASER COMPASS PROTRACTOR STAPLER SCISSORS GLUE FOLDER BINDER NOTEBOOK CALCULATOR MARKER CRAYON HIGHLIGHTER SHARPENER CLIPBOARD THUMBTACK ENVELOPE LABEL".split(),
        "SCHOOL ROOMS":    "CLASSROOM LIBRARY CANTEEN HALL OFFICE GYM LABORATORY CORRIDOR STAFFROOM TOILET RECEPTION COURTYARD LOCKER WORKSHOP AUDITORIUM STUDIO NURSERY CHANGING PLAYGROUND DORMITORY".split(),
        "ACTIVITIES":      "READING WRITING DRAWING PAINTING SINGING DANCING CODING DEBATING CHESS DRAMA QUIZ ASSEMBLY HOMEWORK EXAM REVISION PRESENTATION PROJECT RESEARCH EXPERIMENT FIELDTRIP".split(),
    },
    "transport": {
        "LAND VEHICLES":   "CAR BUS TRUCK TRAIN BICYCLE MOTORCYCLE TRAM TAXI AMBULANCE FIRETRUCK VAN LORRY JEEP SCOOTER SKATEBOARD CARRIAGE BULLDOZER TRACTOR CRANE SEGWAY".split(),
        "AIR VEHICLES":    "PLANE HELICOPTER GLIDER BALLOON DRONE ROCKET SHUTTLE BLIMP PARAGLIDER KITE AIRSHIP BIPLANE FIGHTER BOMBER SEAPLANE MICROLIGHT PARACHUTE CONCORDE JUMBOJET BLIMP".split(),
        "SEA VEHICLES":    "SHIP BOAT FERRY SUBMARINE YACHT CANOE KAYAK RAFT HOVERCRAFT TUGBOAT TANKER LINER DESTROYER FRIGATE SPEEDBOAT GONDOLA CATAMARAN BARGE TRAWLER SAILBOAT".split(),
        "VEHICLE PARTS":   "ENGINE WHEEL PROPELLER RUDDER SAIL ANCHOR HULL CABIN COCKPIT DASHBOARD FUEL BRAKE THROTTLE GEAR EXHAUST PISTON TURBINE ROTOR RADAR ANTENNA".split(),
        "TRANSPORT WORDS": "DRIVE STEER BRAKE ACCELERATE LAND TAKEOFF DOCK LAUNCH CRUISE NAVIGATE OVERTAKE PARK REVERSE TOW SIGNAL REFUEL BOARD DISEMBARK HOVER TRANSIT".split(),
    },

    # ── Pirate / Adventure (kept for preset compatibility) ─────────────
    "pirates": {
        "ON THE SHIP":     "SAIL MAST DECK ANCHOR CANNON RUDDER HULL STERN CABIN GALLEY PLANK ROPE FLAG CREW BARREL LANTERN COMPASS TELESCOPE HAMMOCK SPYGLASS".split(),
        "TREASURE":        "GOLD COINS JEWEL RUBY PEARL EMERALD DIAMOND CHEST MAP CROWN GOBLET DOUBLOON LOOT RING NECKLACE SILVER TREASURE SAPPHIRE TRINKET RELIC".split(),
        "SEA CREATURES":   "SHARK WHALE OCTOPUS CRAB DOLPHIN TURTLE SQUID JELLYFISH EEL SEAL STARFISH LOBSTER SEAHORSE CLAM OYSTER PORPOISE WALRUS BARRACUDA KRAKEN SEAGULL".split(),
        "PIRATE CREW":     "CAPTAIN SAILOR PARROT BUCCANEER PIRATE LOOKOUT COOK NAVIGATOR MATEY SKIPPER GUNNER EXPLORER SMUGGLER ADMIRAL VILLAIN MERMAID CASTAWAY ROGUE CORSAIR".split(),
        "ISLAND AND SEA":  "ISLAND BEACH PALM COCONUT LAGOON REEF WAVE TIDE STORM CAVE JUNGLE VOLCANO HORIZON SUNSET SAND SHELL BAY COVE CLIFF FOG".split(),
    },
}

# ── Keyword → theme mapping ────────────────────────────────────────────────
# Maps any user-typed word to the best bank key above.
_KEYWORD_MAP = {
    # sports
    "cricket":"cricket","batting":"cricket","bowling":"cricket","wicket":"cricket","ipl":"cricket",
    "football":"football","soccer":"football","fifa":"football","premier":"football","bundesliga":"football",
    "basketball":"basketball","nba":"basketball","hoops":"basketball",
    "tennis":"tennis","wimbledon":"tennis","grand slam":"tennis",
    "swimming":"swimming","swim":"swimming","pool":"swimming","aquatic":"swimming",
    "sport":"football","sports":"football","game":"football","athletics":"football",
    # animals
    "animals":"animals","animal":"animals","zoo":"animals","wildlife":"animals","safari":"animals","nature":"animals",
    "birds":"animals","reptiles":"animals","insects":"animals","mammals":"animals","pets":"animals",
    "dog":"animals","cat":"animals","horse":"animals","fish":"animals","bird":"animals",
    # dinosaurs
    "dinosaurs":"dinosaurs","dinosaur":"dinosaurs","dino":"dinosaurs","jurassic":"dinosaurs",
    "prehistoric":"dinosaurs","fossil":"dinosaurs","trex":"dinosaurs","raptor":"dinosaurs",
    # ocean
    "ocean":"ocean","sea":"ocean","marine":"ocean","underwater":"ocean","beach":"ocean",
    "sharks":"ocean","shark":"ocean","whale":"ocean","coral":"ocean","reef":"ocean","fish":"ocean",
    "nautical":"ocean","sailing":"ocean","pirate":"pirates","pirates":"pirates",
    # jungle
    "jungle":"jungle","rainforest":"jungle","amazon":"jungle","tropical":"jungle","safari":"jungle",
    "forest":"jungle","wild":"jungle",
    # fantasy
    "dragons":"dragons","dragon":"dragons","wyvern":"dragons","serpent":"dragons",
    "magic":"magic","wizard":"magic","witches":"magic","witch":"magic","spell":"magic",
    "sorcerer":"magic","fantasy":"magic","enchanted":"magic","fairy":"magic","elves":"magic","elf":"magic",
    "superheroes":"superheroes","superhero":"superheroes","marvel":"superheroes","comics":"superheroes","hero":"superheroes",
    # food
    "food":"food","fruits":"food","fruit":"food","vegetables":"food","meals":"food",
    "cooking":"cooking","baking":"cooking","chef":"cooking","kitchen":"cooking","recipe":"cooking","cuisine":"cooking",
    # science/tech
    "space":"space","planets":"space","astronomy":"space","galaxy":"space","nasa":"space","cosmos":"space",
    "robots":"robots","robot":"robots","technology":"robots","coding":"robots","programming":"robots","ai":"robots",
    "science":"science","physics":"science","chemistry":"science","biology":"science","experiments":"science",
    # arts
    "music":"music","songs":"music","singing":"music","band":"music","concert":"music","instruments":"music",
    "art":"art","painting":"art","drawing":"art","sculpture":"art","colours":"art","colors":"art",
    # school/everyday
    "school":"school","classroom":"school","learning":"school","education":"school","study":"school",
    "transport":"transport","vehicles":"transport","cars":"transport","trains":"transport","planes":"transport",
}

# Fallback generic bank
_GENERAL = {
    "THINGS":      "BOOK CLOCK CHAIR TABLE LAMP DOOR WINDOW PHONE COMPUTER CAMERA MIRROR BOTTLE BASKET CARPET CURTAIN PILLOW BLANKET UMBRELLA LADDER BRIDGE".split(),
    "ADJECTIVES":  "BRIGHT DARK FAST SLOW LONG SHORT WIDE NARROW HEAVY LIGHT THICK THIN ROUGH SMOOTH LOUD QUIET SHARP BLUNT WARM COOL".split(),
    "VERBS":       "RUN JUMP SWIM CLIMB CRAWL PUSH PULL CARRY THROW CATCH OPEN CLOSE WRITE DRAW PAINT BUILD BREAK MEND COOK CLEAN".split(),
    "PLACES":      "CITY TOWN VILLAGE FARM FOREST BEACH PARK MARKET MUSEUM HOSPITAL SCHOOL LIBRARY AIRPORT STATION HARBOUR FACTORY TEMPLE CASTLE STADIUM PLAZA".split(),
    "COLOURS":     "RED BLUE GREEN YELLOW ORANGE PURPLE PINK BROWN BLACK WHITE GREY SILVER GOLD TURQUOISE CRIMSON VIOLET INDIGO SCARLET MAROON CREAM TEAL".split(),
}

# Style presets — picked by hash of theme name
_PALETTES = [
    [(255,110,40),(60,200,110),(60,160,255),(255,70,130),(150,80,240)],
    [(255,60,120),(60,180,255),(255,200,40),(80,220,140),(200,80,255)],
    [(40,180,255),(255,140,40),(80,220,100),(255,80,180),(140,100,255)],
    [(255,180,40),(80,200,180),(255,80,80),(100,150,255),(180,220,60)],
    [(120,220,80),(255,120,80),(80,160,255),(255,60,160),(220,180,40)],
    [(200,80,255),(60,200,160),(255,160,40),(80,200,255),(255,80,100)],
]
_BG_TINTS = [(255,250,235),(238,240,255),(250,242,255),(240,255,245),(255,240,240),(248,248,255)]
_HATS  = ["pirate","space","wizard","pirate","space","wizard"]
_ICONS = [
    ["star","wave","moon","star","wave"],
    ["planet","rocket","moon","star","wave"],
    ["wand","potion","star","moon","wave"],
    ["anchor","xmark","wave","star","ship"],
    ["star","wave","moon","star","wave"],
    ["rocket","star","moon","wave","planet"],
]
_SAYS = [
    ["Let's go!", "Word time!", "Ready?", "You've got this!", "Go!"],
    ["Amazing!", "Keep it up!", "So clever!", "Fantastic!", "Word power!"],
    ["3, 2, 1, go!", "Puzzle time!", "Think hard!", "Brilliant!", "Word wizard!"],
]


def _pick(lst, idx):
    return lst[idx % len(lst)]


def auto_theme(name: str) -> dict:
    """Build a full THEMES-compatible dict from just a theme name."""
    key = name.strip().lower()
    h   = int(hashlib.md5(key.encode()).hexdigest(), 16)
    idx = h % len(_PALETTES)

    # ── Find the best matching bank ─────────────────────────────────────
    # 1. Direct exact match
    bank_key = _KEYWORD_MAP.get(key)

    # 2. Check each word in a multi-word theme name
    if bank_key is None:
        for word in key.split():
            bank_key = _KEYWORD_MAP.get(word)
            if bank_key:
                break

    # 3. Partial substring match across keyword map
    if bank_key is None:
        for kw, bk in _KEYWORD_MAP.items():
            if kw in key or key in kw:
                bank_key = bk
                break

    # 4. Fall back to general
    if bank_key is None or bank_key not in _THEME_WORDS:
        categories = dict(_GENERAL)
    else:
        categories = {k: list(v) for k, v in _THEME_WORDS[bank_key].items()}

    name_title = name.strip().title()
    return dict(
        name        = name_title,
        edition     = f"{name.upper().strip()} EDITION",
        tagline     = f"Explore a world of {name_title.lower()} words!",
        palette     = _pick(_PALETTES, idx),
        bg          = _pick(_BG_TINTS, idx),
        mascot      = dict(name=f"{name_title} Buddy", hat=_pick(_HATS, idx)),
        icons       = _pick(_ICONS, idx),
        says        = _pick(_SAYS, idx % len(_SAYS)),
        categories  = categories,
        riddles     = [],   # engine fills from GENERIC_RIDDLES automatically
        synonyms    = [],
    )
