# Car Component Status Detection

This project is designed to detect the status of car components (e.g., doors, hood) using AI and computer vision. It includes a machine learning model, a dataset collection script, a Flask-based backend, and a frontend for real-time status visualization.

## Features
- **Dataset Collection**: Automates the collection of car component images and their states.
- **Model Training**: Trains a neural network to classify the status of car components.
- **Real-Time Detection**: Captures car images and predicts component statuses in real-time.
- **Frontend Visualization**: Displays the detected statuses and images in a user-friendly interface.

---

## File Structure
- **`train_model.py`**: Script to train the `CarComponentNet` model using the collected dataset.
- **`model.py`**: Defines the `CarComponentNet` neural network architecture.
- **`frontend/index.html`**: Frontend interface for real-time status visualization.
- **`app.py`**: Flask backend for serving the frontend and handling predictions.
- **`collect-data.py`**: Automates the collection of car component images and metadata.
- **`dataset.py`**: Prepares the dataset and data loaders for training and validation.

---

## Setup Instructions

### Prerequisites
1. **Python**: Install Python 3.8 or higher.
2. **Dependencies**: Install required Python libraries:
   ```bash
   pip install torch torchvision flask selenium pillow
   ```
3. **Geckodriver**: Download and install [Geckodriver](https://github.com/mozilla/geckodriver/releases) for Selenium.

### Dataset Collection
1. Update the `geckodriver_path` in `collect-data.py` to the location of your Geckodriver executable.
2. Run the script to collect images and metadata:
   ```bash
   python collect-data.py
   ```
3. The dataset will be saved in the `dataset` folder.

### Model Training
1. Ensure the dataset is ready in the `dataset` folder.
2. Train the model by running:
   ```bash
   python train_model.py
   ```
3. The trained model will be saved in the `models` folder.

### Running the Application
1. Start the Flask backend:
   ```bash
   python app.py
   ```
2. Open the frontend in your browser at `http://localhost:5000`.

---

## Frontend Usage
1. Click the **Capture and Predict** button to capture car images and predict component statuses.
2. View the real-time detected statuses and images in the interface.

---

## Notes
- Ensure your system has a GPU for faster model training and inference (optional).
- The frontend communicates with the backend via the `/status` endpoint.

---

## Example Output
### Frontend
- Displays the status of car components (e.g., "open" or "closed").
- Shows real-time images of the car's left and right views.

### Backend
- Logs the prediction process and any errors encountered.

---