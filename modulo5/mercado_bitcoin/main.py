import datetime
import time

from schedule import repeat,every,run_pending
from mercado_bitcoin.ingestors import DaySummaryIngestor, TradesIngestor
from mercado_bitcoin.writers import DataWriter

if __name__ == '__main__':

    dsi = DaySummaryIngestor(
        coins=['BTC','ETH','LTC'], 
        default_start_date=datetime.date(2021,8,20), 
        writer=DataWriter
    )

    ti = TradesIngestor(

    )

    @repeat(every(1).seconds)
    def job():
        dsi.ingest()
        ti.ingest()

    while True:
        run_pending()
        time.sleep(1)