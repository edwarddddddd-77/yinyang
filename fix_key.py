import re
import os
import time

TARGET_FILE = "backend/main.py"
NEW_KEY = "sk-f00d603b8c704f238c22f4edd0020998"

print(f"🔍 Checking {TARGET_FILE}...")

try:
    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # Regex to find the existing key definition (handles double or single quotes)
    pattern = r'(DEEPSEEK_API_KEY\s*=\s*)(["\'].*?["\'])'
    match = re.search(pattern, content)

    if match:
        current_key_definition = match.group(2).strip('"').strip("'")
        if current_key_definition == NEW_KEY:
            print("✅ Key is ALREADY correct. No changes needed.")
        else:
            print(f"⚠️ Found old/wrong key: {current_key_definition[:5]}...")
            # Replace with new key
            new_content = re.sub(pattern, f'\\1"{NEW_KEY}"', content)
            with open(TARGET_FILE, "w", encoding="utf-8") as f:
                f.write(new_content)
            print(f"✅ UPDATED {TARGET_FILE} with the new key.")
            
            # Trigger Restart
            print("🔄 Restarting server processes...")
            os.system("pkill -f uvicorn")
            os.system("pkill -f python")
            # Start in background
            os.system("nohup python3 backend/main.py > backend.log 2>&1 &")
            print("🚀 Server restarting...")
            time.sleep(5) # Wait for boot
    else:
        print("❌ Could not find 'DEEPSEEK_API_KEY' variable in main.py. Please check file structure.")

except FileNotFoundError:
    print(f"❌ Error: {TARGET_FILE} not found.")
