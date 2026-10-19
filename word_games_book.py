#!/usr/bin/env python3
"""
WORD GAMES BOOK ENGINE  (graffiti + doodle style)

  python word_games_book.py --theme pirates
  python word_games_book.py --theme space --scale 1.2 --out space_book.pdf
  python word_games_book.py --all                      # one PDF per theme

WHERE TO CHANGE THINGS
  BOOK         : title, ages, seed
  SECTIONS     : which puzzle types, how many pages, puzzles per page, time limit, difficulty
  themes.py    : the CONCEPT (words, riddles, colours, mascot...) - add a theme = add a block
  GENERATORS   : one function per puzzle type (add a type: write gen_x + render_x, register it)
  --scale N    : multiplies every section's page count (use it to hit 130-180 pages)
"""
import argparse, math, random, re, os
from collections import Counter, defaultdict, deque
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import simpleSplit
from reportlab.lib.colors import Color
from wordfreq import top_n_list, zipf_frequency
from better_profanity import profanity
from themes import THEMES

profanity.load_censor_words()
W, H = A4

# =====================================================================
# 1. BOOK CONFIG  (edit me)
# =====================================================================
BOOK = dict(
    title_1="WORD GAMES",            # cover line 1   (pick your own title if you publish this)
    title_2="FOR CLEVER KIDS",       # cover line 2
    ages="AGES 8-12",
    seed=7,
)

SECTIONS = [
    # key        header bar title            card title             pages per_page diff
    dict(key="anagram",    title="ANAGRAM ATTACK",         card="LETTER SOUP",        pages=18, per_page=4, diff="EASY",
         blurb="The letters are shuffled! Put them back in order to spell the hidden word. The hint tells you the topic."),
    dict(key="missing",    title="MISSING LETTERS MAYHEM", card="FILL THE GAPS",      pages=18, per_page=4, diff="EASY",
         blurb="Some letters have gone missing. Work out which ones to finish each word."),
    dict(key="vowels",     title="VOWEL VANISH",           card="WHERE DID THEY GO?", pages=14, per_page=4, diff="EASY",
         blurb="All the vowels ran away! Put A, E, I, O and U back to make each word."),
    dict(key="synonyms",   title="SYNONYM SHOWDOWN",       card="WORD TWINS",         pages=14, per_page=4, diff="MEDIUM",
         blurb="Synonyms are words that mean almost the same thing. Pick the twin for each word."),
    dict(key="oddone",     title="ODD ONE OUT",            card="SPOT THE INTRUDER",  pages=10, per_page=4, diff="EASY",
         blurb="Three words belong together. One does not! Can you spot the intruder?"),
    dict(key="sentence",   title="SENTENCE SCRAMBLE",      card="WORD SHUFFLE",       pages=12, per_page=4, diff="MEDIUM",
         blurb="The words in each sentence got mixed up. Write them back in the right order."),
    dict(key="riddle",     title="RIDDLE RUMBLE",          card="WHAT AM I?",          pages=10, per_page=3, diff="MEDIUM",
         blurb="Read the clues and think sideways. Each riddle has a one-word answer."),
    dict(key="code",       title="CODE CRACKERS",          card="SECRET MESSAGE",      pages=12, per_page=3, diff="HARD",
         blurb="Every letter in the message has been moved along the alphabet. Shift them back to read it!"),
    dict(key="ladder",     title="WORD LADDERS",           card="CLIMB THE LADDER",    pages=10, per_page=3, diff="HARD",
         blurb="Change ONE letter at a time to turn the top word into the bottom word. Every step must be a real word."),
    dict(key="maze",       title="MAZE MISSION",           card="FIND THE WAY",        pages=10, per_page=2, diff="EASY",
         blurb="Draw a path from START to END. Every maze has a way through - can you find it?"),
    dict(key="building",   title="WORD BUILDER BLAST",     card="LETTER FACTORY",      pages=16, per_page=3, diff="HARD",
         blurb="Use only the letters you are given to build as many words as you can."),
    dict(key="wordsearch", title="WORD SEARCH WARS",       card="FIND THEM ALL",       pages=28, per_page=1, diff="MEDIUM",
         blurb="Words hide in every direction. Circle them all, then tick them off the list."),
]

# Metadata exposed to the API / frontend (no rendering state)
SECTIONS_META = [
    {"key": s["key"], "title": s["title"], "diff": s["diff"],
     "blurb": s["blurb"]}
    for s in SECTIONS
]
TYPE_TAG = dict(anagram="ANAGRAM", missing="MISSING LETTERS", vowels="VOWELS", synonyms="SYNONYMS", oddone="ODD ONE",
                sentence="SENTENCES", riddle="RIDDLE", code="CODE", ladder="LADDER", maze="MAZE", building="WORD BUILDING",
                wordsearch="WORD SEARCH")

# =====================================================================
# 2. WORD TOOLS (dictionary checks keep puzzles fair and kid-safe)
# =====================================================================
_TOP = [w for w in top_n_list("en", 100000) if w.isalpha() and w.isascii() and w.islower()]
SAFE = lambda w: not profanity.contains_profanity(w)
ANAGRAM_KEYS = defaultdict(set)
for _w in _TOP:
    if 3 <= len(_w) <= 11 and zipf_frequency(_w, "en") >= 3.0:
        ANAGRAM_KEYS["".join(sorted(_w))].add(_w)
STOP = set("ent ern ers eds nus oes ens tis ner ret tor ort ore ars ras sar lat tal alt ect ols res ret ter tre".split())
COMMON = [w for w in _TOP if 3 <= len(w) <= 5 and SAFE(w) and zipf_frequency(w, "en") >= 3.6
          and any(v in w for v in "aeiouy") and w not in STOP]
FOUR = [w for w in _TOP if len(w) == 4 and SAFE(w) and zipf_frequency(w, "en") >= 4.1 and any(v in w for v in "aeiouy")]
LAD = defaultdict(list)
for _w in FOUR:
    for _i in range(4): LAD[_w[:_i] + "_" + _w[_i + 1:]].append(_w)
def nbrs(w): return {x for i in range(4) for x in LAD[w[:i] + "_" + w[i + 1:]] if x != w}

def subwords(src):
    s = src.lower(); cs = Counter(s)
    out = [w for w in COMMON if len(w) < len(s) and not (Counter(w) - cs)]
    out.sort(key=lambda w: -zipf_frequency(w, "en"))
    return out

# =====================================================================
# 3. SHARED CONTENT (works for every theme)
# =====================================================================
GENERIC_SYN = [("HAPPY","JOYFUL"),("SAD","GLOOMY"),("BIG","ENORMOUS"),("SMALL","TINY"),("QUICK","SPEEDY"),("SLOW","SLUGGISH"),
 ("SMART","CLEVER"),("SILLY","FOOLISH"),("BEGIN","START"),("END","FINISH"),("TALK","SPEAK"),("SHOUT","YELL"),("FRIEND","BUDDY"),
 ("ENEMY","FOE"),("SHINY","GLEAMING"),("DULL","BORING"),("TIRED","WEARY"),("COLD","CHILLY"),("HOT","SCORCHING"),
 ("BRAVE","COURAGEOUS"),("SCARED","AFRAID"),("ANGRY","FURIOUS"),("CALM","PEACEFUL"),("LOUD","NOISY"),("QUIET","SILENT"),
 ("STRONG","POWERFUL"),("WEAK","FEEBLE"),("BEAUTIFUL","LOVELY"),("UGLY","HIDEOUS"),("CLEAN","SPOTLESS"),("DIRTY","FILTHY"),
 ("RICH","WEALTHY"),("POOR","PENNILESS"),("OLD","ANCIENT"),("NEW","FRESH"),("EASY","SIMPLE"),("HARD","DIFFICULT"),
 ("FUNNY","HILARIOUS"),("STRANGE","ODD"),("SHAKE","TREMBLE"),("JUMP","LEAP"),("WALK","STROLL"),("RUN","SPRINT"),
 ("LOOK","GAZE"),("GRAB","SEIZE"),("THROW","HURL"),("HIDE","CONCEAL"),("FIND","DISCOVER"),("BUY","PURCHASE"),
 ("CHOOSE","SELECT"),("TRICK","DECEIVE"),("DAMP","MOIST"),("THIN","SLENDER"),("WIDE","BROAD"),("TRUE","GENUINE"),
 ("GIFT","PRESENT"),("PLAN","SCHEME"),("KEEP","RETAIN"),("FAKE","COUNTERFEIT")]
GENERIC_RIDDLES = [("I have hands but I cannot clap. What am I?", "CLOCK"),
 ("I have keys but I cannot open a single lock. What am I?", "PIANO"),
 ("The more of me you take, the more you leave behind. What am I?", "FOOTSTEPS"),
 ("I get wetter the more I dry things. What am I?", "TOWEL"),
 ("I have a neck and wear a cap, but I have no head. What am I?", "BOTTLE"),
 ("I follow you all day long but vanish in the dark. What am I?", "SHADOW"),
 ("I am full of holes, yet I still hold water. What am I?", "SPONGE"),
 ("I can fly without wings and cry without eyes. What am I?", "CLOUD"),
 ("I have a spine and many pages, but I am not a person. What am I?", "BOOK"),
 ("I have four legs and a back, but I cannot walk. You sit on me. What am I?", "CHAIR")]
CODE_TEMPLATES = ["FIND THE {a} BEFORE SUNSET", "THE {a} IS HIDDEN NEAR THE {b}", "MEET ME AT THE {a} TONIGHT",
 "BRING THE {a} AND THE {b}", "I SAW A {a} BY THE {b}", "NEVER TOUCH THE {a}", "THE SECRET IS THE {a}",
 "LOOK UNDER THE {a} FOR THE {b}", "A {a} CAN BEAT A {b}", "WE NEED THE {a} NOW", "WATCH OUT FOR THE {a}",
 "THE {a} KNOWS THE WAY"]
SENT_TEMPLATES = ["THE {a} WAS HIDDEN IN THE DARK", "WE FOUND A {a} ON THE HILL", "SHE CARRIED THE {a} HOME",
 "THE BIG {a} MADE A LOUD NOISE", "HE LOST THE {a} LAST NIGHT", "A TINY {a} SAT BY THE {b}",
 "THEY CAN SEE THE {a} FROM HERE", "OUR {a} IS BETTER THAN YOUR {b}", "THE OLD {a} IS VERY BRAVE",
 "NOBODY KNEW WHERE THE {a} WENT", "I WANT TO FIND A {a} TODAY", "THE {a} AND THE {b} WERE FRIENDS"]

# =====================================================================
# 4. GENERATORS  (return list of puzzle dicts)
# =====================================================================
def theme_words(T, minlen=3, maxlen=11):
    seen, out = set(), []
    for cat, ws in T["categories"].items():
        for w in ws:
            assert w.isalpha() and w.isupper(), w
            if w not in seen and minlen <= len(w) <= maxlen: seen.add(w); out.append((w, cat))
    return out

def take(pool, n, rng):
    pool = pool[:]; rng.shuffle(pool); return pool[:n]

def gen_anagram(T, n, rng):
    out = []
    for w, cat in take([x for x in theme_words(T, 4, 10)], 999, rng):
        keyset = ANAGRAM_KEYS.get("".join(sorted(w.lower())), set())
        if keyset - {w.lower()}: continue
        for _ in range(60):
            l = list(w); rng.shuffle(l); s = "".join(l)
            if s != w: break
        else: continue
        out.append(dict(prompt="Unscramble the letters to spell a word!", hint=cat, tiles=list(s), blanks=len(w), answer=w))
        if len(out) >= n: break
    return out

def gen_missing(T, n, rng):
    out = []
    for w, cat in take(theme_words(T, 4, 11), 999, rng):
        k = max(2, round(len(w) * 0.4)); idx = list(range(1, len(w)))
        for _ in range(50):
            gaps = sorted(rng.sample(idx, min(k, len(idx))))
            if all(b - a > 1 for a, b in zip(gaps, gaps[1:])): break
        else: gaps = idx[::2][:k]
        tiles = ["_" if i in gaps else ch for i, ch in enumerate(w)]
        out.append(dict(prompt="Fill in the missing letters to finish the word!", hint=cat, tiles=tiles, blanks=len(w), answer=w))
        if len(out) >= n: break
    return out

def gen_vowels(T, n, rng):
    out = []
    for w, cat in take(theme_words(T, 4, 10), 999, rng):
        if sum(ch in "AEIOU" for ch in w) < 2: continue
        tiles = ["_" if ch in "AEIOU" else ch for ch in w]
        out.append(dict(prompt="The vowels have vanished! Put them back to spell the word.", hint=cat, tiles=tiles, blanks=len(w), answer=w))
        if len(out) >= n: break
    return out

def gen_synonyms(T, n, rng):
    pairs = list(T["synonyms"]) + take(GENERIC_SYN, 999, rng)
    all_words = [w for p in pairs for w in p]
    out = []
    for t, a in pairs:
        pool = [w for w in all_words if w not in (t, a)]
        wrong = rng.sample(pool, 3); opts = [a] + wrong; rng.shuffle(opts)
        out.append(dict(prompt=f'Which word means almost the same as "{t}"?', opts=opts, answer="ABCD"[opts.index(a)] + ") " + a))
        if len(out) >= n: break
    return out

def gen_oddone(T, n, rng):
    cats = {k: v for k, v in T["categories"].items()}; names = list(cats); out = []; seen = set()
    for _ in range(n * 20):
        a, b = rng.sample(names, 2); three = rng.sample(cats[a], 3); odd = rng.choice(cats[b])
        if odd in cats[a] or any(w == odd for w in three): continue
        key = frozenset(three + [odd])
        if key in seen: continue
        seen.add(key); opts = three + [odd]; rng.shuffle(opts)
        out.append(dict(prompt="Three of these words belong together. Which one does NOT belong?", opts=opts,
                        answer="ABCD"[opts.index(odd)] + ") " + odd + "  (others: " + a.lower() + ")"))
        if len(out) >= n: break
    return out

def gen_sentence(T, n, rng):
    words = [w for w, _ in theme_words(T, 3, 9)]; out = []; seen = set()
    for _ in range(n * 20):
        t = rng.choice(SENT_TEMPLATES); a, b = rng.sample(words, 2); s = t.format(a=a, b=b)
        if s in seen: continue
        seen.add(s); ws = s.split(); sh = ws[:]
        for _ in range(50):
            rng.shuffle(sh)
            if sh != ws: break
        out.append(dict(prompt="Put the words in the right order to make a sentence!", words=sh, answer=s.capitalize() + "."))
        if len(out) >= n: break
    return out

def gen_riddle(T, n, rng):
    rs = take(T["riddles"], 999, rng) + take(GENERIC_RIDDLES, 999, rng)
    return [dict(prompt=q, blanks=len(a), answer=a) for q, a in rs[:n]]

def caesar(s, k): return "".join(chr((ord(ch) - 65 + k) % 26 + 65) if ch.isalpha() else ch for ch in s)

def gen_code(T, n, rng):
    words = [w for w, _ in theme_words(T, 3, 9)]; out = []; seen = set()
    for _ in range(n * 20):
        s = rng.choice(CODE_TEMPLATES).format(a=rng.choice(words), b=rng.choice(words))
        if s in seen: continue
        seen.add(s); k = rng.randint(1, 5)
        out.append(dict(prompt="Crack the code to read the secret message!", coded=caesar(s, k), shift=k, answer=s))
        if len(out) >= n: break
    return out

def bfs_path(a, b):
    prev = {a: None}; q = deque([a])
    while q:
        x = q.popleft()
        if x == b: break
        for y in nbrs(x):
            if y not in prev: prev[y] = x; q.append(y)
    if b not in prev: return None
    p = []; x = b
    while x: p.append(x); x = prev[x]
    return p[::-1]

def gen_ladder(T, n, rng):
    starts = [w.lower() for w, _ in theme_words(T, 4, 4) if w.lower() in LAD_SET] + take(sorted(LAD_SET), 400, rng)
    out = []; used = set()
    for s in starts:
        if s in used: continue
        dist = {s: 0}; q = deque([s]); far = []
        while q:
            x = q.popleft()
            if dist[x] >= 4: continue
            for y in nbrs(x):
                if y not in dist: dist[y] = dist[x] + 1; q.append(y)
        far = [w for w, d in dist.items() if d in (3, 4)]
        if not far: continue
        e = rng.choice(far); path = bfs_path(s, e)
        if not path or len(path) < 4: continue
        assert all(sum(a != b for a, b in zip(path[i], path[i + 1])) == 1 and path[i] in LAD_SET | {s, e} for i in range(len(path) - 1))
        used.add(s); out.append(dict(prompt="Change ONE letter each step to climb from the top word to the bottom word.",
                                     start=s.upper(), end=e.upper(), steps=len(path) - 2,
                                     answer=" > ".join(w.upper() for w in path)))
        if len(out) >= n: break
    return out
LAD_SET = {w for w in FOUR if nbrs(w)}

def solve_maze(walls, start, end):
    H = len(walls); W = len(walls[0])
    prev = {start: None}; q = deque([start])
    while q:
        r, c = q.popleft()
        if (r, c) == end: break
        for dr, dc in ((0, 1), (0, -1), (1, 0), (-1, 0)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < H and 0 <= nc < W and not walls[nr][nc] and (nr, nc) not in prev:
                prev[(nr, nc)] = (r, c); q.append((nr, nc))
    path = []; cur = end
    while cur is not None:
        path.append(cur); cur = prev.get(cur)
    return path[::-1]

def gen_maze(T, n, rng):
    cells = 7; gw = 2 * cells + 1; out = []
    for _ in range(n):
        walls = [[True] * gw for _ in range(gw)]
        visited = [[False] * cells for _ in range(cells)]
        stack = [(0, 0)]; visited[0][0] = True; walls[1][1] = False
        while stack:
            cx, cy = stack[-1]
            dirs = [(0, 1), (0, -1), (1, 0), (-1, 0)]; rng.shuffle(dirs)
            carved = False
            for dx, dy in dirs:
                nx, ny = cx + dx, cy + dy
                if 0 <= nx < cells and 0 <= ny < cells and not visited[ny][nx]:
                    walls[2 * cy + 1 + dy][2 * cx + 1 + dx] = False
                    walls[2 * ny + 1][2 * nx + 1] = False
                    visited[ny][nx] = True; stack.append((nx, ny)); carved = True; break
            if not carved: stack.pop()
        start = (1, 1); end = (gw - 2, gw - 2)
        walls[start[0]][0] = False            # entrance on left wall
        walls[end[0]][gw - 1] = False         # exit on right wall
        solution = solve_maze(walls, start, end)
        out.append(dict(prompt="Draw a path from the mascot to the star! Can you find the way?",
                        grid=walls, start=start, end=end, solution=solution,
                        answer="see maze solutions in the answer key"))
    return out

def gen_building(T, n, rng):
    cands = []
    for w, cat in theme_words(T, 6, 9):
        sw = subwords(w)
        if len(sw) >= 6: cands.append((w, sw))
    rng.shuffle(cands); out = []
    for w, sw in cands[:n]:
        l = list(w); rng.shuffle(l)
        out.append(dict(prompt="Build words (3+ letters) using ONLY these letters. Each letter once per word!",
                        tiles=l, goal=5, answer=", ".join(x.upper() for x in sw[:8]) + "...", source=w))
    return out

DIRS_EASY = [(0, 1), (1, 0)]
DIRS_MED = DIRS_EASY + [(1, 1), (-1, 1)]
DIRS_HARD = DIRS_MED + [(0, -1), (-1, 0), (-1, -1), (1, -1)]

def make_grid(words, n, dirs, rng):
    for _ in range(80):
        g = [[""] * n for _ in range(n)]; placed = {}; ok = True
        for w in sorted(words, key=len, reverse=True):
            done = False
            for _ in range(300):
                dr, dc = rng.choice(dirs); r, c = rng.randrange(n), rng.randrange(n)
                er, ec = r + dr * (len(w) - 1), c + dc * (len(w) - 1)
                if not (0 <= er < n and 0 <= ec < n): continue
                cells = [(r + dr * i, c + dc * i) for i in range(len(w))]
                if all(g[a][b] in ("", ch) for (a, b), ch in zip(cells, w)):
                    for (a, b), ch in zip(cells, w): g[a][b] = ch
                    placed[w] = cells; done = True; break
            if not done: ok = False; break
        if ok:
            letters = "".join(words)
            for a in range(n):
                for b in range(n):
                    if not g[a][b]: g[a][b] = rng.choice("ABCDEFGHIJKLMNOPRSTUW" if rng.random() < .6 else letters)
            return g, placed
    raise RuntimeError("grid failed")

def gen_wordsearch(T, n, rng):
    pool = [w for w, _ in theme_words(T, 4, 11)]; out = []
    for i in range(n):
        dirs = DIRS_EASY if i < n * .3 else DIRS_MED if i < n * .7 else DIRS_HARD
        cat = rng.choice(list(T["categories"]))
        cp = [w for w in T["categories"][cat] if 4 <= len(w) <= 11]
        ws = rng.sample(cp, min(8, len(cp))) + rng.sample([w for w in pool if w not in cp], 10 - min(8, len(cp)))
        g, placed = make_grid(ws, 13, dirs, rng)
        out.append(dict(prompt="Find all 10 hidden words. They can run " + ("across and down." if dirs is DIRS_EASY else
                        "across, down and diagonally." if dirs is DIRS_MED else "in ANY direction, even backwards!"),
                        grid=g, words=sorted(ws), placed=placed, answer="see grids", cat=cat))
    return out

GENERATORS = dict(anagram=gen_anagram, missing=gen_missing, vowels=gen_vowels, synonyms=gen_synonyms, oddone=gen_oddone,
                  sentence=gen_sentence, riddle=gen_riddle, code=gen_code, ladder=gen_ladder, maze=gen_maze,
                  building=gen_building, wordsearch=gen_wordsearch)

# =====================================================================
# 5. DRAWING HELPERS
# =====================================================================
def C(r, g=None, b=None):
    if g is None: r, g, b = r
    return Color(r / 255, g / 255, b / 255)
INK = C(25, 25, 45); WHITE = C(255, 255, 255); YELLOW = C(255, 225, 70); PINK = C(255, 70, 130)
ORANGE = C(255, 110, 40); GREEN = C(60, 200, 110); BLUE = C(60, 160, 255); PURPLE = C(150, 80, 240)

class Ctx: pass
X = Ctx()   # holds theme state during a build

def rrect(c, x, y, w, h, r, fill, stroke=INK, lw=2):
    c.setFillColor(fill); c.setStrokeColor(stroke); c.setLineWidth(lw); c.roundRect(x, y, w, h, r, stroke=1, fill=1)

def graffiti_text(c, x, y, s, size, col, shadow=INK, align="c", off=2.2):
    c.setFont("Helvetica-Bold", size)
    fn = {"c": c.drawCentredString, "l": c.drawString, "r": c.drawRightString}[align]
    c.setFillColor(shadow); fn(x + off, y - off, s); fn(x - .8, y, s); fn(x + .8, y, s)
    c.setFillColor(col); fn(x, y, s)

def drip(c, x, y, h, col):
    c.setFillColor(col); c.setStrokeColor(col); c.setLineWidth(3); c.line(x, y, x, y - h); c.circle(x, y - h, 2.6, stroke=0, fill=1)

def star(c, x, y, r, col, rot=0):
    pts = []
    for i in range(10):
        rr = r if i % 2 == 0 else r * .42; a = math.radians(rot + i * 36 - 90); pts.append((x + rr * math.cos(a), y + rr * math.sin(a)))
    p = c.beginPath(); p.moveTo(*pts[0])
    for q in pts[1:]: p.lineTo(*q)
    p.close(); c.setFillColor(col); c.setStrokeColor(INK); c.setLineWidth(1.2); c.drawPath(p, fill=1, stroke=1)

def splatter(c, n, cols):
    for _ in range(n):
        c.setFillColor(random.choice(cols)); c.setFillAlpha(.3)
        c.circle(random.uniform(0, W), random.uniform(0, H), random.uniform(.6, 3), stroke=0, fill=1)
    c.setFillAlpha(1)

def bricks(c, col):
    c.setStrokeColor(col); c.setLineWidth(.8); row = 0; y = 0
    while y < H:
        c.line(0, y, W, y)
        for x in range(0 if row % 2 == 0 else 30, int(W), 60): c.line(x, y, x, min(y + 20, H))
        y += 20; row += 1

# ---- doodle icons -----------------------------------------------------------
def i_star(c, x, y): star(c, x, y, 8, X.pal[0], random.randint(-20, 20))
def i_spiral(c, x, y):
    c.setStrokeColor(X.pal[4]); c.setLineWidth(1.6); p = c.beginPath(); first = True
    for i in range(0, 220, 8):
        a = math.radians(i * 6); rr = 9 * i / 220; px, py = x + rr * math.cos(a), y + rr * math.sin(a)
        (p.moveTo if first else p.lineTo)(px, py); first = False
    c.drawPath(p, stroke=1, fill=0)
def i_wave(c, x, y):
    c.setStrokeColor(X.pal[2]); c.setLineWidth(2); p = c.beginPath(); p.moveTo(x - 9, y)
    for i in range(1, 5): p.curveTo(x - 9 + i * 4 - 2, y + 5 * (1 if i % 2 else -1), x - 9 + i * 4 - 1, y + 5 * (1 if i % 2 else -1), x - 9 + i * 4, y)
    c.drawPath(p, stroke=1, fill=0)
def i_anchor(c, x, y):
    c.setStrokeColor(INK); c.setLineWidth(2); c.line(x, y + 10, x, y - 9); c.line(x - 5, y + 5, x + 5, y + 5)
    c.arc(x - 9, y - 12, x + 9, y + 2, 200, 140); c.circle(x, y + 12, 2.5, stroke=1, fill=0)
def i_xmark(c, x, y):
    c.setStrokeColor(C(200, 40, 40)); c.setLineWidth(3.5); c.line(x - 7, y - 7, x + 7, y + 7); c.line(x - 7, y + 7, x + 7, y - 7)
def i_ship(c, x, y):
    c.setFillColor(C(150, 100, 60)); c.setStrokeColor(INK); c.setLineWidth(1.3)
    p = c.beginPath(); p.moveTo(x - 12, y - 4); p.lineTo(x + 12, y - 4); p.lineTo(x + 7, y - 11); p.lineTo(x - 7, y - 11); p.close(); c.drawPath(p, fill=1, stroke=1)
    c.line(x, y - 4, x, y + 12); c.setFillColor(WHITE); p = c.beginPath(); p.moveTo(x + 1, y + 11); p.lineTo(x + 10, y); p.lineTo(x + 1, y); p.close(); c.drawPath(p, fill=1, stroke=1)
def i_planet(c, x, y):
    c.setFillColor(X.pal[3]); c.setStrokeColor(INK); c.setLineWidth(1.4); c.circle(x, y, 7, stroke=1, fill=1)
    c.saveState(); c.translate(x, y); c.rotate(-20); c.ellipse(-13, -3.5, 13, 3.5, stroke=1, fill=0); c.restoreState()
def i_rocket(c, x, y):
    c.saveState(); c.translate(x, y); c.rotate(30); c.setFillColor(WHITE); c.setStrokeColor(INK); c.setLineWidth(1.3)
    p = c.beginPath(); p.moveTo(0, 14); p.curveTo(8, 6, 7, -6, 5, -10); p.lineTo(-5, -10); p.curveTo(-7, -6, -8, 6, 0, 14); c.drawPath(p, fill=1, stroke=1)
    c.setFillColor(X.pal[0]); c.circle(0, 3, 3, stroke=1, fill=1); c.setFillColor(YELLOW); p = c.beginPath(); p.moveTo(-4, -10); p.lineTo(4, -10); p.lineTo(0, -17); p.close(); c.drawPath(p, fill=1, stroke=1); c.restoreState()
def i_moon(c, x, y):
    c.setFillColor(YELLOW); c.setStrokeColor(INK); c.setLineWidth(1.4); c.circle(x, y, 8, stroke=1, fill=1)
    c.setFillColor(C(*THEME_BG)); c.setStrokeColor(C(*THEME_BG)); c.circle(x + 5, y + 3, 7, stroke=0, fill=1)
    c.setStrokeColor(INK); c.arc(x - 8, y - 8, x + 8, y + 8, 100, 160)
def i_wand(c, x, y):
    c.setStrokeColor(INK); c.setLineWidth(3); c.line(x - 8, y - 9, x + 6, y + 5); star(c, x + 8, y + 8, 6, YELLOW)
def i_potion(c, x, y):
    c.setFillColor(X.pal[1]); c.setStrokeColor(INK); c.setLineWidth(1.3); c.circle(x, y - 3, 8, stroke=1, fill=1)
    c.setFillColor(WHITE); c.rect(x - 3, y + 4, 6, 8, stroke=1, fill=1); c.setFillColor(C(190, 140, 90)); c.rect(x - 4, y + 12, 8, 3, stroke=1, fill=1)
def i_bulb(c, x, y):
    c.setFillColor(YELLOW); c.setStrokeColor(INK); c.setLineWidth(1.4); c.circle(x, y, 8, stroke=1, fill=1)
    c.setFillColor(C(200, 200, 210)); c.rect(x - 4, y - 15, 8, 6, stroke=1, fill=1)
def i_pencil(c, x, y):
    c.saveState(); c.translate(x, y); c.rotate(35); c.setFillColor(X.pal[1]); c.setStrokeColor(INK); c.setLineWidth(1.3); c.rect(-4, -16, 8, 26, stroke=1, fill=1)
    c.setFillColor(C(255, 220, 180)); p = c.beginPath(); p.moveTo(-4, -16); p.lineTo(4, -16); p.lineTo(0, -25); p.close(); c.drawPath(p, stroke=1, fill=1); c.restoreState()
def i_smiley(c, x, y):
    c.setFillColor(YELLOW); c.setStrokeColor(INK); c.setLineWidth(1.6); c.circle(x, y, 8, stroke=1, fill=1); c.setFillColor(INK)
    c.circle(x - 3, y + 2, .9, stroke=0, fill=1); c.circle(x + 3, y + 2, .9, stroke=0, fill=1); c.arc(x - 4, y - 5, x + 4, y + 3, 200, 140)
def i_heart(c, x, y):
    s = 5; c.setFillColor(PINK); c.setStrokeColor(INK); c.setLineWidth(1.2); p = c.beginPath(); p.moveTo(x, y - s)
    p.curveTo(x - 2 * s, y, x - s, y + s * 1.4, x, y + s * .4); p.curveTo(x + s, y + s * 1.4, x + 2 * s, y, x, y - s); c.drawPath(p, stroke=1, fill=1)
ICON_FUNCS = dict(star=i_star, spiral=i_spiral, wave=i_wave, anchor=i_anchor, xmark=i_xmark, ship=i_ship, planet=i_planet,
                  rocket=i_rocket, moon=i_moon, wand=i_wand, potion=i_potion, bulb=i_bulb, pencil=i_pencil, smiley=i_smiley, heart=i_heart)
THEME_BG = (255, 255, 255)

def margin_doodles(c):
    fns = [ICON_FUNCS[k] for k in X.T["icons"]] * 2 + [i_bulb, i_pencil, i_smiley, i_heart, i_spiral]
    for side in (19, W - 19):
        y = H - 110
        while y > 60: random.choice(fns)(c, side, y); y -= random.randint(50, 68)

def page_bg(c):
    c.setFillColor(C(*X.T["bg"])); c.rect(0, 0, W, H, stroke=0, fill=1)
    bricks(c, C(*[max(0, v - 14) for v in X.T["bg"]])); splatter(c, 60, X.pal); margin_doodles(c)

def page_header(c, text, col):
    c.setFillColor(INK); c.rect(0, H - 62, W, 62, stroke=0, fill=1); c.setFillColor(col); c.rect(0, H - 66, W, 4, stroke=0, fill=1)
    graffiti_text(c, W / 2, H - 44, text, 28 if len(text) < 24 else 24, col, shadow=C(0, 0, 0), off=2.5)
    for x in (70, 170, 330, 470, 525): drip(c, x, H - 66, random.randint(6, 14), col)
    star(c, 40, H - 32, 12, YELLOW, 10); star(c, W - 40, H - 32, 12, YELLOW, -10)

def footer(c, label):
    c.setFillColor(C(120, 120, 140)); c.setFont("Helvetica-Bold", 9)
    c.drawCentredString(W / 2, 18, f"*  *  *   {label}   |   PAGE {c.getPageNumber()}   *  *  *")

def mascot(c, x, y, s=1.0, say=None):
    c.saveState(); c.translate(x, y); c.scale(s, s)
    c.setFillColor(X.pal[0]); c.setStrokeColor(INK); c.setLineWidth(2.5); c.roundRect(-22, -28, 44, 50, 14, stroke=1, fill=1)
    c.setFillColor(WHITE); c.circle(-9, 6, 8, stroke=1, fill=1); c.circle(9, 6, 8, stroke=1, fill=1)
    c.setFillColor(INK); c.circle(-7, 6, 3, stroke=0, fill=1); c.circle(11, 6, 3, stroke=0, fill=1)
    c.setLineWidth(2); c.arc(-10, -16, 10, -2, 200, 140)
    hat = X.T["mascot"]["hat"]
    if hat == "pirate":
        c.setFillColor(INK); p = c.beginPath(); p.moveTo(-26, 22); p.curveTo(-18, 38, 18, 38, 26, 22); p.close(); c.drawPath(p, fill=1, stroke=1)
        c.setFillColor(WHITE); c.circle(0, 28, 3, stroke=0, fill=1)
    elif hat == "wizard":
        c.setFillColor(X.pal[4]); p = c.beginPath(); p.moveTo(-20, 22); p.lineTo(0, 54); p.lineTo(20, 22); p.close(); c.drawPath(p, fill=1, stroke=1); star(c, 0, 36, 5, YELLOW)
    else:
        c.setStrokeColor(INK); c.line(-10, 22, -14, 32); c.line(10, 22, 14, 32); star(c, -14, 34, 4, YELLOW); star(c, 14, 34, 4, YELLOW)
    c.restoreState()
    if say:
        bw = c.stringWidth(say, "Helvetica-Bold", 10) + 20
        rrect(c, x + 34 * s, y + 10 * s, bw, 24, 10, WHITE, lw=1.8); c.setFillColor(INK); c.setFont("Helvetica-Bold", 10); c.drawString(x + 44 * s, y + 18 * s, say)

def tile_row(c, letters, cx, y, size, fill, fs, gap=4):
    n = len(letters); total = n * size + (n - 1) * gap; x = cx - total / 2
    for ch in letters:
        rrect(c, x, y, size, size, 5, fill if ch != "_" else WHITE, lw=1.8)
        if ch != "_": c.setFillColor(INK); c.setFont("Helvetica-Bold", fs); c.drawCentredString(x + size / 2, y + size / 2 - fs * .35, ch)
        x += size + gap

def blank_row(c, cx, y, n, w=22, gap=5):
    total = n * w + (n - 1) * gap; x = cx - total / 2; c.setStrokeColor(INK); c.setLineWidth(1.8)
    for _ in range(n): c.line(x, y, x + w, y); x += w + gap

# =====================================================================
# 6. CARD RENDERERS  (each draws inside x, y, w, ch  - content area under the title strip)
# =====================================================================
def prompt(c, text, x, y, w, ch, col, size=12):
    c.setFillColor(INK); c.setFont("Helvetica-Bold", size); py = y + ch - 16
    for ln in simpleSplit(text, "Helvetica-Bold", size, w - 40): c.drawString(x + 20, py, ln); py -= size + 3
    return py

def hint_chip(c, text, x, py):
    c.setFont("Helvetica-Bold", 9); tw = c.stringWidth("HINT: " + text, "Helvetica-Bold", 9) + 14
    rrect(c, x + 20, py - 9, tw, 15, 6, YELLOW, lw=1.2); c.setFillColor(INK); c.drawString(x + 27, py - 4, "HINT: " + text)

def r_tiles(c, p, x, y, w, ch, col):
    py = prompt(c, p["prompt"], x, y, w, ch, col); hint_chip(c, p["hint"], x, py - 2)
    n = len(p["tiles"]); size = min(30, (w - 60) / n - 4)
    tile_row(c, p["tiles"], x + w / 2, y + 52, size, YELLOW if "_" not in p["tiles"] else C(235, 255, 235), size * .65)
    c.setFont("Helvetica-Bold", 10); c.setFillColor(INK); c.drawString(x + 20, y + 28, "MY ANSWER:")
    blank_row(c, x + w / 2 + 40, y + 28, p["blanks"], 22)

def option_grid(c, opts, x, y, w, col):
    for i, o in enumerate(opts):
        ox = x + 30 + (i % 2) * (w / 2 - 10); oy = y + 68 - (i // 2) * 34
        rrect(c, ox, oy - 8, w / 2 - 50, 26, 8, C(235, 245, 255), lw=1.8)
        c.setFillColor(INK); c.circle(ox + 15, oy + 5, 9, stroke=0, fill=1); c.setFillColor(WHITE); c.setFont("Helvetica-Bold", 11); c.drawCentredString(ox + 15, oy + 1.5, "ABCD"[i])
        c.setFillColor(INK); c.setFont("Helvetica-Bold", 13); c.drawString(ox + 34, oy + 1, o)

def r_options(c, p, x, y, w, ch, col): prompt(c, p["prompt"], x, y, w, ch, col); option_grid(c, p["opts"], x, y, w, col)

def r_riddle(c, p, x, y, w, ch, col):
    py = prompt(c, p["prompt"], x, y, w, ch, col, 14)
    c.setFont("Helvetica-Bold", 10); c.setFillColor(INK); c.drawString(x + 20, y + 46, "I AM A:")
    blank_row(c, x + w / 2 + 20, y + 46, p["blanks"], 20, 4); c.setFont("Helvetica-Oblique", 9); c.drawString(x + 20, y + 30, f"({p['blanks']} letters)")
    star(c, x + w - 40, y + ch - 40, 10, YELLOW); c.setFillColor(col); c.setFont("Helvetica-Bold", 30); c.drawCentredString(x + w - 40, y + ch - 80, "?")

def r_building(c, p, x, y, w, ch, col):
    py = prompt(c, p["prompt"], x, y, w, ch, col, 11); n = len(p["tiles"]); size = 28
    c.setFont("Helvetica-Bold", 10); c.setFillColor(INK); c.drawString(x + 20, y + ch - 62, "LETTERS:")
    for k, chh in enumerate(p["tiles"]):
        rrect(c, x + 90 + k * 32, y + ch - 72, size, size, 5, C(235, 220, 255), lw=1.8)
        c.setFillColor(INK); c.setFont("Helvetica-Bold", 17); c.drawCentredString(x + 90 + k * 32 + 14, y + ch - 63, chh)
    bx = x + w - 130; rrect(c, bx, y + ch - 72, 108, 28, 8, YELLOW, lw=1.5); c.setFillColor(INK); c.setFont("Helvetica-Bold", 10); c.drawCentredString(bx + 54, y + ch - 62, f"GOAL: {p['goal']}+ WORDS")
    c.drawString(x + 20, y + ch - 92, "MY WORDS:")
    for r in range(4):
        for k in range(3):
            lx = x + 20 + k * ((w - 40) / 3); c.setLineWidth(1.3); c.setStrokeColor(INK); c.line(lx, y + ch - 112 - r * 22 + 6, lx + (w - 60) / 3 - 8, y + ch - 112 - r * 22 + 6)

def r_code(c, p, x, y, w, ch, col):
    py = prompt(c, p["prompt"], x, y, w, ch, col)
    rrect(c, x + 20, y + ch - 56, 150, 18, 6, YELLOW, lw=1.2); c.setFillColor(INK); c.setFont("Helvetica-Bold", 9); c.drawString(x + 27, y + ch - 50, f"KEY: A BECOMES {chr(65 + p['shift'])}  (shift {p['shift']})")
    words = p["coded"].split(); lines = [""]
    for wd in words:
        if len(lines[-1]) + len(wd) + 1 > 30: lines.append(wd)
        else: lines[-1] = (lines[-1] + " " + wd).strip()
    rrect(c, x + 20, y + ch - 66 - 22 * len(lines) - 8, w - 40, 22 * len(lines) + 10, 8, C(40, 40, 70), lw=1.8)
    c.saveState(); c.setFillColor(YELLOW)
    for i, ln in enumerate(lines):
        t = c.beginText(x + 34, y + ch - 80 - i * 22); t.setFont("Courier-Bold", 16); t.setCharSpace(3); t.textLine(ln); c.drawText(t)
    c.restoreState()
    c.setStrokeColor(INK); c.setLineWidth(1.4); base = y + 42
    for i in range(2): c.line(x + 20, base - i * 18, x + w - 120, base - i * 18)

def r_ladder(c, p, x, y, w, ch, col):
    py = prompt(c, p["prompt"], x, y, w, ch, col, 11); size = 22; rows = p["steps"] + 2; top = y + ch - 40
    gap = min(28, (ch - 54) / rows)
    for i in range(rows):
        yy = top - i * gap - size
        if i == 0: tile_row(c, list(p["start"]), x + w / 2, yy, size, C(255, 230, 150), 15)
        elif i == rows - 1: tile_row(c, list(p["end"]), x + w / 2, yy, size, C(190, 245, 200), 15)
        else: tile_row(c, ["_"] * 4, x + w / 2, yy, size, WHITE, 15)
    c.setFont("Helvetica-Bold", 10); c.setFillColor(INK); c.drawString(x + 20, top - size / 2 - 3, "START"); c.drawString(x + 20, top - (rows - 1) * gap - size / 2 - 3, "END")
    c.setFillColor(col); c.setFont("Helvetica-Bold", 20); c.drawCentredString(x + w - 60, y + ch / 2, "^")

def r_maze(c, p, x, y, w, ch, col):
    py = prompt(c, p["prompt"], x, y, w, ch, col, 11)
    grid = p["grid"]; n = len(grid)
    cell = min(18, (w - 150) / n, (ch - 60) / n)
    mw = n * cell
    gx = x + (w - mw) / 2
    gy = y + 14 + (ch - 44 - mw) / 2
    for r in range(n):
        for cc in range(n):
            c.setFillColor(INK if grid[r][cc] else WHITE)
            c.rect(gx + cc * cell, gy + (n - 1 - r) * cell, cell, cell, stroke=0, fill=1)
    c.setStrokeColor(INK); c.setLineWidth(2); c.rect(gx, gy, mw, mw, stroke=1, fill=0)
    sr, sc = p["start"]; sy = gy + (n - 1 - sr) * cell + cell / 2
    mascot(c, gx - 32, sy - 12, 0.55)
    c.setStrokeColor(GREEN); c.setLineWidth(2); c.line(gx - 6, sy, gx + 3, sy)
    er, ec = p["end"]; ey = gy + (n - 1 - er) * cell + cell / 2
    star(c, gx + mw + 20, ey, 11, YELLOW, 12)
    c.setStrokeColor(PINK); c.setLineWidth(2); c.line(gx + mw - 3, ey, gx + mw + 7, ey)

def r_sentence(c, p, x, y, w, ch, col):
    prompt(c, p["prompt"], x, y, w, ch, col); cx, cy = x + 20, y + ch - 54; c.setFont("Helvetica-Bold", 11)
    for wd in p["words"]:
        tw = c.stringWidth(wd, "Helvetica-Bold", 11) + 16
        if cx + tw > x + w - 20: cx = x + 20; cy -= 26
        rrect(c, cx, cy - 4, tw, 20, 6, C(255, 235, 200), lw=1.5); c.setFillColor(INK); c.drawString(cx + 8, cy + 2, wd); cx += tw + 6
    c.setStrokeColor(INK); c.setLineWidth(1.4)
    for i in range(2): c.line(x + 20, y + 44 - i * 18, x + w - 120, y + 44 - i * 18)

def r_wordsearch(c, p, x, y, w, ch, col):
    prompt(c, p["prompt"], x, y, w, ch, col); n = 13; cell = 32; gx = x + (w - n * cell) / 2; gy = y + ch - 36 - n * cell
    rrect(c, gx - 6, gy - 6, n * cell + 12, n * cell + 12, 10, WHITE, lw=2.5)
    for r in range(n):
        for k in range(n):
            c.setFillColor(INK); c.setFont("Helvetica-Bold", 16); c.drawCentredString(gx + k * cell + cell / 2, gy + (n - 1 - r) * cell + 9, p["grid"][r][k])
    c.setFont("Helvetica-Bold", 11); c.setFillColor(INK); c.drawString(x + 30, gy - 34, "WORDS TO FIND  (topic: " + p["cat"].lower() + ")")
    for i, wd in enumerate(p["words"]):
        cx = x + 30 + (i % 3) * 165; cy = gy - 58 - (i // 3) * 24
        c.setStrokeColor(INK); c.setLineWidth(1.6); c.rect(cx, cy - 2, 11, 11, stroke=1, fill=0); c.setFont("Helvetica-Bold", 12); c.drawString(cx + 18, cy, wd)

RENDER = dict(anagram=r_tiles, missing=r_tiles, vowels=r_tiles, synonyms=r_options, oddone=r_options, sentence=r_sentence,
              riddle=r_riddle, code=r_code, ladder=r_ladder, maze=r_maze, building=r_building, wordsearch=r_wordsearch)

def draw_card(c, sec, p, ytop, h, col):
    x, w = 40, W - 80; y = ytop - h
    c.setFillColor(C(200, 200, 215)); c.roundRect(x + 4, y - 4, w, h, 12, stroke=0, fill=1); rrect(c, x, y, w, h, 12, WHITE, lw=2.5)
    c.setFillColor(col); c.setStrokeColor(INK); c.setLineWidth(2.5); c.roundRect(x, ytop - 30, w, 30, 12, stroke=1, fill=1); c.rect(x + 1, ytop - 30, w - 2, 14, stroke=0, fill=1)
    c.setStrokeColor(INK); c.line(x, ytop - 30, x + w, ytop - 30)
    c.setFillColor(INK); c.circle(x + 24, ytop - 15, 15, stroke=0, fill=1); c.setFillColor(YELLOW); c.setFont("Helvetica-Bold", 12 if p["num"] > 99 else 14); c.drawCentredString(x + 24, ytop - 20, str(p["num"]))
    c.setFillColor(WHITE); c.setFont("Helvetica-Bold", 14); c.drawString(x + 48, ytop - 20, sec["card"])
    c.setFont("Helvetica-Bold", 9); c.drawString(x + 56 + c.stringWidth(sec["card"], "Helvetica-Bold", 14), ytop - 19, f"[{TYPE_TAG[sec['key']]}]")
    c.setFillColor(WHITE); c.setStrokeColor(INK); c.setLineWidth(1.5); c.roundRect(x + w - 245, ytop - 25, 70, 19, 6, stroke=1, fill=1)
    c.setFillColor(INK); c.setFont("Helvetica-Bold", 9); c.drawCentredString(x + w - 210, ytop - 19, sec["diff"])
    RENDER[sec["key"]](c, p, x, y, w, h - 34, col)

# =====================================================================
# 7. PAGES
# =====================================================================
def cover(c):
    page_bg(c); c.setFillColor(INK); c.rect(0, H - 330, W, 260, stroke=0, fill=1)
    c.saveState(); c.translate(W / 2, H - 150); c.rotate(-4)
    graffiti_text(c, 0, 20, BOOK["title_1"], 70, YELLOW, off=4); graffiti_text(c, 0, -50, BOOK["title_2"], 52, X.pal[0], off=4); c.restoreState()
    for x, col in zip((60, 150, 270, 400, 520), X.pal): drip(c, x, H - 330, random.randint(12, 30), col)
    rrect(c, 90, H - 395, W - 180, 38, 10, X.pal[3], lw=3); c.setFillColor(WHITE); c.setFont("Helvetica-Bold", 17); c.drawCentredString(W / 2, H - 382, X.T["edition"])
    graffiti_text(c, W / 2, H - 450, f"{X.total_puzzles} FUN WORD PUZZLES", 26, X.pal[1], off=2)
    c.setFillColor(INK); c.setFont("Helvetica-Bold", 13); c.drawCentredString(W / 2, H - 475, f"{BOOK['ages']}   |   HAVE FUN!   |   EARN YOUR CERTIFICATE")
    rrect(c, 70, H - 600, W - 140, 100, 14, WHITE, lw=3); c.setFillColor(INK); c.setFont("Helvetica-Bold", 15); c.drawCentredString(W / 2, H - 530, X.T["tagline"])
    c.setFont("Helvetica", 12)
    for i, ln in enumerate(["Grab a pencil and your imagination,", "then check the answer key at the back of the book."]): c.drawCentredString(W / 2, H - 553 - i * 16, ln)
    mascot(c, W - 80, 130, 1.5); mascot(c, 80, 130, 1.5); star(c, 105, H - 500, 14, YELLOW, 15); star(c, W - 105, H - 500, 14, PINK, -15)
    c.setFillColor(C(120, 120, 140)); c.setFont("Helvetica-Oblique", 9); c.drawCentredString(W / 2, 40, "All puzzles in this book are original."); c.showPage()

def how_to_play(c):
    page_bg(c); page_header(c, "HOW TO PLAY", YELLOW); y = H - 120
    steps = [("PICK A PUZZLE", "Choose any puzzle that looks fun - there's no rush!"), ("WRITE YOUR ANSWER", "Pencil is best - you can rub out mistakes."),
             ("GET CREATIVE", "Colour in the doodles and decorate the pages as you go!"), ("CHECK THE KEY", "Answers are at the back. No peeking first!"),
             ("BE A WORD WIZARD", "Finish puzzles to earn your Official Word Wizard certificate!")]
    for i, (head, body) in enumerate(steps):
        col = X.pal[i % 5]; rrect(c, 55, y - 62, W - 110, 66, 12, WHITE, lw=2.5)
        c.setFillColor(col); c.setStrokeColor(INK); c.setLineWidth(2.5); c.circle(95, y - 29, 22, stroke=1, fill=1); c.setFillColor(WHITE); c.setFont("Helvetica-Bold", 26); c.drawCentredString(95, y - 38, str(i + 1))
        c.setFillColor(INK); c.setFont("Helvetica-Bold", 15); c.drawString(135, y - 22, head); c.setFont("Helvetica", 11); c.drawString(135, y - 42, body); y -= 82
    mascot(c, 100, 90, 1.0, random.choice(X.T["says"])); footer(c, "HOW TO PLAY"); c.showPage()

def divider(c, sec, idx, col, first_page):
    page_bg(c); c.setFillColor(INK); c.rect(0, H - 330, W, 270, stroke=0, fill=1)
    graffiti_text(c, W / 2, H - 140, f"PART {idx}", 30, YELLOW, off=3)
    t = sec["title"]; graffiti_text(c, W / 2, H - 205, t, 46 if len(t) < 16 else 34 if len(t) < 24 else 28, col, off=4)
    for x, cc in zip((70, 180, 300, 420, 520), X.pal): drip(c, x, H - 330, random.randint(10, 26), cc)
    graffiti_text(c, W / 2, H - 270, f"{sec['pages'] * sec['per_page']} puzzles  |  {sec['diff']}", 14, WHITE, off=1.5)
    rrect(c, 60, H - 480, W - 120, 110, 14, WHITE, lw=3); c.setFillColor(INK); c.setFont("Helvetica-Bold", 14); c.drawCentredString(W / 2, H - 400, "HOW IT WORKS")
    c.setFont("Helvetica", 12)
    for i, ln in enumerate(simpleSplit(sec["blurb"], "Helvetica", 12, W - 170)): c.drawCentredString(W / 2, H - 428 - i * 17, ln)
    mascot(c, 110, 180, 1.8, random.choice(X.T["says"])); star(c, W - 100, 200, 22, col, 12); star(c, W - 150, 150, 12, YELLOW, -12)
    footer(c, "WORD GAMES"); c.showPage()

def puzzle_pages(c, sec, puzzles, col):
    k = sec["per_page"]; top = H - 82; bottom = 40; gap = 10; h = (top - bottom - (k - 1) * gap) / k
    for pg in range(0, len(puzzles), k):
        page_bg(c); page_header(c, sec["title"], col); t = top
        for p in puzzles[pg:pg + k]: draw_card(c, sec, p, t, h, col); t -= h + gap
        footer(c, f'PUZZLES {puzzles[pg]["num"]} - {puzzles[min(pg + k, len(puzzles)) - 1]["num"]}'); c.showPage()

ANS_ROWS, ANS_COLS = 52, 2
def answer_items(secs):
    items = []
    for s in secs:
        items.append(("H", s["title"], s["col"]))
        if s["key"] == "wordsearch": items.append(("N", "Full solutions are on the word search solution pages.", None))
        elif s["key"] == "maze": items.append(("MZ", None, s["puzzles"]))
        else:
            for p in s["puzzles"]: items.append(("E", p["num"], p["answer"]))
    return items

def ans_layout_pages(secs):
    col = 0; r = 0; pages = 1
    for s in secs:
        need = 1 + (1 if s["key"] == "wordsearch" else
                    1 + math.ceil(len(s["puzzles"]) / 2) * 9 if s["key"] == "maze" else
                    len(s["puzzles"]))
        if r + need > ANS_ROWS:
            col += 1; r = 0
            if col >= ANS_COLS: pages += 1; col = 0
        r += need
    ws = next((s for s in secs if s["key"] == "wordsearch"), None)
    if ws: pages += math.ceil(len(ws["puzzles"]) / 12)
    return pages

def answer_pages(c, secs):
    items = answer_items(secs)
    colw = (W - 100) / ANS_COLS
    col = 0; r = 0

    def new_page():
        nonlocal col, r
        footer(c, "ANSWER KEY"); c.showPage()
        page_bg(c); page_header(c, "ANSWER KEY", X.pal[0])
        col = 0; r = 0

    def ensure_room(rows_needed):
        nonlocal col, r
        if r + rows_needed > ANS_ROWS:
            col += 1; r = 0
            if col >= ANS_COLS: new_page()

    page_bg(c); page_header(c, "ANSWER KEY", X.pal[0])
    for typ, a, b in items:
        if typ == "MZ":
            puzzles = b
            bands = math.ceil(len(puzzles) / 2)
            ensure_room(1 + bands * 9)
            x0 = 50 + col * colw; y0 = H - 92 - r * 13.2
            c.setFillColor(INK); c.setFont("Helvetica-Oblique", 7.5)
            c.drawString(x0 + 4, y0, "Solutions:")
            cell = 6.2; mz = 15 * cell
            for bi in range(bands):
                by = y0 - 16 - bi * (mz + 18)
                for mi, p in enumerate(puzzles[bi * 2:bi * 2 + 2]):
                    gx = x0 + 6 + mi * (mz + 20); gy = by - mz
                    c.setFillColor(INK); c.setFont("Helvetica-Bold", 6.5); c.drawString(gx, by + 3, f"#{p['num']}")
                    n = len(p["grid"])
                    for rr in range(n):
                        for kk in range(n):
                            c.setFillColor(INK if p["grid"][rr][kk] else WHITE)
                            c.rect(gx + kk * cell, gy + (n - 1 - rr) * cell, cell, cell, stroke=0, fill=1)
                    path = p["solution"]
                    if len(path) > 1:
                        pts = [(gx + cc * cell + cell / 2, gy + (n - 1 - rr) * cell + cell / 2) for rr, cc in path]
                        pp = c.beginPath(); pp.moveTo(*pts[0])
                        for pt in pts[1:]: pp.lineTo(*pt)
                        c.saveState(); c.setLineCap(1); c.setStrokeColor(YELLOW); c.setLineWidth(2.2)
                        c.drawPath(pp, stroke=1, fill=0); c.restoreState()
                    c.setStrokeColor(INK); c.setLineWidth(0.8); c.rect(gx, gy, n * cell, n * cell, stroke=1, fill=0)
            r += 1 + bands * 9
        else:
            ensure_room(1)
            x = 50 + col * colw; y = H - 92 - r * 13.2
            if typ == "H":
                c.setFillColor(b); c.roundRect(x, y - 3, colw - 10, 12, 3, stroke=0, fill=1)
                c.setFillColor(WHITE); c.setFont("Helvetica-Bold", 8.5); c.drawString(x + 4, y, a)
            elif typ == "N":
                c.setFillColor(INK); c.setFont("Helvetica-Oblique", 7.5); c.drawString(x + 4, y, a)
            else:
                txt = f"{a}.  {b}"; fs = 8.5
                while c.stringWidth(txt, "Helvetica", fs) > colw - 14 and fs > 5.5: fs -= .3
                c.setFillColor(INK); c.setFont("Helvetica", fs); c.drawString(x + 4, y, txt)
            r += 1
    footer(c, "ANSWER KEY"); c.showPage()
    ws = [s for s in secs if s["key"] == "wordsearch"]
    if ws:
        ps = ws[0]["puzzles"]; per = 12
        for pg in range(0, len(ps), per):
            page_bg(c); page_header(c, "WORD SEARCH SOLUTIONS", PURPLE)
            for i, p in enumerate(ps[pg:pg + per]):
                col_i, r_i = i % 3, i // 3; cell = 10.5; gx = 45 + col_i * 175; gy = H - 100 - (r_i + 1) * 175 + 20
                c.setFillColor(INK); c.setFont("Helvetica-Bold", 9); c.drawString(gx, gy + 13 * cell + 6, f"PUZZLE {p['num']}")
                hl = {cell_ for cells in p["placed"].values() for cell_ in cells}
                for rr in range(13):
                    for kk in range(13):
                        px, py = gx + kk * cell, gy + (12 - rr) * cell
                        if (rr, kk) in hl: c.setFillColor(YELLOW); c.rect(px, py - 1, cell, cell, stroke=0, fill=1)
                        c.setFillColor(INK if (rr, kk) in hl else C(160, 160, 175)); c.setFont("Helvetica-Bold", 7); c.drawCentredString(px + cell / 2, py + 2, p["grid"][rr][kk])
            footer(c, "WORD SEARCH SOLUTIONS"); c.showPage()

def certificate(c, total):
    page_bg(c)
    c.setStrokeColor(INK); c.setLineWidth(4); c.rect(28, 28, W - 56, H - 56, stroke=1, fill=0)
    c.setLineWidth(1.5); c.rect(38, 38, W - 76, H - 76, stroke=1, fill=0)
    graffiti_text(c, W / 2, H - 130, "CERTIFICATE", 46, YELLOW, off=3)
    graffiti_text(c, W / 2, H - 180, "OF WORD POWER", 30, X.pal[0], off=2)
    c.setFillColor(INK); c.setFont("Helvetica-Bold", 15); c.drawCentredString(W / 2, H - 250, "This certifies that")
    c.setStrokeColor(INK); c.setLineWidth(2); c.line(W / 2 - 150, H - 290, W / 2 + 150, H - 290)
    c.setFont("Helvetica-Oblique", 10); c.setFillColor(C(140, 140, 160)); c.drawCentredString(W / 2, H - 305, "(write your name here)")
    c.setFillColor(INK); c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(W / 2, H - 360, f"has bravely conquered {total} word puzzles")
    c.drawCentredString(W / 2, H - 384, "and proved themselves a true")
    graffiti_text(c, W / 2, H - 440, "WORD WIZARD!", 38, X.pal[1], off=2)
    star(c, 90, H - 430, 18, YELLOW, 12); star(c, W - 90, H - 430, 18, PINK, -12)
    star(c, 130, H - 490, 11, X.pal[2], 8); star(c, W - 130, H - 490, 11, X.pal[3], -8)
    mascot(c, W / 2, 160, 2.0, random.choice(X.T["says"]))
    c.setFillColor(INK); c.setFont("Helvetica-Bold", 12)
    c.drawString(80, 90, "DATE:"); c.setStrokeColor(INK); c.setLineWidth(1.5); c.line(140, 87, 280, 87)
    c.drawString(W - 290, 90, "SIGNED:"); c.line(W - 215, 87, W - 80, 87)
    footer(c, "CERTIFICATE"); c.showPage()

def back_cover(c):
    page_bg(c); c.setFillColor(INK); c.rect(0, H - 300, W, 220, stroke=0, fill=1)
    graffiti_text(c, W / 2, H - 180, "WELL DONE!", 62, YELLOW, off=4); graffiti_text(c, W / 2, H - 235, "YOU'RE A WORD WIZARD!", 28, X.pal[0], off=3)
    for x, col in zip((80, 200, 330, 460), X.pal): drip(c, x, H - 300, random.randint(10, 26), col)
    rrect(c, 70, H - 500, W - 140, 140, 14, WHITE, lw=3); c.setFillColor(INK); c.setFont("Helvetica-Bold", 15)
    for i, ln in enumerate(["You cracked the codes and escaped the mazes!", "Now challenge your friends and family", "to see if they can puzzle like you.", "Keep puzzling. Keep learning. Keep having fun!"]): c.drawCentredString(W / 2, H - 395 - i * 22, ln)
    mascot(c, W / 2, 190, 2.2, random.choice(X.T["says"])); c.showPage()

def contents(c, secs, starts):
    page_bg(c); page_header(c, "CONTENTS", X.pal[2]); y = H - 110
    for i, s in enumerate(secs):
        rrect(c, 70, y - 22, W - 140, 34, 8, WHITE, lw=2); c.setFillColor(s["col"]); c.setStrokeColor(INK); c.circle(95, y - 5, 12, stroke=1, fill=1)
        c.setFillColor(WHITE); c.setFont("Helvetica-Bold", 11); c.drawCentredString(95, y - 9, str(i + 1)); c.setFillColor(INK); c.setFont("Helvetica-Bold", 13); c.drawString(120, y - 9, s["title"])
        c.setFont("Helvetica", 10); c.drawRightString(W - 85, y - 9, f"{len(s['puzzles'])} puzzles  -  page {starts[i]}"); y -= 44
    c.setFont("Helvetica-Bold", 12); c.drawString(75, y - 10, f"ANSWER KEY ... page {starts['ans']}"); c.drawString(75, y - 30, f"CERTIFICATE ... page {starts['cert']}")
    footer(c, "CONTENTS"); c.showPage()

# =====================================================================
# 8. BUILD
# =====================================================================
def build(theme_key, scale=1.0, out=None, selected_keys=None):
    T = THEMES[theme_key]; X.T = T; X.pal = [C(*p) for p in T["palette"]]
    global THEME_BG; THEME_BG = T["bg"]
    rng = random.Random(BOOK["seed"]); random.seed(BOOK["seed"])

    # Filter to only the requested game types (default = all)
    active = SECTIONS if not selected_keys else [s for s in SECTIONS if s["key"] in selected_keys]
    if not active:
        active = SECTIONS  # safety fallback

    secs = []; num = 1
    for i, base in enumerate(active):
        sec = dict(base); want = max(1, round(base["pages"] * scale)) * base["per_page"]
        pz = GENERATORS[sec["key"]](T, want, rng)
        usable = (len(pz) // sec["per_page"]) * sec["per_page"]
        if usable < want: print(f"  note: '{sec['key']}' only produced {len(pz)} puzzles (wanted {want}) -> using {usable}")
        pz = pz[:usable]
        for p in pz: p["num"] = num; num += 1
        sec["pages"] = usable // sec["per_page"]; sec["puzzles"] = pz; sec["col"] = X.pal[i % 5]; secs.append(sec)
    secs = [s for s in secs if s["puzzles"]]
    X.secs = secs; X.total_puzzles = sum(len(s["puzzles"]) for s in secs)
    page = 4; starts = {}
    for i, s in enumerate(secs):
        starts[i] = page + 1; page += 1 + s["pages"]
    ans_pages = ans_layout_pages(secs)
    starts["ans"] = page; starts["cert"] = page + ans_pages
    out = out or f"Word_Games_{T['name']}.pdf"
    c = canvas.Canvas(out, pagesize=A4); c.setTitle(f"{BOOK['title_1']} {BOOK['title_2']} - {T['edition']}")
    cover(c); how_to_play(c); contents(c, secs, starts)
    for i, s in enumerate(secs):
        divider(c, s, i + 1, s["col"], starts[i]); puzzle_pages(c, s, s["puzzles"], s["col"])
    answer_pages(c, secs); certificate(c, X.total_puzzles); back_cover(c); c.save()
    print(f"{T['name']}: {X.total_puzzles} puzzles, {c.getPageNumber() - 1} pages  ->  {out}")
    return out

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--theme", default="pirates", choices=list(THEMES)); ap.add_argument("--scale", type=float, default=1.0)
    ap.add_argument("--out"); ap.add_argument("--all", action="store_true"); a = ap.parse_args()
    for k in (THEMES if a.all else [a.theme]): build(k, a.scale, a.out if not a.all else None)
