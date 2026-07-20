# Discord RPC

A Python wrapper for the Discord RPC API that allows you to create your own custom Rich Presence.

---

## Installation

```bash
pip install discord-rpc
```

> Discord desktop app must be running on the same machine.

---

## Getting Application ID

1. Go to https://discord.com/developers/applications
2. Click "New Application" if you don't have application
3. Insert the name of your application
4. Copy `APPLICATION ID`

---

## Quick Start

Step-by-step making simple rich presence using Discord-RPC.

1. Make sure Discord-RPC is installed.
2. Import Discord-RPC
   ```py
   import discordrpc
   ```

3. Make `rpc` variable from `discordrpc.RPC` with your unique [Application ID](#getting-application-id).
   ```py
   # Change `app_id` to your app id
   rpc = discordrpc.RPC(app_id=1234)
   ```

4. Customizing activity using `rpc.set_activity()`.
   ```py
   rpc.set_activity(
      name="Simple RPC",
      state="A super simple rpc",
      details="simple RPC"
   )
   ```

5. Creating loop for `rpc` so that it can keep running. (Only required if you only run Discord RPC on this file or current instance.)
   ```py
   rpc.run()
   ```

6. Done! Run your file.

---

## API Reference

### `RPC`

```python
class RPC:
    def __init__(...): -> None
```

#### `RPC.__init__`

Creates an IPC client and attempts to connect to the local Discord instance.

Parameters:
- **app_id** *(int)* — Your Discord Application (Client) ID.
- **debug** *(bool, default: `False`)* — If `True`, enables verbose logging (DEBUG).
- **output** *(bool, default: `True`)* — If `False`, silences logger output.
- **exit_if_discord_close** *(bool, default: `True`)* — If `True`, raises when Discord is not found or closed.
- **exit_on_disconnect** *(bool, default: `True`)* — If `True`, exits the process when the socket disconnects.

Variables:
- **is_running** *(bool)* — Whether the RPC successfully set an activity.
- **try_reconnecting** *(bool, default: `True`)* — Whether to attempt reconnecting on disconnect.
- **User** *(cached_property)* — Returns a `User` object populated after handshake. See [User](#user).
- **App** *(cached_property)* — Returns an `Application` object fetched from Discord API. Auto-fetched on first access. See [App](#app).

#### `RPC.set_activity`

```python
def set_activity(...): -> Optional[bool]
```

Sets or updates the current Rich Presence. Returns `True` on success.

Parameters (all optional unless stated):

- **name** *(str)* — Name of the activity (required by Discord API).
- **details** *(str)* — Upper line of the activity.
- **state** *(str)* — Lower line of the activity.
- **act_type** *(Activity, default: `Activity.Playing`)* — See [Activity Types](#activity-types).
- **status_type** *(StatusDisplay, default: `StatusDisplay.Name`)* — Which field (name/state/details) is considered the status name for some clients.
- **large_image** *(str)* — Key of an uploaded Rich Presence Asset (application Art Assets) or an external direct URL.
- **large_text** *(str)* — Tooltip text when hovering the large image.
- **large_url** *(str)* — Optional URL for the large image.
- **small_image** *(str)* — Key of a small asset or an external direct URL.
- **small_text** *(str)* — Tooltip for the small image.
- **small_url** *(str)* — Optional URL for the small image.
- **state_url**, **details_url** *(str)* — Optional link targets when clicking the text.
- **ts_start**, **ts_end** *(int)* — Unix timestamps (seconds). See [Utils](#utils) for helpers.
- **party_id** *(str)* — ID to identify a party or session.
- **party_size** *(list[int, int])* — Current and max size, e.g. `[2, 5]`.
- **join_secret**, **spectate_secret**, **match_secret** *(str)* — Secrets for join/spectate/match.
- **buttons** *(list[dict])* — Up to 2 buttons created by [`button()`](#buttons).
- **clear** *(bool)* — If `True`, clears the activity. Same as `rpc.clear()`.

Notes and validation:
- `act_type` **must** be a value of `types.Activity`; otherwise `InvalidActivityType` is raised.
- `Activity.Streaming` and `Activity.Custom` are disabled for Rich Presence updates and will raise `ActivityTypeDisabled`.
- If Discord is not connected and `try_reconnecting` is `True`, `_setup()` will be called automatically.
- Images can be an uploaded asset key (from Discord Developer Portal) or an external direct URL. Supports PNG, JPEG, WebP, GIF, and AVIF.

#### `RPC.run()`

```python
def run(update_every: int = 1, ping_every: int = 15): -> None
```

Keeps the RPC alive. Not required if another task is running on the same file.

Parameters:
- **update_every** *(int, default: `1`)* — `time.sleep` every inputed second in the loop.
- **ping_every** *(int, default: `15`)* — Sends a PING heartbeat every N seconds to keep the socket alive.

Exceptions:
- `KeyboardInterrupt` will call `RPC.disconnect()`.

#### `RPC.clear()`

```python
def clear(): -> None
```

Clears the current activity without disconnecting.

#### `RPC.disconnect()`

```python
def disconnect(): -> None
```

Closes the IPC socket and marks the client as disconnected. If `exit_on_disconnect=True`, the process exits after issuing the close command.

---

### User

```python
rpc = discordrpc.RPC(app_id=1234)
rpc.User  # cached_property, populated after handshake
```

A lightweight `User` model populated after a successful handshake.

Attributes:
- **id** *(int)* — Discord user ID.
- **username** *(str)* — User's username (e.g., `senophyx`).
- **name** *(str)* — User's global display name (global_name).
- **avatar** *(str)* — CDN URL to the user's avatar (supports animated GIF detection).
- **bot** *(bool)* — Whether the user is a bot.
- **premium_type** *(int)* — Discord Nitro tier. See [Discord docs](https://discord.com/developers/docs/resources/user#user-object-premium-types).

Example:
```py
import discordrpc

rpc = discordrpc.RPC(app_id=123456789)
print(rpc.User.id)
print(rpc.User.name)
print(f"@{rpc.User.username}")
print(rpc.User.avatar)

rpc.run()
```

---

### App

```python
rpc = discordrpc.RPC(app_id=1234)
rpc.App  # cached_property, auto-fetched from Discord API on first access
```

An `Application` model populated from the Discord API. The HTTP request is lazy-loaded, meaning it won't execute until `rpc.App` is accessed for the first time.

Attributes:
- **id** *(int)* — Application ID.
- **name** *(str)* — Application name.
- **description** *(str)* — Application description.
- **icon** *(str)* — CDN URL to the application icon.
- **verified** *(bool)* — Whether the application is verified.
- **public** *(bool)* — Whether the bot is public.

---

## Buttons

```python
from discordrpc import button

def button(text: str, url: str): -> dict
```

Creates a Discord-compatible button payload. Discord allows up to **2 buttons** per activity.

Parameters:
- **text** *(str)* — Button label (1-32 chars recommended).
- **url** *(str)* — Must start with `http://` or `https://`. Raises `InvalidURL` otherwise.

Example:
```py
import discordrpc
from discordrpc import button

rpc = discordrpc.RPC(app_id=1234567891011)

rpc.set_activity(
    name="Example RPC with Buttons",
    state="Made by Senophyx",
    details="Discord-RPC",
    buttons=[
        button("Repository", "https://github.com/Senophyx/discord-rpc"),
        button("Discord", "https://discord.gg/qpT2AeYZRN"),
    ]
)

rpc.run()
```

---

## Utils

```python
from discordrpc import utils
```

### `utils.timestamp`

```python
timestamp -> int
```

A variable that returns the current time in epoch timestamp.

### `utils.date_to_timestamp`

```python
def date_to_timestamp(date: str): -> int
```

Date to timestamp converter.

Parameters:
- **date** *(str)* — A date and time string in format `%d/%m/%Y-%H:%M:%S` (day/month/year-hour:minute:second).

Example:
```python
date_to_timestamp('14/06/2025-00:00:00')
```

### `utils.use_local_time`

```python
def use_local_time(): -> dict
```

Returns a simplified `ts_start` payload for `RPC.set_activity()` that starts from midnight today.

### `utils.progress_bar`

```python
def progress_bar(current: int, duration: int): -> dict
```

Returns a `ts_start` and `ts_end` payload for `RPC.set_activity()` based on progress.

Parameters:
- **current** *(int)* — Current progress value.
- **duration** *(int)* — Total duration value.

Raises:
- `ProgressbarError` — If `current` exceeds `duration`.

### `utils.get_app_info`

```python
def get_app_info(app_id: int): -> dict
```

Fetch application info standalone without initializing the `RPC` class.

Parameters:
- **app_id** *(int or str)* — Your Discord Application ID.

Returns:
- Payload `dict` containing application details directly from Discord API.

---

## Activity Types

```python
from discordrpc import Activity
```

| Enum | Value | Description |
|------|-------|-------------|
| `Activity.Playing` | 0 | Playing a game |
| `Activity.Streaming` | 1 | Streaming (disabled for RPC) |
| `Activity.Listening` | 2 | Listening to something |
| `Activity.Watching` | 3 | Watching something |
| `Activity.Custom` | 4 | Custom status (disabled for RPC) |
| `Activity.Competing` | 5 | Competing in something |

> `Streaming` and `Custom` are currently disabled by Discord for Rich Presence updates. Using them will raise `ActivityTypeDisabled`.

---

## Status Display Types

```python
from discordrpc import StatusDisplay
```

| Enum | Value | Description |
|------|-------|-------------|
| `StatusDisplay.Name` | 0 | Name field |
| `StatusDisplay.State` | 1 | State field |
| `StatusDisplay.Details` | 2 | Details field |

---

## Exceptions

Module: `exceptions.py` (all extend `RPCException`)

| Exception | Description |
|-----------|-------------|
| `RPCException` | Base exception for all library errors. |
| `Error(message)` | Generic user error. |
| `DiscordNotOpened()` | Discord not found or running. |
| `ActivityError()` | Malformed or invalid activity payload. |
| `InvalidURL()` | URL did not start with `http://` or `https://`. |
| `InvalidID()` | Invalid Application ID. |
| `ButtonError(message)` | Button-related error (e.g., more than 2 buttons). |
| `ProgressbarError(message)` | Invalid progress values (e.g., current > duration). |
| `InvalidActivityType(message)` | `act_type` is not a `types.Activity` member. |
| `ActivityTypeDisabled()` | `Streaming` or `Custom` types are blocked by Discord. |

> Catch `RPCException` if you want to handle all library errors.

---

## Examples

### Basic presence
```python
import discordrpc

rpc = discordrpc.RPC(app_id=12345678910)

rpc.set_activity(
    name="Simple RPC",
    state="A super simple rpc",
    details="simple RPC"
)

rpc.run()
```

### Presence with buttons
```python
import discordrpc
from discordrpc import button

rpc = discordrpc.RPC(app_id=1234567891011)

rpc.set_activity(
    name="Example RPC with Buttons",
    state="Made by Senophyx",
    details="Discord-RPC",
    buttons=[
        button("Repository", "https://github.com/Senophyx/discord-rpc"),
        button("Discord", "https://discord.gg/qpT2AeYZRN"),
    ]
)

rpc.run()
```

### Presence with images
```python
import discordrpc

rpc = discordrpc.RPC(app_id=123456789)

rpc.set_activity(
    name="Discord-RPC Example",
    state="pip install discord-rpc",
    details="Discord-RPC by Senophyx",
    large_image="eternomm_logo",
    large_text="EterNomm",
    small_image="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png",
    small_text="Github"
)

rpc.run()
```

### Presence with timestamps
```python
import discordrpc
from discordrpc.utils import timestamp

rpc = discordrpc.RPC(app_id=123456789)

rpc.set_activity(
    name="Timestamp Example",
    state="With timestamp!",
    details="Timestamp",
    ts_start=timestamp,
    ts_end=1752426021
)

rpc.run()
```

### Presence with activity type
```python
import discordrpc
from discordrpc import Activity
import time

rpc = discordrpc.RPC(app_id=123456789)

current_time = int(time.time())
finish_time = current_time + 200

rpc.set_activity(
    name="Music Example",
    state="With activity type",
    details="Music",
    act_type=Activity.Listening,
    ts_start=current_time,
    ts_end=finish_time
)

rpc.run()
```

### Presence with party
```python
import discordrpc

rpc = discordrpc.RPC(app_id=123456789)

rpc.set_activity(
    name="Valorant Party",
    details="VALORANT",
    state="Join if you want!",
    party_id=12345,
    party_size=[1, 10],
    join_secret="playvalowithme",
    spectate_secret="spectateme",
    match_secret="idkbrofr"
)

rpc.run()
```

### Presence with progress bar
```python
import discordrpc
from discordrpc import Activity
from discordrpc.utils import progress_bar

rpc = discordrpc.RPC(app_id=1234567891011)

rpc.set_activity(
    name="Music Progressbar",
    state="With Progressbar",
    details="Music",
    act_type=Activity.Listening,
    **progress_bar(50, 200)
)

rpc.run()
```

### Clear activity
```python
import discordrpc
import time

rpc = discordrpc.RPC(app_id=123456789)

rpc.set_activity(
    name="Example RPC",
    state="Working hard",
    details="Coding in Python",
    large_image="eternomm_logo",
    large_text="EterNomm"
)

time.sleep(10)

rpc.clear()

time.sleep(5)
rpc.disconnect()
```

### Local time helper
```python
import discordrpc
from discordrpc import use_local_time

rpc = discordrpc.RPC(app_id=123456789)

rpc.set_activity(
    name="Local Time Example",
    state="Wow! It's shows my clock",
    details="Local time example",
    **use_local_time()
)

rpc.run()
```

### Debug mode
```python
import discordrpc

rpc = discordrpc.RPC(app_id=123456789, debug=True)

rpc.set_activity(
    name="Debug RPC",
    state="A super simple rpc",
    details="simple RPC"
)

rpc.run()
```

More examples can be found [here](https://github.com/Senophyx/Discord-RPC/tree/main/examples).

---

## Troubleshooting

- **"Discord is closed" / could not find IPC** — Ensure the desktop app is open. On Linux, confirm `$XDG_RUNTIME_DIR` or `/tmp` contains `discord-ipc-*` sockets.
- **`ActivityTypeDisabled`** — Discord no longer accepts `Streaming` and `Custom` via Rich Presence updates. Use another `Activity` value.
- **Buttons don't show** — You can only have up to **2** buttons. All URLs must begin with `http://` or `https://`.
- **No images appear** — Upload assets to the **Art Assets** section of your application and reference their keys, not file paths.
- **App exits on disconnect** — Set `exit_on_disconnect=False` when creating `RPC` if you prefer to handle disconnects yourself.
- **Silence logs** — Pass `output=False` to `RPC(...)` to disable log output.

---

## FAQ

**Q: Do I need a bot token?**  
A: No. This library communicates locally with the Discord client via IPC; only an Application ID is needed.

**Q: Can I update the presence from a server?**  
A: No. This is a client-side integration; the user's Discord app must run on the same machine.

**Q: Can I use streaming or custom activity?**  
A: Those types are disabled for RPC updates and raise `ActivityTypeDisabled`.

---

## Links
- [GitHub Repository](https://github.com/Senophyx/Discord-RPC)
- [PyPI Project page](https://pypi.org/project/discord-rpc/)
- [TestPyPI Project page](https://test.pypi.org/project/discord-rpc/)
- [Discord Server](https://discord.gg/qpT2AeYZRN)

## Licence & Copyright
```
Discord-RPC project is under MIT License.
Copyright (c) 2021-2025 Senophyx.
```