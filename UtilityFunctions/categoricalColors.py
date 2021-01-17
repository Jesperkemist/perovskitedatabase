# =============================================================================
# Returns a list of 61 hex-colors for categorical ploting
# 
# By Jesper Jacobsson
# 2019 06
# =============================================================================

from operator import itemgetter

def categoricalColors(*args): 
    ''' Returns a list of 61 hex-colors for categorical ploting'''
    # colorpalets importred from matplotlib
    tab10 = ['#1f77b4','#ff7f0e','#2ca02c','#d62728','#9467bd','#8c564b','#e377c2','#7f7f7f','#bcbd22','#17becf']
    
    Set3 = ['#8dd3c7', '#ffffb3', '#bebada', '#fb8072', '#80b1d3', '#fdb462', '#b3de69', '#fccde5', '#d9d9d9', '#bc80bd', '#ccebc5', '#ffed6f']
    
    Dark2 = ['#1b9e77', '#d95f02', '#7570b3', '#e7298a', '#66a61e', '#e6ab02', '#a6761d', '#666666']
    
    Pastel1 = ['#fbb4ae', '#b3cde3', '#ccebc5', '#decbe4', '#fed9a6', '#ffffcc', '#e5d8bd', '#fddaec', '#f2f2f2'] 
    
    Paired = ['#a6cee3', '#1f78b4', '#b2df8a', '#33a02c', '#fb9a99', '#e31a1c', '#fdbf6f', '#ff7f00', '#cab2d6', '#6a3d9a', '#ffff99', '#b15928']
    
    Jesper = ['#ffd700', '#000080', '#FFA500', '#008080', '#6a5acd', '#b22222', '#ffe4e1', '#ff00ff', '#d2691e', '#000000', '#ccccff']
              
                
    cmap =  tab10 + Dark2 + Set3 + Pastel1 + Paired + Jesper
#    cmap = list(set(cmap))
    
    if args[0] == 'Dark':
        cmap =  tab10 + Dark2 + Paired + Jesper
        # Remove too light colors
        keep = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 19, 21, 22, 23, 24, 25, 26, 27, 29, 30, 31, 32, 33, 34, 35, 37, 38, 39]
        cmap = list(itemgetter(*keep)(cmap))

    return cmap





#%% Testplot
#import matplotlib.pyplot as plt
#
#for i in range(67):
#    plt.plot([0,1],[i,i],color = cmap[i], lw = 3)
#
#plt.show()  

#%%Get Cmap from matplotlib
#import matplotlib
#cmapObject = matplotlib.cm.get_cmap('Paired')
#c = []
#for i in range(cmapObject.N):
#    rgb = cmapObject(i)[:3]  #  return rgba, the first 3 give rgb
#    rgb_hex = matplotlib.colors.rgb2hex(rgb)
#    c.append(rgb_hex)
#    
#print(c) 