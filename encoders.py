import pygame
from gpiozero import RotaryEncoder, Button, Device
from gpiozero.pins.lgpio import LGPIOFactory
from signal import pause
import time

# Use LGPIO for better performance
Device.pin_factory = LGPIOFactory()

# Initialize pygame event system
pygame.init()


class EncoderManager:
    def __init__(self, encoder_config, debounce_ms=200):
        """
        encoder_config: dict of
            {"Encoder1": {"a":17, "b":18, "btn":27}, ...}
        debounce_ms: minimum time between events (ms)
        """
        self.encoders = {}
        self.debounce_ms = debounce_ms
        self.last_event_time = {}  # track last event time per encoder+event

        for name, pins in encoder_config.items():
            rot = RotaryEncoder(a=pins["a"], b=pins["b"], max_steps=0)
            btn = Button(pins["btn"], pull_up=True)
            self.encoders[name] = {"rot": rot, "btn": btn}

    def _debounced(self, name, event_name, callback):
        """Wrap callback with debounce"""
        def wrapper(*args, **kwargs):
            now = int(time.time() * 1000)
            last_time = self.last_event_time.get((name, event_name), 0)
            if now - last_time >= self.debounce_ms:
                self.last_event_time[(name, event_name)] = now
                callback(*args, **kwargs)
        return wrapper

    def set_callbacks(self, name, clockwise=None, counter_clockwise=None, button=None):
        enc = self.encoders[name]
        if clockwise:
            enc["rot"].when_rotated_clockwise = self._debounced(name, "cw", clockwise)
        if counter_clockwise:
            enc["rot"].when_rotated_counter_clockwise = self._debounced(name, "ccw", counter_clockwise)
        if button:
            enc["btn"].when_pressed = self._debounced(name, "btn", button)

    def start(self):
        print("Encoders initialized and running. Press Ctrl+C to exit.")
        pause()
