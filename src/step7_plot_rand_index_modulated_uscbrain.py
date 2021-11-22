import numpy as np
import os
from copy import deepcopy, copy
from dfsio import readdfs
from statsmodels.stats.weightstats import CompareMeans as cms
from surfproc import patch_color_attrib, patch_color_labels, view_patch, view_patch_vtk
from fmri_methods_sipi import reduce3_to_bci_lh, reduce3_to_bci_rh


roiregion = ['angular gyrus', 'anterior orbito-frontal gyrus', 'cingulate', 'cuneus', 'fusiforme gyrus', 'gyrus rectus', 'inferior occipital gyrus', 'inferior temporal gyrus', 'lateral orbito-frontal gyrus', 'lingual gyrus',
             'middle frontal gyrus', 'middle occipital gyrus', 'middle orbito-frontal gyrus', 'middle temporal gyrus', 'parahippocampal gyrus', 'pars opercularis', 'pars orbitalis', 'pars triangularis', 'post-central gyrus',
             'posterior orbito-frontal gyrus', 'pre-central gyrus', 'precuneus', 'subcallosal gyrus', 'superior frontal gyrus', 'superior occipital gyrus', 'superior parietal gyrus', 'supramarginal gyrus', 'superior temporal gyrus',
             'temporal pole', 'transvers frontal gyrus', 'transverse temporal gyrus', 'Insula']
right_hemisphere = np.array([226, 168, 184, 446, 330, 164, 442, 328, 172, 444, 130, 424, 166, 326, 342, 142, 146, 144, 222, 170,
                             150, 242, 186, 120, 422, 228, 224, 322, 310, 162, 324, 500])

left_hemisphere = np.array([227, 169, 185, 447, 331, 165, 443, 329, 173, 445, 131, 425, 167, 327, 343, 143, 147, 145, 223, 171,
                            151, 243, 187, 121, 423, 229, 225, 323, 311, 163, 325, 501])
# 143,
nClusters = np.array([3, 1, 3, 2, 2, 2, 3, 3, 2, 2, 2, 3, 1,
                     4, 1, 2, 1, 3, 2, 1, 4, 2, 1, 2, 2, 2, 2, 3, 1, 2, 1, 2])

for hemi in ['left', 'right']:

    direct = readdfs(os.path.join('/big_disk/ajoshi/coding_ground.donotdelete/hybridatlas/src/',
                                  '100307.BCI2reduce3.very_smooth.'+hemi+'.dfs'))
    sessions = readdfs(os.path.join('/big_disk/ajoshi/coding_ground.donotdelete/hybridatlas/src/',
                                  '100307.BCI2reduce3.very_smooth.'+hemi+'.dfs'))

    zscore = readdfs(os.path.join('/big_disk/ajoshi/coding_ground.donotdelete/hybridatlas/src/',
                                  '100307.BCI2reduce3.very_smooth.'+hemi+'.dfs'))
    zscore = readdfs('/data_disk/HCP_data/reference.old/100307.aparc.a2009s.32k_fs.reduce3.very_smooth.'+hemi+'.dfs')                              


    direct.attributes = np.ones(direct.vertices.shape[0])
    sessions.attributes = np.ones(sessions.vertices.shape[0])
    zscore.attributes = np.zeros(sessions.vertices.shape[0])

    rand_indices = np.load('rand_index'+hemi+'.npz',
                           allow_pickle=True)['rand_index']

    for i, roi in enumerate(locals()[(hemi+'_hemisphere')]):

        msk_small_region = np.in1d(direct.labels, roi)
        if nClusters[i] == 1:
            direct.attributes[msk_small_region] = 1.0
            sessions.attributes[msk_small_region] = 1.0
        else:        
            direct.attributes[msk_small_region] = np.mean(rand_indices[2*i])
            sessions.attributes[msk_small_region] = np.mean(rand_indices[2*i+1])
        

        # z-score computation
        sd1 = np.std(rand_indices[2*i])
        sd2 = np.std(rand_indices[2*i+1])
        #pooledSE = np.sqrt(sd1**2/len(rand_indices[2*i]) + sd2**2/len(rand_indices[2*i+1]))
        pooledSD = np.sqrt((sd1**2*(len(rand_indices[2*i])-1) + sd2**2*(len(rand_indices[2*i+1])-1))/(len(rand_indices)-2))

        zscore.attributes[msk_small_region] = (np.mean(rand_indices[2*i+1] - np.mean(rand_indices[2*i])))/(pooledSD+1e-6)
        #cms(100,100).ztest_ind(np.array(rand_indices[2*i]),np.array(rand_indices[2*i+1]))
        #

    if hemi == 'left':
        att = reduce3_to_bci_lh(direct.attributes)
        direct = readdfs('/ImagePTE1/ajoshi/code_farm/svreg/BCI-DNI_brain_atlas/BCI-DNI_brain.left.mid.cortex.dfs')
        direct.attributes = att

        att = reduce3_to_bci_lh(sessions.attributes)
        sessions = readdfs('/ImagePTE1/ajoshi/code_farm/svreg/BCI-DNI_brain_atlas/BCI-DNI_brain.left.mid.cortex.dfs')
        sessions.attributes = att

        att = reduce3_to_bci_lh(zscore.attributes)
        zscore = readdfs('/ImagePTE1/ajoshi/code_farm/svreg/BCI-DNI_brain_atlas/BCI-DNI_brain.left.mid.cortex.dfs')
        zscore.attributes = att


    else:
        att = reduce3_to_bci_rh(direct.attributes)
        direct = readdfs('/ImagePTE1/ajoshi/code_farm/svreg/BCI-DNI_brain_atlas/BCI-DNI_brain.right.mid.cortex.dfs')
        direct.attributes = att

        att = reduce3_to_bci_rh(sessions.attributes)
        sessions = readdfs('/ImagePTE1/ajoshi/code_farm/svreg/BCI-DNI_brain_atlas/BCI-DNI_brain.right.mid.cortex.dfs')
        sessions.attributes = att

        att = reduce3_to_bci_rh(zscore.attributes)
        zscore = readdfs('/ImagePTE1/ajoshi/code_farm/svreg/BCI-DNI_brain_atlas/BCI-DNI_brain.right.mid.cortex.dfs')
        zscore.attributes = att


    patch_color_attrib(direct, cmap='hot', clim=[0, 1])
    patch_color_attrib(sessions, cmap='hot', clim=[0, 1])
    patch_color_attrib(zscore, cmap='hot', clim=[0, 1])

    view_patch_vtk(direct, azimuth=-100,  elevation=180, roll=-90,
                   outfile=hemi+'_rand_index_direct_mapping_1.png')
    view_patch_vtk(direct, azimuth=100,  elevation=180, roll=90,
                   outfile=hemi+'_rand_index_direct_mapping_2.png')

    view_patch_vtk(sessions, azimuth=-100,  elevation=180, roll=-
                   90, outfile=hemi+'_rand_index_sessions_1.png')
    view_patch_vtk(sessions, azimuth=100,  elevation=180, roll=90,
                   outfile=hemi+'_rand_index_sessions_2.png')

    view_patch_vtk(zscore, azimuth=-100,  elevation=180, roll=-
                   90, outfile=hemi+'_rand_index_zscore_1.png')
    view_patch_vtk(zscore, azimuth=100,  elevation=180, roll=90,
                   outfile=hemi+'_rand_index_zscore_2.png')

