import numpy as np

class FlowExceedance:

    def __init__(self, start_date, end_date, duration, exceedance):
        self.start_date = start_date
        self.end_date = end_date
        self.duration = duration
        self.flow = []
        self.exceedance = exceedance
        self.max_magnitude = None

    def add_flow(self, flow_data):
        self.flow.append(flow_data)

    def get_max_magnitude(self):
        self.max_magnitude = np.nanmax(self.flow)
