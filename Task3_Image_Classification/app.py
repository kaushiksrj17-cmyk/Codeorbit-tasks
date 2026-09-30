"""
Task 3: Image Classification Using a Pretrained Model
=====================================================
A beginner-friendly, polished Streamlit application that classifies images
using a pretrained MobileNetV2 convolutional neural network from TorchVision.

Key Capabilities:
- Single image upload (JPG, JPEG, PNG, WEBP)
- Pre-packaged sample image testing
- Real-time inference using MobileNetV2 (ImageNet weights)
- Prominent top prediction with confidence scoring
- Top-3 classification breakdown with confidence interpretation
- Image metadata inspection (dimensions, format, file size)
- In-memory session prediction history with clear functionality
- Educational expandable section explaining convolutional networks & inference flow
"""

import os
import io
from typing import List, Tuple, Optional
from PIL import Image, UnidentifiedImageError
import streamlit as st
import torch
import torchvision.models as models
from torchvision.models import MobileNet_V2_Weights


# ============================================================================
# PAGE CONFIGURATION
# ============================================================================
st.set_page_config(
    page_title="Image Classification AI",
    page_icon="🖼️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================================
# 1. MODEL LOADING & CACHING
# ============================================================================
@st.cache_resource(show_spinner="Loading pretrained MobileNetV2 model...")
def load_model():
    """
    Loads the pretrained MobileNetV2 model and associated preprocessing pipeline.
    Cached via @st.cache_resource so the model weights are loaded into memory
    only once across user interactions.
    """
    # Use the latest recommended default weights for MobileNetV2 trained on ImageNet-1K
    weights = MobileNet_V2_Weights.DEFAULT
    model = models.mobilenet_v2(weights=weights)
    
    # Set model to evaluation mode (disables dropout and batch norm training behavior)
    model.eval()
    
    # Preprocessing transforms associated with the pretrained weights
    # (Resizes, center crops to 224x224, converts to tensor, and applies ImageNet normalization)
    preprocess = weights.transforms()
    
    # Human-readable ImageNet category labels (1,000 classes)
    categories = weights.meta["categories"]
    
    return model, preprocess, categories


# ============================================================================
# 2. IMAGE PREDICTION & INFERENCE
# ============================================================================
def predict_image(
    image: Image.Image,
    model: torch.nn.Module,
    preprocess,
    categories: List[str],
    top_k: int = 3
) -> List[Tuple[str, float]]:
    """
    Preprocesses an input PIL image, runs inference through MobileNetV2,
    and returns the top-k predicted category labels and percentage probabilities.
    """
    # Ensure image is in RGB format (handles grayscale or RGBA PNGs gracefully)
    if image.mode != "RGB":
        image = image.convert("RGB")
    
    # Apply preprocessing transform and add batch dimension (Batch size = 1)
    input_tensor = preprocess(image).unsqueeze(0)
    
    # Perform forward pass without computing gradients (saves memory & speeds up inference)
    with torch.no_grad():
        output = model(input_tensor)
        # Apply Softmax activation across the 1,000 class logits to compute probabilities
        probabilities = torch.nn.functional.softmax(output[0], dim=0)
    
    # Extract the top-k highest scoring indices and probabilities
    top_probs, top_indices = torch.topk(probabilities, top_k)
    
    results = []
    for prob, idx in zip(top_probs, top_indices):
        category_name = categories[idx.item()]
        # Format label: replace underscores with spaces and capitalize
        clean_label = category_name.replace("_", " ").title()
        confidence_pct = prob.item() * 100.0
        results.append((clean_label, confidence_pct))
    
    return results


# ============================================================================
# 3. HELPER UTILITIES
# ============================================================================
def get_confidence_badge(confidence: float) -> Tuple[str, str, str]:
    """
    Returns an interpretation badge, color style, and message for a confidence score.
    """
    if confidence >= 80.0:
        return "High Confidence", "🟢", "The model is strongly confident in this category."
    elif confidence >= 50.0:
        return "Moderate Confidence", "🟡", "The model considers this the most likely category among alternatives."
    else:
        return "Low Confidence", "🔴", "The model is uncertain; the image may be ambiguous or outside ImageNet categories."


def get_image_details(image: Image.Image, file_bytes: Optional[bytes] = None) -> dict:
    """
    Extracts basic dimensions, format, and size information from an image.
    """
    size_str = "N/A"
    if file_bytes:
        size_kb = len(file_bytes) / 1024.0
        size_str = f"{size_kb:.1f} KB" if size_kb < 1024 else f"{(size_kb / 1024):.2f} MB"
    
    return {
        "Dimensions": f"{image.width} × {image.height} px",
        "Format": image.format if image.format else "Standard Image",
        "Color Mode": image.mode,
        "File Size": size_str
    }


def inject_custom_theme(is_dark: bool):
    """
    Applies custom CSS styling for Dark Mode or Light Mode.
    Ensures seamless contrast, beautiful card elevation, responsive layout,
    and polished typography across the entire interface.
    """
    if is_dark:
        theme_css = """
        <style>
            /* Base Dark Theme Overrides */
            .stApp {
                background: linear-gradient(180deg, #0b0f19 0%, #0f172a 100%) !important;
                color: #f8fafc !important;
            }
            [data-testid="stSidebar"] {
                background-color: #0b1120 !important;
                border-right: 1px solid #1e293b !important;
            }
            [data-testid="stSidebar"] hr {
                border-color: #1e293b !important;
            }
            [data-testid="stHeader"] {
                background: rgba(11, 15, 25, 0.85) !important;
                backdrop-filter: blur(8px) !important;
            }
            /* Headings */
            h1, h2, h3, h4 {
                color: #f1f5f9 !important;
            }
            /* Cards, expanders & containers */
            .stExpander {
                background-color: #111827 !important;
                border: 1px solid #1f2937 !important;
                border-radius: 10px !important;
            }
            .stExpander details summary {
                color: #e2e8f0 !important;
            }
            /* Buttons */
            .stButton > button {
                background: #1e293b !important;
                color: #f8fafc !important;
                border: 1px solid #334155 !important;
                border-radius: 8px !important;
                font-weight: 600 !important;
                transition: all 0.2s ease-in-out !important;
            }
            .stButton > button:hover {
                background: #2563eb !important;
                color: #ffffff !important;
                border-color: #60a5fa !important;
                box-shadow: 0 0 14px rgba(59, 130, 246, 0.45) !important;
            }
            /* Code and pre tags */
            code, pre {
                background-color: #1e293b !important;
                color: #38bdf8 !important;
            }
            /* Streamlit divider */
            hr {
                border-color: #1e293b !important;
            }
        </style>
        """
    else:
        theme_css = """
        <style>
            /* Base Light Theme Overrides */
            .stApp {
                background: linear-gradient(180deg, #f8fafc 0%, #eef2f6 100%) !important;
                color: #0f172a !important;
            }
            [data-testid="stSidebar"] {
                background-color: #ffffff !important;
                border-right: 1px solid #e2e8f0 !important;
            }
            [data-testid="stSidebar"] hr {
                border-color: #e2e8f0 !important;
            }
            [data-testid="stHeader"] {
                background: rgba(248, 250, 252, 0.85) !important;
                backdrop-filter: blur(8px) !important;
            }
            /* Headings */
            h1, h2, h3, h4 {
                color: #0f172a !important;
            }
            /* Cards, expanders & containers */
            .stExpander {
                background-color: #ffffff !important;
                border: 1px solid #e2e8f0 !important;
                border-radius: 10px !important;
            }
            .stExpander details summary {
                color: #1e293b !important;
            }
            /* Buttons */
            .stButton > button {
                background: #ffffff !important;
                color: #0f172a !important;
                border: 1px solid #cbd5e1 !important;
                border-radius: 8px !important;
                font-weight: 600 !important;
                transition: all 0.2s ease-in-out !important;
            }
            .stButton > button:hover {
                background: #2563eb !important;
                color: #ffffff !important;
                border-color: #1d4ed8 !important;
                box-shadow: 0 0 12px rgba(37, 99, 235, 0.25) !important;
            }
            /* Code and pre tags */
            code, pre {
                background-color: #f1f5f9 !important;
                color: #0369a1 !important;
            }
            /* Streamlit divider */
            hr {
                border-color: #e2e8f0 !important;
            }
        </style>
        """
    st.markdown(theme_css, unsafe_allow_html=True)


# ============================================================================
# 4. MAIN STREAMLIT APPLICATION
# ============================================================================
def main():
    # Header Section
    st.title("🖼️ Image Classification AI")
    st.markdown("**Classify images using a pretrained MobileNetV2 model**")
    st.caption("Internship Project • Task 3: Deep Learning Inference with PyTorch & TorchVision")
    st.divider()

    # Initialize in-memory session prediction history
    if "history" not in st.session_state:
        st.session_state["history"] = []

    # Attempt to load model
    try:
        model, preprocess, categories = load_model()
    except Exception as e:
        st.error(f"⚠️ Unable to initialize the pretrained model: {e}")
        st.info("Please ensure you have an active internet connection on first launch to allow TorchVision to download the model weights.")
        return

    # ------------------------------------------------------------------------
    # SIDEBAR: SETTINGS, CONTROLS & SESSION HISTORY
    # ------------------------------------------------------------------------
    with st.sidebar:
        # Theme Toggle Card
        st.header("🎨 Appearance")
        theme_mode = st.radio(
            "Display Theme:",
            options=["Dark 🌙", "Light ☀️"],
            index=0,
            horizontal=True,
            help="Switch between Dark and Light mode."
        )
        is_dark = theme_mode.startswith("Dark")
        inject_custom_theme(is_dark)

        st.divider()

        st.header("⚙️ Input Selection")
        input_source = st.radio(
            "Choose Image Source:",
            options=["📤 Upload an Image", "🖼️ Try a Sample Image"],
            help="Upload your own picture or choose from pre-bundled sample images."
        )

        st.divider()

        # Model Architecture Info Card
        st.subheader("🤖 Model Details")
        st.markdown(
            """
            - **Architecture:** MobileNetV2
            - **Framework:** PyTorch & TorchVision
            - **Pretrained Dataset:** ImageNet-1K (1,000 classes)
            - **Model Size:** ~14 MB (3.5M parameters)
            """
        )
        st.caption(
            "MobileNetV2 is an efficient convolutional neural network designed "
            "for mobile and edge devices. It enables instant image classification on a standard CPU."
        )

        st.divider()

        # Session Prediction History Card
        st.subheader("📜 Recent Predictions")
        if st.session_state["history"]:
            for item in reversed(st.session_state["history"][-5:]):
                st.markdown(f"• **{item['label']}** ({item['confidence']}) — *{item['filename']}*")
            
            if st.button("🗑️ Clear History", use_container_width=True):
                st.session_state["history"] = []
                st.rerun()
        else:
            st.caption("No images classified yet in this session.")

        st.divider()
        st.caption(
            "📌 **Disclaimer:** Predictions represent statistical probabilities based on ImageNet categories. "
            "They do not guarantee factual accuracy for ambiguous images."
        )

    # ------------------------------------------------------------------------
    # MAIN WORKSPACE: IMAGE ACQUISITION
    # ------------------------------------------------------------------------
    active_image: Optional[Image.Image] = None
    image_name: str = ""
    raw_bytes: Optional[bytes] = None

    if input_source == "📤 Upload an Image":
        st.subheader("1. Upload Image")
        uploaded_file = st.file_uploader(
            "Select an image file (JPG, JPEG, PNG, WEBP):",
            type=["jpg", "jpeg", "png", "webp"],
            help="Images are processed in runtime memory and are never saved to disk."
        )

        if uploaded_file is not None:
            try:
                raw_bytes = uploaded_file.getvalue()
                active_image = Image.open(io.BytesIO(raw_bytes))
                image_name = uploaded_file.name
            except (UnidentifiedImageError, OSError):
                st.error("⚠️ The uploaded file could not be recognized as a valid image. Please select a valid JPG, PNG, or WEBP file.")
                active_image = None

    else:
        # Sample image selection mode
        st.subheader("1. Select a Sample Image")
        sample_dir = os.path.join(os.path.dirname(__file__), "sample_images")
        
        # Scan for supported sample images in sample_images directory
        valid_extensions = (".jpg", ".jpeg", ".png", ".webp")
        sample_files = []
        if os.path.exists(sample_dir):
            sample_files = [
                f for f in os.listdir(sample_dir)
                if f.lower().endswith(valid_extensions)
            ]

        if sample_files:
            selected_sample = st.selectbox(
                "Choose a sample image to test:",
                options=sample_files,
                index=0
            )
            sample_path = os.path.join(sample_dir, selected_sample)
            try:
                with open(sample_path, "rb") as f:
                    raw_bytes = f.read()
                active_image = Image.open(io.BytesIO(raw_bytes))
                image_name = selected_sample
            except Exception as e:
                st.error(f"⚠️ Could not load selected sample: {e}")
                active_image = None
        else:
            st.info("ℹ️ No sample images found in `sample_images/`. Switch to 'Upload an Image' above to classify any photo.")

    # ------------------------------------------------------------------------
    # DISPLAY & CLASSIFICATION WORKFLOW
    # ------------------------------------------------------------------------
    if active_image is not None:
        col_img, col_results = st.columns([1, 1], gap="large")

        with col_img:
            st.subheader("📷 Image Preview")
            # Display image cleanly with bounded width
            st.image(active_image, caption=image_name, use_container_width=True)

            # Feature 6: Image Information
            details = get_image_details(active_image, raw_bytes)
            with st.container():
                st.markdown("**Image Information:**")
                info_cols = st.columns(2)
                with info_cols[0]:
                    st.write(f"• **Dimensions:** {details['Dimensions']}")
                    st.write(f"• **Format:** {details['Format']}")
                with info_cols[1]:
                    st.write(f"• **Color Mode:** {details['Color Mode']}")
                    st.write(f"• **File Size:** {details['File Size']}")

        with col_results:
            st.subheader("🔍 Prediction Results")
            
            with st.spinner("Analyzing visual features with MobileNetV2..."):
                try:
                    predictions = predict_image(active_image, model, preprocess, categories, top_k=3)
                except Exception as e:
                    st.error("⚠️ An unexpected error occurred while analyzing this image. Please try another image.")
                    return

            top_label, top_conf = predictions[0]
            level_text, badge_icon, level_desc = get_confidence_badge(top_conf)

            # Record in session history if newly classified
            history_entry = {
                "filename": image_name,
                "label": top_label,
                "confidence": f"{top_conf:.1f}%"
            }
            if not st.session_state["history"] or st.session_state["history"][-1] != history_entry:
                st.session_state["history"].append(history_entry)

            # Feature 3: Visually Prominent Main Prediction Card
            card_bg = "rgba(15, 23, 42, 0.75)" if is_dark else "#ffffff"
            card_border = "#3b82f6" if is_dark else "#2563eb"
            card_shadow = "0 8px 30px rgba(59, 130, 246, 0.25)" if is_dark else "0 8px 24px rgba(37, 99, 235, 0.10)"
            header_color = "#94a3b8" if is_dark else "#64748b"
            label_color = "#38bdf8" if is_dark else "#0284c7"
            conf_color = "#f8fafc" if is_dark else "#0f172a"

            st.markdown(
                f"""
                <div style="background: {card_bg}; border: 2px solid {card_border}; border-radius: 14px; padding: 20px 24px; margin-bottom: 16px; box-shadow: {card_shadow}; backdrop-filter: blur(10px);">
                    <div style="font-size: 0.85rem; text-transform: uppercase; color: {header_color}; font-weight: 700; letter-spacing: 0.05em;">Predicted Object</div>
                    <div style="font-size: 2.2rem; font-weight: 800; color: {label_color}; margin: 4px 0; letter-spacing: -0.02em;">{top_label}</div>
                    <div style="font-size: 1.15rem; font-weight: 600; color: {conf_color};">Confidence: <span style="color: #10b981; font-weight: 700;">{top_conf:.1f}%</span></div>
                </div>
                """,
                unsafe_allow_html=True
            )

            # Feature 5: Confidence Interpretation
            st.info(f"{badge_icon} **{level_text} ({top_conf:.1f}%):** {level_desc}")

            # Feature 4: Top 3 Predictions Breakdown
            st.markdown("### Top 3 Predictions")
            for rank, (label, conf) in enumerate(predictions, start=1):
                col_rank, col_bar = st.columns([2, 3])
                with col_rank:
                    st.write(f"**{rank}. {label}**")
                with col_bar:
                    st.progress(conf / 100.0, text=f"{conf:.1f}%")

    else:
        # Prompt user to provide an image if none is currently selected
        st.info("👈 Please upload an image from the sidebar or select a sample image to view predictions.")

    # ------------------------------------------------------------------------
    # FEATURE 10: HOW THE AI WORKS (EDUCATIONAL EXPANDER)
    # ------------------------------------------------------------------------
    st.divider()
    with st.expander("📘 How the AI Works (Architecture & Pipeline)", expanded=False):
        st.markdown(
            """
            ### The Visual Classification Flow
            ```text
            Input Image ➔ Resize & Normalize (224×224) ➔ MobileNetV2 Neural Network ➔ Visual Feature Extraction ➔ Softmax Probabilities ➔ Top Predictions
            ```

            ---

            #### 1. What is a Pretrained Model?
            A **pretrained model** is a machine learning model that has already been trained on an extensive, diverse dataset (such as ImageNet). Instead of training a model from scratch—which requires thousands of images, high-end GPUs, and days of computation—we reuse its pre-learned visual knowledge to classify new pictures instantly.

            #### 2. What is MobileNetV2?
            **MobileNetV2** is a lightweight, efficient deep learning architecture created by Google researchers. It utilizes **depthwise separable convolutions** and **inverted residual bottlenecks** to achieve high classification accuracy while requiring significantly fewer computations and memory (~14 MB). This makes it fast and responsive on everyday laptops and CPUs.

            #### 3. What is ImageNet?
            **ImageNet** is an academic computer vision benchmark dataset comprising millions of labeled images spanning **1,000 distinct categories** (ranging from dog breeds and birds to household items, musical instruments, and vehicles).

            #### 4. Why Preprocess the Image?
            Neural networks expect inputs of an exact mathematical shape and numerical scale:
            - **Resizing & Cropping:** The input image is resized to `224 × 224` pixels so every layer in the network receives tensors of consistent dimension.
            - **Normalization:** Pixel brightness values (initially 0 to 255) are converted to tensors and normalized using ImageNet's standard mean (`[0.485, 0.456, 0.406]`) and standard deviation (`[0.229, 0.224, 0.225]`).

            #### 5. How Does MobileNetV2 Analyze Visual Patterns?
            As the image flows through MobileNetV2's convolutional layers:
            - **Early Layers** detect simple, low-level visual building blocks (edges, colors, gradients, lines).
            - **Middle Layers** assemble edges into textures, motifs, and geometrical patterns.
            - **Deep Layers** recognize complex, high-level object features (eyes, wheels, paws, handles).

            #### 6. How is the Final Prediction Selected?
            The final layer produces 1,000 numerical scores (logits). The **Softmax activation function** converts these logits into a normalized probability distribution where all 1,000 scores sum up to `100%`. The category with the highest probability is identified as the primary prediction.
            """
        )

    # ------------------------------------------------------------------------
    # FEATURE 12: DISCLAIMER & FOOTER
    # ------------------------------------------------------------------------
    st.markdown(
        """
        <div style="text-align: center; color: #94a3b8; font-size: 0.8rem; margin-top: 2rem;">
            Internship Task 3 • Built with PyTorch, TorchVision & Streamlit • 100% Client-Side Machine Learning Inference
        </div>
        """,
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
