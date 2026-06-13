# =========================================================
# LITTLE RED RIDING THROUGH THE HOOD — COMPLETE ENGINE
# PART 1/4 — CORE + HOME + NEIGHBORHOOD + STORE
# =========================================================

def new_game_state():
    return {
        "location": "home",
        "lives": 3,
        "inventory": [],
        "flags": {
            "met_lisa": False,
            "warned_about_brad": False,
            "brad_angry": False,
            "confronted_brad": False,

            "found_y_wood": False,
            "found_leather": False,
            "found_rubber_band": False,
            "made_slingshot": False,

            "dog_seen": False,
            "gang_seen": False,
        },
        "_last_text": "",
        "_return_to": "",
    }


# =========================================================
# HELPERS
# =========================================================

def _has(state, item):
    return item in state["inventory"]

def _add(state, item):
    if item not in state["inventory"]:
        state["inventory"].append(item)

def _remove(state, item):
    if item in state["inventory"]:
        state["inventory"].remove(item)

def _set_message(state, text, return_to):
    state["_last_text"] = text
    state["_return_to"] = return_to
    state["location"] = "message"
    return state

def _lose_life(state, text, return_to):
    state["lives"] -= 1

    if state["lives"] <= 0:
        state["_last_text"] = text + "\n\nYou’re out of lives."
        state["location"] = "game_over"
        return state

    hearts = "❤️ " * state["lives"]
    state["_last_text"] = text + f"\n\nYou lost a life. Lives left: {hearts}"
    state["_return_to"] = return_to
    state["location"] = "message"
    return state

def _end_game(state, title, text):
    state["_last_text"] = f"{title}\n\n{text}\n\n(Ending)"
    state["location"] = "ending"
    return state


# =========================================================
# MESSAGE + INVENTORY
# =========================================================

def render_message(state):
    return (state["_last_text"], ["Continue"])

def apply_message_choice(state, _):
    back = state.get("_return_to") or "home"
    state["_return_to"] = ""
    state["location"] = back
    return state

def render_inventory_view(state):
    if state["inventory"]:
        items = "\n".join(f"- {x}" for x in state["inventory"])
        return (f"You're carrying:\n{items}", ["Back"])
    return ("Your inventory is empty.", ["Back"])

def apply_inventory_view_choice(state, _):
    back = state.get("_return_to") or "home"
    state["_return_to"] = ""
    state["location"] = back
    return state


# =========================================================
# HOME
# =========================================================

def render_home(state):
    text = (
        "You wake up to your alarm clock blaring. Another school day.\n\n"
        "Your red hoodie hangs on the chair — the one that gave you your nickname."
    )
    choices = [
        "Put on your hoodie",
        "Check your backpack",
        "Look around your room",
        "Go to the kitchen",
    ]
    return text, choices


def apply_home_choice(state, choice):
    if choice == 0:
        if not _has(state, "red hoodie"):
            _add(state, "red hoodie")
            return _set_message(
                state,
                "You pull on your red hoodie.\n\n[RED HOODIE added]",
                "home",
            )
        return state

    if choice == 1:
        if not _has(state, "rubber band"):
            _add(state, "rubber band")
            state["flags"]["found_rubber_band"] = True
            return _set_message(
                state,
                "Inside your bag you find a rubber band.\n\n[RUBBER BAND added]",
                "home",
            )
        return state

    if choice == 2:
        return _set_message(
            state,
            "Posters. Homework. Mess. Nothing useful.",
            "home",
        )

    if choice == 3:
        state["location"] = "kitchen"
        return state

    return state


# =========================================================
# KITCHEN GATE
# =========================================================

def render_kitchen(state):
    text = (
        "Your mom’s already gone, but she left lunch money on the counter.\n"
        "A note reads: 'Be careful. Love, Mom.'"
    )

    if not _has(state, "lunch money"):
        return text, ["Take the lunch money", "Go back"]

    if _has(state, "red hoodie"):
        return text + "\n\nYou’re ready for school.", ["Leave for school", "Go back"]

    return text + "\n\nYou feel like you're forgetting something.", ["Go back"]


def apply_kitchen_choice(state, choice):
    if not _has(state, "lunch money"):
        if choice == 0:
            _add(state, "lunch money")
            return _set_message(state, "[LUNCH MONEY added]", "kitchen")
        state["location"] = "home"
        return state

    if _has(state, "red hoodie"):
        if choice == 0:
            state["location"] = "neighborhood"
            return state
        state["location"] = "home"
        return state

    state["location"] = "home"
    return state


# =========================================================
# NEIGHBORHOOD HUB
# =========================================================

def render_neighborhood(state):
    text = (
        "You step outside. Sirens echo somewhere in the distance.\n\n"
        "Time to get to school."
    )
    choices = [
        "Take the direct route past the corner",
        "Cut through Mrs. Johnson's yard",
        "Stop by the corner store",
        "Check your inventory",
    ]
    return text, choices


def apply_neighborhood_choice(state, choice):
    if choice == 0:
        state["location"] = "corner_gang"
        return state
    if choice == 1:
        state["location"] = "yard_dog"
        return state
    if choice == 2:
        state["location"] = "corner_store"
        return state
    if choice == 3:
        state["_return_to"] = "neighborhood"
        state["location"] = "inventory_view"
        return state
    return state


# =========================================================
# CORNER GANG SCENE
# =========================================================

def render_corner_gang(state):
    state["flags"]["gang_seen"] = True
    text = (
        "At the corner, guys in red and blue bandanas glare at each other.\n"
        "Tension thick enough to cut."
    )
    choices = [
        "Keep your head down and walk",
        "Cross the street",
        "Pull up your hood and walk bold",
        "Turn back",
    ]
    return text, choices


def apply_corner_gang_choice(state, c):
    if c == 0 or c == 1:
        return _set_message(state, "You slip past safely.", "school_entrance")

    if c == 2:
        return _lose_life(
            state,
            "Someone shouts. A gun pops.\n\nYou dive but get grazed.",
            "school_entrance",
        )

    if c == 3:
        state["location"] = "neighborhood"
        return state

    return state


# =========================================================
# DOG YARD
# =========================================================

def render_yard_dog(state):
    state["flags"]["dog_seen"] = True
    text = "Crusher the pit bull growls. The chain looks long."
    choices = [
        "Run",
        "Move slowly along the fence",
        "Distract the dog",
        "Go back",
    ]
    return text, choices


def apply_yard_dog_choice(state, c):
    if c == 0:
        return _lose_life(
            state,
            "The dog lunges and tears your leg before you escape.",
            "school_entrance",
        )

    if c in (1, 2):
        if not _has(state, "Y-shaped wood"):
            _add(state, "Y-shaped wood")
            state["flags"]["found_y_wood"] = True
        return _set_message(
            state,
            "[Y-SHAPED WOOD added]\n\nYou escape the yard.",
            "school_entrance",
        )

    if c == 3:
        state["location"] = "neighborhood"
        return state

    return state


# =========================================================
# CORNER STORE
# =========================================================

def render_corner_store(state):
    text = "Mr. Garcia nods. 'Morning, Red.'"
    choices = [
        "Browse",
        "Ask about slingshots",
        "Buy candy",
        "Leave",
    ]
    return text, choices


def apply_corner_store_choice(state, c):
    if c == 0:
        return _set_message(
            state,
            "You see a professional slingshot behind the counter.\n$15.",
            "corner_store",
        )

    if c == 1:
        return _set_message(
            state,
            "'You could make one yourself,' Garcia says.",
            "corner_store",
        )

    if c == 2:
        if _has(state, "lunch money") and not _has(state, "candy"):
            _add(state, "candy")
            return _set_message(state, "[CANDY added]", "corner_store")
        return _set_message(state, "You can’t buy anything.", "corner_store")

    if c == 3:
        state["location"] = "neighborhood"
        return state

    return state
# =========================================================
# LITTLE RED RIDING THROUGH THE HOOD — COMPLETE ENGINE
# PART 2/4 — SCHOOL ENTRANCE + HALLWAY + LOCKER + CLASSROOM
# Paste DIRECTLY UNDER PART 1
# =========================================================

# =========================================================
# SCHOOL ENTRANCE (security + Lisa + Brad)
# =========================================================

def render_school_entrance(state):
    text = (
        "You arrive at Jefferson High.\n\n"
        "Students crowd the entrance.\n"
        "A security guard stands by the metal detectors checking backpacks."
    )
    choices = [
        "Head straight to the entrance",
        "Look for Lisa",
        "Scan for Brad and his crew",
        "Check your inventory",
    ]
    return text, choices


def apply_school_entrance_choice(state, c):
    if c == 0:
        # contraband check like original: Y-shaped wood triggers attention
        if _has(state, "Y-shaped wood"):
            state["location"] = "security_contraband"
            return state
        return _set_message(
            state,
            "You pass through the metal detector without incident.",
            "school_hallway",
        )

    if c == 1:
        state["location"] = "entrance_lisa"
        return state

    if c == 2:
        state["location"] = "entrance_brad"
        return state

    if c == 3:
        state["_return_to"] = "school_entrance"
        state["location"] = "inventory_view"
        return state

    return state


# ---------------- SECURITY: CONTRABAND ----------------

def render_security_contraband(state):
    text = (
        "‘Hold up,’ the guard says, pointing to your backpack.\n\n"
        "‘What’s that you got in there?’"
    )
    choices = [
        "Hand over your backpack",
        "Make an excuse and try to get past",
        "Run for it",
        "Create a distraction",
    ]
    return text, choices


def apply_security_contraband_choice(state, c):
    if c == 0:
        _remove(state, "Y-shaped wood")
        state["flags"]["found_y_wood"] = False
        return _set_message(
            state,
            "The guard confiscates the Y-shaped wood.\n\n"
            "‘No weapons in school,’ he says.\n\n"
            "[Y-SHAPED WOOD removed]\n\n"
            "You’re allowed in… but you lost a key slingshot part.",
            "school_hallway",
        )

    if c == 1:
        return _set_message(
            state,
            "‘Science project,’ you lie.\n\n"
            "The guard looks skeptical… then waves you through.\n\n"
            "‘Keep it in your bag,’ he warns.",
            "school_hallway",
        )

    if c == 2:
        # lose life + confiscate
        if _has(state, "Y-shaped wood"):
            _remove(state, "Y-shaped wood")
            state["flags"]["found_y_wood"] = False
        return _lose_life(
            state,
            "You try to run past security.\n\n"
            "Bad move. You’re caught and dragged to the office.\n\n"
            "You get detention and humiliation as your reward.\n\n"
            "[Y-SHAPED WOOD confiscated]",
            "school_hallway",
        )

    if c == 3:
        return _set_message(
            state,
            "You point behind him: ‘Those kids are smoking!’\n\n"
            "He turns. You slip through.",
            "school_hallway",
        )

    return state


# ---------------- ENTRANCE: LISA ----------------

def render_entrance_lisa(state):
    text = (
        "You spot Lisa near the steps with her friends.\n\n"
        "She looks like she belongs in a music video and not this school."
    )
    choices = [
        "Go talk to her",
        "Watch from a distance",
        "Head inside",
        "Check your inventory",
    ]
    return text, choices


def apply_entrance_lisa_choice(state, c):
    if c == 0:
        state["flags"]["met_lisa"] = True
        return _set_message(
            state,
            "You walk over.\n\n"
            "‘Hey,’ you say.\n\n"
            "Lisa smiles. ‘Hey, Red! Did you finish the math homework?’\n\n"
            "The warning bell rings.\n\n"
            "‘See you in class!’",
            "school_entrance",
        )

    if c == 1:
        return _set_message(
            state,
            "You watch her for a second… then the crowd starts moving.\n\n"
            "Maybe later.",
            "school_entrance",
        )

    if c == 2:
        state["location"] = "school_hallway"
        return state

    if c == 3:
        state["_return_to"] = "entrance_lisa"
        state["location"] = "inventory_view"
        return state

    return state


# ---------------- ENTRANCE: BRAD ----------------

def render_entrance_brad(state):
    text = (
        "Brad and his crew are by the bike racks, hassling a freshman.\n\n"
        "Brad’s laugh is loud on purpose."
    )
    choices = [
        "Avoid them and head inside",
        "Watch what they're doing",
        "Confront them",
        "Check your inventory",
    ]
    return text, choices


def apply_entrance_brad_choice(state, c):
    if c == 0:
        return _set_message(
            state,
            "You avoid trouble and head inside.\n\n"
            "Not today.",
            "school_hallway",
        )

    if c == 1:
        state["flags"]["brad_angry"] = True
        return _set_message(
            state,
            "Brad shoves the freshman.\n\n"
            "‘Lunch money. Now.’\n\n"
            "Brad spots you watching.\n\n"
            "‘You’re next, Little Red,’ he calls out.",
            "school_entrance",
        )

    if c == 2:
        state["location"] = "brad_confront_morning"
        return state

    if c == 3:
        state["_return_to"] = "entrance_brad"
        state["location"] = "inventory_view"
        return state

    return state


def render_brad_confront_morning(state):
    text = (
        "You step up.\n\n"
        "‘Leave him alone,’ you say.\n\n"
        "Brad turns, amused.\n\n"
        "‘Little Red got brave today.’\n\n"
        "He leans closer.\n\n"
        "‘You want his spot instead?’"
    )
    choices = [
        "Stand your ground",
        "Back away slowly",
        "Run inside",
        "Throw a punch",
    ]
    return text, choices


def apply_brad_confront_morning_choice(state, c):
    if c == 0:
        state["flags"]["confronted_brad"] = True
        state["flags"]["brad_angry"] = True
        return _set_message(
            state,
            "You hold his gaze.\n\n"
            "A teacher walks by and Brad fakes a smile.\n\n"
            "As she passes, Brad leans in:\n"
            "‘After school, Little Red.’",
            "school_hallway",
        )

    if c == 1:
        state["flags"]["brad_angry"] = True
        return _set_message(
            state,
            "You back away.\n\n"
            "Brad laughs.\n\n"
            "‘See you after school, Little Red.’",
            "school_entrance",
        )

    if c == 2:
        state["flags"]["brad_angry"] = True
        return _set_message(
            state,
            "You run inside.\n\n"
            "Behind you:\n‘Run, Little Red Riding Hood!’",
            "school_hallway",
        )

    if c == 3:
        state["flags"]["confronted_brad"] = True
        state["flags"]["brad_angry"] = True
        return _lose_life(
            state,
            "You swing.\n\n"
            "Brad dodges and shoves you to the ground.\n\n"
            "His friends hold you while he lands a punch.\n\n"
            "A teacher breaks it up, but your face is burning.",
            "school_hallway",
        )

    return state


# =========================================================
# SCHOOL HALLWAY (locker + principal)
# =========================================================

def render_school_hallway(state):
    text = (
        "You’re in the main hallway. Students rush to lockers before first period.\n\n"
        "Your locker is just ahead."
    )
    choices = [
        "Go to your locker",
        "Head to class",
        "Look for Lisa",
        "Check your inventory",
    ]
    return text, choices


def apply_school_hallway_choice(state, c):
    if c == 0:
        state["location"] = "locker_combo"
        return state

    if c == 1:
        state["location"] = "principal_pass"
        return state

    if c == 2:
        return _set_message(
            state,
            "You look around for Lisa but don’t see her.\n\n"
            "Probably already in class.",
            "school_hallway",
        )

    if c == 3:
        state["_return_to"] = "school_hallway"
        state["location"] = "inventory_view"
        return state

    return state


# ---------------- PRINCIPAL WOLFE (restores original hallway-to-class moment) ----------------

def render_principal_pass(state):
    text = (
        "As you turn the corner, you come face to face with Principal Wolfe.\n\n"
        "‘Where’s your hall pass?’ he demands."
    )
    choices = [
        "Tell the truth — you don't have one",
        "Make an excuse about the bathroom",
        "Pretend to search your pockets",
        "Run for it",
    ]
    return text, choices


def apply_principal_pass_choice(state, c):
    if c == 0:
        return _set_message(
            state,
            "‘I don’t have one, sir. I’m just going to class.’\n\n"
            "Wolfe squints… then nods.\n\n"
            "‘Honesty. Get to class. Next time have a pass.’",
            "classroom",
        )

    if c == 1:
        # contraband: firecrackers trigger suspension-like hit
        if _has(state, "firecrackers"):
            _remove(state, "firecrackers")
            return _lose_life(
                state,
                "‘Bathroom emergency,’ you say.\n\n"
                "Wolfe makes you empty your pockets.\n\n"
                "He finds the firecrackers.\n\n"
                "‘Contraband. Automatic discipline.’\n\n"
                "[FIRECRACKERS confiscated]",
                "school_hallway",
            )
        return _set_message(
            state,
            "You claim it’s a bathroom emergency.\n\n"
            "Wolfe sighs, warns you, and sends you to class.",
            "classroom",
        )

    if c == 2:
        return _set_message(
            state,
            "You pat your pockets like it’s a magic trick.\n\n"
            "‘Must’ve left it in class.’\n\n"
            "Wolfe glares.\n\n"
            "‘Get to class. Don’t let me catch you again.’",
            "classroom",
        )

    if c == 3:
        # run -> caught -> paddling -> lose life + confiscate firecrackers if held
        if _has(state, "firecrackers"):
            _remove(state, "firecrackers")
            confiscation = "\n\n[FIRECRACKERS confiscated]"
        else:
            confiscation = ""
        return _lose_life(
            state,
            "You bolt.\n\n"
            "Wolfe barks and radios ahead.\n\n"
            "A teacher blocks your escape.\n\n"
            "You’re marched to the office and punished the old-school way." + confiscation,
            "school_hallway",
        )

    return state


# =========================================================
# LOCKER (combo + firecrackers + leather + craft gate)
# =========================================================

def render_locker_combo(state):
    text = "You reach your locker.\n\nPick a combination:"
    choices = [
        "12-24-7",
        "10-20-5",
        "99-99-99",
        "Back",
    ]
    return text, choices

def apply_locker_combo_choice(state, choice_index):

    # CORRECT COMBO
    if choice_index == 0:
        if not _has(state, "firecrackers"):
            _add(state, "firecrackers")

        if not state["flags"]["found_leather"]:
            _add(state, "leather scraps")
            state["flags"]["found_leather"] = True

        msg = (
            "The locker opens with a satisfying click.\n\n"
            "Inside you find a small package wrapped in brown paper.\n"
            "A note reads: 'For emergencies. -Carlos'\n\n"
            "You unwrap it to find a pack of firecrackers.\n"
            "You also notice leather scraps at the bottom.\n\n"
            "[FIRECRACKERS + LEATHER SCRAPS added]"
        )

        has_parts = (
            _has(state, "Y-shaped wood")
            and _has(state, "rubber band")
            and _has(state, "leather scraps")
            and not state["flags"]["made_slingshot"]
        )

        if has_parts:
            return _set_message(state, msg, "slingshot_craft")

        return _set_message(state, msg, "school_hallway")

    # ❌ WRONG COMBOS → LOSE LIFE
    if choice_index in (1, 2):
        return _lose_life(
            state,
            "Wrong combination.\n\n"
            "You spin the dial wrong. Metal clacks loud…\n"
            "Someone slams into you in the crowd and your head hits the locker.",
            "locker_combo",
        )

    # BACK
    if choice_index == 3:
        state["location"] = "school_hallway"
        return state

    return state


def render_slingshot_craft(state):
    text = (
        "You’ve got everything to make a slingshot:\n"
        "- Y-shaped wood\n"
        "- Rubber band\n"
        "- Leather scraps\n\n"
        "Assemble it now?"
    )
    return text, ["Assemble now", "Wait until later"]


def apply_slingshot_craft_choice(state, c):
    if c == 0:
        for part in ("Y-shaped wood", "rubber band", "leather scraps"):
            _remove(state, part)
        _add(state, "slingshot")
        state["flags"]["made_slingshot"] = True
        return _set_message(state, "You craft a homemade slingshot.\n\n[SLINGSHOT added]", "school_hallway")

    state["location"] = "school_hallway"
    return state


# =========================================================
# CLASSROOM (keeps original Lisa homework depth)
# =========================================================

def render_classroom(state):
    text = (
        "You enter Ms. Chen’s classroom as the bell rings.\n\n"
        "Lisa sits by the window. An empty seat waits near her."
    )
    choices = [
        "Sit next to Lisa",
        "Sit somewhere else",
        "Ask to go to the bathroom",
        "Check your inventory",
    ]
    return text, choices


def apply_classroom_choice(state, c):
    if c == 0:
        state["flags"]["met_lisa"] = True
        state["location"] = "lisa_homework"
        return state

    if c == 1:
        return _set_message(
            state,
            "You sit elsewhere and keep your head down.\n\nClass drifts by.",
            "lesson_message",
        )

    if c == 2:
        # bathroom: if you have parts but haven't crafted, offer craft
        has_parts = (
            _has(state, "Y-shaped wood")
            and _has(state, "rubber band")
            and _has(state, "leather scraps")
            and not state["flags"]["made_slingshot"]
        )
        if has_parts:
            state["location"] = "bathroom_craft_prompt"
            return state

        return _set_message(
            state,
            "You step into the hallway with the pass.\n\nIt’s quiet. Too quiet.",
            "lesson_message",
        )

    if c == 3:
        state["_return_to"] = "classroom"
        state["location"] = "inventory_view"
        return state

    return state


def render_lisa_homework(state):
    text = (
        "Lisa smiles.\n\n"
        "‘Hey, Red. Did you finish the homework?’"
    )
    choices = [
        "Say you finished it",
        "Admit you didn’t finish",
        "Ask to see hers",
        "Change the subject",
    ]
    return text, choices


def apply_lisa_homework_choice(state, c):
    state["flags"]["met_lisa"] = True

    if c == 0:
        return _set_message(
            state,
            "‘Yeah… mostly,’ you say, hoping she doesn’t notice the blanks.\n\n"
            "She points at one you DID do.\n\n"
            "‘Okay, that makes sense.’\n\n"
            "For a second, you feel like you might actually be smart.",
            "lesson_message",
        )

    if c == 1:
        return _set_message(
            state,
            "You admit you got stuck.\n\n"
            "Lisa nods.\n\n"
            "‘Math can be brutal. Want to compare answers?’\n\n"
            "Honesty lands better than you expected.",
            "lesson_message",
        )

    if c == 2:
        return _set_message(
            state,
            "Lisa gives you a look.\n\n"
            "‘You mean copy?’\n\n"
            "She slides it over anyway.\n\n"
            "‘Just this once.’",
            "lesson_message",
        )

    if c == 3:
        state["flags"]["warned_about_brad"] = True
        return _set_message(
            state,
            "You change the subject.\n\n"
            "Lisa listens… then her expression shifts.\n\n"
            "‘Brad’s been running his mouth today. Just… watch yourself after school.’",
            "lesson_message",
        )

    return state


def render_bathroom_craft_prompt(state):
    text = (
        "You’re in the quiet hallway with the pass.\n\n"
        "This is the perfect moment to assemble your slingshot."
    )
    return text, ["Assemble the slingshot now", "Return to class"]


def apply_bathroom_craft_prompt_choice(state, c):
    if c == 0:
        state["location"] = "slingshot_craft"
        return state

    return _set_message(
        state,
        "You return to class before anyone notices you’re gone.",
        "classroom",
    )


# =========================================================
# AFTER SCHOOL (placeholder entry point — Part 3 builds it)
# =========================================================

def render_after_school(state):
    # Part 3 replaces this with full after-school hub + break etc.
    return ("After school content loads in Part 3/4.", ["Continue"])

def apply_after_school_choice(state, c):
    state["location"] = "after_school_hub"
    return state
# =========================
# PART 3/4 — Break + After School Hub + Routes
# =========================


# ---------------- BREAK HUB ----------------

def render_break_hub(state):
    text = (
        "The hallway floods with students as break begins.\n\n"
        "Lockers slam. Someone’s yelling about lunch. Someone else is already running.\n\n"
        "You’ve got a few minutes before next class."
    )
    choices = [
        "Find Lisa",
        "Go outside to the yard",
        "Check your locker",
        "Avoid everyone and walk the halls",
        "Head to next class",
    ]
    return text, choices


def apply_break_hub_choice(state, choice_index):

    if choice_index == 0:
        state["location"] = "break_lisa"
        return state

    if choice_index == 1:
        state["location"] = "break_yard"
        return state

    if choice_index == 2:
        state["location"] = "locker_combo"
        return state

    if choice_index == 3:
        return _set_message(
            state,
            "You keep moving. Sometimes the safest move is to stay in motion.\n\n"
            "No one stops you. No one calls your name.\n\n"
            "Just a few quiet minutes in a loud building.",
            "break_hub",
        )

    if choice_index == 4:
        state["location"] = "period2_message"
        return state

    return state


# ---------------- BREAK: LISA ----------------

def render_break_lisa(state):
    text = (
        "You find Lisa by the vending machines.\n\n"
        "She looks relieved when she sees you.\n\n"
        "'Hey, Red… you heard about Brad, right?'"
    )
    choices = [
        "Ask what Brad is planning",
        "Joke it off",
        "Ask about homework instead",
        "Go back",
    ]
    return text, choices


def apply_break_lisa_choice(state, choice_index):

    if choice_index == 0:
        state["flags"]["warned_about_brad"] = True
        return _set_message(
            state,
            "Lisa lowers her voice.\n\n"
            "'He’s been talking trash about you all morning.'\n"
            "'Said he’d catch you after school.'\n\n"
            "'Please don’t be alone out there.'",
            "break_hub",
        )

    if choice_index == 1:
        return _set_message(
            state,
            "Lisa rolls her eyes.\n\n"
            "'You laugh now… but I’m serious. Just be careful, okay?'",
            "break_hub",
        )

    if choice_index == 2:
        return _set_message(
            state,
            "She sighs.\n\n"
            "'We’ll survive the test. I’m more worried about after school.'",
            "break_hub",
        )

    if choice_index == 3:
        state["location"] = "break_hub"
        return state

    return state


# ---------------- BREAK: YARD ----------------

def render_break_yard(state):
    text = (
        "You step outside into the school yard.\n\n"
        "Clusters of students lean on fences and swap gossip.\n\n"
        "Across the yard, you spot Brad and his crew."
    )
    choices = [
        "Stay near the doors",
        "Walk across the yard",
        "Pretend not to see them",
        "Go back inside",
    ]
    return text, choices


def apply_break_yard_choice(state, choice_index):

    if choice_index == 0:
        return _set_message(
            state,
            "You hang near the doors.\n\n"
            "Brad notices you… but doesn’t move.\n\n"
            "Not yet.",
            "break_hub",
        )

    if choice_index == 1:
        state["flags"]["brad_angry"] = True
        return _set_message(
            state,
            "You walk straight across the yard.\n\n"
            "Brad watches you go by. His crew whispers.\n\n"
            "Something’s definitely coming.",
            "break_hub",
        )

    if choice_index == 2:
        return _set_message(
            state,
            "You keep your head down and move along the wall.\n\n"
            "Brad doesn’t call out — but you feel eyes on you.",
            "break_hub",
        )

    if choice_index == 3:
        state["location"] = "break_hub"
        return state

    return state


# ---------------- PERIOD 2 MESSAGE ----------------

# ---------------- LESSON MESSAGE ----------------

def render_lesson_message(state):
    text = (
        "The lesson drags on.\n\n"
        "Ms. Chen talks about chemical reactions while students fight to stay awake.\n\n"
        "Finally — the bell rings."
    )
    choices = ["Go to break"]
    return text, choices


def apply_lesson_message_choice(state, choice_index):
    state["location"] = "break_hub"
    return state

def render_period2_message(state):
    text = (
        "Second period goes by in a blur.\n\n"
        "You keep hearing Lisa’s warning in your head.\n\n"
        "Finally — the last bell of the day rings."
    )
    return text, ["After school"]


def apply_period2_message_choice(state, choice_index):
    state["location"] = "after_school_hub"
    return state


# ---------------- AFTER SCHOOL HUB ----------------

def render_after_school_hub(state):
    text = (
        "School’s out.\n\n"
        "The front gates are crowded. Cars creep along the curb.\n\n"
        "You feel it — today might end badly if you choose wrong."
    )
    choices = [
        "Look for Lisa",
        "Head straight home",
        "Take the long way (avoid the front)",
        "Check your inventory",
        "Wait by the gates (see who shows up)",
    ]
    return text, choices


def apply_after_school_hub_choice(state, choice_index):

    if choice_index == 0:
        return _set_message(
            state,
            "You spot Lisa near the steps.\n\n"
            "'Red… Brad’s outside. Please don’t do anything stupid.'",
            "after_school_hub",
        )

    if choice_index == 1:
        state["location"] = "route_home_front"
        return state

    if choice_index == 2:
        state["location"] = "route_long_way"
        return state

    if choice_index == 3:
        state["_return_to"] = "after_school_hub"
        state["location"] = "inventory_view"
        return state

    if choice_index == 4:
        state["location"] = "brad_confrontation"
        return state

    return state


# ---------------- ROUTE: FRONT ----------------

def render_route_home_front(state):
    text = (
        "You step toward the front sidewalk.\n\n"
        "Brad and his crew are posted near the corner like they own it.\n\n"
        "Brad grins when he sees you."
    )
    choices = [
        "Keep walking (act normal)",
        "Talk your way out of it",
        "Run for it",
        "Turn back inside",
    ]
    return text, choices


def apply_route_home_front_choice(state, choice_index):

    if choice_index == 0:
        if "slingshot" in state["inventory"]:
            state["location"] = "brad_confrontation"
            return state

        return _lose_life(
            state,
            "You try to act normal.\n\n"
            "Brad shoulder-checks you hard.\n\n"
            "'Where you going, Red?' His crew laughs as you stumble.",
            "after_school_hub",
        )

    if choice_index == 1:
        if state["flags"]["met_lisa"]:
            return _end_game(
                state,
                "ENDING 1/6 — GOOD: Talked it down",
                "You keep your voice steady.\n\n"
                "Brad tries to clown you, but you don’t bite.\n"
                "People are watching.\n\n"
                "He backs off with a fake laugh.\n\n"
                "You walk home shaken — but proud you didn’t swing first.",
            )
        return _lose_life(
            state,
            "You try to talk.\n\n"
            "Brad cuts you off and shoves you.\n\n"
            "'You think you’re smart?'\n\n"
            "You hit the ground.",
            "after_school_hub",
        )

    if choice_index == 2:
        return _lose_life(
            state,
            "You bolt.\n\n"
            "Brad’s crew chases.\n\n"
            "Somebody clips your backpack and you slam the pavement.",
            "after_school_hub",
        )

    if choice_index == 3:
        state["location"] = "after_school_hub"
        return state

    return state


# ---------------- ROUTE: LONG WAY ----------------

def render_route_long_way(state):
    text = (
        "You cut around the side of the school, avoiding the main sidewalk.\n\n"
        "It’s quieter back here — fences, dumpsters, and shadows.\n\n"
        "But quiet can be dangerous too."
    )
    choices = [
        "Keep moving (don’t stop)",
        "Duck behind the gym and wait",
        "Use the alley shortcut",
        "Go back",
    ]
    return text, choices


def apply_route_long_way_choice(state, choice_index):

    if choice_index == 0:
        return _end_game(
            state,
            "ENDING 2/6 — OK: Made it home",
            "You keep your pace steady.\n\n"
            "You don’t see Brad.\n\n"
            "Maybe you got lucky. Maybe tomorrow won’t be.",
        )

    if choice_index == 1:
        if state["flags"]["brad_angry"]:
            state["location"] = "brad_confrontation"
            return state

        return _set_message(
            state,
            "You wait it out.\n\n"
            "Footsteps pass… then fade.\n\n"
            "Looks like you avoided trouble this time.",
            "route_long_way",
        )

    if choice_index == 2:
        if "firecrackers" in state["inventory"]:
            return _end_game(
                state,
                "ENDING 3/6 — SECRET: Smoke and noise escape",
                "You hear voices — Brad’s crew.\n\n"
                "You light a firecracker and toss it.\n\n"
                "BANG!\n\n"
                "They scatter.\n\n"
                "You slip past and vanish into the neighborhood.",
            )
        return _lose_life(
            state,
            "You take the alley.\n\n"
            "A figure steps out.\n\n"
            "You walked straight into it.\n\n"
            "You get hit before you can react.",
            "after_school_hub",
        )

    if choice_index == 3:
        state["location"] = "after_school_hub"
        return state

    return state
# =========================
# PART 4/4 — Final Confrontation + Endings + FULL step() wiring
# =========================


# ---------------- FINAL: BRAD CONFRONTATION ----------------

def render_brad_confrontation(state):
    text = (
        "Brad steps into your path.\n\n"
        "'There you are, Red.'\n\n"
        "His crew fans out behind him.\n\n"
        "People slow down to watch.\n\n"
        "You have one shot to choose right."
    )
    choices = [
        "Stand your ground",
        "Try to walk away",
        "Use your slingshot (if you have it)",
        "Use firecrackers (if you have them)",
        "Call out to the crowd for help",
    ]
    return text, choices


def apply_brad_confrontation_choice(state, choice_index):
    state["flags"]["confronted_brad"] = True

    has_slingshot = "slingshot" in state["inventory"]
    has_firecrackers = "firecrackers" in state["inventory"]

    if choice_index == 0:
        # stand your ground: risky
        if has_slingshot:
            return _end_game(
                state,
                "ENDING 4/6 — HERO: David vs Goliath",
                "Brad swings.\n\n"
                "You backstep, snap your slingshot up, and crack a shot off the ground near his feet.\n\n"
                "The crowd reacts — like it’s a cartoon sound effect in real life.\n\n"
                "Brad freezes.\n\n"
                "Not because it hurt…\n"
                "Because everyone saw him flinch.\n\n"
                "His crew suddenly finds somewhere else to be.\n\n"
                "Brad backs off, red-faced.\n\n"
                "Somebody mutters: 'Man just got Goliath’d.'",
            )
        return _lose_life(
            state,
            "You stand your ground.\n\n"
            "Brad swings first.\n\n"
            "You take a hit and stagger.\n\n"
            "The crowd makes that 'OOOOH' noise that never helps anybody.",
            "after_school_hub",
        )

    if choice_index == 1:
        # walk away: works if warned + met lisa
        if state["flags"]["warned_about_brad"] and state["flags"]["met_lisa"]:
            return _end_game(
                state,
                "ENDING 5/6 — GOOD: You chose peace",
                "You take one step back.\n\n"
                "Then another.\n\n"
                "Brad keeps talking, but you don’t give him the moment.\n\n"
                "He wants a scene.\n\n"
                "You refuse.\n\n"
                "You walk home alive — and that’s a win.",
            )
        return _lose_life(
            state,
            "You try to walk away.\n\n"
            "Brad grabs your hoodie and yanks you back.\n\n"
            "You go down hard.",
            "after_school_hub",
        )

    if choice_index == 2:
        # slingshot option
        if not has_slingshot:
            return _lose_life(
                state,
                "You reach for a slingshot you don’t have.\n\n"
                "Brad laughs — then hits you.\n\n"
                "Classic you.",
                "after_school_hub",
            )

        # Bart Simpson meets David & Goliath vibe
        return _end_game(
            state,
            "ENDING 4/6 — HERO: Bart meets David",
            "You whip out the slingshot.\n\n"
            "Brad squints. 'What is that, a toy?'\n\n"
            "You load a pebble from your pocket (or the ground — you’re resourceful).\n\n"
            "You don’t aim at him.\n\n"
            "You aim at the tree branch above him.\n\n"
            "SNAP.\n\n"
            "Leaves, dust, and a sad little bird feather rain down on Brad like a mythological prank.\n\n"
            "The crowd erupts.\n\n"
            "Brad wipes his face like he’s on camera.\n\n"
            "'Whatever. This ain't over,' he spits.\n\n"
            "But his feet are already moving backward.",
        )

    if choice_index == 3:
        # firecrackers option
        if not has_firecrackers:
            return _lose_life(
                state,
                "You fumble for firecrackers you don’t have.\n\n"
                "Brad doesn’t wait.\n\n"
                "You get rocked before you can blink.",
                "after_school_hub",
            )

        return _end_game(
            state,
            "ENDING 6/6 — CHAOS: Firecracker vanish",
            "You light a firecracker and toss it between them.\n\n"
            "BANG!\n\n"
            "Everyone jumps.\n\n"
            "Somebody yells: 'COPS!'\n\n"
            "Brad’s crew scatters like roaches under kitchen lights.\n\n"
            "You sprint away before anyone can think twice.\n\n"
            "Carlos would be proud.\n"
            "Your mom would not.",
        )

    if choice_index == 4:
        # crowd help: depends on met_lisa
        if state["flags"]["met_lisa"]:
            return _end_game(
                state,
                "ENDING 1/6 — GOOD: Crowd shut it down",
                "You raise your voice:\n\n"
                "'Back up!'\n\n"
                "Heads turn.\n\n"
                "Brad hates witnesses.\n\n"
                "A teacher steps outside.\n\n"
                "Brad backs off, cursing under his breath.\n\n"
                "Lisa finds you after.\n\n"
                "'You okay?' she asks.\n\n"
                "You nod.\n\n"
                "It’s not victory like the movies — it’s better.\n"
                "It’s real.",
            )
        return _lose_life(
            state,
            "You call out for help.\n\n"
            "Nobody moves.\n\n"
            "Brad smiles like he already knew that.",
            "after_school_hub",
        )

    return state


# ---------------- ENDING / GAME OVER ----------------

def render_ending(state):
    return (state.get("_last_text", "(Ending)"), ["Restart"])


def apply_ending_choice(state, choice_index):
    state.clear()
    state.update(new_game_state())
    return state


def render_game_over(state):
    text = state.get("_last_text", "Game Over.")
    return (f"{text}\n\nGAME OVER.", ["Restart"])


def apply_game_over_choice(state, choice_index):
    state.clear()
    state.update(new_game_state())
    return state

# =========================================================
# PRINCIPAL HALL PASS SCENE (fixes "Head to class" glitch)
# =========================================================

def render_principal_pass(state):
    text = (
        "You start toward class — but Principal Wolfe steps into the hall.\n\n"
        "He watches students like a hawk.\n\n"
        "'Late again?' he asks.\n\n"
        "You need to answer fast."
    )
    choices = [
        "Say you're heading to class right now",
        "Make an excuse",
        "Keep walking without answering",
    ]
    return text, choices


def apply_principal_pass_choice(state, c):

    # Honest answer = safe route
    if c == 0:
        return _set_message(
            state,
            "He studies you for a second… then nods.\n\n"
            "'Move it.'\n\n"
            "You slip into class just before the bell.",
            "classroom",
        )

    # Excuse = coin-flip tension
    if c == 1:
        return _lose_life(
            state,
            "He doesn’t buy it.\n\n"
            "'Office. Now.'\n\n"
            "You lose time, dignity, and a chunk of your morning.",
            "classroom",
        )

    # Ignore = definite punishment
    if c == 2:
        return _lose_life(
            state,
            "You try to walk past.\n\n"
            "A hand grabs your shoulder.\n\n"
            "'Wrong move.'\n\n"
            "You’re escorted to class under watch.",
            "classroom",
        )

    return state


# ---------------- FULL ENGINE ----------------
# IMPORTANT: apply choice, then render based on NEW location.

# ✅ EDITED step() — adds principal_pass + fixes corner_gang indent

def step(state, choice_index=None):
    loc = state.get("location", "home")

    # APPLY
    if choice_index is not None:
        if loc == "home":
            apply_home_choice(state, choice_index)

        elif loc == "kitchen":
            apply_kitchen_choice(state, choice_index)

        elif loc == "neighborhood":
            apply_neighborhood_choice(state, choice_index)

        elif loc == "neighborhood_direct":
            apply_neighborhood_direct_choice(state, choice_index)  # type: ignore

        elif loc == "yard_dog":
            apply_yard_dog_choice(state, choice_index)

        elif loc == "corner_store":
            apply_corner_store_choice(state, choice_index)

        elif loc == "school_entrance":
            apply_school_entrance_choice(state, choice_index)

        elif loc == "corner_gang":
            apply_corner_gang_choice(state, choice_index)

        elif loc == "security_contraband":
            apply_security_contraband_choice(state, choice_index)

        elif loc == "entrance_lisa":
            apply_entrance_lisa_choice(state, choice_index)

        elif loc == "entrance_brad":
            apply_entrance_brad_choice(state, choice_index)

        elif loc == "brad_confront_morning":
            apply_brad_confront_morning_choice(state, choice_index)

        elif loc == "school_hallway":
            apply_school_hallway_choice(state, choice_index)

        elif loc == "principal_pass":
            apply_principal_pass_choice(state, choice_index)

        elif loc == "locker_combo":
            apply_locker_combo_choice(state, choice_index)

        elif loc == "slingshot_craft":
            apply_slingshot_craft_choice(state, choice_index)

        elif loc == "classroom":
            apply_classroom_choice(state, choice_index)

        # ✅ ADDED
        elif loc == "lisa_homework":
            apply_lisa_homework_choice(state, choice_index)

        # ✅ ADDED
        elif loc == "bathroom_craft_prompt":
            apply_bathroom_craft_prompt_choice(state, choice_index)

        elif loc == "lesson_message":
            apply_lesson_message_choice(state, choice_index)  # type: ignore

        elif loc == "break_hub":
            apply_break_hub_choice(state, choice_index)

        elif loc == "break_lisa":
            apply_break_lisa_choice(state, choice_index)

        elif loc == "break_yard":
            apply_break_yard_choice(state, choice_index)

        elif loc == "period2_message":
            apply_period2_message_choice(state, choice_index)

        elif loc == "after_school_hub":
            apply_after_school_hub_choice(state, choice_index)

        elif loc == "route_home_front":
            apply_route_home_front_choice(state, choice_index)

        elif loc == "route_long_way":
            apply_route_long_way_choice(state, choice_index)

        elif loc == "brad_confrontation":
            apply_brad_confrontation_choice(state, choice_index)

        elif loc == "inventory_view":
            apply_inventory_view_choice(state, choice_index)

        elif loc == "message":
            apply_message_choice(state, choice_index)

        elif loc == "ending":
            apply_ending_choice(state, choice_index)

        elif loc == "game_over":
            apply_game_over_choice(state, choice_index)

    # RENDER
    loc = state.get("location", "home")

    if loc == "home":
        return render_home(state)

    if loc == "kitchen":
        return render_kitchen(state)

    if loc == "neighborhood":
        return render_neighborhood(state)

    if loc == "neighborhood_direct":
        return render_neighborhood_direct(state)

    if loc == "yard_dog":
        return render_yard_dog(state)

    if loc == "corner_gang":
        return render_corner_gang(state)

    if loc == "corner_store":
        return render_corner_store(state)

    if loc == "school_entrance":
        return render_school_entrance(state)

    if loc == "security_contraband":
        return render_security_contraband(state)

    if loc == "entrance_lisa":
        return render_entrance_lisa(state)

    if loc == "entrance_brad":
        return render_entrance_brad(state)

    if loc == "brad_confront_morning":
        return render_brad_confront_morning(state)

    if loc == "school_hallway":
        return render_school_hallway(state)

    if loc == "principal_pass":
        return render_principal_pass(state)

    if loc == "locker_combo":
        return render_locker_combo(state)

    if loc == "slingshot_craft":
        return render_slingshot_craft(state)

    if loc == "classroom":
        return render_classroom(state)

    # ✅ ADDED
    if loc == "lisa_homework":
        return render_lisa_homework(state)

    # ✅ ADDED
    if loc == "bathroom_craft_prompt":
        return render_bathroom_craft_prompt(state)

    if loc == "lesson_message":
        return render_lesson_message(state)

    if loc == "break_hub":
        return render_break_hub(state)

    if loc == "break_lisa":
        return render_break_lisa(state)

    if loc == "break_yard":
        return render_break_yard(state)

    if loc == "period2_message":
        return render_period2_message(state)

    if loc == "after_school_hub":
        return render_after_school_hub(state)

    if loc == "route_home_front":
        return render_route_home_front(state)

    if loc == "route_long_way":
        return render_route_long_way(state)

    if loc == "brad_confrontation":
        return render_brad_confrontation(state)

    if loc == "inventory_view":
        return render_inventory_view(state)

    if loc == "message":
        return render_message(state)

    if loc == "ending":
        return render_ending(state)

    if loc == "game_over":
        return render_game_over(state)

    return ("Scene not built yet.", ["Restart"])