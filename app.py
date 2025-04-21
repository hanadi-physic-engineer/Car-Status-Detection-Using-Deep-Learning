from flask import Flask, jsonify, send_from_directory
from PIL import Image
import torch
from torchvision import transforms
from model import CarComponentNet
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.common.exceptions import NoSuchElementException, WebDriverException
import os
import time
import base64
from io import BytesIO
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

model = CarComponentNet()
model.load_state_dict(torch.load("models/car_component_model.pth"))
model.eval()
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

inference_transforms = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

geckodriver_path = "C:/Program Files/geckodriver-v0.34.0-win64/geckodriver.exe"

try:
    service = Service(geckodriver_path)
    driver = webdriver.Firefox(service=service)
    driver.get("https://euphonious-concha-ab5c5d.netlify.app/")
    time.sleep(3)
    logger.info("Successfully loaded web page")
except WebDriverException as e:
    logger.error(f"Failed to initialize WebDriver: {e}")
    raise

def get_screenshot_prediction():
    try:
        try:
            rotate_left_btn = driver.find_element(By.ID, "rotate-left")
            for _ in range(5):
                rotate_left_btn.click()
                time.sleep(0.5)
            logger.info("Rotated camera to left")
        except NoSuchElementException:
            logger.warning("Rotate left button not found, skipping rotation")

        screenshot_left_path = "temp_screenshot_left.png"
        driver.save_screenshot(screenshot_left_path)
        logger.info("Captured left screenshot")

        try:
            rotate_right_btn = driver.find_element(By.ID, "rotate-right")
            for _ in range(10):
                rotate_right_btn.click()
                time.sleep(0.5)
            logger.info("Rotated camera to right")
        except NoSuchElementException:
            logger.warning("Rotate right button not found, skipping rotation")

        screenshot_right_path = "temp_screenshot_right.png"
        driver.save_screenshot(screenshot_right_path)
        logger.info("Captured right screenshot")

        img = Image.open(screenshot_left_path).convert("RGB")
        img_tensor = inference_transforms(img).unsqueeze(0).to(device)

        with torch.no_grad():
            output = model(img_tensor)
            predictions = (output > 0.5).int().cpu().numpy()[0]

        components = ["door_front_left", "door_front_right", "door_rear_left", "door_rear_right", "hood"]
        status = {comp: "open" if pred == 1 else "closed" for comp, pred in zip(components, predictions)}

        with open(screenshot_left_path, "rb") as f:
            left_image_base64 = base64.b64encode(f.read()).decode('utf-8')
        with open(screenshot_right_path, "rb") as f:
            right_image_base64 = base64.b64encode(f.read()).decode('utf-8')

        os.remove(screenshot_left_path)
        os.remove(screenshot_right_path)

        return {
            "status": status,
            "images": {
                "left": left_image_base64,
                "right": right_image_base64
            }
        }

    except Exception as e:
        logger.error(f"Error during screenshot prediction: {e}")
        components = ["door_front_left", "door_front_right", "door_rear_left", "door_rear_right", "hood"]
        status = {comp: "closed" for comp in components}
        placeholder_base64 = base64.b64encode(b"").decode('utf-8')
        return {
            "status": status,
            "images": {
                "left": placeholder_base64,
                "right": placeholder_base64
            },
            "error": str(e)
        }

@app.route('/')
def serve_frontend():
    return send_from_directory('frontend', 'index.html')

@app.route('/status', methods=['GET'])
def get_status():
    data = get_screenshot_prediction()
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)

import atexit
atexit.register(lambda: driver.quit())