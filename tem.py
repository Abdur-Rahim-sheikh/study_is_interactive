import streamlit as st
from streamlit_drawable_canvas import st_canvas
import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib.patches import Arc

st.set_page_config(page_title="Angle Visualizer", layout="centered")
st.title("📐 Draw 3 Points, See the Angle")

st.markdown(
    """
Use the **circle tool** to draw exactly 3 points on the canvas.<br>
The app will treat them as **A → B → C** and show the angle ∠ABC.
""",
    unsafe_allow_html=True,
)

# Canvas with cross lines
canvas_result = st_canvas(
    fill_color="rgba(0, 0, 255, 0.3)",
    stroke_width=2,
    stroke_color="#000000",
    background_color="#FFFFFF",
    height=400,
    width=400,
    drawing_mode="circle",
    key="angle_points_canvas",
    initial_drawing={
        "objects": [
            # Horizontal and vertical semi-transparent lines for guidance
            {
                "type": "line",
                "version": "4.4.0",
                "originX": "center",
                "originY": "center",
                "left": 0,
                "top": 200,
                "width": 400,
                "height": 0,
                "stroke": "gray",
                "strokeWidth": 2,
                "opacity": 0.3,
                "angle": 0,
                "offsetX": 0,
                "offsetY": 0,
                "path": [],
                "fill": None,
            },
            {
                "type": "line",
                "version": "4.4.0",
                "originX": "center",
                "originY": "center",
                "left": 200,
                "top": 0,
                "width": 0,
                "height": 400,
                "stroke": "gray",
                "strokeWidth": 2,
                "opacity": 0.3,
                "angle": 0,
                "offsetX": 0,
                "offsetY": 0,
                "path": [],
                "fill": None,
            },
        ]
    },
)

# Extract circle centers
points = []
if canvas_result.json_data:
    for obj in canvas_result.json_data["objects"]:
        if obj["type"] == "circle":
            x = obj["left"] + obj["radius"]
            y = obj["top"] + obj["radius"]
            points.append((x, y))

if len(points) == 3:
    A, B, C = points

    def angle_between(p1, vertex, p2):
        v1 = np.array(p1) - np.array(vertex)
        v2 = np.array(p2) - np.array(vertex)
        dot = np.dot(v1, v2)
        norm = np.linalg.norm(v1) * np.linalg.norm(v2)
        angle_rad = np.arccos(np.clip(dot / norm, -1.0, 1.0))
        return np.degrees(angle_rad)

    angle = angle_between(A, B, C)

    # Classify angle
    if math.isclose(angle, 90, abs_tol=2):
        label = "Right angle"
    elif angle < 90:
        label = "Acute angle"
    elif angle < 180:
        label = "Obtuse angle"
    elif math.isclose(angle, 180, abs_tol=2):
        label = "Straight angle"
    else:
        label = "Reflex angle"

    st.success(f"∠ABC = **{angle:.2f}°** → *{label}*")

    # Plot it using matplotlib
    fig, ax = plt.subplots()
    ax.set_aspect("equal")
    ax.set_xlim(0, 400)
    ax.set_ylim(400, 0)  # Invert Y for canvas coordinates
    ax.axis("off")

    # Draw points
    for pt, name in zip([A, B, C], ["A", "B", "C"]):
        ax.plot(*pt, "ko")
        ax.text(pt[0] + 5, pt[1] - 5, name, fontsize=12)

    # Draw lines
    ax.plot([A[0], B[0]], [A[1], B[1]], "b-", lw=2)
    ax.plot([C[0], B[0]], [C[1], B[1]], "b-", lw=2)

    # Draw arc for angle
    def draw_angle_arc(center, p1, p2, radius=30):
        v1 = np.array(p1) - np.array(center)
        v2 = np.array(p2) - np.array(center)
        angle1 = math.degrees(math.atan2(-v1[1], v1[0]))
        angle2 = math.degrees(math.atan2(-v2[1], v2[0]))

        theta1, theta2 = sorted([angle1, angle2])
        if abs(theta2 - theta1) > 180:
            theta1, theta2 = theta2, theta1 + 360

        arc = Arc(
            center,
            radius * 2,
            radius * 2,
            angle=0,
            theta1=theta1,
            theta2=theta2,
            color="red",
        )
        ax.add_patch(arc)
        # Label angle
        mid_angle = math.radians((theta1 + theta2) / 2)
        label_x = center[0] + (radius + 10) * np.cos(mid_angle)
        label_y = center[1] - (radius + 10) * np.sin(mid_angle)
        ax.text(label_x, label_y, f"{angle:.1f}°", color="red", fontsize=12)

    draw_angle_arc(B, A, C)

    st.pyplot(fig)

elif len(points) < 3:
    st.info(
        f"Draw 3 points using the **circle tool**. Points placed: {len(points)} / 3"
    )
else:
    st.warning("More than 3 points detected. Please clear and try again.")

if st.button("🔄 Clear Canvas"):
    st.rerun()
