class PopUpProgressB(QWidget):

    def __init__(self):
        super().__init__()
        self.pbar = QProgressBar(self)
        self.pbar.setGeometry(30, 40, 500, 75)
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.pbar)
        self.setLayout(self.layout)
        self.setGeometry(300, 300, 550, 100)
        self.setWindowTitle('Progress Bar')
        # self.show()

        self.obj = Worker()
        self.thread = QThread()
        self.obj.intReady.connect(self.on_count_changed)
        #self.obj.moveToThread(self.thread)
        self.obj.finished.connect(self.thread.quit)
        self.obj.finished.connect(self.hide)  # To hide the progress bar after the progress is completed
        self.thread.started.connect(self.obj.proc_counter)
        # self.thread.start()  # This was moved to start_progress

    def start_progress(self):  # To restart the progress every time
        self.show()
        self.thread.start()

    def on_count_changed(self, value):
        self.pbar.setValue(value)
