import os, time, requests
from dotenv import load_dotenv

load_dotenv()
KEY = os.getenv("SCENARIO_API_KEY")
SECRET = os.getenv("SCENARIO_API_SECRET")
BASE = "https://api.cloud.scenario.com/v1"

def scenario_txt2img(prompt):
    if not KEY or not SECRET:
        print("❌ Missing Scenario keys in .env")
        return

    # 1) start job
    start = requests.post(
        f"{BASE}/generate/txt2img",
        auth=(KEY, SECRET),
        headers={"Content-Type": "application/json"},
        json={"prompt": prompt, "modelId": "flux.1-dev", "width": 512, "height": 512, "numSamples": 1},
        timeout=30,
    )
    start.raise_for_status()
    job_id = start.json()["job"]["jobId"]
    print("▶️    Started job:", job_id)

    # 2) poll
    while True:
        r = requests.get(f"{BASE}/jobs/{job_id}", auth=(KEY, SECRET), timeout=20)
        r.raise_for_status()
        data = r.json()
        status = data["job"]["status"]
        print("status:", status)
        if status in ("success", "failure", "canceled"):
            break
        time.sleep(3)

    if status != "success":
        print("❌ Job failed")
        return

    # 3) fetch assets
    asset_ids = data["job"]["metadata"]["assetIds"]
    for asset_id in asset_ids:
        a = requests.get(f"{BASE}/assets/{asset_id}", auth=(KEY, SECRET), timeout=20)
        a.raise_for_status()
        asset = a.json()
        url = asset["asset"]["url"]
        print("✅ Image URL:", url)