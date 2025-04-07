from temporalio import workflow
from parent_child_policy.activities.notification_activities import send_notification
import asyncio
from typing import List
from datetime import timedelta



@workflow.defn
class ChildNotificationReceiverWorkflow:
	def __init__(self):
		self.updates: List[str] = []
		self._completed = False


	@workflow.signal
	def send_update(self, message: str) -> None:
		self.updates.append(message)
		print(f"child received signal, new update to process: {message}")


	@workflow.signal
	def complete_my_wk(self)->str:
		self._completed = True
		return "completed child workflow, received complete signal...."

	@workflow.run
	async def run(self) -> str:
		print("child workflow run method...")

		try:
			while True:
				print(f"size of updates to process :- {len(self.updates)}")
				print(f"is completion signal sent ? :- {self._completed}")
				if not self._completed:
					await workflow.wait_condition(lambda: len(self.updates) > 0)

				while self.updates:
					message = self.updates.pop(0)
					print(f"new message received...:{message}")
					await workflow.start_activity(
						send_notification,
						message,
						start_to_close_timeout=timedelta(seconds=10),
					)

				if self._completed:
					print("exiting....")
					break

		except asyncio.CancelledError:
			while self.updates:
				message = self.updates.pop(0)
				print(f"new message received during cleanup...:{message}")
				await workflow.execute_activity(
						send_notification,
						message,
						start_to_close_timeout=10,
					)
				print(f"finishing child update....{message}")
			print("child workflow cleanly exit, no updates left to process")
			raise
		return "child workflow completed"


