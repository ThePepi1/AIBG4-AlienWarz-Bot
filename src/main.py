import sys
from bot import Bot
from utils.logger import log
import time

bot = Bot()

while True:
    new_state = sys.stdin.readline().strip()
    start = time.perf_counter()
    bot.make_move(new_state)
    end = time.perf_counter()
    log(f"total time {end - start}")
    log(f"{bot.state.me().energy}")
    log(f"End make move")
    log("="*20)
