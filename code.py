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
text_area = label.Label(terminalio.FONT, text="Booting...", x=20, y=60)
main_group.append(text_area)
board.DISPLAY.root_group = main_group

# --- Shift register buttons (4 buttons only) ---
keys = keypad.ShiftRegisterKeys(
    clock=board.BUTTON_CLOCK,
    latch=board.BUTTON_LATCH,
    data=board.BUTTON_OUT,
    key_count=4,
    value_when_pressed=False
)

# Button index mapping
BUTTON_NAMES = ["A", "B", "SELECT", "START"]

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
    for i in range(NUM_PIXELS):
        pixels[i] = color
        pixels.show()
        time.sleep(wait)

def rainbow_cycle(wait):
    for j in range(255):
        for i in range(NUM_PIXELS):
            idx = (i * 256 // NUM_PIXELS) + j
            pixels[i] = wheel(idx & 255)
        pixels.show()
        time.sleep(wait)

def theater_chase(color, wait):
    for q in range(3):
        for i in range(0, NUM_PIXELS, 3):
            pixels[i + q] = color
        pixels.show()
        time.sleep(wait)
        for i in range(0, NUM_PIXELS, 3):
            pixels[i + q] = (0, 0, 0)

def twinkle(wait):
    pixels.fill((0, 0, 0))
    for _ in range(NUM_PIXELS // 4):
        i = random.randint(0, NUM_PIXELS - 1)
        pixels[i] = (random.randint(100, 255),) * 3
    pixels.show()
    time.sleep(wait)

def pulse(color, steps=50):
    for i in range(steps):
        scale = (1 - abs((i / steps) - 0.5) * 2)
        scaled = tuple(int(c * scale) for c in color)
        pixels.fill(scaled)
        pixels.show()
        time.sleep(DELAY)

def color_chase(color, wait):
    for i in range(NUM_PIXELS):
        pixels.fill((0, 0, 0))
        pixels[i] = color
        pixels.show()
        time.sleep(wait)

def fire_flicker():
    for i in range(NUM_PIXELS):
        r = random.randint(180, 255)
        g = random.randint(30, 80)
        pixels[i] = (r, g, 0)
    pixels.show()
    time.sleep(0.05)

def confetti():
    pixels.fill((0, 0, 0))
    for _ in range(NUM_PIXELS // 5):
        i = random.randint(0, NUM_PIXELS - 1)
        pixels[i] = wheel(random.randint(0, 255))
    pixels.show()
    time.sleep(DELAY)

def lightning():
    pixels.fill((0, 0, 0))
    for _ in range(random.randint(1, 3)):
        i = random.randint(0, NUM_PIXELS - 1)
        pixels[i] = (255, 255, 255)
        pixels.show()
        time.sleep(0.02)
        pixels[i] = (0, 0, 0)
    pixels.show()
    time.sleep(random.uniform(0.2, 1.0))

def bounce(color):
    for i in list(range(NUM_PIXELS)) + list(range(NUM_PIXELS - 1, -1, -1)):
        pixels.fill((0, 0, 0))
        pixels[i] = color
        pixels.show()
        time.sleep(DELAY)

def meteor_rain():
    pixels.fill((0, 0, 0))
    for head in range(NUM_PIXELS + 5):
        for i in range(NUM_PIXELS):
            fade = int(255 / (i + 1))
            if i == NUM_PIXELS - head:
                pixels[i] = (fade, fade, 255)
            else:
                pixels[i] = tuple(int(c * 0.6) for c in pixels[i])
        pixels.show()
        time.sleep(0.05)

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

effect_index = 0
running = True
led_enabled = True

# --- Main loop ---
while True:
    # Display current effect
    text_area.text = effects[effect_index][0]

    # Button events
    event = keys.events.get()
    if event and event.pressed:
        btn = BUTTON_NAMES[event.key_number]
        if btn == "A":
            effect_index = (effect_index + 1) % len(effects)
            print(f"Effect: {effects[effect_index][0]}")
        elif btn == "B":
            running = not running
            print(f"Running: {running}")
        elif btn == "START":
            led_enabled = True
            print("LEDs turned ON")
        elif btn == "SELECT":
            led_enabled = False
            print("LEDs turned OFF")

    # Run the current effect
    if running and led_enabled:
        effects[effect_index][1]()
    elif not led_enabled:
        pixels.fill((0, 0, 0))
        pixels.show()
        time.sleep(0.05)
