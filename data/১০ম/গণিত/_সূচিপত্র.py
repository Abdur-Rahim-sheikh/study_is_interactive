from domain import BasePage


class Index(BasePage):
    def __init__(self):
        super().__init__(file_location=str(__file__))


index = Index()
index.info("পছন্দনীয় টপিকে ক্লিক করুন", expanded=True)
index.index_page()
