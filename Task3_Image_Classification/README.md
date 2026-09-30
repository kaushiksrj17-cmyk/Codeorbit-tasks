# Image Classification AI (MobileNetV2)

A clean, beginner-friendly, and interactive web application built with **Streamlit**, **PyTorch**, and **TorchVision** to perform real-time image classification using a pretrained **MobileNetV2** deep learning model.

Developed as **Task 3** of an internship project showcasing deep learning inference, model evaluation, and accessible web UI design.

---

## 📌 Project Overview

**Image Classification AI** allows users to either upload custom images (in JPG, JPEG, PNG, or WEBP format) or select from pre-bundled sample images to instantly classify them into one of 1,000 recognizable object categories. The application performs on-device machine learning inference, visualizes the top predictions with confidence percentages, interprets the reliability of the prediction, displays image metadata, and maintains a session prediction history—all without relying on external cloud APIs or databases.

---

## 🎯 Internship Task Requirements Satisfied

This project completely fulfills all required objectives for Internship Task 3:
- **Pretrained Deep Learning Model**: Uses MobileNetV2 with official `MobileNet_V2_Weights.DEFAULT` pretrained on the ImageNet-1K dataset.
- **Sample Classification & Display**: Accurately classifies sample and uploaded images and presents the predicted labels prominently.
- **Educational Explanations**: Features a detailed, beginner-friendly breakdown of how convolutional neural networks, transfer learning, and preprocessing pipelines work.
- **Small Dataset & Clean Code**: Kept lightweight, modular, and readable with zero training from scratch or external database overhead.

---

## ✨ Key Features

1. **Flexible Image Input**:
   - Upload personal photos in `JPG`, `JPEG`, `PNG`, or `WEBP` formats.
   - Or test immediately with pre-bundled sample images from `sample_images/`.
2. **Real-Time Pretrained Inference**:
   - Employs MobileNetV2 from TorchVision with evaluation caching (`@st.cache_resource`) and gradient-free inference (`torch.no_grad()`).
3. **Visually Prominent Primary Prediction**:
   - Clearly highlights the winning class label and percentage confidence.
4. **Top-3 Prediction Breakdown**:
   - Displays the top 3 highest-probability classes alongside animated progress bars.
5. **Confidence Interpretation**:
   - **High Confidence** ($\ge 80\%$): Strong statistical alignment with the detected class.
   - **Moderate Confidence** ($50\% - 79\%$): Most likely candidate among close alternatives.
   - **Low Confidence** ($< 50\%$): Ambiguous, multiple objects present, or outside ImageNet training data.
6. **Image Information Panel**:
   - Displays pixel dimensions, image file format, color mode, and file size.
7. **Session Prediction History**:
   - Tracks recent classifications in browser session memory with a single-click **Clear History** button.
8. **Interactive AI Architecture Guide**:
   - Educational expander illustrating the end-to-end data flow from pixel normalization to Softmax output.
9. **Dark & Light Mode Themes**:
   - Seamless interactive theme toggle in the sidebar with high-contrast, modern UI styling for both midnight dark mode and crisp daylight mode.
10. **Zero Cloud Dependencies & Privacy Safe**:
    - 100% local CPU inference; uploaded images are processed in volatile memory and never saved to disk.

---

## 🛠️ Technologies Used

| Technology | Purpose |
| :--- | :--- |
| **Python 3.11** | Core programming language |
| **Streamlit** | Fast, modern web application framework |
| **PyTorch (`torch`)** | Deep learning framework for tensor computing and neural network inference |
| **TorchVision** | Computer vision library providing pretrained models, weights, and image transforms |
| **Pillow (`PIL`)** | Python Imaging Library for reading, converting, and inspecting image metadata |

---

## 🧠 Pretrained Model Architecture: MobileNetV2

### 1. What is a Pretrained Model?
A **pretrained model** is a neural network that has previously undergone extensive training on a massive dataset (such as ImageNet) to learn general visual patterns (lines, edges, colors, shapes, and complex object parts). By leveraging a pretrained model, we avoid the need to train a network from scratch, which would otherwise demand millions of images, high-performance GPUs, and weeks of computation.

### 2. What is MobileNetV2?
**MobileNetV2** is a convolutional neural network architecture engineered by Google specifically for mobile and embedded vision applications. It introduces:
- **Depthwise Separable Convolutions**: Drastically reduces parameter count and computational complexity by separating spatial filtering from feature combination.
- **Inverted Residuals & Linear Bottlenecks**: Preserves rich information through thin bottleneck layers while enabling memory-efficient residual connections.
- **Lightweight Footprint**: Weighing only approximately **14 MB** (3.5 million parameters), it runs smoothly on standard laptop CPUs without needing a dedicated GPU.

### 3. What is ImageNet?
**ImageNet** is an academic visual benchmark dataset consisting of over 14 million annotated images organized into more than 20,000 categories. The standard ImageNet Large Scale Visual Recognition Challenge (ILSVRC) subset used by MobileNetV2 includes **1,000 diverse classes** spanning animal breeds, vehicles, everyday objects, household tools, and food items.

---

## 🔬 How the Prediction Pipeline Works

```text
Input Image (Any Size)
        ↓
Image Normalization & Resize (224 × 224 pixels)
        ↓
MobileNetV2 Deep Convolutional Backbone
        ↓
Visual Feature Extraction (Edges → Textures → Shapes → High-Level Parts)
        ↓
Linear Classifier (1,000 Output Logits)
        ↓
Softmax Activation Function (Probability Distribution)
        ↓
Top-3 Predicted Classes & Confidence Scores
```

### 1. Image Preprocessing
Neural networks require strictly uniform numerical inputs:
1. **Format Harmonization**: Any RGBA or grayscale image is converted to standard 3-channel RGB.
2. **Resizing & Cropping**: Scaled to `256 × 256` and center-cropped to `224 × 224` pixels to fit the model's receptive field.
3. **Tensor Conversion**: Scaled from integer byte values ($0 - 255$) to floating-point tensors ($0.0 - 1.0$).
4. **Standardization**: Normalized using ImageNet's dataset-wide RGB mean (`[0.485, 0.456, 0.406]`) and standard deviation (`[0.229, 0.224, 0.225]`).

### 2. Confidence Scoring (Softmax)
The final dense layer produces 1,000 raw unnormalized numbers known as **logits**. The **Softmax** mathematical function exponents and normalizes these logits so they sum up to $1.0$ ($100\%$):

$$\text{Softmax}(z_i) = \frac{e^{z_i}}{\sum_{j=1}^{1000} e^{z_j}}$$

The category corresponding to the maximum probability is selected as the top prediction.

> **Important Note:** A confidence score represents the model's relative certainty among its 1,000 known classes. It is **not** an absolute guarantee of real-world accuracy, particularly if the subject does not belong to the ImageNet ontology.

---

## 📁 Project Structure

```text
Task3_Image_Classification/
├── app.py                # Main Streamlit web application & inference logic
├── requirements.txt      # Minimal dependency manifest (streamlit, torch, torchvision, Pillow)
├── README.md             # Comprehensive project documentation
└── sample_images/        # Directory containing test sample images
    ├── .gitkeep          # Git directory tracking placeholder
    ├── cat.jpg           # Sample image 1: Domestic cat
    ├── coffee_mug.jpg    # Sample image 2: Coffee cup / mug
    └── sports_car.jpg    # Sample image 3: Sports car / vehicle
```

---

## 🚀 Installation & Local Setup

### Prerequisites
- **Python 3.8+** (Python 3.11 recommended).
- Internet connection on the first run (TorchVision will automatically download the ~14 MB MobileNetV2 weights into your local user cache).

### Step-by-Step Setup (Windows PowerShell)

1. Open PowerShell and navigate to the project directory:
   ```powershell
   cd D:\Task3_Image_Classification
   ```

2. *(Optional but Recommended)* Create and activate a Python virtual environment:
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```
   > **Note on PowerShell Execution Policy:** If you encounter a script execution policy restriction when activating the virtual environment, run the following temporary command in your PowerShell session:
   > ```powershell
   > Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
   > ```

3. Install the required dependencies:
   ```powershell
   pip install -r requirements.txt
   ```

4. Launch the Streamlit application:
   ```powershell
   streamlit run app.py
   ```

5. The application will automatically open in your default web browser at:
   ```text
   http://localhost:8501
   ```

---

## 🧪 Example Workflow

1. **Launch the Application**: Run `streamlit run app.py`.
2. **Choose Input Mode**: In the left sidebar, choose **"📤 Upload an Image"** or **"🖼️ Try a Sample Image"**.
3. **Inspect Output**:
   - Review the image preview and image metadata (resolution, format, size).
   - Check the **Predicted Object** card for the highest-confidence category.
   - Review the **Confidence Interpretation** note and the **Top 3 Predictions** progress bars.
4. **View History**: Look at the sidebar to review previously classified items. Click **"Clear History"** anytime to reset.
5. **Explore AI Architecture**: Expand the **"How the AI Works"** guide to learn about neural networks and image preprocessing.

---

## ⚠️ Limitations

- **ImageNet Scope (1,000 Classes)**: The model can only classify objects that map to its 1,000 ImageNet categories. Abstract art, specialized medical imagery, or novel items will be mapped to the closest mathematical visual proxy.
- **Multiple Objects**: Standard MobileNetV2 performs whole-image classification, not multi-object bounding-box detection (like YOLO). If an image contains both a dog and a bicycle, the model will output the dominant object.
- **Adversarial / Noisy Backgrounds**: Heavy clutter, poor lighting, or extreme crops may reduce model confidence.

---

## 🔮 Future Enhancements

- **Object Detection Integration**: Add bounding-box detection (e.g., using SSD-MobileNet or YOLO) to classify multiple objects simultaneously.
- **Explainable AI (Grad-CAM)**: Implement visual heatmaps to highlight the exact pixel regions MobileNetV2 focused on to reach its decision.
- **Batch Processing**: Support uploading multiple images simultaneously with batch export of predictions to CSV.

---

## 🎓 Internship Learning Outcomes

- Practical implementation of deep learning inference in Python using PyTorch and TorchVision.
- Understanding convolutional neural network architectures and model efficiency trade-offs (MobileNetV2).
- Mastery of computer vision preprocessing techniques (normalization, resizing, tensor transformation).
- Development of intuitive, responsive machine learning web applications using Streamlit.
