# starter/start_workflow.py

import asyncio
from temporalio.client import Client
from parent_child_policy.workflows.parent_workflow import ParentNotificationSenderWorkflow


async def main():
    client = await Client.connect("localhost:7233")
    result = await client.execute_workflow(
        ParentNotificationSenderWorkflow.run,
        id="parent_wkf",
        task_queue="my-tq",
    )
    print(f"Started parent workflow: {result}")


if __name__ == "__main__":
    asyncio.run(main())