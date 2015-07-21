from Visualizer import *
import Bot
from DataIO import *

bot = read_data()

# show_path(bot)
# show_vectors(bot)
# bot.print_hist()

print bot.zone_predict()

# show_histo(bot)