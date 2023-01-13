import matplotlib
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.lines import Line2D
import numpy as np

# general plot settings
plt.rcParams.update({'font.size': 14})
plt.rcParams['figure.dpi'] = 300
plt.rcParams['figure.figsize'] = [8, 5]
plt.rc('text.latex', preamble=r'\usepackage{amsmath}')


# relevant labels for plot directions in this project, translating labels into LaTeX
dirLabel = dict()
dirLabel["boost_a"] = r"$\gamma\beta_a$ [GeV]"
dirLabel["abs3mom_a"] = r"$|\vec{p}_a|$ [GeV]"
dirLabel["mtt"] = r"$m_{tt}$ [GeV]"
dirLabel["mmumu"] = r"$m_{\mu\bar{\mu}}$ [GeV]"
dirLabel["pT"] = r"$p_T$ [GeV]"
dirLabel["pT_a"] = r"$p_T^a$ [GeV]"
dirLabel["pT_t"] = r"$p_T^t$ [GeV]"
dirLabel["pT_at"] = r"$p_T^{\bar{t}}$ [GeV]"
dirLabel["pT_mu"] = r"$p_T^{\mu}$ [GeV]"
dirLabel["pT_amu"] = r"$p_T^{\bar{\mu}}$ [GeV]"
dirLabel["theta"] = r"$\vartheta$ [$^\circ$]"
dirLabel["theta_a"] = r"$\vartheta_a$ [$^\circ$]"
dirLabel["theta_t"] = r"$\vartheta_t$ [$^\circ$]"
dirLabel["theta_at"] = r"$\vartheta_{\bar{t}}$ [$^\circ$]"
dirLabel["theta_mu"] = r"$\vartheta_{\mu}$ [$^\circ$]"
dirLabel["y"] = r"$y$"
dirLabel["y_a"] = r"$y_a$"
dirLabel["y_t"] = r"$y_t$"
dirLabel["y_at"] = r"$y_{\bar{t}}$"
dirLabel["y_mu"] = r"$y_{\mu}$"
dirLabel["eta"] = r"$\eta$"
dirLabel["eta_a"] = r"$\eta_a$"
dirLabel["eta_t"] = r"$\eta_t$"
dirLabel["eta_at"] = r"$\eta_{\bar{t}}$"
dirLabel["eta_mu"] = r"$\eta_{\mu}$"
dirLabel["eta_t-eta_at"] = r"$\eta_t-\eta_{\bar{t}}$"
dirLabel["deltaR"] = r"$\DeltaR$"
dirLabel["deltaR_at"] = r"$\Delta$R($at$)"
dirLabel["deltaR_tat"] = r"$\Delta$R($t\bar{t}$)"
dirLabel["deltaR_ata"] = r"$\Delta$R($a\bar{t}$)"
dirLabel["deltaR_muons"] = r"$\Delta$R($\mu\bar{\mu}$)"
dirLabel["oA"] = r"$\sphericalangle$ [$^\circ$]"
dirLabel["oA_at"] = r"$\sphericalangle(\vec{p}_a,\vec{p}_t)$ [$^\circ$]"
dirLabel["oA_tat"] = r"$\sphericalangle(\vec{p}_t,\vec{p}_{\bar{t}})$ [$^\circ$]"
dirLabel["oA_ata"] = r"$\sphericalangle(\vec{p}_{\bar{t}},\vec{p}_a)$ [$^\circ$]"
dirLabel["oAo"] = r"$\sphericalangle_\perp$ [$^\circ$]"
dirLabel["oAo_at"] = r"$\sphericalangle_\perp(\vec{p}_a,\vec{p}_t)$ [$^\circ$]"
dirLabel["oAo_tat"] = r"$\sphericalangle_\perp(\vec{p}_t,\vec{p}_{\bar{t}})$ [$^\circ$]"
dirLabel["oAo_ata"] = r"$\sphericalangle_\perp(\vec{p}_{\bar{t}},\vec{p}_a)$ [$^\circ$]"
dirLabel["oA_att"] = r"$\sphericalangle(\vec{p}_a,\vec{p}_{t\bar{t}})$ [$^\circ$]"
dirLabel["oA_muons"] = r"$\sphericalangle(\vec{p}_\mu,\vec{p}_{\bar{\mu}})$ [$^\circ$]"
dirLabel["dmumu"] = r"$d_{\mu,\bar{\mu}}$ [cm]"
dirLabel["ma"] = r"$m_a$ [GeV]"
dirLabel["ctt"] = r"$c_{tt}(\Lambda)$"
dirLabel["ctau"] = r"$c_\tau$ [cm]"
dirLabel["track_mu"] = r"$d_\mu$ [cm]"


def colour(r: int, g: int, b: int, a: float):
    """turns Integer 0-255 values r g and b into floats, keeps opacity a float
    
    returns a tuple of the float values for all colour channels: (r,g,b,a)"""
    return (r/256, g/256, b/256, a)

def colours(alpha: float):
    """defines a list of seven colour tuples with opacity alpha"""
    darkBlue = colour(0, 114, 178, alpha)
    lightBlue = colour(86, 180, 233, alpha)
    green = colour(0, 158, 115, alpha)
    yellow = colour(240, 228, 66, alpha)
    orange = colour(230, 159, 0, alpha)
    red = colour(215, 94, 0, alpha)
    pink = colour(204, 121, 167, alpha)
    return [darkBlue, lightBlue, green, yellow, orange, red, pink]
    
def coloursX(alpha, X):
    """returns a list of X colour tuples with opacity alpha, loops after 7"""
    if X>7:
        return colours(alpha) + coloursX(alpha/2, X-7)
    if X==7:
        return colours(alpha)
    if X==6:
        return colours(alpha)[0:6]
    if X==5:
        return colours(alpha)[0:4]+[colours(alpha)[5]]
    if X==4:
        return [colours(alpha)[0], colours(alpha)[1], colours(alpha)[2],
                colours(alpha)[3]]
    if X==3:
        return [colours(alpha)[1], colours(alpha)[2], colours(alpha)[4]]
    if X==2:
        return [colours(alpha)[5], colours(alpha)[6]]
    if X==1:
        return [colours(alpha)[4]]
    return []

def hist1d(data, labels, xlabel, filename=None,
           nbins=50, customXlim=None, title=None, log_scale=False, clip=False):
    """Plots 1d histogram
    
    data - list of datasets, each of which is plotted as a line
    labels - list of labels of the datasets
    xlabel - x label of the histogram
    filename - if None, the plot is not saved, otherwise it is
    nbins - the number of bins, default: 50
    customXlim - if not set, the x axis contains all values in data
    title - if not given, the plot is not given a title
    log_scale - if true the y-axis is displayed in log scale
    clip - option to plot the overflow of a cut off x-axis in the last bin, 
        using numpy clip function
    """
    n = len(data)
    if (len(data)!=len(labels)):
        print("Different array lengths")
    if customXlim == None:
        lmax = max(data[0])
        lmin = min(data[0])
        for date in data:
            if (len(date)>0):
                lmax = max(lmax, max(date))
                lmin = min(lmin, min(date))
    else:
        lmin = customXlim[0]
        lmax = customXlim[1]
    # binList = np.arange(lmin*0.95, lmax*1.05, (lmax*1.05-lmin*0.95)/nbins)
    binList = np.arange(lmin, lmax+(lmax-lmin)/nbins, (lmax-lmin)/nbins)
    maxheight = 0
    for i in range(n):
        if clip:
            data[i] = np.clip(data[i],binList[0],binList[-1])
        heights, bins, patches = plt.hist(data[i], histtype='step', 
                                color=coloursX(1,n)[i], bins=binList,
                                label=labels[i], lw=1, density = True)
        maxheight = max(max(heights), maxheight)
    plt.xlabel(xlabel)
    plt.ylabel("number of events [a.u.]")
    plt.xlim([lmin, lmax])
    if not log_scale:
        plt.ylim(bottom=0)
        plt.gca().get_yaxis().set_major_formatter(matplotlib.ticker.
                                              FormatStrFormatter('%.2f'))
    else:
        plt.yscale("log")
    handles = [Line2D([], [], c=coloursX(1,n)[i], lw=3) for i in range(n)]
    plt.legend(handles, labels, handlelength=1, bbox_to_anchor=(1.05,1.05),
               loc="upper left")
    if title is not None:
        plt.title(title)
    if filename is not None:
        plt.savefig(filename)
    plt.show()
    
def hist1dcomp(data1, data2, data3, labels, xlabel, filename=None, 
               nbins=50, customXlim=None, customXlabels=None, title = None, log_scale = False, stacked3 = False, selLabel=None):
    """Plots 1d histogram from (up to) three separate lists of datasets
    
    data1 - list of datasets, each of which is plotted as a solid line
    data2 - list of datasets, each of which is plotted as a dashed line
    data3 - list of datasets, each of which is plotted as a dotted line
        (if data3 is empty, data2 is plotted with dotted lines)
    labels - list of labels of the datasets (same for data1,2,3)
    xlabel - x label of the histogram
    filename - if None, the plot is not saved, otherwise it is
    nbins - the number of bins, default: 50
    customXlim - if not set, the x axis contains all values in data
    customXlabels -  if not set, data1 is understood as an ALP dataset, 
        data2 as a Top dataset, and data3 as an AntiTop dataset
    title - if not given, the plot is not given a title
    log_scale - if true the y-axis is displayed in log scale
    stacked3 - if true data3 will be stacked
    selLabel - list of strings for selection, if None no text will be printed
    """
    n = len(data1)
    if (len(data1)!=len(labels)) or (len(data2)!=len(labels)):
        print("Different array lengths: "+str(len(data1))+", "
              +str(len(data2))+", "+str(len(data3))+", "+str(len(labels)))
    if customXlim == None:
        lmax = max(data1[0])
        lmin = min(data1[0])
        for i in range(0,n):
            lmax = max(lmax, max(data1[i]))
            lmin = min(lmin, min(data1[i]))
        for j in range(0,len(data2)):
            lmax = max(lmax, max(data2[j]))
            lmin = min(lmin, min(data2[j]))
        if not len(data3)==0:
            for i in range(0,len(data3)):
                lmax = max(lmax, max(data3[i]))
                lmin = min(lmin, min(data3[i]))
    else:
        lmin = customXlim[0]
        lmax = customXlim[1]
    binList = np.arange(lmin, lmax+(lmax-lmin)/nbins, (lmax-lmin)/nbins)
    maxheight = 0
    if len(data3) > 1:
        colours = coloursX(1,n)
    else:
        colours = coloursX(1,1)
    if stacked3:
        if not len(data3[i]) == 0:
            weights3 = []
            total_length = 0
            for i in range(len(data3)):
                total_length += len(data3[i])
            for i in range(len(data3)):
                weights3.append(len(data3[i])*[1/total_length])
            heights, _, _ = plt.hist(data3, histtype='step', 
                                    weights=weights3,
                                    color=coloursX(1,len(data3)), bins=binList,
                                    lw=1, ls='dotted', stacked=stacked3)
            # maxheight = max(max(heights), maxheight)
    else:
        for i in range(len(data3)):
            if not len(data3[i]) == 0:
                heights, _, _ = plt.hist(data3[i], histtype='step',
                                        weights=len(data3[i])*[1/len(data3[i])],
                                        color=coloursX(1,n)[i], bins=binList,
                                        lw=1, ls='dotted')
                maxheight = max(max(heights), maxheight)
    for i in range(n):
        if not len(data1[i]) == 0:
            heights, _, _ = plt.hist(data1[i], histtype='step', 
                                    weights=len(data1[i])*[1/len(data1[i])],
                                    color=coloursX(1,n)[i], bins=binList, 
                                    lw=1, ls='solid')
            maxheight = max(max(heights), maxheight)
    for i in range(len(data2)):
        if not len(data3)==0:
            linestyle = 'dashed'
        else:
            linestyle = 'dotted'
        if not len(data2[i]) == 0:
            heights, _, _ = plt.hist(data2[i], histtype='step',
                                    weights=len(data2[i])*[1/len(data2[i])],
                                    color=coloursX(1,n)[i], bins=binList,
                                    lw=1, ls=linestyle)
            maxheight = max(max(heights), maxheight)
    plt.xlabel(xlabel)
    plt.ylabel("number of events [a.u.]")
    plt.xlim([lmin,lmax])
    if not log_scale:
        plt.ylim(bottom=0)
        plt.gca().get_yaxis().set_major_formatter(matplotlib.ticker.
                                              FormatStrFormatter('%.2f'))
    else:
        plt.yscale("log")
    handles = [Line2D([],[],c=coloursX(1,n)[i],lw=3) for i in range(n)]
    if not len(data3)==0:
        handles += [Line2D([], [], c='k', lw=3, ls=style) 
                    for style in ['solid', 'dashed', 'dotted']]
    else:
        handles += [Line2D([], [], c='k', lw=3, ls=style) 
                    for style in ['solid', 'dotted']]
    if customXlabels == None:
        labelList = labels + ['ALP', 'Top', 'Anti-Top']
    else:
        labelList = labels + customXlabels
    plt.legend(handles, labelList, handlelength=1, bbox_to_anchor=(1.05,1.15),
               loc="upper left")
    # if selLabel is not None:
        # xmin, xmax, ymin, ymax = plt.axes()
        # plt.text(0.8*xmax,0.8*ymax, 'Selection:  ' + selLabel)
    if title is not None:
        plt.title(title)
    if filename is not None:
        plt.savefig(filename)
    plt.show()

def hist1dcomp2(data1, data2, data3, labels, xlabel, filename=None, 
               nbins=50, customXlim=None, customXlabels=None, title = None, 
               log_scale = False, stacked3 = False, selLabel=[], clip=False):
    """Plots 1d histogram from (up to) three separate lists of datasets
    
    data1 - list of datasets, each of which is plotted as a solid line
    data2 - list of datasets, each of which is plotted as a dashed line
    data3 - list of datasets, each of which is plotted as a dotted line
        (if data3 is empty, data2 is plotted with dotted lines)
    labels - list of labels of the datasets (same for data1,2,3)
    xlabel - x label of the histogram
    filename - if None, the plot is not saved, otherwise it is
    nbins - the number of bins, default: 50
    customXlim - if not set, the x axis contains all values in data
    customXlabels -  if not set, data1 is understood as an ALP dataset, 
        data2 as a Top dataset, and data3 as an AntiTop dataset
    title - if not given, the plot is not given a title
    log_scale - if true the y-axis is displayed in log scale
    stacked3,stacked2 - if true all dataset in data1/data2 will be stacked together
    selLabel - list of strings for selection, if None no text will be printed
    clip - option to plot the overflow of a cut off x-axis in the last bin, 
        using numpy clip function
    """
    n = len(data1)
    if (len(data1)!=len(labels)) or (len(data2)!=len(labels)):
        print("Different array lengths: "+str(len(data1))+", "
              +str(len(data2))+", "+str(len(data3))+", "+str(len(labels)))
    if customXlim == None:
        lmax = max(data1[0])
        lmin = min(data1[0])
        for i in range(0,n):
            lmax = max(lmax, max(data1[i]))
            lmin = min(lmin, min(data1[i]))
        for j in range(0,len(data2)):
            lmax = max(lmax, max(data2[j]))
            lmin = min(lmin, min(data2[j]))
        if not len(data3)==0:
            for i in range(0,len(data3)):
                lmax = max(lmax, max(data3[i]))
                lmin = min(lmin, min(data3[i]))
    else:
        lmin = customXlim[0]
        lmax = customXlim[1]
    binList = np.arange(lmin, lmax+(lmax-lmin)/nbins, (lmax-lmin)/nbins)
    maxheight = 0
    if len(data3) > 1:
        colours = coloursX(1,n)
    else:
        colours = coloursX(1,3)
    if stacked3:
        if not len(data3[i]) == 0:
            weights3 = []
            total_length = 0
            for i in range(len(data3)):
                total_length += len(data3[i])
            for i in range(len(data3)):
                weights3.append(len(data3[i])*[1/total_length])
            if clip:
                data3[i] = np.clip(data3[i],binList[0],binList[-1])
            heights, _, _ = plt.hist(data3, histtype='step', 
                                    weights=weights3,
                                    color=colours, bins=binList,
                                    lw=1, ls='solid', stacked=stacked3)
            # maxheight = max(max(heights), maxheight)
    else:
        for i in range(len(data3)):
            if clip:
                data3[i] = np.clip(data3[i],binList[0],binList[-1])
            if not len(data3[i]) == 0:
                heights, _, _ = plt.hist(data3[i], histtype='step',
                                        weights=len(data3[i])*[1/len(data3[i])],
                                        color=coloursX(1,n)[i], bins=binList,
                                        lw=1, ls='solid')
                maxheight = max(max(heights), maxheight)
    for i in range(n):
        if not len(data1[i]) == 0:
            if clip:
                data1[i] = np.clip(data1[i],binList[0],binList[-1])
            heights, _, _ = plt.hist(data1[i], histtype='step', 
                                    weights=len(data1[i])*[1/len(data1[i])],
                                    color=coloursX(1,n)[i], bins=binList, 
                                    lw=1, ls='solid')
            maxheight = max(max(heights), maxheight)
    for i in range(len(data2)):
        if not len(data3)==0:
            linestyle = 'dashed'
        else:
            linestyle = 'dotted'
        if not len(data2[i]) == 0:
            if clip:
                data2[i] = np.clip(data2[i],binList[0],binList[-1])
            heights, _, _ = plt.hist(data2[i], histtype='step',
                                    weights=len(data2[i])*[1/len(data2[i])],
                                    color=coloursX(1,len(data2))[i], bins=binList,
                                    lw=1, ls='solid')
            maxheight = max(max(heights), maxheight)
    plt.xlabel(xlabel)
    plt.ylabel("number of events [a.u.]")
    plt.xlim([lmin,lmax])
    if not log_scale:
        plt.ylim(bottom=0)
        plt.gca().get_yaxis().set_major_formatter(matplotlib.ticker.
                                              FormatStrFormatter('%.2f'))
    else:
        plt.yscale("log")
    handles = [Line2D([],[],c=coloursX(1,n)[i],lw=3) for i in range(n)]
    if not len(data3)==0:
        handles += [Line2D([], [], c=coloursX(1,len(data2))[i], lw=3, ls='solid') 
                    for i in range(len(data2))]
        if len(data3) > 1:
            handles += [Line2D([], [], c=coloursX(1,len(data2))[i], lw=3, ls='solid') 
                        for i in range(len(data3))]
        else:
            handles += [Line2D([], [], c=coloursX(1,3)[i], lw=3, ls='solid')]
    else:
        handles += [Line2D([], [], c=coloursX(1,len(data2))[i], lw=3, ls='solid') 
                    for i in range(len(data2))]
    if customXlabels == None:
        labelList = labels + ['ALP', 'Top', 'Anti-Top']
    else:
        labelList = labels + customXlabels
    if len(selLabel) != 0:
        labelList = labelList + ['Selections:'] + selLabel
        handles += [Line2D([],[],c='white',lw=0) for i in range(len(selLabel)+1)]
        # xmin, xmax, ymin, ymax = plt.axis()
        # plt.text(,0.9*ymax, selLabel, horizontalalignment='right',
        # verticalalignment='top')
    plt.legend(handles, labelList, handlelength=1, bbox_to_anchor=(1.05,1.15),
               loc="upper left")
    if title is not None:
        plt.title(title)
    if filename is not None:
        plt.savefig(filename)
    plt.show()

def hist1dcross(data1, data2, data3, crosssec1, crosssec2, crosssec3, N1, N2, N3, 
                intlumi, labels, xlabel, filename=None, nbins=50, customXlim=None, 
                customXlabels=None, title = None, log_scale = False, stacked2 = False, 
                stacked3 = False, selLabel=None, clip=False):
    """Plots 1d histogram from (up to) three separate lists of datasets
    
    data1,data2,data3 - list of datasets, each of which is plotted as a solid line
    crossec1,crossec2,crossec3 - cross section value for data1,data2,data3
               TODO - make use of the cross section variable implemented in Dataset
    intlumi - integrated luminosity
    labels - list of labels of the datasets (same for data1,2,3)
    xlabel - x label of the histogram
    filename - if None, the plot is not saved, otherwise it is
    nbins - the number of bins, default: 50
    customXlim - if not set, the x axis contains all values in data
    customXlabels -  if not set, data1 is understood as an ALP dataset, 
        data2 as a Top dataset, and data3 as an AntiTop dataset
    title - if not given, the plot is not given a title
    log_scale - if true the y-axis is displayed in log scale
    stacked3,stacked2 - if true all dataset in data1/data2 will be stacked together
    selLabel - list of strings for selection, if None no text will be printed 
    clip - option to plot the overflow of a cut off x-axis in the last bin, 
        using numpy clip function
    """

    n = len(data1)
    if (len(data1)!=len(labels)) or (len(data2)!=len(labels)):
        print("Different array lengths: "+str(len(data1))+", "
              +str(len(data2))+", "+str(len(data3))+", "+str(len(labels)))
    if customXlim == None:
        lmax = max(data1[0])
        lmin = min(data1[0])
        for i in range(0,n):
            lmax = max(lmax, max(data1[i]))
            lmin = min(lmin, min(data1[i]))
        for j in range(0,len(data2)):
            lmax = max(lmax, max(data2[j]))
            lmin = min(lmin, min(data2[j]))
        if not len(data3)==0:
            for i in range(0,len(data3)):
                lmax = max(lmax, max(data3[i]))
                lmin = min(lmin, min(data3[i]))
    else:
        lmin = customXlim[0]
        lmax = customXlim[1]
    binList = np.arange(lmin, lmax+(lmax-lmin)/nbins, (lmax-lmin)/nbins)
    maxheight = 0
    #for i in range(len(data3)):
    if len(data3) > 1:
        colours = coloursX(1,n)
    else:
        colours = coloursX(1,1)
    if stacked3:
            weights3 = []
            total_length = 0
            for i in range(len(data3)):
                total_length += len(data3[i])
            for i in range(len(data3)):
                if not len(data3[i]) == 0:
                    weights3.append(np.array(len(data3[i])*[1/N3[i]])*crosssec3[i]*intlumi)
                if clip:
                    data3[i] = np.clip(data3[i],binList[0],binList[-1])
            heights, _, _ = plt.hist(data3, histtype='step', 
                                    weights=weights3,
                                    color=coloursX(1,len(data3)), bins=binList,
                                    lw=1, ls='solid', log=log_scale, stacked=stacked3)
            # maxheight = max(max(heights), maxheight)
    else:
        for i in range(len(data3)):
            if not len(data3[i]) == 0:
                if clip:
                    data3[i] = np.clip(data3[i],binList[0],binList[-1])
                heights, _, _ = plt.hist(data3[i], histtype='step',
                                        weights=np.array(len(data3[i])*[1/N3[i]])*crosssec3[i]*intlumi,
                                        color=coloursX(1,n)[i], bins=binList,
                                        lw=1, ls='solid', log=log_scale)
                maxheight = max(max(heights), maxheight)
    if stacked2:
        weights2 = []
        total_length = 0
        for i in range(len(data2)):
            total_length += len(data2[i])
        for i in range(len(data2)):
            if not len(data2[i]) == 0:
                weights2.append(np.array(len(data2[i])*[1/N2[i]])*crosssec2[i]*intlumi)
            if clip:
                data2[i] = np.clip(data2[i],binList[0],binList[-1])
        heights, _, _ = plt.hist(data2, histtype='step', 
                                weights=weights2,
                                color=coloursX(1,len(data2)), bins=binList,
                                lw=1, ls='solid', log=log_scale, stacked=stacked2)
    else:
        for i in range(len(data2)):
            if not len(data2[i]) == 0:
                if clip:
                    data2[i] = np.clip(data2[i],binList[0],binList[-1])
                heights, _, _ = plt.hist(data2[i], histtype='step',
                                        weights=np.array(len(data2[i])*[1/N2[i]])*crosssec2[i]*intlumi,
                                        color=coloursX(1,len(data2))[i], bins=binList,
                                        lw=1, ls='solid', log=log_scale)
                maxheight = max(max(heights), maxheight)
    for i in range(n):
        if not len(data1[i]) == 0:
            if clip:
                data1[i] = np.clip(data1[i],binList[0],binList[-1])
            heights, _, _ = plt.hist(data1[i], histtype='step', 
                                    weights=np.array(len(data1[i])*[1/N1[i]])*crosssec1[i]*intlumi,
                                    color=coloursX(1,n)[i], bins=binList, 
                                    lw=1, ls='solid', log=log_scale)
            maxheight = max(max(heights), maxheight)
    plt.xlabel(xlabel)
    plt.ylabel("number of events [a.u.]")
    plt.xlim([lmin,lmax])
    if not log_scale:
        plt.ylim(bottom=0)
    if not log_scale:
        plt.gca().get_yaxis().set_major_formatter(matplotlib.ticker.
                                                  FormatStrFormatter('%.2f')) 
    handles = [Line2D([],[],c=coloursX(1,n)[i],lw=3) for i in range(n)]
    if not len(data3)==0:
        handles += [Line2D([], [], c='k', lw=3, ls=style) 
                    for style in ['solid', 'dashed', 'dotted']]
    else:
        handles += [Line2D([], [], c=coloursX(1,len(data2))[i], lw=3, ls='solid') 
                    for i in range(len(data2))]
    if customXlabels == None:
        labelList = labels + ['ALP', 'Top', 'Anti-Top']
    else:
        labelList = labels + customXlabels
    if len(selLabel) != 0:
        labelList = labelList + ['Selections:'] + selLabel
        handles += [Line2D([],[],c='white',lw=0) for i in range(len(selLabel)+1)]
    plt.legend(handles, labelList, handlelength=1, bbox_to_anchor=(1.05,1.15),
               loc="upper left")
    if title is not None:
        plt.title(title)
    if filename is not None:
        plt.savefig(filename)
    plt.show()
    
def scatter(datax, datay, labels, xlabel, ylabel, filename=None,
            customXlim=None, customYlim=None, title=None):
    """Plots a scatterlot from given x and y data
    
    datax - list of x-values
    datay - list of corresponding y-values
    labels - list of labels of the datasets
    xlabel - x label of the scatterplot
    ylabel - y label of the scatterplot
    filename - if None, the plot is not saved, otherwise it is
    customXlim - if not set, the x axis contains all values in data
    customYlim - if not set, the y axis contains all values in data
    title - if not given, the plot is not given a title"""
    n = len(datax)
    if (len(datax)!=len(datay)) or (len(datax)!=len(labels)):
        print("Different array lengths")
    for i in range(n):
        plt.scatter(datax[i], datay[i], s=0.1, color=coloursX(1,n)[i])
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    if customXlim is not None:
        plt.xlim(customXlim)
    if customYlim is not None:
        plt.ylim(customYlim)
    handles = [Line2D([], [], c=coloursX(1,n)[i], lw=3) for i in range(n)]
    plt.legend(handles, labels, handlelength=1, bbox_to_anchor=(1.05,1.05),
               loc="upper left")
    if title is not None:
        plt.title(title)
    if filename is not None:
        plt.savefig(filename)
    plt.show()
    
def hist1d_part(ax, data, labels, xlabel, nbins=50,
                customXlim=None, title=None):
    """Plots 1d histogram as a part of plotMatrix
    
    data - list of datasets, each of which is plotted as a line
    labels - list of labels of the datasets
    xlabel - x label of the histogram
    filename - if None, the plot is not saved, otherwise it is
    nbins - the number of bins, default: 50
    customXlim - if not set, the x axis contains all values in data
    title - if not given, the plot is not given a title"""
    n = len(data)
    if (len(data)!=len(labels)):
        print("Different array lengths")
    if customXlim == None:
        lmax = max(data[0])
        lmin = min(data[0])
        for date in data:
            if (len(date)>0):
                lmax = max(lmax, max(date))
                lmin = min(lmin, min(date))
    else:
        lmin = customXlim[0]
        lmax = customXlim[1]
    binList = np.arange(lmin*0.95, lmax*1.05, (lmax*1.05-lmin*0.95)/nbins)
    maxheight = 0
    for i in range(n):
        heights, _, _ = ax.hist(data[i], histtype='step', 
                                weights=len(data[i])*[1/len(data[i])],
                                color=coloursX(1,n)[i], bins=binList,
                                label=labels[i], lw=1)
        maxheight = max(max(heights), maxheight)
    ax.set_xlabel(xlabel)
    ax.set_ylabel("number of events [a.u.]")
    ax.set_xlim([lmin, lmax])
    ax.set_ylim(bottom=0)
    if title is not None:
        ax.title(title)

def scatter_part(ax, datax, datay, labels, xlabel, ylabel,
                 customXlim=None, customYlim=None, title=None):
    """Plots a scatterplot from given x and y data as a part of plotMatrix
    
    datax - list of x-values
    datay - list of corresponding y-values
    labels - list of labels of the datasets
    xlabel - x label of the scatterplot
    ylabel - y label of the scatterplot
    filename - if None, the plot is not saved, otherwise it is
    customXlim - if not set, the x axis contains all values in data
    customYlim - if not set, the y axis contains all values in data
    title - if not given, the plot is not given a title"""
    n = len(datax)
    if (len(datax)!=len(datay)) or (len(datax)!=len(labels)):
        print("Different array lengths")
    for i in range(n):
        ax.scatter(datax[i], datay[i], s=0.1, color=coloursX(1,n)[i])
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    if customXlim is not None:
        plt.xlim(customXlim)
    if customYlim is not None:
        plt.ylim(customYlim)
    if title is not None:
        plt.title(title)
    

def plotMatrix(data, labelKeys, labelDict, dataLabels, filename=None, title=None):
    """matrix of histograms and scatterplots comparing different datasets
    
    data - list of datasets to compare
    labelKeys - keys for the labelDict
    labelDict - dictionary containing the axis labels
    dataLabels - labels of the datasets
    filename - if None, the plot is not saved, otherwise it is
    title - if not given, the plot is not given a title"""
    n = len(data)
    fig, axs = plt.subplots(n,n,figsize=(n*5,n*5))
    for i in range(n):
        for j in range(n):
            if i<=j:
                if not i==j:
                    scatter_part(axs[i][j], data[i], data[j], dataLabels, 
                            labelDict[labelKeys[i]], labelDict[labelKeys[j]])
                else:
                    hist1d_part(axs[i][j], data[i], dataLabels,
                                labelDict[labelKeys[i]])
                axs[i][j].ticklabel_format(style='sci', axis='x',
                                           scilimits=(0,0), useMathText=True)
                axs[i][j].ticklabel_format(style='sci', axis='y',
                                           scilimits=(0,0), useMathText=True)
    handles = [Line2D([], [], c=coloursX(1, len(data[0]))[i], lw=3) 
               for i in range(len(data[0]))]
    plt.legend(handles, dataLabels, handlelength=1, bbox_to_anchor=(1,1),
               loc="center left")
    if title is not None:
        plt.title(title)
    if filename is not None:
        plt.savefig(filename)
    plt.show()
    
    
def scatter_w_c(datax, datay, dataz, datas, xlabel, ylabel, zlabel, log: bool = False,
             filename=None, customXlim=None, customYlim=None, title=None):
    """Plots a scatterplot with a colourbar from given x, y, and z data (+ point size data)
    
    datax - list of x-values
    datay - list of y-values
    dataz - list of corresponding z-values (shown in colour values of points)
    datas - list of corresponding s-values (shown in size of points)
    xlabel - x label of the scatterplot
    ylabel - y label of the scatterplot
    zlabel - z label of the scatterplot (colourbar label)
    log - colourbar logarithmic or linear (default: False = linear)
    filename - if None, the plot is not saved, otherwise it is
    customXlim - if not set, the x axis contains all values in data
    customYlim - if not set, the y axis contains all values in data
    title - if not given, the plot is not given a title"""
    if log and not dataz==len(dataz)*[0.0]:
        plt.scatter(datax, datay, c=dataz, s=datas, norm=matplotlib.colors.LogNorm())
    else:
        plt.scatter(datax, datay, c=dataz, s=datas, norm=matplotlib.colors.Normalize())
    cbar = plt.colorbar()
    cbar.set_label(zlabel)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xscale('log')
    plt.yscale('log')
    if title is not None:
        plt.title(title)
    if filename is not None:
        plt.savefig(filename)
    plt.show()
