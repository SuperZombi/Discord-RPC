import discordrpc
from discordrpc import use_local_time


rpc = discordrpc.RPC(app_id=123456789)

rpc.set_activity(
    name="Local Time Example",
    state="Wow! It's shows my clock",
    details="Local time example",
    **use_local_time()
)

# rpc.set_activity(
#     **use_local_time("Europe/Berlin")
# )

# from zoneinfo import available_timezones
# print(available_timezones())

rpc.run()
