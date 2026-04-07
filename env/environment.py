from env.tasks import load_tasks
from env.grader import grade
from env.models import Observation, Reward, Action

class OpsFlowEnv:
    def __init__(self):
        self.tasks = load_tasks()
        self.index = 0
        self.total_reward = 0

    def reset(self):
        self.index = 0
        self.total_reward = 0
        obs = self.tasks[self.index]["observation"]
        return Observation(**obs)

    def step(self, action: Action):
        task = self.tasks[self.index]

        # Use dict() for action to pass standard dict to grade
        reward_dict = grade(task, action.model_dump() if hasattr(action, "model_dump") else action.dict())
        reward = Reward(**reward_dict)

        self.total_reward += reward.score

        done = self.index >= len(self.tasks) - 1
        self.index += 1

        next_obs = None
        if not done:
            next_obs = Observation(**self.tasks[self.index]["observation"])

        return next_obs, reward, done, {}

    def state(self):
        return {
            "current_task_index": self.index,
            "remaining_tasks": len(self.tasks) - self.index,
            "total_reward": self.total_reward
        }
