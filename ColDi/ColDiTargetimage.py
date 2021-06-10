class targetimage:

    def __init__(self, filename="", savename="", filelocation="", savelocation="", refObj="", pixelrefObj="",
                 cropZoneX="", cropZoneY="", cropZoneHW="", circularity_start="0.5", circularity_end="1", size_start="0.5", size_end="Infinity",
                 threshold_front="188", threshold_back="255", average=0, median=0) -> object:

        self.filename = filename
        self.savename = savename
        self.filelocation = filelocation
        self.savelocation = savelocation
        self.refObj = refObj
        self.pixelrefObj = pixelrefObj
        self.cropZoneX = cropZoneX
        self.cropZoneY = cropZoneY
        self.cropZoneHW = cropZoneHW
        self.circularity_start = circularity_start
        self.circularity_end = circularity_end
        self.size_start = size_start
        self.size_end = size_end
        self.threshold_front = threshold_front
        self.threshold_back = threshold_back
        self.average = average
        self.median = median
