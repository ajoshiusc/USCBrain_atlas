import numpy as np
import os

from dfsio import readdfs
from surfproc import patch_color_labels, view_patch
roiregion=['angular gyrus','anterior orbito-frontal gyrus','cingulate','cuneus','fusiforme gyrus','gyrus rectus','inferior occipital gyrus','inferior temporal gyrus','lateral orbito-frontal gyrus','lingual gyrus',
           'middle frontal gyrus','middle occipital gyrus','middle orbito-frontal gyrus','middle temporal gyrus','parahippocampal gyrus','pars opercularis','pars orbitalis','pars triangularis','post-central gyrus',
           'posterior orbito-frontal gyrus','pre-central gyrus','precuneus','subcallosal gyrus','superior frontal gyrus','superior occipital gyrus','superior parietal gyrus','supramarginal gyrus','superior temporal gyrus',
           'temporal pole','transvers frontal gyrus','transverse temporal gyrus','Insula']
right_hemisphere=np.array([226,168,184,446,330,164,442,328,172,444,130,424,166,326,342,142,146,144,222,170,
150,242,186,120,422,228,224,322,310,162,324,500])

left_hemisphere =np.array([227,169,185,447,331,165,443,329,173,445,131,425,167,327,343,143,147,145,223,171,
151,243,187,121,423,229,225,323,311,163,325,501])
#143,
nClusters=np.array([3,1,3,2,2,2,3,3,2,2,2,3,1,4,1,2,1,3,2,1,4,2,1,2,2,2,2,3,1,2,1,2])

def plot_histogram(nsub,temp,lst):
    import matplotlib.pyplot as plt
    import pandas as pd
    Color = ['r', 'g', 'b', 'y', 'k', 'c', 'm', '#A78F1E', '#F78F1E', '#BE3224', 'w', 'r', 'g', 'b', 'y', 'k', 'c', 'm', '#A78F1E',
             '#F78F1E', '#BE3224', 'w', 'w']
    Color = np.tile(Color, nsub)
    cmap = plt.get_cmap('jet',268)
    cmap.set_under('gray')
    cmaplist = [cmap(i) for i in range(cmap.N)]
    cnt=0
    cmaplist[0]=(0.5,0.5,0.5,1.0)
    print(temp.__len__())
    for i in range(0,len(temp)/4):
        cmaplist[cnt] = cmap(i)
        cmaplist[cnt+1] = cmap(i)
        cmaplist[cnt+2] = cmap(i)
        cmaplist[cnt+3] = cmap(i)
        cnt+=4
        #print cnt , i
    cmap=cmap.from_list('Custom cmap',cmaplist,cmap.N)
    temp = pd.Series.from_array(temp)
    plt.figure(figsize=(12, 8))
    #ax = temp.plot(kind='bar', stacked=True, rot=0, color=cmaplist)
    ax = temp.plot(kind='bar', stacked=True, rot=0, color=Color)
    ax.set_title("VALIDATION PLOT", fontsize=53, fontweight='bold')
    plt.subplots_adjust(left=0.06, right=0.96, top=0.90, bottom=0.09)
    ax.set_xlabel("SUBJECT "+str(nsub)+"( LEFT HEMISPHERE FOLLOWED BY RIGHT HEMISPHERE )", fontsize=30, fontweight='bold')
    ax.set_ylabel("RAND INDEX", fontsize=20, fontweight='bold')
    ax.set_ylim(0, 1.5)
    import matplotlib.patches as mpatches

    NA = mpatches.Patch(color='r', label='Direct Mapping to Session 1')
    EU = mpatches.Patch(color='g', label='Direct Mapping to Session 2')
    AP = mpatches.Patch(color='b', label='Direct Mapping to Session 3')
    SA = mpatches.Patch(color='y', label='Direct Mapping to Session 4')
    NA1 = mpatches.Patch(color='k', label='Session 1 to Session 2')
    EU1 = mpatches.Patch(color='c', label='Session 1 to Session 3')
    AP1 = mpatches.Patch(color='m', label='Session 1 to Session 4')
    SA1 = mpatches.Patch(color='#A78F1E', label='Session 2 to Session 3')
    SA2 = mpatches.Patch(color='#F78F1E', label='Session 2 to Session 4')
    SA3 = mpatches.Patch(color='#BE3224', label='Session 3 to Session 4')
    roiregion = ['angular gyrus', 'anterior orbito-frontal gyrus', 'cingulate', 'cuneus', 'fusiforme gyrus',
                 'gyrus rectus', 'inferior occipital gyrus', 'inferior temporal gyrus', 'lateral orbito-frontal gyrus',
                 'lingual gyrus', 'middle frontal gyrus', 'middle occipital gyrus', 'middle orbito-frontal gyrus',
                 'middle temporal gyrus', 'parahippocampal gyrus', 'pars opercularis', 'pars orbitalis',
                 'pars triangularis', 'post-central gyrus', 'posterior orbito-frontal gyrus', 'pre-central gyrus',
                 'precuneus', 'subcallosal gyrus', 'superior frontal gyrus', 'superior occipital gyrus',
                 'superior parietal gyrus', 'supramarginal gyrus', 'temporal', 'temporal pole',
                 'transvers frontal gyrus', 'transverse temporal gyrus', 'Insula']
    cmap = plt.get_cmap('jet',70)
    cmap.set_under('gray')
    cmaplist = [cmap(i) for i in range(cmap.N)]
    cmaplist[0]=(0.0,0.0,0.0,1.0)
    cmap=cmap.from_list('Custom cmap',cmaplist,cmap.N)
    cnt=0
    for n in range(roiregion.__len__()):
        handle=[mpatches.Patch(color=cmaplist[n],label=roiregion[n])]
        if cnt == 0:
            handles = handle
        else :
            handles += handle
        cnt+=1
    #plt.legend(handles=handles, loc=9,ncol=4)
    plt.legend(handles=[NA,EU,AP,SA,SA1,SA2,SA3,NA1,EU1,AP1],loc=2,ncol=2)
    raw_data = {'first_name': lst,
                'pre_score': [4, 24, 31, 2,1,1,1,1,1,1],
                'mid_score': [25, 94, 57, 62,1,1,1,1,1,1],
                'post_score': [5, 43, 23, 23,1,1,1,1,1,1]}
    df = pd.DataFrame(raw_data, columns=['first_name', 'pre_score', 'mid_score', 'post_score'])

    # manually plotted
    ax.set_xticks([10, 32, 55.5, 79,102,125,148,171,194,217])

    ax.set_xticklabels(df['first_name'])
    plt.show()

def plot_hist_each_subject(nsub,temp):
    import matplotlib.pyplot as plt
    labels = ["D-to-S1", "D-to-S2", "S1-to-S2", ""]
    labels = np.tile(labels, nsub * 2)
    import pandas as pd
    temp = pd.Series.from_array(temp)
    ax = temp.plot(kind='bar')
    rects = ax.patches
    plt.figure(figsize=(12, 8))
    ax = temp.plot(kind='bar', stacked=True)
    ax.set_title("VALIDATION PLOT", fontsize=53, fontweight='bold')
    plt.subplots_adjust(left=0.06, right=0.96, top=0.90, bottom=0.09)
    ax.set_xlabel("SUBJECT_151526 ( LEFT HEMISPHERE FOLLOWED BY RIGHT HEMISPHERE )", fontsize=30, fontweight='bold')
    ax.set_ylabel("RAND INDEX", fontsize=20, fontweight='bold')

    for rect, label in zip(rects, labels):
        height = rect.get_height()
        # if height > 0:
        ax.text(rect.get_x() + rect.get_width() / 2, 1.007 * height, label, ha='center', va='bottom')
        prev = rect.get_x() + rect.get_width() / 2
    font = {'family': 'serif',
            'color': 'green',
            'weight': 'normal',
            'size': 11,
            }
    labels = "D-to-Si= Direct_Mapping_"
    plt.text(prev - .47, 0.96, labels, fontdict=font)
    labels = "               _to_ith_Session"
    plt.text(prev - .50, 0.93, labels, fontdict=font)
    labels = "Si-to-sj= ith_Session_to_"
    plt.text(prev - .50, 0.88, labels, fontdict=font)
    labels = "                  _jth_Session"
    plt.text(prev - .50, 0.85, labels, fontdict=font)
    plt.show()

def plot_fmri_subject(lst):
    sdir=['_RL','_LR']
    scan_type=['left','right']
    session_type=[1,2]
    data_file = 'validation'
    class sc:
        pass
    for sub in lst:
        for hemi in range(0,2):
            left=np.load(data_file + str(sub) + '_' + scan_type[hemi]  + sdir[0] + '_' + str(session_type[0]) + '.npz')
            sc.labels = left['labels']
            sc.vertices = left['vertices']
            sc.faces = left['faces']
            sc.vColor = np.zeros([sc.vertices.shape[0]])
            sc = patch_color_labels(sc, cmap='Paired', shuffle=True)
            view_patch(sc, show=1, colormap='Paired', colorbar=0)

def box_plot(temp,temp1,map_roilists,fig_name,scan_type):
    ## numpy is used for creating fake data
    import numpy as np
    import matplotlib as mpl

    ## agg backend is used to create plot as a .png file
    #mpl.use('agg')

    import matplotlib.pyplot as plt

    ## combine these different collections into a list
    data_to_plot=[]
    cnt=0
    for i in range(temp.__len__()):
        data_to_plot.append(temp[i])
        data_to_plot.append(temp1[i])
    # Create a figure instance
    save_dir = '.'

    import scipy as sp
    sp.savez(os.path.join(save_dir, 'rand_index'+ scan_type + '.npz'),rand_index=data_to_plot,roilists=list(map_roilists.values()))
    
    fig = plt.figure(figsize=(20, 10))

    # Create an axes instance
    ax = fig.add_subplot(111)

    # Create the boxplot
    bp = ax.boxplot(data_to_plot[:32], patch_artist=True, showmeans=True)

    ax.set_title('VALIDATION PLOT ' + scan_type +' HEMISPHERE set 1', fontsize=53, fontweight='bold')
    plt.subplots_adjust(left=0.06, right=0.96, top=0.90, bottom=0.09)
    ax.set_xlabel("nSubjects "+str(fig_name)+"( Direct_to_session followed by session_to_session )", fontsize=30, fontweight='bold')
    ax.set_ylabel("RAND INDEX", fontsize=20, fontweight='bold')
    ax.set_ylim(0, 1.3)
    #colors = ['cyan','cyan', 'lightblue','lightblue', 'lightgreen','lightgreen', 'tan','tan', 'pink','pink','#7570b3','#7570b3', '#F78F1E','#F78F1E', '#BE3224','#BE3224',
             #'#F78F1E','#F78F1E', '#BE3224','#BE3224','#A78F1E','#A78F1E','m','m' ]
    Colors = ['cyan','#F78F1E', 'lightblue','y', 'lightgreen','#F78F1E', 'tan','#AEF2F4', 'pink', '#A78F1E', '#7570b3',  'm', 'k','#E78F1E','#BEF2F4','blue']
    Colors=np.tile(Colors,2)
    colors=[0 for i in range(2*Colors.__len__())]
    cnt=0
    for c in range(Colors.__len__()):
        colors[cnt]=Colors[c]
        colors[cnt+1]=Colors[c]
        cnt+=2
    colors = np.tile(colors, 6)
    for patch, color in zip(bp['boxes'], colors):
        patch.set_facecolor(color)
    import matplotlib.patches as mpatches
    cnt=0
    for roilist in map_roilists.keys():
        if cnt == 0:
            handles = [mpatches.Patch(color=Colors[cnt], label=map_roilists[roilist])]
            # handles += [mpatches.Patch(color=colors[cnt], label= map_roilists[roilist])]
        else:
            handles += [mpatches.Patch(color=Colors[cnt], label=map_roilists[roilist])]
            # handles += [mpatches.Patch(color=colors[cnt], label= map_roilists[roilist])]
        cnt += 1


    ## change color and linewidth of the whiskers
    for whisker in bp['whiskers']:
        whisker.set(color='#7570b3', linewidth=2)

    ## change color and linewidth of the caps
    for cap in bp['caps']:
        cap.set(color='#7570b3', linewidth=2)

    ## change color and linewidth of the medians
    for median in bp['medians']:
        median.set(color='green', linewidth=2)

    ## change the style of fliers and their fill
    for flier in bp['fliers']:
        flier.set(marker='o', color='#e7298a', alpha=0.5)

    # Save the figure
    '''plt.figtext(0.80, 0.08, ' superior frontal gyrus', color='cyan', weight='roman',
                size='x-small')


    plt.figtext(0.80, 0.045, 'pre-central gyrus',
                color='lightblue', weight='roman', size='x-small')
    plt.figtext(0.80, 0.015, 'angular gyrus', color='lightgreen', backgroundcolor='silver',
                weight='roman', size='medium')
    plt.figtext(0.815, 0.013, 'superior parietal gyrus', color='tan', weight='roman',
                size='x-small')
    plt.figtext(0.815, 0.010, 'pre-cuneus', color='pink', weight='roman',
                size='x-small')
    plt.figtext(0.815, 0.010, 'Insula', color='#7570b3', weight='roman',
                size='x-small')'''
    #plt.legend(handles=[NA, NA1,EU,EU1, AP,AP1, SA,SA1,AA, AA1, AU1,AU,AU2,AU3], loc=2, ncol=4)
    plt.legend(handles=handles[:16], loc=2, ncol=5)
    plt.show()
    fig.savefig('fig'+str(fig_name)+'_1.png', bbox_inches='tight')
    plt.close()


    fig = plt.figure(figsize=(20, 10))

    # Create an axes instance
    ax = fig.add_subplot(111)

    # Create the boxplot
    bp = ax.boxplot(data_to_plot[32:], patch_artist=True, showmeans=True)

    ax.set_title('VALIDATION PLOT ' + scan_type +' HEMISPHERE set 2', fontsize=53, fontweight='bold')
    plt.subplots_adjust(left=0.06, right=0.96, top=0.90, bottom=0.09)
    ax.set_xlabel("nSubjects "+str(fig_name)+"( Direct_to_session followed by session_to_session )", fontsize=30, fontweight='bold')
    ax.set_ylabel("RAND INDEX", fontsize=20, fontweight='bold')
    ax.set_ylim(0, 1.3)
    #colors = ['cyan','cyan', 'lightblue','lightblue', 'lightgreen','lightgreen', 'tan','tan', 'pink','pink','#7570b3','#7570b3', '#F78F1E','#F78F1E', '#BE3224','#BE3224',
             #'#F78F1E','#F78F1E', '#BE3224','#BE3224','#A78F1E','#A78F1E','m','m' ]
    Colors = ['cyan','#F78F1E', 'lightblue','y', 'lightgreen','#F78F1E', 'tan','#AEF2F4', 'pink', '#A78F1E', '#7570b3',  'm', 'k','#E78F1E','#BEF2F4','blue']
    Colors=np.tile(Colors,2)
    colors=[0 for i in range(2*Colors.__len__())]
    cnt=0
    for c in range(Colors.__len__()):
        colors[cnt]=Colors[c]
        colors[cnt+1]=Colors[c]
        cnt+=2
    colors = np.tile(colors, 6)
    for patch, color in zip(bp['boxes'], colors):
        patch.set_facecolor(color)
    import matplotlib.patches as mpatches
    cnt=0
    for roilist in map_roilists.keys():
        if cnt == 0:
            handles = [mpatches.Patch(color=Colors[cnt], label=map_roilists[roilist])]
            # handles += [mpatches.Patch(color=colors[cnt], label= map_roilists[roilist])]
        else:
            handles += [mpatches.Patch(color=Colors[cnt], label=map_roilists[roilist])]
            # handles += [mpatches.Patch(color=colors[cnt], label= map_roilists[roilist])]
        cnt += 1


    ## change color and linewidth of the whiskers
    for whisker in bp['whiskers']:
        whisker.set(color='#7570b3', linewidth=2)

    ## change color and linewidth of the caps
    for cap in bp['caps']:
        cap.set(color='#7570b3', linewidth=2)

    ## change color and linewidth of the medians
    for median in bp['medians']:
        median.set(color='green', linewidth=2)

    ## change the style of fliers and their fill
    for flier in bp['fliers']:
        flier.set(marker='o', color='#e7298a', alpha=0.5)

    # Save the figure
    '''plt.figtext(0.80, 0.08, ' superior frontal gyrus', color='cyan', weight='roman',
                size='x-small')


    plt.figtext(0.80, 0.045, 'pre-central gyrus',
                color='lightblue', weight='roman', size='x-small')
    plt.figtext(0.80, 0.015, 'angular gyrus', color='lightgreen', backgroundcolor='silver',
                weight='roman', size='medium')
    plt.figtext(0.815, 0.013, 'superior parietal gyrus', color='tan', weight='roman',
                size='x-small')
    plt.figtext(0.815, 0.010, 'pre-cuneus', color='pink', weight='roman',
                size='x-small')
    plt.figtext(0.815, 0.010, 'Insula', color='#7570b3', weight='roman',
                size='x-small')'''
    #plt.legend(handles=[NA, NA1,EU,EU1, AP,AP1, SA,SA1,AA, AA1, AU1,AU,AU2,AU3], loc=2, ncol=4)
    plt.legend(handles=handles[16:], loc=2, ncol=5)
    plt.show()
    fig.savefig('fig'+str(fig_name)+'_2.png', bbox_inches='tight')
    plt.close()


def session_to_session(msk,scan_type,sub_lst):
    lst=[]
    save_dir = '/ImagePTE1/ajoshi/code_farm/USCBrain_atlas/validation/' + scan_type
    cnt=0
    count=[3,2,1,4]
    sub_lst=sorted(sub_lst)
    for sub in sub_lst:
        if not (sub.startswith('s') or sub.startswith('d')):
            #print sub[:6]
            if cnt%4 ==0:
                cnt=0
            cnt+=1
            fmri1 = np.load(os.path.join(save_dir, str(sub)))
            fmri1_labels = fmri1['labels'][msk]
            for scan2 in range(cnt , 4):
                fmri2 = np.load(os.path.join(save_dir, str(sub_lst[sub_lst.index(sub)+1])))
                fmri2_labels = fmri2['labels'][msk]
                lst.append(adjusted_rand_score(fmri1_labels, fmri2_labels))
                print(sub,sub_lst[sub_lst.index(sub)+1],len(np.unique(fmri1_labels)),len(np.unique(fmri2_labels)))
    ''''a=np.arange(lst.__len__())
    lst1=[[]]
    for i in range(6):
        msk=a%6 ==i
        lst1.append(np.array(lst)[msk])
    return np.array(lst1[1:])'''
    return np.array(lst)

def dir_session(msk,scan_type,sub_lst):
    lst1=[[]]
    save_dir = '/ImagePTE1/ajoshi/code_farm/USCBrain_atlas/validation/' + scan_type
    lst=[]
    cnt=0
    direct = np.load(os.path.join(direct_mapping_dir, 'direct_mapping' + scan_type + '.npz'))
    dir_labels = direct['labels'][msk]
    for sub in sub_lst:
        cnt+=1
        fmri = np.load(os.path.join(save_dir, str(sub) ))
        fmri_labels = fmri['labels'][msk]
        lst.append(adjusted_rand_score(dir_labels, fmri_labels))
    '''a = np.arange(lst.__len__())
    for i in range(4):
        msk = a % 4 == i
        lst1.append(np.array(lst)[msk])
    return np.array(lst1[1:])'''
    return np.array(lst)

def RI_mean(lst_left,lst_right):
    import scipy as sp
    roilists=[]
    scan_type = ['left', 'right']
    for hemi in range(0,1):
        direct = np.load('very_smooth_data_'+scan_type[hemi]+'.npz')
        if roilists.__len__() ==  0:
            roilists=direct['roilists'].tolist()
        else :
            roilists += direct['roilists'].tolist()
    map_roilists={}
    for i in range (left_hemisphere.shape[0]):
        map_roilists[left_hemisphere[i]]=roiregion[i]
    refined_left=readdfs(os.path.join('/big_disk/ajoshi/coding_ground.donotdelete/hybridatlas/src/', '100307.BCI2reduce3.very_smooth.left.dfs'))
    refined_left=refined_left.labels
    refined_right = readdfs(os.path.join('/big_disk/ajoshi/coding_ground.donotdelete/hybridatlas/src/', '100307.BCI2reduce3.very_smooth.right.dfs'))
    refined_right=refined_right.labels
    temp = []
    temp1 = []
    cnt=0
    for roilist in map_roilists:
        #print roilist
        cnt += 1
        # msk_small_region = np.in1d(refined_right,roilist)
        msk_small_region = np.in1d(refined_left, roilist)
        if temp.__len__() > 0:
            # temp = sp.vstack([calculate_mean(msk_small_region, sub, scan_type[1]), temp])
            temp = sp.vstack([temp, dir_session(msk_small_region, scan_type[0],lst_left)])
            temp1 = sp.vstack([temp1, session_to_session(msk_small_region, scan_type[0],lst_left)])
        else:
            # temp=calculate_mean(msk_small_region,sub,scan_type[1])
            temp = dir_session(msk_small_region, scan_type[0],lst_left)
            temp1 = session_to_session(msk_small_region, scan_type[0],lst_left)
            # msk_small_region = np.in1d(refined_left, roilist+1)
            # temp=sp.vstack([calculate_mean(msk_small_region,sub,scan_type[0]),temp])
    box_plot(temp.tolist(),temp1.tolist(),map_roilists,'left_60',scan_type[0])


    map_roilists={}
    for i in range (right_hemisphere.shape[0]):
        map_roilists[right_hemisphere[i]]=roiregion[i]

    temp = []
    temp1 = []
    cnt=0
    for roilist in map_roilists:
        #print roilist
        cnt += 1
        # msk_small_region = np.in1d(refined_right,roilist)
        msk_small_region = np.in1d(refined_right, roilist)
        if temp.__len__() > 0:
            # temp = sp.vstack([calculate_mean(msk_small_region, sub, scan_type[1]), temp])
            temp = sp.vstack([temp, dir_session(msk_small_region, scan_type[1],lst_right)])
            temp1 = sp.vstack([temp1, session_to_session(msk_small_region, scan_type[1],lst_right)])
        else:
            # temp=calculate_mean(msk_small_region,sub,scan_type[1])
            temp = dir_session(msk_small_region, scan_type[1],lst_right)
            temp1 = session_to_session(msk_small_region, scan_type[1],lst_right)
            # msk_small_region = np.in1d(refined_left, roilist+1)
            # temp=sp.vstack([calculate_mean(msk_small_region,sub,scan_type[0]),temp])
    box_plot(temp.tolist(),temp1.tolist(),map_roilists,'right_60',scan_type[1])


from sklearn.metrics import adjusted_rand_score ,adjusted_mutual_info_score
lst_left = os.listdir('/ImagePTE1/ajoshi/code_farm/USCBrain_atlas/validation/left')
lst_right = os.listdir('/ImagePTE1/ajoshi/code_farm/USCBrain_atlas/validation/right')

direct_mapping_dir='/ImagePTE1/ajoshi/code_farm/USCBrain_atlas/direct_mapping'
#lst=['101915','106016','108828','122317','125525','136833','138534','147737','148335','156637']

sdir=['_RL','_LR']
scan_type=['left','right']
session_type=[1,2]
temp=[]
#box_plot()
RI_mean(lst_left,lst_right)

""" 
for sub in lst:
    if not (sub.startswith('direct_mapping')):
        for hemi in range(0,2):
            direct= np.load(os.path.join(direct_mapping_dir, 'direct_mapping'+scan_type[hemi] + '.npz'))
            dir_labels = direct['labels']
            if not (sub.startswith('s') or sub.startswith('d')):
                for scan in range(0,4):
                    fmri= np.load(os.path.join(save_dir, str(sub[:6]) + '_' + scan_type[hemi]  + sdir[int(np.floor(scan/2))] + '_' + str(session_type[scan%2]) + '.npz' ))
                    fmri_labels = fmri['labels']
                    temp.append(adjusted_mutual_info_score(dir_labels,fmri_labels))
                for scan1 in range(0, 4):
                    fmri1 = np.load(os.path.join(save_dir,  str(sub[:6]) + '_' + scan_type[hemi]  + sdir[int(np.floor(scan1/2))] + '_' + str(session_type[scan1%2]) + '.npz'))
                    fmri1_labels = fmri1['labels']
                    for scan2 in range(scan1 + 1, 4):
                        fmri2 = np.load(os.path.join(save_dir, str(sub[:6]) + '_' + scan_type[hemi]  + sdir[int(np.floor(scan2/2))] + '_' + str(session_type[scan2%2]) + '.npz'))
                        fmri2_labels = fmri2['labels']
                        if adjusted_rand_score(fmri1_labels, fmri2_labels) > 0:
                            temp.append(adjusted_mutual_info_score(fmri1_labels, fmri2_labels))
            temp.append(0)
        temp.append(0)
temp.append(0)
temp=np.array(temp)
import scipy as sp
sp.savez(
    os.path.join(save_dir, 'sub_and_rand-index_data.npz'),
    rand_index=temp,subjects=lst)
nsub=lst.__len__()
plot_histogram(nsub,temp,lst) """