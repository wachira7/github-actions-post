import hashlib
import hmac
import json
from datetime import datetime, timezone
import urllib.request

SIGNING_SECRET = "hello-there-from-b12"
ENDPOINT = "https://b12.io/apply/submission"

payload = {
    "action_run_link": "https://github.com/wachira7/github-actions-post/actions/runs/24109231295",
    "email": "waruterewachira7@gmail.com",
    "name": "Emmanuel Warutere Wachira",
    "repository_link": "https://github.com/wachira7/github-actions-post",
    "resume_link": "https://linkedin.com/in/emmanuelwaruts77",
    "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.") + 
                 f"{datetime.now(timezone.utc).microsecond // 1000:03d}Z"
}

# Canonicalize: keys sorted, no extra whitespace, UTF-8
body = json.dumps(payload, separators=(',', ':'), sort_keys=True)
body_bytes = body.encode('utf-8')

# HMAC-SHA256 signature
signature = hmac.new(
    SIGNING_SECRET.encode('utf-8'),
    body_bytes,
    hashlib.sha256
).hexdigest()

headers = {
    "Content-Type": "application/json",
    "X-Signature-256": f"sha256={signature}"
}

req = urllib.request.Request(
    ENDPOINT,
    data=body_bytes,
    headers=headers,
    method="POST"
)

with urllib.request.urlopen(req) as response:
    result = response.read().decode('utf-8')
    print("Submission response:", result)
    receipt = json.loads(result).get("receipt")
    print(f"YOUR RECEIPT: {receipt}")
    