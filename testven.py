import asyncio
from datetime import timedelta
import pytz
from openleadr import OpenADRClient, enable_default_logging
import os
import logging

VEN_NAME = os.environ['VEN_NAME']
VTN_URL  = os.environ['VTN_URL']
RESOURCE_NAME = os.environ['RESOURCE_NAME']

VEN_ID   = VEN_NAME + "_id"

tz_local = pytz.timezone('America/Chicago')

if __name__ == "__main__":
    #code here
    pass

enable_default_logging(level=logging.DEBUG)
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('openleadr')

logger.debug(f"VEN START {VEN_NAME} {VTN_URL} {RESOURCE_NAME} {VEN_ID}")

async def collect_report_value():
    # This callback is called when you need to collect a value for your Report
    logger.debug("collect_report_value")
    return 1.23

async def handle_event(event):
    # This callback receives an Event dict.
    # You should include code here that sends control signals to your resources.
    logger.debug(f"handle_event {event}")
    return 'optIn'

# Create the client object
client = OpenADRClient(ven_name=VEN_NAME, vtn_url=VTN_URL, debug=True)
# , ven_id=VEN_ID

# Add the report capability to the client
client.add_report(callback=collect_report_value,
                  resource_id=RESOURCE_NAME,
                  measurement='voltage',
                  sampling_rate=timedelta(seconds=10))

# Add event handling capability to the client
client.add_handler('on_event', handle_event)

logger.debug("After add_handler on_event")

loop = asyncio.new_event_loop()
loop.set_debug(True)
asyncio.set_event_loop(loop)
loop.create_task(client.run())
# Using this line causes failure
# asyncio.run(client.run(), debug=True)
loop.run_forever()
