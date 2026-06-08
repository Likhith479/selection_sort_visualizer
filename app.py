import streamlit as st
import random
import time
import pandas as pd
import altair as alt

# Page Configuration
st.set_page_config(page_title="Selection Sort Visualizer", layout="wide")
st.title("📊 Selection Sort Visualizer")

st.markdown("""
Selection Sort divides the input list into two parts: a sorted sublist at the front 
and an unsorted sublist at the back. It repeatedly finds the **minimum element** from the unsorted sublist and swaps it with the leftmost unsorted element.
""")

# Sidebar Control Panel
st.sidebar.header("🔧 Control Panel")
array_size = st.sidebar.slider("Array Size", min_value=5, max_value=50, value=20, step=5)
speed = st.sidebar.slider("Animation Delay (seconds)", min_value=0.05, max_value=1.5, value=0.2, step=0.05)

# Session state initialization to hold data across interactions
if "array" not in st.session_state or st.sidebar.button("🔄 Generate New Array"):
    st.session_state.array = [random.randint(10, 100) for _ in range(array_size)]
    st.session_state.sorting = False

arr = st.session_state.array

# Rendering helper function
def render_chart(array, current_i=-1, current_j=-1, min_idx=-1, is_done=False):
    status_colors = []
    for idx in range(len(array)):
        if is_done or idx < current_i:
            status_colors.append("Sorted")
        elif idx == min_idx:
            status_colors.append("Current Minimum")
        elif idx == current_j:
            status_colors.append("Scanning Element")
        else:
            status_colors.append("Unsorted")
            
    df = pd.DataFrame({
        "Index": [str(x) for x in range(len(array))],
        "Value": array,
        "Status": status_colors
    })
    
    # Altair chart configuration
    chart = alt.Chart(df).mark_bar().encode(
        x=alt.X("Index:O", sort=None, title="Array Index Location"),
        y=alt.Y("Value:Q", title="Value"),
        color=alt.Color("Status:N", scale=alt.Scale(
            domain=["Unsorted", "Scanning Element", "Current Minimum", "Sorted"],
            range=["#A0AEC0", "#ECC94B", "#E53E3E", "#38A169"] # Muted Grey, Yellow, Red, Green
        ), title="Element State")
    ).properties(height=400)
    
    return chart

# Create visual container placeholder
chart_placeholder = st.empty()
chart_placeholder.altair_chart(render_chart(arr), use_container_width=True)

# Run Sort Process Execution
if st.sidebar.button("🚀 Start Sorting"):
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            # Update visual highlighting comparison pass
            chart_placeholder.altair_chart(render_chart(arr, i, j, min_idx), use_container_width=True)
            time.sleep(speed)
            
            if arr[j] < arr[min_idx]:
                min_idx = j
                chart_placeholder.altair_chart(render_chart(arr, i, j, min_idx), use_container_width=True)
                time.sleep(speed)
                
        # Swap found absolute minimum index with targeted left index edge
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
        chart_placeholder.altair_chart(render_chart(arr, i + 1, -1, -1), use_container_width=True)
        time.sleep(speed)
        
    st.success("🎉 Sorting complete! All elements are arranged in ascending order.")
    chart_placeholder.altair_chart(render_chart(arr, is_done=True), use_container_width=True)