# worker/worker.py

import asyncio
from temporalio.worker import Worker
from temporalio.client import Client
from parent_child_policy.workflows.parent_workflow import  ParentNotificationSenderWorkflow
from parent_child_policy.workflows.child_workflow import ChildNotificationReceiverWorkflow
from parent_child_policy.activities.notification_activities import send_notification



async def main():
    client = await Client.connect("localhost:7233")
    worker = Worker(
        client,
        task_queue="my-tq",
        workflows=[ChildNotificationReceiverWorkflow, ParentNotificationSenderWorkflow],
        activities=[send_notification],
    )
    print("starting worker.....")
    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())
