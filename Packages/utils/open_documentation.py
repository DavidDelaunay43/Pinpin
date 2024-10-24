import webbrowser


class Doc:


    @staticmethod
    def open_rtd_doc(cls):
        webbrowser.open(
            "https://pinpin.readthedocs.io/fr/latest/"
        )


    @staticmethod
    def open_ggd_doc(cls):
        webbrowser.open(
            "https://docs.google.com/document/d/1rPS77PSQjkBSydIM28LkLp33c41GZ0vKGNcw-vSjWic/edit?pli=1#heading=h.trwjrx4xtl9u"
        )


    @staticmethod
    def open_video_doc(cls):
        webbrowser.open(
            "https://www.youtube.com/watch?v=gC3nZN_dA2U&t=6s"
        )
