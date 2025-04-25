from domain import BasePage

class RealNumbers(BasePage):
    def __init__(self):
        super().__init__(file_location=__file__)
        

    def drawGraph(self):
        pass
    
realNumbers = RealNumbers()
