import scipy.io
import os
import scipy as sp
import numpy as np
import xml.etree.ElementTree
from centroid import mapping
from dfsio import readdfs

roiregion=['angular gyrus','anterior orbito-frontal gyrus','cingulate','cuneus','fusiforme gyrus','gyrus rectus','inferior occipital gyrus','inferior temporal gyrus','lateral orbito-frontal gyrus','lingual gyrus','middle frontal gyrus','middle occipital gyrus','middle orbito-frontal gyrus','middle temporal gyrus','parahippocampal gyrus','pars opercularis','pars orbitalis','pars triangularis','post-central gyrus','posterior orbito-frontal gyrus','pre-central gyrus','precuneus','subcallosal gyrus','superior frontal gyrus','superior occipital gyrus','superior parietal gyrus','supramarginal gyrus','temporal','temporal pole','transvers frontal gyrus','transverse temporal gyrus','Insula']
#intensity_file_anterior orbito-frontal gyrus_169_nCluster=1_BCI
right_hemisphere=np.array([226,168,184,446,330,164,442,328,172,444,130,424,166,326,342,142,146,144,222,170,
150,242,186,120,422,228,224,322,310,162,324,500])

left_hemisphere=np.array([227,169,185,447,331,165,443,329,173,445,131,425,167,327,343,143,147,145,223,171,
151,243,187,121,423,229,225,323,311,163,325,501])
#intensity_file_ttransverse temporal gyrus_325_nCluster=1_BCI
nClusters=np.array([3,1,3,2,2,2,3,3,2,2,2,3,1,4,1,2,1,3,2,1,4,2,1,2,2,2,2,3,1,2,1,2])
scan_type=['left','right']
p_dir='.'

def plot_figure(dfs_left,labels):
    from mayavi import mlab

    mlab.figure(size=(1024, 768), \
                bgcolor=(1, 1, 1), fgcolor=(0.5, 0.5, 0.5))
    mlab.triangular_mesh(dfs_left.vertices[:, 0], dfs_left.vertices[:, 1], dfs_left.vertices[:, 2], dfs_left.faces,
                         representation='surface',
                         opacity=1, scalars=np.float64(labels.transpose()))
    mlab.gcf().scene.parallel_projection = True
    mlab.view(azimuth=0, elevation=90)
    mlab.colorbar(orientation='vertical')
    mlab.show()

def fun(data):
    z1 = (data['labs_all'])
    temp = []
    for var in range(z1.shape[1]):
        if z1[0][var] not in temp:
            temp.append(z1[0][var])
    print(temp)


for hemi in range(0,2):
    dfs_left = readdfs(os.path.join('/big_disk/ajoshi/coding_ground.donotdelete/hybridatlas/src', '100307.BCI2reduce3.very_smooth.' + scan_type[hemi] + '.dfs'))
    labels=np.zeros([dfs_left.vertices.shape[0]])
    for n in range(nClusters.shape[0]):
        roilist=left_hemisphere[n]
        if hemi ==1:
            roilist=right_hemisphere[n]
        #print n, roiregion[n], roilist
        msk_small_region = np.in1d(dfs_left.labels, roilist)
        data=scipy.io.loadmat(os.path.join(p_dir,'intensity_file_'+roiregion[n]+'_'+str(roilist)+'_nCluster='+str(nClusters[n])+'_BCI.mat'))
        labels[msk_small_region] = roilist*10 + data['labs_all'].flatten()[msk_small_region]
        #plot_figure(dfs_left,labels)
        #fun(data)
    if hemi ==0:
        sp.savez(
        'very_smooth_data_'+scan_type[hemi],
        labels=labels, vertices=dfs_left.vertices,faces=dfs_left.faces,vColor=np.zeros([dfs_left.vertices.shape[0]]),roilists=sorted(left_hemisphere))
    else :
        sp.savez(
            'very_smooth_data_' + scan_type[hemi],
            labels=labels, vertices=dfs_left.vertices, faces=dfs_left.faces,
            vColor=np.zeros([dfs_left.vertices.shape[0]]), roilists=sorted(right_hemisphere))

