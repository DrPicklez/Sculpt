# Import libraries

from math import dist
from random import seed
from statistics import multimode
from tkinter import Y
from turtle import color
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.widgets import Slider, Button, RadioButtons
from matplotlib.patches import Circle, PathPatch, Rectangle
from matplotlib.markers import MarkerStyle
from matplotlib.transforms import Affine2D
import mpl_toolkits.mplot3d.art3d as art3d
import numpy as np
from gradient import GetColorFrom2DNoise
import time


babble = np.array([[446.606225, 0.0, 0.0]
,[425.575487, 130.071916, 9.946644]
,[368.310562, 248.591116, 20.138466]
,[278.282524, 344.673546, 30.171853]
,[164.041564, 410.143326, 40.281247]
,[35.599222, 439.028969, 50.430562]
,[-95.643056, 428.669638, 60.594982]
,[-217.906101, 379.841942, 70.793175]
,[-320.088388, 296.84857, 81.022506]
,[-392.902355, 187.190667, 91.282636]
,[-429.591015, 60.77209, 101.574261]
,[-426.605502, -70.821615, 111.898503]
,[-384.180319, -195.409281, 122.256825]
,[-306.149869, -301.395831, 132.648955]
,[-199.660114, -378.737293, 143.075402]
,[-74.711827, -420.039014, 153.538211]
,[56.870617, -421.318601, 164.037803]
,[182.539838, -382.28684, 174.57403]
,[290.12246, -306.522942, 185.148379]
,[369.1327, -201.321362, 195.76245]
,[411.777457, -76.861036, 206.416268]
,[413.675227, 54.689241, 217.110166]
,[374.472573, 180.263449, 227.84604]
,[298.003176, 287.288281, 238.62502]
,[191.825055, 364.925342, 249.447146]
,[66.585711, 405.123519, 260.313104]
,[-64.923153, 403.612032, 271.224823]
,[-189.13681, 360.437295, 282.183286]
,[-293.106068, 279.921868, 293.188662]
,[-365.789255, 170.33746, 304.241706]
,[-399.335399, 43.206468, 315.344268]
,[-390.039964, -87.930927, 326.49746]
,[-338.728503, -208.964228, 337.701606]
,[-250.770825, -306.661547, 348.95732]
,[-135.674238, -370.149905, 360.266199]
,[-6.121069, -392.266116, 371.629684]
,[123.458314, -370.371246, 383.048354]
,[238.428404, -306.722995, 394.522661]
,[325.570809, -208.368378, 406.053688]
,[374.700531, -86.511174, 417.643034]
,[379.949737, 44.754102, 429.291743]
,[340.503092, 170.050837, 441.00039]
,[260.814564, 274.471651, 452.769569]
,[150.238306, 345.3564, 464.600326]
,[22.057803, 373.937558, 476.494063]
,[-108.092164, 356.530377, 488.451855]
,[-224.114778, 295.072956, 500.474358]
,[-311.425113, 197.027551, 512.56216]
,[-358.819447, 74.602871, 524.716007]
,[-360.013268, -56.657002, 536.93697]
,[-314.63135, -179.807059, 549.226221]
,[-228.385662, -278.710595, 561.584618]
,[-112.466366, -340.181491, 574.012804]
,[17.796517, -355.813645, 586.511368]
,[144.877914, -323.248164, 599.080951]
,[251.384651, -246.674422, 611.722303]
,[322.473133, -136.449994, 624.436307]
,[348.022451, -7.822878, 637.22383]
,[324.190841, 121.112372, 650.085568]
,[254.132201, 231.92295, 663.02211]
,[147.73569, 308.490177, 676.033995]
,[20.37215, 339.431873, 689.121751]
,[-109.222148, 319.924322, 702.285893]
,[-221.656097, 252.616438, 715.527025]
,[-299.805117, 147.44739, 728.845644]
,[-331.509765, 20.332546, 742.242347]
,[-311.61185, -109.136864, 755.717643]
,[-242.963625, -220.672906, 769.27206]
,[-136.199339, -296.493325, 782.906035]
,[-8.248252, -324.249207, 796.619985]
,[120.236317, -299.18638, 810.414278]
,[228.166239, -225.144034, 824.289298]
,[297.512633, -114.162085, 838.245386]
,[316.426902, 15.309936, 852.282873]
,[281.433746, 141.369948, 866.402085]
,[198.268407, 242.335225, 880.603284]
,[81.139453, 300.525475, 894.88677]
,[-49.533622, 305.489894, 909.25281]
,[-170.582801, 256.073405, 923.70167]
,[-260.187883, 160.887038, 938.233531]
,[-301.891611, 37.012467, 952.848618]
,[-287.781664, -92.90868, 967.547103]
,[-220.203036, -204.740015, 982.329202]
,[-111.600744, -277.355979, 997.195048]
,[17.572556, -296.75098, 1012.144777]
,[142.576663, -258.933136, 1027.178491]
,[239.085966, -170.975379, 1042.296337]
,[287.989864, -49.92403, 1057.498401]
,[279.338731, 80.324398, 1072.784769]
,[214.592862, 193.647123, 1088.15552]
,[106.631741, 266.948621, 1103.610708]
,[-22.588874, 284.98995, 1119.150394]
,[-146.357403, 243.764335, 1134.774605]
,[-238.690307, 151.636999, 1150.483341]
,[-279.867156, 27.897249, 1166.276557]
,[-260.83055, -101.092716, 1182.154175]
,[-185.429003, -207.435143, 1198.1161]
,[-69.900721, -267.772056, 1214.162297]
,[60.406606, -268.567958, 1230.2927]
,[176.472595, -209.381643, 1246.507301]
,[252.062089, -103.292955, 1262.806117]
,[269.775101, 25.739972, 1279.189114]
,[225.275672, 148.124281, 1295.656246]
,[128.631704, 235.373239, 1312.207277]
,[2.317047, 266.843383, 1328.84185]
,[-123.835892, 234.843266, 1345.559753]
,[-219.625038, 146.774737, 1362.360889]
,[-261.772087, 23.693259, 1379.245243]
,[-239.764288, -104.50881, 1396.212873]
,[-158.749945, -206.25168, 1413.263638]
,[-38.647533, -256.091888, 1430.396985]
,[90.513744, -241.305911, 1447.612407]
,[196.022952, -165.398358, 1464.909797]
,[250.795177, -47.55013, 1482.289279]
,[240.477342, 81.974665, 1499.750895]
,[167.487221, 189.443838, 1517.294054]
,[50.801133, 246.4903, 1534.917991]
,[-78.764082, 237.797237, 1552.622512]
,[-186.571684, 165.448057, 1570.407853]
,[-243.40592, 48.73647, 1588.27399]
,[-233.560784, -80.678833, 1606.219959]
,[-159.523885, -187.245027, 1624.245087]
,[-41.604446, -241.340448, 1642.349482]
,[87.385683, -227.639046, 1660.533445]
,[191.076473, -149.74021, 1678.796046]
,[239.877015, -29.610693, 1697.136262]
,[219.619982, 98.435405, 1715.554312]
,[135.90919, 197.397479, 1734.050518]
,[12.934489, 238.284995, 1752.623608]
,[-113.256896, 208.908933, 1771.272705]
,[-205.297246, 117.749537, 1789.998394]
,[-235.556826, -8.187978, 1808.800441]
,[-194.721406, -131.075646, 1827.677134]
,[-94.986096, -213.629878, 1846.628546]
,[33.362228, -230.475524, 1865.655203]
,[150.850426, -176.187972, 1884.755444]
,[220.98071, -67.443134, 1903.928608]
,[221.681204, 61.931829, 1923.175533]
,[152.483373, 171.21992, 1942.494841]
,[35.184716, 225.684387, 1961.885399]
,[-92.872899, 207.762923, 1981.348137]
,[-190.469624, 122.976205, 2000.881745]
,[-225.889493, -1.332331, 2020.484969]
,[-187.395217, -124.701761, 2040.158872]
,[-87.404377, -206.540603, 2059.901746]
,[41.11323, -219.675643, 2079.712728]
,[155.420133, -159.527344, 2099.592783]
,[217.102551, -46.06748, 2119.539417]
,[205.234468, 82.50515, 2139.554014]
,[123.614166, 182.523176, 2159.640075]
,[0.014775, 219.791621, 2179.735432]
,[-123.182744, 181.083346, 2200]], dtype="float")

class SculptureViewer():
    def __init__(self, points) -> None:
        
        self.points = points

        self.pointToPointX = np.ptp(points[:,0])
        self.minX = np.min(points[:,0])
        self.maxX = np.max(points[:,0])
        self.mutX = self.minX / self.maxX + 1.  #get multiplier for funnel
        print(self.mutX)

        self.pointToPointY = np.ptp(points[:,1])
        self.minY = np.min(points[:,1])
        self.maxY = np.max(points[:,1])
        self.mutY = self.minY / self.maxY + 1.  #get multiplier for funnel
        print(self.mutY)

        
        self.pointToPointZ = np.ptp(points[:,2])
        print(self.pointToPointZ)

        #TOFIX
        #make noise the width and height of the rise of the tower
        #distMinX = dist((0, 0), (0,self.minX))
        #distMinX /= self.pointToPointX
        #distMinX += 1.
        #distMinY = dist((0, 0), (0,self.minY))
        #distMinY /= self.pointToPointY
        #distMinY += 1.
        #self.distMinX = distMinX
        #self.distMinY = distMinY
        #print(distMinX)
        #print(distMinY)

        # self.distMult = np.array([0, 0])
        self.distMult = [self.minX, self.minY]

        self.fig = plt.figure(figsize=(10, 10))
        self.ax = plt.axes(projection='3d')
        self.ax.set_box_aspect((np.ptp(self.points[:,0]), np.ptp(self.points[:,1]), np.ptp(self.points[:,2])))

        hugh = plt.axes([0.25, 0.0, 0.65, 0.03])
        octave = plt.axes([0.25, 0.025, 0.65, 0.03])
        offsetNoiseX = plt.axes([0.25, 0.05, 0.65, 0.03])
        offsetNoiseY = plt.axes([0.25, 0.075, 0.65, 0.03])
        
        self.hugh = 0.
        self.seed = 1
        self.octave = 2
        self.offsetNoiseX = 0.
        self.offsetNoiseY = 0.

        self.s_hugh = Slider(hugh, 'Hugh', 0.01, 1., valinit=self.hugh)
        self.s_octave = Slider(octave, 'Octaves', 0, 12, valinit=self.octave, valstep=2)
        self.s_offsetNoiseX = Slider(offsetNoiseX, 'offsetNoiseX', 0., 1., valinit=self.offsetNoiseX)
        self.s_offsetNoiseY = Slider(offsetNoiseY, 'offsetNoiseY', 0., 1., valinit=self.offsetNoiseY)
        
        self.s_hugh.on_changed(self.updateHugh)
        self.s_octave.on_changed(self.updateSeed)
        self.s_offsetNoiseX.on_changed(self.updateOffX)
        self.s_offsetNoiseY.on_changed(self.updateOffY)

        marker = MarkerStyle('s')
        # marker._transform = marker.get_transform().rotate_deg(30.)
        marker = marker.scaled(1, 1.62)
        # marker._transform().
        self.marker = marker
        

        self.colorMan = GetColorFrom2DNoise(self.octave, self.seed)
        self.colorMan.setRes(self.pointToPointX + 0.5, self.pointToPointY + 0.5, self.pointToPointZ)

        self.updatePlot(self.makeColors(self.hugh, self.offsetNoiseX, self.offsetNoiseY))
        #v self.drawPlanes()


    def makeColors(self, hugh, _xOffset, _yOffset):
        colorArray = []
        for poin in self.points:
            x = poin[0]
            y = poin[1]

            w =(0., 0)
            w = np.array([poin[0], poin[1]])
            h = np.array([self.mutX, self.mutY])
            w *= h
            normX = (x+ w[0] + (self.pointToPointX * 0.5)) #centreOffset
            normY = (y+ w[1] + (self.pointToPointY * 0.5))

            #normX = (poin[0] + (self.pointToPointX * 0.5)) #centreOffset
            #normY = (poin[1] + (self.pointToPointY * 0.5))
            

            self.colorMan.addOffset(_xOffset, _yOffset)
            col = self.colorMan.getColorRGB(normX, normY, hugh)
            colorArray.append(col)
        return colorArray

#https://matplotlib.org/stable/gallery/mplot3d/pathpatch3d.html
    def updatePlot(self, colorArray):
        self.ax.clear()
        self.ax.scatter(self.points[:,0],self.points[:,1],self.points[:,2], s=500, color=colorArray, marker=self.marker)
        self.ax.set_axis_off()
    
    def drawPlanes(self):
        self.ax.clear()
        for point in self.points:
            x = point[0] /self.fig.get_figwidth()
            y = point[1] /self.fig.get_figheight()
            p = Rectangle((x,y), 0.5, 0.5, angle=0, rotation_point='center')
            self.ax.add_patch(p)    
            art3d.pathpatch_2d_to_3d(p, z=0.5, zdir="z")
    
    #OCtave dont work well during runtime???
    def updateOctave(self, val):
        self.octave = int(val)
        self.colorMan = GetColorFrom2DNoise(self.octave, self.seed)
        self.updatePlot(self.makeColors(self.hugh, self.offsetNoiseX, self.offsetNoiseY))
    
    def updateSeed(self, val):
        self.seed = int(val)
        self.colorMan = GetColorFrom2DNoise(self.octave, self.seed)
        self.updatePlot(self.makeColors(self.hugh, self.offsetNoiseX, self.offsetNoiseY))

    def updateHugh(self, val):
        self.hugh = val
        self.updatePlot(self.makeColors(self.hugh, self.offsetNoiseX, self.offsetNoiseY))

    def updateOffX(self, val):
        self.offsetNoiseX = val
        self.updatePlot(self.makeColors(self.hugh, self.offsetNoiseX, self.offsetNoiseY))
    
    def updateOffY(self, val):
        self.offsetNoiseY = val
        self.updatePlot(self.makeColors(self.hugh, self.offsetNoiseX, self.offsetNoiseY))
    
    def show(self):
        plt.show()

sculpture = SculptureViewer(babble)
sculpture.show()