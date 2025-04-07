from temporalio import workflow
from .child_workflow import ChildNotificationReceiverWorkflow


@workflow.defn
class ParentNotificationSenderWorkflow:

	@workflow.run
	async def run(self)-> None:
		workflow.logger.info("starting child workflow")

		child_handle = await workflow.start_child_workflow(

			ChildNotificationReceiverWorkflow.run,
			id="child_wkf",
			task_queue=workflow.info().task_queue,
			parent_close_policy=workflow.ParentClosePolicy.REQUEST_CANCEL
			)

		STAGES = [
				"Building",
	            "Testing",
	            "Staging",
	            "Production"
		]

		for stage in STAGES:
			await child_handle.signal(ChildNotificationReceiverWorkflow.send_update, stage)
			workflow.logger.info(f"[Parent] Sent signal: {stage}")
			# await workflow.sleep(10)


		await child_handle.signal(ChildNotificationReceiverWorkflow.complete_my_wk)
		print("complete child now")

		print("[Parent] All signals sent. completing parent_workflow")


