import os
import json
import time
from openai import OpenAI
from env.environment import OpsFlowEnv
from env.models import Action

# ✅ Required environment variables
API_BASE_URL = os.getenv("API_BASE_URL", "https://router.huggingface.co/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "meta-llama/Meta-Llama-3-8B-Instruct")
HF_TOKEN = os.getenv("HF_TOKEN")

client = OpenAI(
    base_url=API_BASE_URL,
    api_key=HF_TOKEN
)

def call_llm(prompt):
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": "You are a logistics decision agent."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

def format_prompt(obs):
    schema = ""
    if obs.task_type == "address_fix":
        schema = '{"fixed_address": "kolkata sector 5 near tcs gitanjali park"}'
    elif obs.task_type == "prioritization":
        schema = '{"order_sequence": ["B", "C", "A"]}'
    elif obs.task_type == "driver_assignment":
        schema = '{"assigned_orders": 2, "urgent_handled": true}'

    return f"""
    Task: {obs.task_type}
    Data: {obs.data}

    You must return ONLY a JSON response without any markdown, reasoning, or additional text.
    The JSON structure MUST exactly match this format:
    {schema}
    """

def run():
    print("START")

    env = OpsFlowEnv()
    obs = env.reset()

    total_score = 0
    step_count = 0
    done = False

    while not done:
        step_count += 1

        prompt = format_prompt(obs)
        llm_output = call_llm(prompt)

        try:
            # Clean possible markdown formatting
            clean_out = llm_output.strip()
            if clean_out.startswith("```json"):
                clean_out = clean_out[7:].strip()
                if clean_out.endswith("```"):
                    clean_out = clean_out[:-3].strip()
            elif clean_out.startswith("```"):
                clean_out = clean_out[3:].strip()
                if clean_out.endswith("```"):
                    clean_out = clean_out[:-3].strip()
            
            parsed_decision = json.loads(clean_out)
        except Exception:
            parsed_decision = {"raw_output": llm_output}

        # ⚠️ Basic parsing (safe fallback)
        action = Action(decision=parsed_decision)

        obs, reward, done, _ = env.step(action)

        total_score += reward.score

        print(f"STEP {step_count}: reward={reward.score}")

    print(f"END: total_score={total_score}")
    
    # Hugging Face Spaces require a web server listening on port 7860 to pass the health check.
    print("Simulation complete. Starting dummy server on port 7860 to keep Hugging Face Space active...")
    import http.server
    import socketserver
    
    class DummyHandler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(f"OpsFlow Simulation Complete!\nFinal Score: {total_score}".encode('utf-8'))
            
        def log_message(self, format, *args):
            pass # Suppress HTTP logging to keep the logs clean
            
    with socketserver.TCPServer(("", 7860), DummyHandler) as httpd:
        httpd.serve_forever()

if __name__ == "__main__":
    run()
