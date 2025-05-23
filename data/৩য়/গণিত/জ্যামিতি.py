from datetime import datetime
from io import BytesIO

import streamlit as st
from PIL import Image
from streamlit_drawable_canvas import st_canvas

from domain import BasePage
from domain.models import Point
from domain.services import (
    AngleApproximator,
    Animate,
    StCanvasConverter,
    VerticesManipulator,
)

allowed_distance = 10
allowed_side_diff = 20

if "geometry_choice" not in st.session_state:
    st.session_state.geometry_choice = "কোন"


class GeometryPage(BasePage):
    def __init__(self):
        super().__init__(file_location=str(__file__))
        self.angle_approximator = AngleApproximator()
        self.height = 400
        self.width = 400
        self.animate = Animate(frame_height=self.height, frame_width=self.width)
        self.canvas_converter = StCanvasConverter()
        self.vertices_merger = VerticesManipulator(allowed_distance=allowed_distance)
        self.stroke_width = st.sidebar.slider("কলমের প্রস্থ: ", 1, 25, 3)
        self.stroke_color = st.sidebar.color_picker("কলমের কালার: ")
        self.bg_color = st.sidebar.color_picker("বোর্ডের কালার: ", "#eee")
        self.drawing_mode = "freedraw"
        self.point_display_radius = 3
        self.bg_image = None
        if st.session_state.geometry_choice == "আঁকিবুঁকি":
            self.drawing_mode = st.sidebar.selectbox(
                "ড্রয়িং টুল:",
                ("point", "freedraw", "line", "rect", "circle", "transform"),
                index=1,
            )

            self.point_display_radius = 3
            if self.drawing_mode == "point":
                self.point_display_radius = st.sidebar.slider(
                    "বিন্দুর ব্যস্যার্ধ: ", 1, 25, 3
                )
            self.bg_image = st.sidebar.file_uploader(
                "ব্যাকগ্রাউন্ডের ছবি:", type=["png", "jpg"]
            )
            if self.bg_image:
                self.bg_image = Image.open(self.bg_image)
        else:
            self.help_choice = st.sidebar.pills(
                "কোনো সাহায্য নেবেন?",
                ["না", "আধা", "পুরা"],
                selection_mode="single",
                default="আধা",
                key="help_choice",
            )

    def build_page(self, **args):
        # tabs = st.tabs(["কোন", "ত্রিভুজ", "চতুর্ভুজ", "পরীক্ষা", "আঁকিবুঁকি"])

        chosen = st.selectbox(
            "আকার ধরন পছন্দ করুন?",
            ["কোন", "ত্রিভুজ", "আঁকিবুঁকি"],
            key="geometry_choice",
        )
        if chosen == "কোন":
            self.angle()
        elif chosen == "ত্রিভুজ":
            self.triangle()
        else:
            self.freedraw()

    @st.fragment
    def angle(self):
        col1, col2, col3 = st.columns(3)
        bg_image = None
        if self.help_choice == "আধা":
            bg_image = self.angle_approximator.get_angle_preview(graph_style=False)
        elif self.help_choice == "পুরা":
            bg_image = self.angle_approximator.get_angle_preview(graph_style=True)
        with col1:
            st.write("প্রথমে `AB` এরপর `BC` বাহু আকো")

            canvas_result = st_canvas(
                fill_color="rgba(255, 165, 0, 0.3)",
                drawing_mode="line",
                background_color=self.bg_color,
                background_image=bg_image,
                stroke_width=self.stroke_width,
                stroke_color=self.stroke_color,
                height=self.height,
                width=self.width,
                key="angle_canvas",
            )

        with col2:
            title = st.empty()
            approximated_angle = None
            points = self.__extract_angle_from_lines(canvas_result.json_data)
            if len(points) > 4:
                st.error("আপনি ২টির বেশি রেখা এঁকেছেন")
                return
            elif len(points) != 4:
                title.write("প্রতিচ্ছবি :sunglasses:")
                startpoints = [points[i] for i in range(0, len(points), 2)]
                endpoints = [points[i] for i in range(1, len(points), 2)]
                self.animate.draw_lines(
                    startpoints,
                    endpoints,
                    stroke_width=self.stroke_width,
                    stroke_color=self.stroke_color,
                )
                return
            dist = points[1].distance_from(points[2])
            if dist > allowed_distance:
                st.error("সংযোগ বিন্দু আরো কাছাকাছি আনুন")
                return

            middle_x = (points[1].x + points[2].x) / 2
            middle_y = (points[1].y + points[2].y) / 2
            middle = Point(middle_x, middle_y)
            p1, p2, p3 = self.angle_approximator.get_angle_points(
                points[0], middle, points[3]
            )
            approximated_angle = self.angle_approximator.get_approximated_angle(
                p1, p2, p3, rad=False
            )

            title.write("আনুমানিক প্রদর্শন :brain:")
            self.animate.draw_angle(
                [
                    p1,
                    p2,
                    p3,
                ],
                stroke_width=self.stroke_width,
                stroke_color=self.stroke_color,
            )
        with col3:
            if not approximated_angle:
                st.write("এখনো কোন কোণ আকা হয়নি")
                return
            answer = st.pills(
                "বলতে পারো কি কোন একেছো?", ["সূক্ষ্মকোণ", "সমকোন", "সরলকোণ", "স্থূলকোণ"]
            )
            if answer and st.button("উত্তর মিলাই"):
                status, message = self.__match_angle_answer(approximated_angle, answer)
                if status:
                    st.balloons()
                    self.animate.write(message)

                else:
                    self.animate.write(message)

    @st.fragment
    def triangle(self):
        col1, col2, col3 = st.columns(3)
        bg_image = None
        if self.help_choice == "আধা":
            bg_image = self.angle_approximator.get_triangle_preview(graph_style=False)
        elif self.help_choice == "পুরা":
            bg_image = self.angle_approximator.get_triangle_preview(graph_style=True)

        with col1:
            st.write("প্রথমে `AB` এরপর `BC` শেষে `CA` বাহু আকো")

            canvas_result = st_canvas(
                fill_color="rgba(255, 165, 0, 0.3)",
                drawing_mode="line",
                background_color=self.bg_color,
                background_image=bg_image,
                stroke_width=self.stroke_width,
                stroke_color=self.stroke_color,
                height=self.height,
                width=self.width,
                key="triangle_canvas",
            )

        with col2:
            title = st.empty()
            approximated_angle = None
            points = self.__extract_angle_from_lines(canvas_result.json_data)
            startpoints = [points[i] for i in range(0, len(points), 2)]
            endpoints = [points[i] for i in range(1, len(points), 2)]
            if len(points) > 6:
                st.error("আপনি ৩ টির বেশি রেখা এঁকেছেন")
                return
            elif len(points) != 6:
                title.write("প্রতিচ্ছবি :sunglasses:")

                self.animate.draw_lines(
                    startpoints,
                    endpoints,
                    stroke_width=self.stroke_width,
                    stroke_color=self.stroke_color,
                )
                return

            status, points = self.vertices_merger.merge_line_vertices(
                startpoints, endpoints
            )
            if not status:
                st.error("সংযোগ বিন্দু আরো কাছাকাছি আনুন")
                return

            p1, p2, p3 = self.angle_approximator.get_angle_points(
                points[0], points[1], points[2]
            )
            approximated_angle = self.angle_approximator.get_approximated_angle(
                p1, p2, p3, rad=False
            )

            title.write("আনুমানিক প্রদর্শন :brain:")
            self.animate.draw_angle(
                [
                    p1,
                    p2,
                    p3,
                ],
                polygon=True,
                show_side_diff=True,
                allowed_diff=allowed_side_diff,
                stroke_width=self.stroke_width,
                stroke_color=self.stroke_color,
            )
        with col3:
            if not approximated_angle:
                st.write("এখনো কোন ত্রিভুজ আকা হয়নি")
                return
            answer = st.pills(
                "বলতে পারো কি ত্রিভুজ একেছো?",
                ["সমবাহু", "সমদ্বিবাহু", "বিষমবাহু"],  # এই নামের সাথে ম্যাচ করা হবে
                selection_mode="single",
            )
            if answer and st.button("উত্তর মিলাই", key="triangle"):
                status, message = self.__match_triangle_answer(
                    p1, p2, p3, answer, allowed_diff=allowed_side_diff
                )
                if status:
                    st.balloons()
                    self.animate.write(message)

                else:
                    self.animate.write(message)

    @st.fragment
    def freedraw(self):
        width = 1100
        height = 550
        # we can write a bg_image resizer
        col1, col2 = st.columns([3, 1], gap="large")
        with col1:
            canvas_result = st_canvas(
                fill_color="rgba(255, 165, 0, 0.3)",
                drawing_mode=self.drawing_mode,
                background_color=self.bg_color,
                background_image=self.bg_image if self.bg_image else None,
                stroke_width=self.stroke_width,
                stroke_color=self.stroke_color,
                width=width,
                height=height,
                point_display_radius=self.point_display_radius,
                key="freedraw_canvas",
            )

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f"interactive_study_{timestamp}.png"
        if canvas_result.image_data is not None:
            buffer = self.__download_image(
                canvas_result.image_data, width=width, height=height
            )
            col2.download_button(
                label="ডাউনলোড করি",
                data=buffer,
                file_name=file_name,
                mime="image/png",
                icon=":material/download:",
            )

    def __download_image(self, image, width, height):
        drawn_img = Image.fromarray((image).astype("uint8"))

        if self.bg_image:
            background = self.bg_image.convert("RGBA").resize((width, height))
            combined_img = Image.alpha_composite(background, drawn_img)
        else:
            combined_img = drawn_img
        # Save to in-memory file
        buffer = BytesIO()
        combined_img.save(buffer, format="PNG")
        buffer.seek(0)
        return buffer

    def __match_angle_answer(self, approximated_deg, given_answer):
        approximated_deg = (approximated_deg + 360) % 360
        if approximated_deg > 180:
            approximated_deg = 360 - approximated_deg
        data = ""
        if approximated_deg < 90:
            answer = "সূক্ষ্মকোণ"
            data = (
                f"{approximated_deg}° কোণটি এক সমকোণের চেয়ে ছোট তাই একে `সূক্ষ্মকোণ` বলা হয়"
            )
        elif approximated_deg == 90:
            answer = "সমকোন"
            data = f"{approximated_deg}° কোণটি একটি এক `সমকোন`"
        elif approximated_deg == 180:
            answer = "সরলকোণ"
            data = f"{approximated_deg}° কোণটি দুই সমকোণের সমান তাই একে `সরলকোণ` বলা হয়"
        else:
            answer = "স্থূলকোণ"
            data = f"{approximated_deg}° কোণটি এক সমকোণের চেয়ে বড় তাই একে `স্থূলকোণ` বলা হয়"

        status = True
        message = f"হুররাহ! সঠিক উত্তর এটি একটি `{answer}`!"
        if answer != given_answer:
            status = False
            message = f"দুঃখিত! তোমার {given_answer} উত্তর টি ভুল! এটি একটি `{answer}`!"

        message = f"{message}\n\n{data}"

        return status, message

    def __match_triangle_answer(
        self, p1: Point, p2: Point, p3: Point, given_answer: str, allowed_diff: int
    ):
        ab = p1.distance_from(p2)
        bc = p2.distance_from(p3)
        ca = p3.distance_from(p1)
        angle_deg = self.angle_approximator.get_approximated_angle(
            p1, p2, p3, rad=False
        )

        angle_msg = "পাশাপাশি এটি একটি `সূক্ষ্মকোণী` ত্রিভুজও বটে"

        if angle_deg == 90:
            angle_msg = "পাশাপাশি এটি একটি `সমকোণী` ত্রিভুজও বটে"
        elif angle_deg > 90:
            angle_msg = "পাশাপাশি এটি একটি `স্থূলকোণী` ত্রিভুজও বটে"

        triangle = "বিষমবাহু"

        def allowed(a, b):
            return abs(a - b) <= allowed_diff

        if allowed(ab, bc) and allowed(bc, ca):
            triangle = "সমবাহু"
        elif allowed(ab, bc) or allowed(bc, ca) or allowed(ca, ab):
            triangle = "সমদ্বিবাহু"

        status = True
        answer_msg = "হুররাহ! তোমার উত্তরটি সঠিক হয়েছে"
        if given_answer != triangle:
            status = False
            answer_msg = "দুঃখিত! তোমার উত্তরটি ভুল"

        triangle_msg = f"এটি একটি `{triangle}` ত্রিভুজ"
        msg = f"- {answer_msg} \n- {triangle_msg} এবং {angle_msg}"

        return status, msg

    def __extract_angle_from_lines(self, json_data) -> list[Point]:
        if json_data is None:
            return []
        points = []
        for obj in json_data["objects"]:
            if obj["type"] != "line":
                continue

            p1, p2 = self.canvas_converter.get_points_of_line(obj)
            points.append(Point(*p1))
            points.append(Point(*p2))
        return points


geometry = GeometryPage()
message = """
আমরা বিভিন্ন ধরনের কোন, ত্রিভুজ, চতুর্ভুজ আঁকতে পারি। এগুলি অনুশীলন করার জন্যই 
এই টপিক টি। বাম পাশের বোর্ডে মোটামুটি সিলেক্টেড বিষয়টি আকার চেষ্টা কর, আমার ইঞ্জিন 
ক্ষুদ্র ভুল ভ্রান্তি প্রেডিক্ট করে একটি ভালো চিত্র ডানে দেখাবে। এবার বল এটা কি এঁকেছ
অপশন থেকে। 

সাইডবারের অপশন গুলি দেখতে ভুল না। 

এছাড়াও এখানে আছে একটি বোর্ড যেখানে তুমি যা খুশি আঁকতে পারো, এবং স্মৃতির পাতায় 
রাখার জন্য সেভ ও করতে পারো। 


"""
geometry.info(message)
geometry.build_page()
