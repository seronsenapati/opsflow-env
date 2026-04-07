from fastapi import FastAPI
from env.environment import OpsFlowEnv
from env.models import Action

app = FastAPI(title="OpsFlow Environment API")

# Initialize a global environment instance
env = OpsFlowEnv()

@app.get("/")
def health_check():
    return {"status": "ok"}

@app.post("/reset")
def reset():
    obs = env.reset()
    return obs

@app.post("/step")
def step(action: Action):
    obs, reward, done, info = env.step(action)
    return {
        "observation": obs,
        "reward": reward,
        "done": done,
        "info": info
    }

@app.get("/state")
def state():
    return env.state()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=7860)
