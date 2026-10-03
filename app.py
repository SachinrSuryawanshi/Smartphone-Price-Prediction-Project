import streamlit as st
from prediction import predict_price

st.set_page_config(
    page_title="Smartphone Price Predictor",
    page_icon="📱",
    layout="wide"
)

st.title("📱 Smartphone Price Predictor")
st.markdown("This application predicts the price of a smartphone based on its features.")

with st.form(key="price_prediction_form"):
    st.subheader("1. General & Hardware Features")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        brand = st.selectbox(
            "Brand",
            ["samsung", "apple", "xiaomi", "oneplus", "realme", "vivo", "oppo", "motorola", "iqoo", "poco", "google", "other"]
        )
        os = st.selectbox(
            "Operating System",
            ["android", "ios", "other"]
        )

    with col2:
        processor_name = st.selectbox(
            "Processor Name",
            ["snapdragon", "dimensity", "bionic", "helio", "exynos", "unisoc", "other"]
        )
        notches = st.selectbox(
            "Display Notch",
            ["punch hole", "water drop", "notch", "bezel-less", "other"]
        )

    with col3:
        rating = st.slider("Rating", min_value=50.0, max_value=100.0, value=82.0, step=0.5)
        core = st.selectbox(
            "Processor Core",  
            [4.0, 6.0, 8.0, 10.0], index=2
        )

    with col4:
        speed = st.number_input("Processor Speed (GHz)", min_value=1.0, max_value=4.0, value=2.4, step=0.1)
        sim = st.selectbox("SIM Type", [1.0, 2.0], format_func=lambda x: "Single SIM" if x == 1.0 else "Dual SIM")

    st.markdown("---")
    st.subheader("2. Memory & Display Features")
    col5, col6, col7, col8 = st.columns(4)

    with col5:
        ram = st.select_slider(
            "RAM (GB)", options=[2.0, 3.0, 4.0, 6.0, 8.0, 12.0, 16.0], value=8.0
        )
        rom = st.select_slider(
            "ROM (GB)", options=[32.0, 64.0, 128.0, 256.0, 512.0, 1024.0], value=128.0
        )

    with col6:
        inches = st.number_input("Display Size (inches)", min_value=4.0, max_value=8.0, value=6.67, step=0.01)
        hz = st.select_slider(
            "Refresh Rate (Hz)", options=[60.0, 90.0, 120.0, 144.0, 165.0], value=120.0
        )

    with col7:
        xaxis = st.number_input("Horizontal Resolution (px)", min_value=480.0, max_value=3000.0, value=1080.0, step=10.0)
        yaxis = st.number_input("Vertical Resolution (px)", min_value=800.0, max_value=4000.0, value=2400.0, step=10.0)

    with col8:
        has_memory_card = st.checkbox("Supports Memory Card", value=False)
        is_hybrid = st.checkbox("Hybrid SIM Slot", value=False)
        extra_support = st.number_input("Extra Memory Support (GB)", min_value=0.0, max_value=2048.0, value=0.0, step=128.0)

    st.markdown("---")
    st.subheader("3. Battery & Camera Features")
    col9, col10, col11, col12 = st.columns(4)

    with col9:
        capacity = st.number_input("Battery Capacity (mAh)", min_value=1500.0, max_value=8000.0, value=5000.0, step=100.0)
        watt = st.number_input("Charging Wattage (W)", min_value=5.0, max_value=240.0, value=45.0, step=1.0)
        fast_charging = st.checkbox("Supports Fast Charging", value=True)

    with col10:
        rear_camera = st.selectbox("Has Rear Camera", [1.0, 0.0], format_func=lambda x: "Yes" if x == 1.0 else "No")
        rear_camera_count = st.slider("Rear Camera Count", min_value=1.0, max_value=4.0, value=3.0, step=1.0)

    with col11:
        rear_mp = st.number_input("Rear Camera Megapixels (MP)", min_value=5.0, max_value=200.0, value=50.0, step=1.0)
        front_mp = st.number_input("Front Camera Megapixels (MP)", min_value=2.0, max_value=60.0, value=16.0, step=1.0)

    with col12:
        st.write("**Connectivity Features**")
        five_g = st.checkbox("5G Support", value=True)
        nfc = st.checkbox("NFC Support", value=False)
        ir_blaster = st.checkbox("IR Blaster Support", value=False)

    submitted = st.form_submit_button("Predict Smartphone Price", use_container_width=True)

if submitted:
    smartphone_features = {
        "Brand": brand,
        "OS": os,
        "Notches": notches,
        "ProcessorName": processor_name,
        "rating": float(rating),
        "Speed": float(speed),
        "Core": float(core),
        "Ram": float(ram),
        "Rom": float(rom),
        "Inches": float(inches),
        "Xaxis": float(xaxis),
        "Yaxis": float(yaxis),
        "Hz": float(hz),
        "Capacity": float(capacity),
        "Watt": float(watt),
        "RearCamera": float(rear_camera),
        "RearMP": float(rear_mp),
        "FrontMP": float(front_mp),
        "RearCameraCount": float(rear_camera_count),
        "Sim": float(sim),
        "5G": int(five_g),
        "NFC": int(nfc),
        "IrBlaster": int(ir_blaster),
        "FastCharging": int(fast_charging),
        "HasMemoryCard": int(has_memory_card),
        "IsHybrid": int(is_hybrid),
        "ExtraSupport": float(extra_support)
    }

    try:
        predicted_price = predict_price(smartphone_features)
        st.success(f"Predicted Smartphone Price: ₹ {predicted_price:,.2f}")
    except Exception as e:
        st.error(f"Error in prediction: {e}")