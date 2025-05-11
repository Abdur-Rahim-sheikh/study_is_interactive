from ..models import Line, Point


class VerticesManipulator:
    def __init__(self, allowed_distance: int = 5):
        self.allowed_distance = allowed_distance

    def allowed(self, a: Point, b: Point):
        return a.distance_from(b) <= self.allowed_distance

    def merge_line_vertices(self, start_points: list[Point], end_points: list[Point]):
        if len(start_points) != len(end_points):
            raise ValueError(
                f"starts and ends should equal to form correct line {len(start_points)}!={len(end_points)}"
            )

        points = start_points + end_points
        visited = [False] * len(points)
        ans = []
        for i in range(len(points)):
            if visited[i]:
                continue

            found_pair = False
            for j in range(i + 1, len(points)):
                if visited[j]:
                    continue

                if self.allowed(points[i], points[j]):
                    found_pair = True
                    visited[j] = True
                    break
            if not found_pair:
                return False, []
            x = (points[i].x + points[j].x) / 2
            y = (points[i].y + points[j].y) / 2

            ans.append(Point(x, y))

        if len(ans) * 2 != len(points):
            return False, []

        return True, ans
