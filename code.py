import board
import neopixel
import time
import random
import displayio
import terminalio
from adafruit_display_text import label
import keypad

# --- LED config ---
NUM_PIXELS = 30
PIXEL_PIN = board.D3
BRIGHTNESS = 0.3
DELAY = 0.05
pixels = neopixel.NeoPixel(PIXEL_PIN, NUM_PIXELS, brightness=BRIGHTNESS, auto_write=False)

# --- Display setup ---
main_group = displayio.Group()
text_area = label.Label(terminalio.FONT, text="Booting...", x=10, y=60)
main_group.append(text_area)
board.DISPLAY.root_group = main_group

# --- Button setup ---
keys = keypad.ShiftRegisterKeys(
    clock=board.BUTTON_CLOCK,
    latch=board.BUTTON_LATCH,
    data=board.BUTTON_OUT,
    key_count=4,
    value_when_pressed=False
)
BUTTON_NAMES = ["A", "B", "SELECT", "START"]
interrupted_button = None  # Global interrupt holder

# --- State flags ---
effect_index = 0
running = True
led_enabled = True

# --- Helper: interrupt check ---
def check_interrupt():
    global interrupted_button, running
    event = keys.events.get()
    if event and event.pressed:
        interrupted_button = BUTTON_NAMES[event.key_number]
        print(f"Interrupt detected: {interrupted_button}")
        if interrupted_button == "B":
            running = not running
            print(f"Running: {running}")
        return True
    if not running:
        print("Effect halted due to running = False")
        return True
    return False

# --- LED Effects ---
def wheel(pos):
    if pos < 85:
        return (255 - pos * 3, pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return (0, 255 - pos * 3, pos * 3)
    else:
        pos -= 170
        return (pos * 3, 0, 255 - pos * 3)

def color_wipe(color, wait):
    print("Effect: Color Wipe")
    for i in range(NUM_PIXELS):
        pixels[i] = color
        pixels.show()
        time.sleep(wait)
        if check_interrupt(): return

def rainbow_cycle(wait):
    print("Effect: Rainbow Cycle")
    for j in range(255):
        for i in range(NUM_PIXELS):
            idx = (i * 256 // NUM_PIXELS) + j
            pixels[i] = wheel(idx & 255)
        pixels.show()
        time.sleep(wait)
        if check_interrupt(): return

def theater_chase(color, wait):
    print("Effect: Theater Chase")
    for q in range(3):
        for i in range(0, NUM_PIXELS, 3):
            pixels[i + q] = color
        pixels.show()
        time.sleep(wait)
        for i in range(0, NUM_PIXELS, 3):
            pixels[i + q] = (0, 0, 0)
        if check_interrupt(): return

def twinkle(wait):
    print("Effect: Twinkle")
    for _ in range(10):
        pixels.fill((0, 0, 0))
        for _ in range(NUM_PIXELS // 4):
            i = random.randint(0, NUM_PIXELS - 1)
            pixels[i] = (random.randint(100, 255),) * 3
        pixels.show()
        time.sleep(wait)
        if check_interrupt(): return

def pulse(color, steps=50):
    print("Effect: Pulse")
    for i in range(steps):
        scale = (1 - abs((i / steps) - 0.5) * 2)
        scaled = tuple(int(c * scale) for c in color)
        pixels.fill(scaled)
        pixels.show()
        time.sleep(DELAY)
        if check_interrupt(): return

def color_chase(color, wait):
    print("Effect: Color Chase")
    for i in range(NUM_PIXELS):
        pixels.fill((0, 0, 0))
        pixels[i] = color
        pixels.show()
        time.sleep(wait)
        if check_interrupt(): return

def fire_flicker():
    print("Effect: Fire Flicker")
    for _ in range(30):
        for i in range(NUM_PIXELS):
            r = random.randint(180, 255)
            g = random.randint(30, 80)
            pixels[i] = (r, g, 0)
        pixels.show()
        time.sleep(0.05)
        if check_interrupt(): return

def confetti():
    print("Effect: Confetti")
    for _ in range(20):
        pixels.fill((0, 0, 0))
        for _ in range(NUM_PIXELS // 5):
            i = random.randint(0, NUM_PIXELS - 1)
            pixels[i] = wheel(random.randint(0, 255))
        pixels.show()
        time.sleep(DELAY)
        if check_interrupt(): return

def lightning():
    print("Effect: Lightning")
    for _ in range(3):
        pixels.fill((0, 0, 0))
        for _ in range(random.randint(1, 3)):
            i = random.randint(0, NUM_PIXELS - 1)
            pixels[i] = (255, 255, 255)
            pixels.show()
            time.sleep(0.02)
            pixels[i] = (0, 0, 0)
        pixels.show()
        time.sleep(random.uniform(0.2, 1.0))
        if check_interrupt(): return

def bounce(color):
    print("Effect: Bounce")
    for i in list(range(NUM_PIXELS)) + list(range(NUM_PIXELS - 1, -1, -1)):
        pixels.fill((0, 0, 0))
        pixels[i] = color
        pixels.show()
        time.sleep(DELAY)
        if check_interrupt(): return

def meteor_rain():
    print("Effect: Meteor Rain")
    for head in range(NUM_PIXELS + 5):
        pixels.fill((0, 0, 0))
        for i in range(NUM_PIXELS):
            fade = int(255 / (i + 1))
            if i == NUM_PIXELS - head:
                pixels[i] = (fade, fade, 255)
            else:
                pixels[i] = tuple(int(c * 0.6) for c in pixels[i])
        pixels.show()
        time.sleep(0.05)
        if check_interrupt(): return

# --- Effects list ---
effects = [
    ("Color Wipe", lambda: color_wipe((255, 0, 0), DELAY)),
    ("Rainbow Cycle", lambda: rainbow_cycle(DELAY)),
    ("Theater Chase", lambda: theater_chase((0, 255, 0), DELAY)),
    ("Twinkle", lambda: twinkle(DELAY)),
    ("Pulse", lambda: pulse((0, 0, 255))),
    ("Color Chase", lambda: color_chase((255, 255, 0), DELAY)),
    ("Fire Flicker", fire_flicker),
    ("Confetti", confetti),
    ("Lightning", lightning),
    ("Bounce", lambda: bounce((255, 0, 255))),
    ("Meteor Rain", meteor_rain),
]

# --- Main loop ---
while True:
    interrupted_button = None
    name, effect_fn = effects[effect_index]

    if running and led_enabled:
        text_area.text = name
        print(f"Launching effect: {name}")
        effect_fn()
    elif not led_enabled:
        pixels.fill((0, 0, 0))
        pixels.show()
        text_area.text = "LEDs Off"
        time.sleep(0.1)
    elif not running:
        pixels.fill((0, 0, 0))
        pixels.show()
        text_area.text = "Paused"
        if interrupted_button == "B":
            text_area.text = effects[effect_index][0]  # Show current effect
            time.sleep(0.5)  # Optional: brief pause to show update


    # --- Handle the button interrupt ---
    if interrupted_button:
        print(f"Processing button: {interrupted_button}")
        if interrupted_button == "A":
            effect_index = (effect_index + 1) % len(effects)
            next_name = effects[effect_index][0]
            text_area.text = f"Coming up: {next_name}"
            time.sleep(0.5)
        elif interrupted_button == "SELECT":
            led_enabled = False
            print("LEDs turned OFF")
        elif interrupted_button == "START":
            led_enabled = True
            print("LEDs turned ON")
