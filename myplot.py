import matplotlib
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.lines import Line2D
import numpy as np

plt.rcParams.update({'font.size': 14})
plt.rcParams['figure.dpi']= 300
plt.rc('text.latex', preamble=r'\usepackage{amsmath}')

def colour(r: int, g: int, b: int, a: int):
    return (r/256, g/256, b/256, a)

def colours(alpha: int):
    darkBlue = colour(0, 114, 178, alpha)
    lightBlue = colour(86, 180, 233, alpha)
    green = colour(0, 158, 115, alpha)
    yellow = colour(240, 228, 66, alpha)
    orange = colour(230, 159, 0, alpha)
    red = colour(215, 94, 0, alpha)
    pink = colour(204, 121, 167, alpha)
    return [darkBlue, lightBlue, green, yellow, orange, red, pink]
    
def coloursX(alpha, X):
    if X>7:
        return colours(alpha) + coloursX(alpha/2, X-7)
    if X==7:
        return colours(alpha)
    if X==6:
        return colours(alpha)[0:6]
    if X==5:
        return colours(alpha)[0:4]+[colours(alpha)[5]]
    if X==4:
        return [colours(alpha)[1], colours(alpha)[2], colours(alpha)[3],
                colours(alpha)[5]]
    if X==3:
        return [colours(alpha)[1], colours(alpha)[2], colours(alpha)[5]]
    if X==2:
        return [colours(alpha)[0], colours(alpha)[5]]
    if X==1:
        return [(0,0,0,alpha)]
    return []

def hist1d(data, labels, xlabel, filename=None,
           nbins=50, customXlim=None, title=None):
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
        heights, bins, patches = plt.hist(data[i], histtype='step', 
                                weights=len(data[i])*[1/len(data[i])],
                                color=coloursX(1,n)[i], bins=binList,
                                label=labels[i], lw=1)
        maxheight = max(max(heights), maxheight)
    plt.xlabel(xlabel)
    plt.ylabel("number of events [a.u.]")
    plt.xlim([lmin, lmax])
    plt.ylim(bottom=0)
    plt.gca().get_yaxis().set_major_formatter(matplotlib.ticker.
                                              FormatStrFormatter('%.2f'))
    handles = [Line2D([], [], c=coloursX(1,n)[i], lw=3) for i in range(n)]
    plt.legend(handles, labels, handlelength=1, bbox_to_anchor=(1.05,1.05),
               loc="upper left")
    if title is not None:
        plt.title(title)
    if filename is not None:
        plt.savefig(filename)
    plt.show()
    
def hist1dcomp(data1, data2, data3, labels, xlabel, filename=None, 
               nbins=50, customXlim=None, customXlabels=None, title = None):
    n = len(data1)
    if (len(data1)!=len(labels)) or (len(data2)!=len(labels)):
        print("Different array lengths: "+str(len(data1))+", "
              +str(len(data2))+", "+str(len(data3))+", "+str(len(labels)))
    if customXlim == None:
        lmax = max(data1[0])
        lmin = min(data1[0])
        for i in range(n):
            lmax = max(lmax, max(data1[i]))
            lmin = min(lmin, min(data1[i]))
            lmax = max(lmax, max(data2[i]))
            lmin = min(lmin, min(data2[i]))
        if not len(data3)==0:
            for i in range(len(data3)):
                lmax = max(lmax, max(data3[i]))
                lmin = min(lmin, min(data3[i]))
    else:
        lmin = customXlim[0]
        lmax = customXlim[1]
    binList = np.arange(lmin, lmax, (lmax-lmin)/nbins)
    maxheight = 0
    for i in range(n):
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
        heights, _, _ = plt.hist(data2[i], histtype='step',
                                 weights=len(data2[i])*[1/len(data2[i])],
                                 color=coloursX(1,n)[i], bins=binList,
                                 lw=1, ls=linestyle)
        maxheight = max(max(heights), maxheight)
    for i in range(len(data3)):
        if len(data3) > 1:
            colours = coloursX(1,n)
        else:
            colours = coloursX(1,1)
        heights, _, _ = plt.hist(data3[i], histtype='step', 
                                 weights=len(data3[i])*[1/len(data3[i])],
                                 color=colours[i], bins=binList,
                                 lw=1, ls='dotted')
        maxheight = max(max(heights), maxheight)
    plt.xlabel(xlabel)
    plt.ylabel("number of events [a.u.]")
    plt.xlim([lmin,lmax])
    plt.ylim(bottom=0)
    plt.gca().get_yaxis().set_major_formatter(matplotlib.ticker.
                                              FormatStrFormatter('%.2f')) 
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
    if title is not None:
        plt.title(title)
    if filename is not None:
        plt.savefig(filename)
    plt.show()
    
def scatter(datax, datay, labels, xlabel, ylabel, filename=None,
            customXlim=None, customYlim=None, title=None):
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
    
    
def scatter_w_c(datax, datay, dataz, xlabel, ylabel, log: bool = False,
             filename=None, customXlim=None, customYlim=None, title=None):
    if log:
        plt.scatter(datax, datay, facecolors='none', edgecolors='k')
        if not dataz==len(dataz)*[0.0]:
            plt.scatter(datax, datay, c=dataz, norm=matplotlib.colors.LogNorm())
    else:
        plt.scatter(datax, datay, c=dataz, norm=matplotlib.colors.Normalize())
    plt.colorbar()
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xscale('log')
    plt.yscale('log')
    if title is not None:
        plt.title(title)
    if filename is not None:
        plt.savefig(filename)
    plt.show()