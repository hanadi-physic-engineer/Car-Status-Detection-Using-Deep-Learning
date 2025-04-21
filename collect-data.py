from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
import time
import os
import json

geckodriver_path = "C:/Program Files/geckodriver-v0.34.0-win64/geckodriver.exe"
service = Service(geckodriver_path)
driver = webdriver.Firefox(service=service)

output_dir = "dataset"
os.makedirs(output_dir, exist_ok=True)

driver.get("http://103.154.152.215:11234/")
time.sleep(3)

components = ["door_front_left", "door_front_right", "door_rear_left", "door_rear_right", "hood"]
button_labels = {
    "door_front_left": "Front Left Door",
    "door_front_right": "Front Right Door",
    "door_rear_left": "Rear Left Door",
    "door_rear_right": "Rear Right Door",
    "hood": "Hood"
}
metadata = []

def click_button(label):
    try:
        button = driver.find_element(By.XPATH, f'//button[text()="{label}"]')
        button.click()
        time.sleep(1.2)
    except Exception as e:
        print(f"[ERROR] Tidak bisa klik {label}: {e}")

def capture_screenshot(states, sid):
    path = os.path.join(output_dir, f"screenshot_{sid:02d}.png")
    driver.save_screenshot(path)
    metadata.append({
        "screenshot_id": sid,
        "file_path": path,
        "component_states": states.copy()
    })

def close_all():
    print("[RESET] Menutup semua komponen...")
    for comp in components:
        click_button(button_labels[comp])
        click_button(button_labels[comp])

    time.sleep(2)

screenshot_id = 0
component_states = {
    "door_front_left": "closed",
    "door_front_right": "closed",
    "door_rear_left": "closed",
    "door_rear_right": "closed",
    "hood": "closed"
}

close_all()
capture_screenshot(component_states, screenshot_id)
screenshot_id += 1

click_button(button_labels["door_front_left"])
component_states["door_front_left"] = "open"
capture_screenshot(component_states, screenshot_id)
screenshot_id += 1

click_button(button_labels["door_front_right"])
component_states["door_front_right"] = "open"
capture_screenshot(component_states, screenshot_id)
screenshot_id += 1

click_button(button_labels["door_rear_right"])
component_states["door_rear_right"] = "closed"

click_button(button_labels["door_rear_left"])
component_states["door_rear_left"] = "open"
capture_screenshot(component_states, screenshot_id)
screenshot_id += 1

click_button(button_labels["door_rear_left"])
component_states["door_rear_left"] = "closed"

click_button(button_labels["door_rear_right"])
component_states["door_rear_right"] = "open"
capture_screenshot(component_states, screenshot_id)
screenshot_id += 1

click_button(button_labels["door_rear_right"])
component_states["door_rear_right"] = "closed"

click_button(button_labels["hood"])
component_states["hood"] = "open"
capture_screenshot(component_states, screenshot_id)
screenshot_id += 1

click_button(button_labels["hood"])
component_states["hood"] = "closed"

click_button(button_labels["door_front_right"])
component_states["door_front_right"] = "open"
capture_screenshot(component_states, screenshot_id)
screenshot_id += 1

with open(os.path.join(output_dir, "metadata.json"), "w") as f:
    json.dump(metadata, f, indent=4)

driver.quit()
