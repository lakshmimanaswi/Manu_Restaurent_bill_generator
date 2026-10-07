import streamlit as st
from datetime import datetime
import pandas as pd

st.set_page_config(
    page_title="Restaurant Billing",
    page_icon="🍽️",
    layout="wide"
)

# -----------------------------
# Menu
# -----------------------------
menu = {
    "Margherita Pizza": 249,
    "Veg Burger": 149,
    "White Sauce Pasta": 199,
    "Veg Noodles": 159,
    "Veg Biryani": 219,
    "Tacos": 179,
    "Club Sandwich": 129,
    "French Fries": 99,
    "Chocolate Cake": 129,
    "Ice Cream": 89,
    "Cold Coffee": 109,
    "Fresh Juice": 79
}

# -----------------------------
# Session state
# -----------------------------
if "bill_history" not in st.session_state:
    st.session_state.bill_history = []

# -----------------------------
# Custom CSS
# -----------------------------
st.markdown(
    """
    <style>
    .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
        max-width: 1200px;
    }

    .main-title {
        background: #ff6b35;
        padding: 16px;
        border-radius: 12px;
        text-align: center;
        color: white;
        margin-bottom: 12px;
    }

    .main-title h1 {
        margin: 0;
        font-size: 30px;
    }

    .main-title p {
        margin: 4px 0 0;
    }

    .menu-card {
        background: #ffffff;
        padding: 14px;
        border-radius: 10px;
        border: 1px solid #e5e5e5;
        margin-bottom: 8px;
        min-height: 95px;
    }

    .menu-name {
        font-weight: 700;
        font-size: 17px;
        color: #222222;
    }

    .menu-price {
        color: #e65100;
        font-weight: 700;
        font-size: 16px;
        margin-top: 6px;
    }

    .receipt {
        background: white;
        padding: 16px;
        border-radius: 10px;
        border: 1px solid #e5e5e5;
    }

    .grand-total {
        background: #fff3e0;
        padding: 12px;
        border-radius: 8px;
        text-align: right;
        margin-top: 8px;
    }

    .grand-total-text {
        font-size: 25px;
        font-weight: 700;
        color: #e65100;
    }

    div[data-testid="stVerticalBlock"] > div {
        gap: 0.5rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# -----------------------------
# Header
# -----------------------------
st.markdown(
    """
    <div class="main-title">
        <h1>🍽️ RESTAURANT BILLING SYSTEM</h1>
        <p>Simple • Fast • Professional</p>
    </div>
    """,
    unsafe_allow_html=True
)

# -----------------------------
# Customer details
# -----------------------------
st.subheader("👤 Customer Details")

c1, c2, c3 = st.columns(3)

with c1:
    customer_name = st.text_input(
        "Customer Name",
        placeholder="Enter customer name"
    )

with c2:
    phone = st.text_input(
        "Phone Number",
        placeholder="Enter phone number"
    )

with c3:
    order_type = st.selectbox(
        "Order Type",
        ["Dine-In", "Takeaway"]
    )

# -----------------------------
# Food menu
# -----------------------------
st.subheader("🍴 Food Menu")

menu_cols = st.columns(3)
selected_items = {}

for i, (food, price) in enumerate(menu.items()):
    with menu_cols[i % 3]:

        # Food name and price are clearly visible
        st.markdown(
            f"""
            <div class="menu-card">
                <div class="menu-name">🍴 {food}</div>
                <div class="menu-price">₹{price:.2f}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

        # The food name is also included in the input label
        qty = st.number_input(
            label=f"Quantity for {food}",
            min_value=0,
            max_value=20,
            value=0,
            step=1,
            key=f"qty_{i}",
            label_visibility="visible"
        )

        if qty > 0:
            selected_items[food] = qty

# -----------------------------
# Billing
# -----------------------------
if selected_items:

    st.subheader("💰 Billing Details")

    d1, d2 = st.columns(2)

    with d1:
        discount_rate = st.selectbox(
            "Discount",
            [0, 5, 10, 15, 20],
            format_func=lambda x: f"{x}%"
        )

    with d2:
        gst_rate = st.selectbox(
            "GST",
            [0, 5, 12, 18],
            format_func=lambda x: f"{x}%"
        )

    subtotal = sum(
        menu[food] * qty
        for food, qty in selected_items.items()
    )

    discount_amount = subtotal * discount_rate / 100
    after_discount = subtotal - discount_amount
    gst_amount = after_discount * gst_rate / 100
    grand_total = after_discount + gst_amount

    now = datetime.now()
    bill_no = now.strftime("BILL-%Y%m%d-%H%M%S")

    # -----------------------------
    # Bill preview
    # -----------------------------
    st.subheader("🧾 Bill Preview")

    st.markdown(
        '<div class="receipt">',
        unsafe_allow_html=True
    )

    left, right = st.columns(2)

    with left:
        st.write("**🍽️ FOOD PALACE**")
        st.write(f"**Bill No.:** {bill_no}")
        st.write(
            f"**Customer:** "
            f"{customer_name or 'Walk-in Customer'}"
        )
        st.write(
            f"**Phone:** "
            f"{phone or 'Not Provided'}"
        )

    with right:
        st.write(
            f"**Date:** "
            f"{now.strftime('%d-%m-%Y')}"
        )
        st.write(
            f"**Time:** "
            f"{now.strftime('%I:%M %p')}"
        )
        st.write(
            f"**Order Type:** {order_type}"
        )

    rows = [
        {
            "Food Item": food,
            "Quantity": qty,
            "Price (₹)": menu[food],
            "Amount (₹)": menu[food] * qty
        }
        for food, qty in selected_items.items()
    ]

    bill_df = pd.DataFrame(rows)

    st.dataframe(
        bill_df,
        use_container_width=True,
        hide_index=True
    )

    total_left, total_right = st.columns([3, 1])

    with total_left:
        st.write("**Subtotal**")
        st.write(f"**Discount ({discount_rate}%)**")
        st.write(f"**GST ({gst_rate}%)**")

    with total_right:
        st.write(f"₹{subtotal:.2f}")
        st.write(f"- ₹{discount_amount:.2f}")
        st.write(f"+ ₹{gst_amount:.2f}")

    st.markdown(
        f"""
        <div class="grand-total">
            GRAND TOTAL
            <div class="grand-total-text">
                ₹{grand_total:.2f}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )

    # -----------------------------
    # Summary metrics
    # -----------------------------
    m1, m2, m3 = st.columns(3)

    m1.metric(
        "Total Items",
        sum(selected_items.values())
    )

    m2.metric(
        "Subtotal",
        f"₹{subtotal:.2f}"
    )

    m3.metric(
        "Grand Total",
        f"₹{grand_total:.2f}"
    )

    # -----------------------------
    # Save bill
    # -----------------------------
    if st.button(
        "✅ Finalize and Save Bill",
        type="primary",
        use_container_width=True
    ):
        saved_time = datetime.now()

        st.session_state.bill_history.append(
            {
                "Bill Number": saved_time.strftime(
                    "BILL-%Y%m%d-%H%M%S"
                ),
                "Date": saved_time.strftime("%d-%m-%Y"),
                "Time": saved_time.strftime("%I:%M:%S %p"),
                "Customer": customer_name or "Walk-in Customer",
                "Phone": phone or "Not Provided",
                "Order Type": order_type,
                "Items": ", ".join(
                    f"{food} x{qty}"
                    for food, qty in selected_items.items()
                ),
                "Total Items": sum(selected_items.values()),
                "Subtotal (₹)": round(subtotal, 2),
                "Discount (%)": discount_rate,
                "Discount Amt (₹)": round(discount_amount, 2),
                "GST (%)": gst_rate,
                "GST Amt (₹)": round(gst_amount, 2),
                "Grand Total (₹)": round(grand_total, 2)
            }
        )

        st.success("Bill saved successfully!")

else:
    st.info(
        "Select the quantity of at least one food item "
        "to see the bill."
    )

# -----------------------------
# Saved bill history
# -----------------------------
st.divider()
st.subheader("📋 Saved Bill History")

if st.session_state.bill_history:

    history_df = pd.DataFrame(
        st.session_state.bill_history
    )

    st.dataframe(
        history_df,
        use_container_width=True,
        hide_index=True
    )

    st.download_button(
        "⬇️ Download History as CSV",
        data=history_df.to_csv(index=False).encode("utf-8"),
        file_name="bill_history.csv",
        mime="text/csv",
        use_container_width=True
    )

else:
    st.caption("No bills saved yet.")

st.caption("🍽️ Food Palace Billing System")