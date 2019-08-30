
#!/usr/bin/env python3
import pstats
import sys

p = pstats.Stats(sys.argv[1])
p.strip_dirs()
p.sort_stats("tottime")
p.print_stats(50)
