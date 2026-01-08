from kuest_data.kuest_client import KuestClient
from kuest_stats.account_stats import update_stats_once

import pandas as pd
import time
import traceback

client = KuestClient()

if __name__ == '__main__':
    while True:
        try:
            update_stats_once(client)
        except Exception as e:
            traceback.print_exc()

        print("Now sleeping\n")
        time.sleep(60 * 60 * 3) #3 hours