clc; clear;
addpath(genpath('.'));
addpath /hd2/sw1/MATLAB18/gifti
addpath(genpath('/hd2/sw1/bfp/'))
addpath('/hd2/sw1/cifti-matlab');

%%

folder_32k = '/hd2/research/Connectivity/data/Essens_Files/32K/Common_Anatomy/';
cort32k = load([folder_32k, 'IdxNaN.mat']);
clearvars folder_32k

cort_data_root = '/hd2/research/Connectivity/data/';
sfL_32k = loadGii([cort_data_root 'surface/Conte69.L.inflated.32k_fs_LR.surf.gii']);
sfR_32k = loadGii([cort_data_root 'surface/Conte69.R.inflated.32k_fs_LR.surf.gii']);

%%
clc

data_root = '/hd2/research/Connectivity/data/';

neuroim = load('/hd2/research/Connectivity/data/Atlases/neuroim18_avg_atlas/atlas_group_brodmann_32k.mat');
neuroim_ba = neuroim.label;
length(unique(neuroim_ba))

%%

model_list = ["uscbrain-130", "bci-dni-66", "power-130", "AALv3-96", "destrieux-150", ...
             "yeo-51", "yeo-114", "desikan-70", "brainnetome-210", ...
             "schaefer-100", "schaefer-200", "schaefer-300", ...
             "gordon-333", "gordon2-333", "glasser-360"];
         
cnt = 0;
anat_rst = {};

for cur_model = model_list
    
    fprintf('%s ', cur_model);

    cur_label = relabel(loadAtlas(cur_model));    
    [~, cur_atlas_type] = loadAtlas(cur_model);

    cur_cluster_num = length(unique(cur_label));
    
    if ismember(0, cur_label)
        cur_cluster_num = cur_cluster_num - 1;
    end

    [cur_dice, cur_joined, cur_dice_var ] = dice_atlas_align(neuroim_ba, cur_label);
    fprintf('dice: %.3f\n', cur_dice);
    
    cnt = cnt + 1;
    anat_rst{cnt, 1} = cur_model;
    anat_rst{cnt, 2} = cur_cluster_num;
    anat_rst{cnt, 3} = cur_dice;
    anat_rst{cnt, 4} = cur_atlas_type;
    anat_rst{cnt, 5} = cur_dice_var;
    
end    

anat_rst = cell2table(anat_rst);
writetable(anat_rst, 'others/eval_uscbrain/anat_rst.csv');

%% plot figure

clc;

f = figure;
ax = axes(f, 'Position', [.05 .075 .8 .92]);
var_scale= 1.23e4;

for i = 1: size(anat_rst)
    switch anat_rst{i, 4}
        case "anat"
            cur_color = 'b';
        case "func"
            cur_color = 'r';
        case "hybrid"
            cur_color = 'k';
    end
    
    scatter(anat_rst{i, 2}, anat_rst{i, 3}, anat_rst{i, 5}*var_scale, 'filled', cur_color);
    hold on;
    
    switch anat_rst{i, 1}
        case "desikan-70"
            text(anat_rst{i, 2} - 35, anat_rst{i, 3}, formatAtlasName(anat_rst{i, 1}), 'fontweight', 'bold', 'fontsize', 18);
        case "bci-dni-66"
            text(anat_rst{i, 2} - 35, anat_rst{i, 3}, formatAtlasName(anat_rst{i, 1}), 'fontweight', 'bold', 'fontsize', 18);
        case "AALv3-96"
            text(anat_rst{i, 2} + 5, anat_rst{i, 3} + 0.005, formatAtlasName(anat_rst{i, 1}), 'fontweight', 'bold', 'fontsize', 18);
        case "schaefer-300"
            text(anat_rst{i, 2} - 2 , anat_rst{i, 3} + 0.03, formatAtlasName(anat_rst{i, 1}), 'fontweight', 'bold', 'fontsize', 18);
           
        otherwise
            text(anat_rst{i, 2} + 5, anat_rst{i, 3}, formatAtlasName(anat_rst{i, 1}), 'fontweight', 'bold', 'fontsize', 18);
    end
    
    
   
end

grid on;
xlabel('Number of clusters', 'fontweight', 'bold', 'fontsize', 18);
ylabel('Average dice coefficient', 'fontweight', 'bold', 'fontsize', 18);
% title('Agreement with Brodmann areas', 'fontweight', 'bold',  'fontsize', 18);
xlim([0, 400]);
ylim([0.24, 0.81]);

hold on;
pos1_x = 70; pos1_y = 0.775; h01 = 0.02;
scatter(pos1_x, pos1_y + h01, 0.01*var_scale, 'filled', 'k'); 
t1 = text(pos1_x + 6, pos1_y + h01, ['Variance ' num2str(0.01)]); t1.FontSize = 18; t1.FontWeight = 'bold';
scatter(pos1_x, pos1_y, 0.025*var_scale, 'filled', 'k'); 
t2 = text(pos1_x + 6, pos1_y, ['Variance ' num2str(0.025)]); t2.FontSize = 18; t2.FontWeight = 'bold'; 
scatter(pos1_x, pos1_y - h01, 0.05*var_scale, 'filled', 'k'); 
t3 = text(pos1_x + 6, pos1_y - h01, ['Variance ' num2str(0.05)]); t3.FontSize = 18; t3.FontWeight = 'bold'; 


legend('Hybrid', 'Anatomical', 'Functional', 'fontweight', 'bold', 'fontsize', 18);
set(legend, 'location', 'northwest');
grid(gca,'minor');
set(gca, 'fontweight', 'bold', 'fontsize', 18);


