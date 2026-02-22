# EnergySense ⚡

**Real-time Energy Intelligence through Computer Vision.**

EnergySense is a smart monitoring system designed to tackle one of the most common invisible costs: **unnecessary power consumption.** By leveraging computer vision, this project transforms standard camera feeds into intelligent sensors capable of judging energy wastage in real-time.

### 🧠 The Intelligence Behind It

Rather than relying on expensive smart hardware for every appliance, EnergySense uses **OpenCV** and **HSV color filtering** to "see" the environment like a human would:

* **Lighting Analysis:** Detects if lights are left on in unoccupied spaces by monitoring specific luminosity and HSV ranges.
* **Device Tracking:** Identifies active fans and projectors within specific camera frames.
* **Wastage Calculation:** Automatically calculates the energy (and money) being lost based on the duration these devices remain active without necessity.
* **Individual Reporting:** Provides actionable data to inform individuals and encourage better energy habits.

---

### 🚀 Getting Started

To keep the repository clean and efficient, the environment folder (`mp_env`) is excluded. You can set up your local instance in seconds:

**1. Clone the Project**

```bash
git clone https://github.com/arvinkhan/energySense.git
cd energySense

```

**2. Initialize Your Environment**

```powershell
# Create your local virtual environment
python -m venv mp_env

# Activate it (Windows)
.\mp_env\Scripts\activate

# Activate it (Mac/Linux)
source mp_env/bin/activate

```

**3. Install Dependencies**

```bash
pip install -r requirements.txt

```

---

### 🛠 Usage

Ensure your camera is positioned to cover the target devices, then run:

```bash
python main.py

```

### 📈 Key Features

* **Non-Invasive Monitoring:** No need for smart plugs; just use your existing camera infrastructure.
* **Zone-Specific Detection:** Fine-tuned tracking for projectors and fans.
* **Data-Driven Insights:** Converts visual "ON" states into tangible energy waste metrics.

---

**Developed by [Arvin Khan**](https://www.google.com/search?q=https://github.com/arvinkhan) *Driving sustainability through intelligent vision.*
