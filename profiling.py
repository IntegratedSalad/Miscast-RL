import cProfile
import pstats
from main import main

cProfile.run('main()', 'profiling')

data = pstats.Stats('profiling')

data.sort_stats('calls')
data.print_stats()
