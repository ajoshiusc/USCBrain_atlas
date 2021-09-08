from fmri_parcellation import parcellate_region
import os
import scipy as sp
import numpy as np
from tqdm import tqdm

roiregion=['angular gyrus','anterior orbito-frontal gyrus','cingulate','cuneus','fusiforme gyrus','gyrus rectus','inferior occipital gyrus','inferior temporal gyrus','lateral orbito-frontal gyrus','lingual gyrus','middle frontal gyrus','middle occipital gyrus','middle orbito-frontal gyrus','middle temporal gyrus','parahippocampal gyrus','pars opercularis','pars orbitalis','pars triangularis','post-central gyrus','posterior orbito-frontal gyrus','pre-central gyrus','precuneus','subcallosal gyrus','superior frontal gyrus','superior occipital gyrus','superior parietal gyrus','supramarginal gyrus','temporal','temporal pole','transvers frontal gyrus','transverse temporal gyrus','Insula']
#intensity_file_anterior orbito-frontal gyrus_169_nCluster=1_BCI
right_hemisphere=np.array([226,168,184,446,330,164,442,328,172,444,130,424,166,326,342,142,146,144,222,170,
150,242,186,120,422,228,224,322,310,162,324,500])

left_hemisphere=np.array([227,169,185,447,331,165,443,329,173,445,131,425,167,327,343,143,147,145,223,171,
151,243,187,121,423,229,225,323,311,163,325,501])
#intensity_file_ttransverse temporal gyrus_325_nCluster=1_BCI
nClusters=np.array([3,1,3,2,2,2,3,3,2,2,2,3,1,4,1,2,1,3,2,1,4,2,1,2,2,2,2,3,1,2,1,2])
scan_type=['left','right']
p_dir='/big_disk/ajoshi/cortical_parcellation'



#roilist =  np.array([[443],[442]])
#roiregion=['inferior occipital gyrus','motor','temporal','precuneus','semato','visual']
#nClusters=np.array([3])

p_dir = '/data_disk/HCP_data/data'
lst = os.listdir(p_dir) #{'100307'}

sdir=['_LR','_RL']
scan_type=['left','right']
session_type=[1,2]
fadd_1='.rfMRI_REST'
fadd_2='.reduce3.ftdata.NLM_11N_hvar_25.mat'
# %% Across session study
for n in range(nClusters.shape[0]):
    roilist = [left_hemisphere[n],right_hemisphere[n]]
    for i in range(0,2):
        R_all = []

        labs_all_1 = []
        vert_all_1 = []
        faces_all_1 = []
        all_centroid = np.array([])
        count1 = 0
        count_break = 0
        session = []
        centroid = []
        for sub in tqdm(lst):
            count_break += 1
            print(count_break)
            if os.path.isfile(os.path.join(p_dir, sub, sub + fadd_1 + str(session_type[0]) + sdir[1] + fadd_2)):
                # (46,28,29) motor 243 is precuneus
                labs1, correlation_within_precuneus_vector, correlation_with_rest_vector, mask, centroid = parcellate_region(
                    roilist[i], sub, nClusters[n], sdir[1], scan_type[i],
                    1, session_type[0], 0, 0)
                count1 += 1
                if count1 == 1:
                    labs_all_1 = np.array(labs1.labels)
                    vert_all_1 = np.array(labs1.vertices)
                    faces_all_1 = np.array(labs1.faces)
                    correlation_within_precuneus = np.array(correlation_within_precuneus_vector)
                    correlation_with_rest = np.array(correlation_with_rest_vector)
                    all_centroid = np.array(centroid)
                else:
                    labs_all_1 = np.vstack([labs_all_1, labs1.labels])
                    vert_all_1 = np.array([labs1.vertices])
                    faces_all_1 = np.array([labs1.faces])
                    correlation_within_precuneus = np.vstack(
                        [correlation_within_precuneus, correlation_within_precuneus_vector])
                    correlation_with_rest = np.vstack([correlation_with_rest, correlation_with_rest_vector])
                    all_centroid = np.vstack([all_centroid, centroid])

        data_file = 'data_file'
        sp.savez(data_file + roiregion[n] +str(i) +'BCI_overall.npz', correlation_within_precuneus=correlation_within_precuneus,
                 correlation_with_rest=correlation_with_rest, labels=labs_all_1, vertices=labs1.vertices,
                 faces=labs1.faces, mask=mask, centroid=all_centroid)

