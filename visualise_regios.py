###############################################################################
#
#   Author:  Lisa Hoek
#   Project: HANDS-RX
#            https://github.com/LisaHoek/HANDS-RX
#
###############################################################################

from functionsXML import *
import numpy as np
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

#data_dir = r"C:\Users\LHoek\Documents\Overlijdensdata\Training_set\Training_set\page"
data_dir = r"C:\Users\LHoek\Documents\Overlijdensdata\Transkribus\OR_1879-1884\OR_1879-1884\page"
#data_dir = r"C:\Users\LHoek\Documents\Overlijdensdata\Transkribus\OR_1885-1889\OR_1885-1889\page"
#data_dir = r"C:\Users\LHoek\Documents\Overlijdensdata\Transkribus\OR_1890-1894\OR_1890-1894\page"
#data_dir = r"C:\Users\LHoek\Documents\Overlijdensdata\Transkribus\OR_1931-1934\page"
#data_dir = r"C:\Users\LHoek\Documents\Overlijdensdata\Transkribus\OR_1938-1939_1945-1946_Stad\page"
#data_dir = r"C:\Users\LHoek\Documents\Overlijdensdata\Transkribus\OR_1946_Buiten+1947-1949\page"
#data_dir = r"C:\Users\LHoek\Documents\Overlijdensdata\Transkribus\OR_1908-1909+1930\page"
#data_dir = r"D:\backup\Documents\Overlijdensdata\Transkribus\OR_1938-1939_1945-1946_Stad\page"

texts, metadata, textregions = read_files(data_dir)

small_lst = []
for certificate in textregions.keys():
    small_lst.append(certificate)

fig, ax = plt.subplots(tight_layout=True)
ap = annotated_patches(fig, ax)

wrong_pages = [] # optional: choose a list of page numbers to inspect, leave empty to inspect all

for cert_id, cert in enumerate(small_lst[0:50]): # set here the certificates to view at once, e.g., 0:50
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

# choose a fitting baseline
ap.add_patches("baseline", 'open_poly', [[650,-125]], "0", [[('650','-1000'), ('1400','-1000'), ('1400','-125')]]) # general baseline
#ap.add_patches("baseline", 'open_poly', [[650,-250]], "0", [[('650','-1000'), ('1350','-1000'), ('1350','-250')]]) # twoLate strict
#ap.add_patches("baseline", 'open_poly', [[650,-250]], "0", [[('650','-920'), ('1310','-920'), ('1310','-250')]]) # twoLate not strict
#ap.add_patches("baseline", 'open_poly', [[650,-165]], "0", [[('650','-920'), ('1310','-920'), ('1310','-165')]]) # twoLate improved

plt.axis('equal')
plt.axis('off')
plt.show()