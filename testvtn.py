import asyncio
from datetime import datetime, timezone, timedelta
from openleadr import OpenADRServer, enable_default_logging
from openleadr.utils import generate_id
from functools import partial
import os
import logging

VTN_NAME=os.environ['VTN_NAME']

enable_default_logging(level=logging.DEBUG)
logger = logging.getLogger('openleadr')


print("vtn at top")

def ven_lookup(ven_id):
    logger.info(f"ven_lookup {ven_id}")
    return {
        'ven_id': ven_id,
        'ven_name': ven_id,
        'fingerprint': ven_id,
        'registration_id': generate_id()
    }
    # Look up the information about this VEN.
    ## PSEUDO ven_info = database.lookup('vens').where(ven_id=ven_id) # Pseudo code
    ## PSEUDO if ven_info:
    ## PSEUDO    return {'ven_id': ven_info['ven_id'],
    ## PSEUDO            'ven_name': ven_info['ven_name'],
    ## PSEUDO            'fingerprint': ven_info['fingerprint'],
    ## PSEUDO            'registration_id': ven_info['registration_id']}
    ## PSEUDO else:
    ## PSEUDO    return {}

# async def on_create_party_registration(registration_info):
#    """
#    Inspect the registration info and return a ven_id and registration_id.
#    """
#    if registration_info['ven_name'] == 'ven123':
#        ven_id = generate_id()
#        registration_id = generate_id()
#        return ven_id, registration_id
#    else:
#        return False

async def on_create_party_registration(registration_info):
    """
    Inspect the registration info and return a ven_id and registration_id.
    """
    logger.debug(f"on_create_party_registration START {registration_info}")
    ven_id = generate_id()
    registration_id = generate_id()
    logger.debug(f"on_create_party_registration {ven_id} {registration_id}")
    return ven_id, registration_id

async def on_register_report(ven_id, resource_id, measurement, unit, scale,
                             min_sampling_interval, max_sampling_interval):
    """
    Inspect a report offering from the VEN and return a callback and sampling interval for receiving the reports.
    """
    logger.debug(f"on_register_report {ven_id} {resource_id} {measurement}")
    callback = partial(on_update_report, ven_id=ven_id, resource_id=resource_id, measurement=measurement)
    sampling_interval = min_sampling_interval
    return callback, sampling_interval

async def on_update_report(data, ven_id, resource_id, measurement):
    """
    Callback that receives report data from the VEN and handles it.
    """
    for time, value in data:
        logger.debug(f"Ven {ven_id} reported {measurement} = {value} at time {time} for resource {resource_id}")

async def event_response_callback(ven_id, event_id, opt_type):
    """
    Callback that receives the response from a VEN to an Event.
    """
    logger.debug(f"VEN {ven_id} responded to Event {event_id} with: {opt_type}")

logger.debug("vtn before OpenADRServer")

# Create the server object
server = OpenADRServer(vtn_id='myvtn',
                       http_host='0.0.0.0',
                       ven_lookup=ven_lookup)

logger.debug(f"vtn created server {server}")

# Add the handler for client (VEN) registrations
server.add_handler('on_create_party_registration', on_create_party_registration)

logger.debug(f"vtn add_handler on_create_party_registration")

# Add the handler for report registrations from the VEN
server.add_handler('on_register_report', on_register_report)

logger.debug(f"vtn add_handler on_register_report")

# Add a prepared event for a VEN that will be picked up when it polls for new messages.
server.add_event(ven_id='ven_id_123',
                 signal_name='simple',
                 signal_type='level',
                 intervals=[{'dtstart': datetime(2021, 1, 1, 12, 0, 0, tzinfo=timezone.utc),
                             'duration': timedelta(minutes=10),
                             'signal_payload': 1}],
                 callback=event_response_callback)

logger.debug(f"Configured server {server}")

# https://techoverflow.net/2020/10/01/how-to-fix-python-asyncio-runtimeerror-there-is-no-current-event-loop-in-thread/
# def get_or_create_eventloop():
#     try:
#         return asyncio.get_event_loop()
#     except RuntimeError as ex:
#         if "There is no current event loop" in str(ex):
#             print('Inside error handler')
#             loop = asyncio.new_event_loop()
#             asyncio.set_event_loop(loop)
#             return asyncio.get_event_loop()

# Run the server on the asyncio event loop
# asyncio.set_event_loop_policy(None)
# asyncio.set_event_loop(asyncio.new_event_loop())
# loop = asyncio.get_running_loop()
# loop = get_or_create_eventloop()
# loop.create_task(server.run())
# loop.run_forever()


  
# Defining main function
# def main():
    # loop = asyncio.get_running_loop()
    # loop = get_or_create_eventloop()
    # loop.create_task(server.run())
    # loop.run_forever()

loop = asyncio.new_event_loop()
logger.debug("after new loop")
asyncio.set_event_loop(loop)
logger.debug("after set event loop")
asyncio.run(server.run())
logger.debug(f"//{server.http_host}:{server.http_port}{server.http_path_prefix}".center(80))

loop.run_forever()

# Using the special variable 
# __name__
# if __name__=="__main__":
#     main()