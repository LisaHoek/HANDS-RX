###############################################################################
#
#   Author:  Lisa Hoek
#   Project: HANDS-RX
#            https://github.com/LisaHoek/HANDS-RX
#
#   This script draws the certificate regions in an interactive plot.
#   SET YOUR VALUES AT THE UPPERCASE INSTRUCTIONS.
#
###############################################################################

from XML_utils import *
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.collections import PatchCollection

class annotated_patches:
    def __init__(self, fig, ax):
        self.fig = fig
        self.ax = ax

        self.annot = self.ax.annotate("", xy=(0,0),
                            xytext=(20,20),
                            textcoords="offset points",
                            bbox=dict(boxstyle="round", fc="w"),
                            arrowprops=dict(arrowstyle="->"))
        
        self.annot.set_visible(False)
        
        self.collectionsDict = {}
        self.coordsDict = {}
        self.namesDict = {}
        self.isActiveDict = {}

        self.motionCallbackID = self.fig.canvas.mpl_connect("motion_notify_event", self.hover)

    def add_patches(self, groupName, kind, xyCoords, names, polyCoordsEnd, *params):
        if kind== 'open_poly':
            polygons = [mpatches.Polygon([(xy[0], xy[1])]+pxy+[(xy[0]-0.1, xy[1]-0.1)], closed=False, ec="none") for xy, pxy in zip(xyCoords, polyCoordsEnd)]
            #polygon = [mpatches.Polygon([(xy[0], xy[1])]+polyCoordsEnd, ec="none") for xy in xyCoords]
            thisCollection = PatchCollection(polygons, facecolor="none", alpha=0.5, edgecolor=None)
            ax.add_collection(thisCollection)
        elif kind =='closed_poly':
            polygon = [mpatches.Polygon([(xy[0], xy[1])]+polyCoordsEnd, ec="none") for xy in xyCoords]
            thisCollection = PatchCollection(polygon, facecolor="none", alpha=0.5, edgecolor=None)
            ax.add_collection(thisCollection)
        
        else:
            raise ValueError('Unexpected kind', kind)
            
        self.collectionsDict[groupName] = thisCollection
        self.coordsDict[groupName] = xyCoords
        self.namesDict[groupName] = names
        self.isActiveDict[groupName] = False
        
    def update_annot(self, groupName, patchIdxs):
        self.annot.xy = self.coordsDict[groupName][patchIdxs[0]]
        self.annot.set_text(groupName + ': ' + self.namesDict[groupName][patchIdxs[0]])
        self.collectionsDict[groupName].set_edgecolor('red')
        self.isActiveDict[groupName] = True

    def hover(self, event):
        vis = self.annot.get_visible()
        updatedAny = False
        if event.inaxes == self.ax:            
            for groupName, collection in self.collectionsDict.items():
                cont, ind = collection.contains(event)
                if cont:
                    self.update_annot(groupName, ind["ind"])
                    self.annot.set_visible(True)
                    self.fig.canvas.draw_idle()
                    updatedAny = True
                else:
                    if self.isActiveDict[groupName]:
                        collection.set_edgecolor(None)
                        self.isActiveDict[groupName] = True
                    
            if (not updatedAny) and vis:
                self.annot.set_visible(False)
                self.fig.canvas.draw_idle()

# SET YOUR DATA DIRECTORY
data_dir = ""

# import from functionsXML to obtain the regions
_, _, _, _, textregions = read_files(data_dir)

# get a list of the keys (certificate ID's)    
small_lst = []
for certificate in textregions.keys():
    small_lst.append(certificate)

# SET YOUR CERTIFICATES TO VIEW IN THE PLOT
view = small_lst[0:1000]

# (optional) CHOOSE A LIST OF PAGE NUMBERS TO INSPECT, LEAVE EMPTY TO INSPECT ALL FROM SELECTED VIEW
wrong_pages = [] 

# create plot figure
fig, ax = plt.subplots(tight_layout=True)
ap = annotated_patches(fig, ax)
for cert_id, cert in enumerate(view):
    if len(wrong_pages) == 0 or cert_id+1 in wrong_pages:
        t_regions = textregions[cert]
        polys = []
        for id, regio in enumerate(t_regions):
            poly = []
            coords = regio.split(" ")
            for coord in coords:
                x = coord.split(",")[0]
                y = str(int(coord.split(",")[1])*-1)
                poly.append((x,y))
            polys.append(poly)
        polyBegins = []
        polyEnds = []
        for i in range(len(polys)):
            polyBegins.append([int(polys[i][0][0]), int(polys[i][0][1])])
            polyEnds.append(polys[i][1:])
        ap.add_patches("p"+str(cert_id+1)+": "+cert, 'open_poly', polyBegins, "0123456789", polyEnds)

# CHOOSE A FITTING BASELINE
ap.add_patches("baseline", 'open_poly', [[650,-125]], "0", [[('650','-1000'), ('1400','-1000'), ('1400','-125')]])

# opens an interactive plot
plt.axis('equal')
plt.axis('off')
plt.show()