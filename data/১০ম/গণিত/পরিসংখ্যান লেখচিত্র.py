from domain import BasePage


class StatisticsGraph(BasePage):
    def __init__(self):
        super().__init__(file_location=__file__)

    def build_page(self, **args):
        pass


sg = StatisticsGraph()
sg.build_page()
