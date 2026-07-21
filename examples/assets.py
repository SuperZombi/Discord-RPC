import discordrpc

rpc = discordrpc.RPC(app_id=123456789)

rpc.set_activity(
      state="Assets example",
      large_image=rpc.assets.get("cat")
)
rpc.run()
