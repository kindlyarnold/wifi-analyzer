DERIV TRADER — ANDROID + TELEGRAM, SHARED ENGINE
================================================

IMPORTANT SAFETY NOTES
- Demo account first. Real accounts are blocked by default.
- Never commit your Deriv PAT or Telegram token to GitHub or send them in Telegram.
- A trading strategy can lose money; this project does not promise profits.
- Start with a small demo stake and verify the correct account/market in Deriv.
- The engine stops on session loss/profit limits, a losing streak, or a tick timeout.
- MAX_STAKE defaults to 5. The engine checks Deriv authorization metadata and refuses to trade if account type
  cannot be verified. Real-account access requires ALLOW_REAL=1; do not enable it casually.

SHARED ENGINE
- deriv_synth_bot.py: shared strategy, Deriv WebSocket client, risk manager and engine.
- main.py: Kivy Android app entry point.
- telegram_trader.py: Telegram command interface using the same TradingEngine.

TELEGRAM SETUP (PC, VPS, or Termux environment that supports the dependencies)
1. Install Python 3.10+.
2. pip install -r requirements-telegram.txt
3. Create a bot with @BotFather and obtain your numeric Telegram user ID.
4. Set these environment variables (use a DEMO account):
   TELEGRAM_TOKEN=... TELEGRAM_OWNER_ID=...
   DERIV_PAT=... DERIV_APP_ID=... DERIV_ACCOUNT_ID=...
   Optional: MAX_STAKE=5
5. Run: python telegram_trader.py
6. In Telegram, use /start then /status and /run. Only TELEGRAM_OWNER_ID is allowed.

On Linux/macOS, for example:
  export TELEGRAM_TOKEN='...'
  export TELEGRAM_OWNER_ID='12345678'
  export DERIV_PAT='...'
  export DERIV_APP_ID='...'
  export DERIV_ACCOUNT_ID='...'
  python telegram_trader.py

MARKETS
- Synthetic indices such as R_100 and R_50: 5-tick Rise/Fall contracts.
- Forex symbols such as frxEURUSD and frxGBPUSD: 1-minute bar closes feed the
  strategy; contracts use a 5-minute duration. These are Deriv Rise/Fall options,
  not spot forex. Forex markets are generally closed on weekends. Confirm that the
  chosen symbol and contract duration are offered on your Deriv account.
- Add markets in Telegram with /add SYMBOL, or enter comma-separated symbols in
  the Android app. Only use symbols supported by your account.

ANDROID APK BUILD
1. Create a private GitHub repository and upload all project files, including .github.
2. Open Actions -> Build APK -> Run workflow (or push to main).
3. Download the synthbot-apk artifact from the successful workflow.
4. Install the APK on your Android device and enter credentials directly in the app.
5. Keep the app open while testing. Android may pause background work; do not assume
   the bot will run reliably when the app is backgrounded or the screen is off.

OFFLINE TEST
  python deriv_synth_bot.py backtest
This is a random-walk simulation only, not evidence of real-market profitability.
