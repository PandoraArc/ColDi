#!/usr/bin/env conda run -n pyimagej python

import re


def capture_Filename(fileLocation):
    fileLocation = fileLocation.split(sep="/")
    match = re.match(r'(^.*)\.jpeg', fileLocation[len(fileLocation) - 1])
    if match is not None:
        match.group()
        return match[1]
    else:
        match = re.match(r'(^.*)\.png', fileLocation[len(fileLocation) - 1])
        if match is not None:
            match.group()
            return match[1]
        else:
            match = re.match(r'(^.*)\.jpg', fileLocation[len(fileLocation) - 1])
            if match is not None:
                match.group()
                return match[1]
            else:
                return 1


def SaveAs(order, savelocation="", savename=""):
    if order == 5:
        save_out = 'saveAs("Results", "' + savelocation + '/' + savename + str(-order) + '.csv");\n'
    else:
        save_out = 'saveAs("Tiff", "' + savelocation + '/' + savename + str(-order) + '.tif");\n'
    return save_out


def macro_generate(filelocation, pixelrefObj, refObj, cropZoneX, cropZoneY, cropZoneHW, threshold_front, theshold_back, size_start, size_end,
                   circularity_start, circularity_end, savelocation, savename):
    openfile = 'open(' + '"' + filelocation + '");\n'
    set_scale = 'run("Set Scale...", "distance=' + pixelrefObj + ' known=' + refObj + ' pixel=1 unit=mm");\n'
    make_oval = 'makeOval(' + cropZoneX + ',' + cropZoneY + ',' + cropZoneHW + ',' + cropZoneHW + ');\n'
    crop = 'run("Crop");\n'
    bit = 'run("8-bit");\n'
    cut_filter = 'run("Bandpass Filter...", "filter_large=40 filter_small=3 suppress=None tolerance=5 autoscale saturate");run("Clear Outside");\n'
    threshold = ("""setThreshold(""" + threshold_front + """,""" +
                 theshold_back + """);setOption("BlackBackground", false);run("Convert to Mask");\n""")
    set_measurement = 'run("Set Measurements...", "area mean min redirect=None decimal=3");\n'
    analyze = ("""run("Analyze Particles...", "size=""" + size_start + """-""" + size_end + """ circularity=""" + circularity_start + """-""" +
               circularity_end + """ show=Outlines display exclude clear");\n""")
    macro = (openfile + set_scale + make_oval + crop + bit + SaveAs(1, savelocation, savename) + cut_filter + SaveAs(2, savelocation, savename)
             + threshold + SaveAs(3, savelocation, savename) + set_measurement + analyze + SaveAs(4, savelocation, savename) +
             SaveAs(5, savelocation, savename))
    return macro

def macro_generate_half_plate(filelocation, pixelrefObj, refObj, cropZoneX, cropZoneY, cropZoneH, cropZoneW, threshold_front, theshold_back, size_start, size_end,
                   circularity_start, circularity_end, savelocation, savename):
    openfile = 'open(' + '"' + filelocation + '");\n'
    set_scale = 'run("Set Scale...", "distance=' + pixelrefObj + ' known=' + refObj + ' pixel=1 unit=mm");\n'
    make_rectangle = 'makeRectangle(' + cropZoneX + ',' + cropZoneY + ',' + cropZoneH + ',' + cropZoneW + ');\n'
    crop = 'run("Crop");\n'
    bit = 'run("8-bit");\n'
    cut_filter = 'run("Bandpass Filter...", "filter_large=40 filter_small=3 suppress=None tolerance=5 autoscale saturate");\n'
    threshold = ("""setThreshold(""" + threshold_front + """,""" +
                 theshold_back + """);setOption("BlackBackground", false);run("Convert to Mask");\n""")
    set_measurement = 'run("Set Measurements...", "area mean min redirect=None decimal=3");\n'
    analyze = ("""run("Analyze Particles...", "size=""" + size_start + """-""" + size_end + """ circularity=""" + circularity_start + """-""" +
               circularity_end + """ show=Outlines display exclude clear");\n""")
    
    macro = (openfile + set_scale + make_rectangle + crop + bit + SaveAs(1, savelocation, savename) + cut_filter + SaveAs(2, savelocation, savename)
             + threshold + SaveAs(3, savelocation, savename) + set_measurement + analyze + SaveAs(4, savelocation, savename) +
             SaveAs(5, savelocation, savename))
    
    return macro
