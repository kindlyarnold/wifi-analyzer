"""Kivy Android front-end for the shared Deriv TradingEngine."""
import asyncio
import logging
import threading

from kivy.app import App
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput

import deriv_synth_bot as bot


class UILogHandler(logging.Handler):
    def __init__(self, callback):
        super().__init__()
        self.callback = callback
        self.setFormatter(logging.Formatter("%(asctime)s %(message)s", "%H:%M:%S"))

    def emit(self, record):
        msg = self.format(record)
        Clock.schedule_once(lambda dt: self.callback(msg))


class SynthBotApp(App):
    title = "Deriv Trader (demo first)"

    def build(self):
        self.loop = self.task = None
        root = BoxLayout(orientation="vertical", padding=8, spacing=5)

        def field(hint, text="", password=False):
            widget = TextInput(hint_text=hint, text=text, password=password,
                               multiline=False, size_hint_y=None, height=42)
            root.add_widget(widget)
            return widget

        self.pat = field("Deriv Personal Access Token", password=True)
        self.app_id = field("Deriv App ID")
        self.acct = field("Deriv account ID (use DEMO)")
        self.symbols = field("Markets, comma-separated", "R_100,frxEURUSD")
        self.stake = field("Stake (max limited by MAX_STAKE)", "1")
        self.max_loss = field("Session max loss", "10")
        self.target = field("Session profit target", "10")
        self.strategy = field("Strategy: trend or meanrev", "trend")

        warning = Label(text="DEMO FIRST • Real accounts blocked unless ALLOW_REAL=1 is configured outside the app.",
                        size_hint_y=None, height=48, halign="left", valign="middle")
        warning.bind(width=lambda w, v: setattr(w, "text_size", (v, None)))
        root.add_widget(warning)
        self.btn = Button(text="START", size_hint_y=None, height=52)
        self.btn.bind(on_press=self.toggle)
        root.add_widget(self.btn)

        self.log_label = Label(text="", size_hint_y=None, halign="left", valign="top")
        self.log_label.bind(width=lambda w, v: setattr(w, "text_size", (v, None)))
        self.log_label.bind(texture_size=lambda w, size: setattr(w, "height", size[1]))
        self.scroll = ScrollView()
        self.scroll.add_widget(self.log_label)
        root.add_widget(self.scroll)
        bot.log.addHandler(UILogHandler(self.append))
        bot.log.setLevel(logging.INFO)
        return root

    def append(self, msg):
        self.log_label.text = "\n".join((self.log_label.text + "\n" + msg).splitlines()[-200:])
        self.scroll.scroll_y = 0

    def toggle(self, *_):
        if self.task is not None:
            self.loop.call_soon_threadsafe(self.task.cancel)
            self.btn.text = "STOPPING..."
            return
        try:
            stake, max_loss, target = float(self.stake.text), float(self.max_loss.text), float(self.target.text)
            strategy = self.strategy.text.strip().lower()
            symbols = [item.strip() for item in self.symbols.text.split(",") if item.strip()]
            cfg = bot.Config(pat=self.pat.text.strip(), app_id=self.app_id.text.strip(),
                             account_id=self.acct.text.strip(), stake=stake,
                             max_daily_loss=max_loss, take_profit=target, strategy=strategy)
            cfg.validate()
            if not symbols:
                raise ValueError("Enter at least one market symbol.")
            for symbol in symbols:
                if not symbol.startswith("frx") and not (symbol.startswith("R_") or symbol.startswith("1HZ") or symbol.startswith("JD") or symbol.startswith("stpRNG")):
                    raise ValueError(f"Unsupported symbol format: {symbol}")
        except ValueError as exc:
            self.append(f"Configuration error: {exc}")
            return
        self.btn.text = "STARTING..."
        threading.Thread(target=self._run, args=(cfg, symbols), daemon=True).start()

    def _run(self, cfg, symbols):
        loop = asyncio.new_event_loop()
        self.loop = loop
        asyncio.set_event_loop(loop)
        engine = bot.TradingEngine(cfg, symbols=symbols)
        self.task = loop.create_task(engine.run())
        try:
            loop.run_until_complete(self.task)
        except asyncio.CancelledError:
            bot.log.info("Stop requested.")
        except Exception as exc:
            bot.log.exception("Engine stopped: %s", exc)
        finally:
            pending = asyncio.all_tasks(loop)
            for task in pending:
                task.cancel()
            if pending:
                loop.run_until_complete(asyncio.gather(*pending, return_exceptions=True))
            loop.close()
            self.task = self.loop = None
            Clock.schedule_once(lambda dt: setattr(self.btn, "text", "START"))


if __name__ == "__main__":
    SynthBotApp().run()
