from temporalio import activity
import asyncio

@activity.defn
async def send_notification(update: str)-> None:
    print(f"sending notification {update}")
    await asyncio.sleep(2)
    print(f"finished sending: {update}")