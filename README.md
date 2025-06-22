# pygamer_led# 🎮 PyGamer LED Controller

This project turns your [Adafruit PyGamer](https://www.adafruit.com/product/4242) into a colorful handheld controller for a WS2811-based addressable LED strip.

With only 4 built-in buttons, you can cycle through 11 stunning LED effects, pause animations, and toggle LEDs on and off. The display shows the current or upcoming effect name, making it intuitive and fun to use.

---

## ✨ Features

* 🎆 11 colorful effects including rainbow, pulse, confetti, fire flicker, meteor rain, and more
* 🕹️ Controlled by PyGamer's built-in A, B, Start, and Select buttons
* 📺 On-screen label shows:

  * Current running effect
  * "Coming up" preview when cycling
* ⚡ Designed to be responsive — effects can be interrupted mid-animation
* 🌈 Optimized for 30 WS2811 LEDs connected via `D3` (JST port)

---

## 🧰 Hardware Required

| Item                                                      | Description                         |
| --------------------------------------------------------- | ----------------------------------- |
| [Adafruit PyGamer](https://www.adafruit.com/product/4242) | Microcontroller + display + buttons |
| WS2811 LED strip (30 LEDs)                                | Addressable RGB LEDs                |
| JST SM 3-pin cable or jumper wires                        | To connect Data, GND, and 5V        |
| Optional: External power supply                           | Needed if using more than \~30 LEDs |

---

## 🔌 Wiring

| LED Wire | Connect To                     |
| -------- | ------------------------------ |
| **Data** | `D3` on PyGamer (JST Port 2)   |
| **GND**  | `GND`                          |
| **5V**   | `VOUT` (for short strips only) |

> Note: The PyGamer can power short LED strips directly. For larger setups, use a separate 5V power supply and common ground.

---

## 📦 Installation Instructions

1. **Install CircuitPython** on your PyGamer
   → [https://circuitpython.org/board/pygamer/](https://circuitpython.org/board/pygamer/)

2. **Download Library Bundle**
   → [https://circuitpython.org/libraries](https://circuitpython.org/libraries)

3. **Copy Libraries to `lib/`** on your CIRCUITPY drive:

4. Copy `code.py` from this repo to the root of the CIRCUITPY drive

---

## 🎮 Controls

| Button   | Function                 |
| -------- | ------------------------ |
| `A`      | Cycle to next effect     |
| `B`      | Pause / resume animation |
| `Start`  | Turn LEDs on             |
| `Select` | Turn LEDs off            |

When you press `A`, the screen will briefly show **"Coming up: \[Effect]"** before loading it.

---

## 🎆 Included Effects

* Color Wipe
* Rainbow Cycle
* Theater Chase
* Twinkle Stars
* Pulse/Breathing
* Color Chase
* Fire Flicker
* Confetti
* Lightning Flash
* Bounce
* Meteor Rain

All effects are **interruptible**, meaning you can switch to a new one at any time.

---

## 🧪 Notes & Future Ideas

* You can modify the number of LEDs by editing `NUM_PIXELS` in `code.py`
* You may also adjust `DELAY` or brightness for tuning performance
* Want to add motion detection or "shake to shuffle"? The PyGamer has an onboard accelerometer!

---

## 🧑‍💻 Author

Built by \[Your Name] using Adafruit hardware and CircuitPython.
Inspired by the joy of colorful LEDs and classic gamepads.

---

## 📜 License

MIT License.
See [LICENSE](LICENSE) file for details.

---

## ❤️ Special Thanks

* [Adafruit](https://www.adafruit.com) for excellent hardware and CircuitPython
* The CircuitPython community for making embedded fun and accessible
