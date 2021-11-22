clc; clear; close all;
addpath(genpath('.'));
addpath /hd2/sw1/MATLAB18/gifti
addpath('/hd2/sw1/cifti-matlab');
addpath(genpath('/hd2/sw1/bfp/'))

%%

VERT_NUM = 59412;
LEFT_VERT_NUM = 29696;
data_root = '/hd2/research/Connectivity/data/';

%% Beijing ADHD resting-state connectivity

func_con_beijing = load('/hd2/research/Connectivity/data/Beijing_ADHD/Beijing_ADHD_funcCon_32k.mat');
func_beijing_rest = func_con_beijing.avg_func_con;
clearvars func_con_beijing

% to accomodate for fisher r-to-z
func_beijing_rest = func_beijing_rest - eye(VERT_NUM);
func_beijing_rest(func_beijing_rest == 1) = 0.99999;
func_beijing_rest = func_beijing_rest + eye(VERT_NUM);
func_beijing_rest_fisher = atanh(func_beijing_rest);

clearvars func_beijing_rest

%% load parcellations and compute func. homo.
clc

cur_func = func_beijing_rest_fisher;

model_list = ["uscbrain-130", "bci-dni-66", "power-130", "AALv3-96", "destrieux-150", ...
             "yeo-51", "yeo-114", "desikan-70", "brainnetome-210", ...
             "schaefer-100", "schaefer-200", "schaefer-300", ...
             "gordon-333", "gordon2-333", "glasser-360"];

homo_rst = {};
cnt = 0;

for cur_model = model_list
    
    fprintf('%s ', cur_model);
    cur_label = relabel(loadAtlas(cur_model));
    [~, cur_atlas_type] = loadAtlas(cur_model);
    
    [~, ~, cur_homo, cur_homo_var] = homogeneity2(cur_label, cur_func);
    
    cur_cluster_num = length(unique(cur_label));
    
    if ismember(0, cur_label)
        cur_cluster_num = cur_cluster_num - 1;
    end
    
    fprintf('homo: %.3f\n', cur_homo);
    
    cnt = cnt + 1;
    homo_rst{cnt, 1} = cur_model;
    homo_rst{cnt, 2} = cur_cluster_num;
    homo_rst{cnt, 3} = cur_homo;
    homo_rst{cnt, 4} = cur_atlas_type;
    homo_rst{cnt, 5} = cur_homo_var;
    
end    


%% plot figure

clc;

f = figure;
ax = axes(f, 'Position', [.05 .075 .8 .92]);
var_scale= 3.5e6;

for i = 1: size(homo_rst)
    switch homo_rst{i, 4}
        case "anat"
            cur_color = 'b';
        case "func"
            cur_color = 'r';
        case "hybrid"
            cur_color = 'k';
    end
        
    scatter(homo_rst{i, 2}, homo_rst{i, 3}, homo_rst{i, 5}*var_scale, 'filled', cur_color);
    hold on;
    
    switch homo_rst{i, 1}
        case "yeo-51"
            text(homo_rst{i, 2} - 20, homo_rst{i, 3} + 0.02 , formatAtlasName(homo_rst{i, 1}), 'fontweight', 'bold', 'fontsize', 18);
        case "yeo-114"
            text(homo_rst{i, 2} - 30, homo_rst{i, 3} - 0.02 , formatAtlasName(homo_rst{i, 1}), 'fontweight', 'bold', 'fontsize', 18);
        case "uscbrain-130"
            text(homo_rst{i, 2} - 2, homo_rst{i, 3} - 0.02 , formatAtlasName(homo_rst{i, 1}), 'fontweight', 'bold', 'fontsize', 18);
        case "power-130"
            text(homo_rst{i, 2} - 2, homo_rst{i, 3} - 0.02 , formatAtlasName(homo_rst{i, 1}), 'fontweight', 'bold', 'fontsize', 18);
        case "schaefer-100"
            text(homo_rst{i, 2} - 2, homo_rst{i, 3} + 0.02 , formatAtlasName(homo_rst{i, 1}), 'fontweight', 'bold', 'fontsize', 18);
        case "desikan-70"
            text(homo_rst{i, 2} - 7, homo_rst{i, 3} + 0.02 , formatAtlasName(homo_rst{i, 1}), 'fontweight', 'bold', 'fontsize', 18);
        case "bci-dni-66"
            text(homo_rst{i, 2} + 1 , homo_rst{i, 3} - 0.01 , formatAtlasName(homo_rst{i, 1}), 'fontweight', 'bold', 'fontsize', 18);
        case "gordon2-333"
            text(homo_rst{i, 2} - 2, homo_rst{i, 3} - 0.02 , formatAtlasName(homo_rst{i, 1}), 'fontweight', 'bold', 'fontsize', 18);
        otherwise
            text(homo_rst{i, 2} + 2.5, homo_rst{i, 3} , formatAtlasName(homo_rst{i, 1}), 'fontweight', 'bold', 'fontsize', 18);
    end
end

grid on;
xlabel('Number of clusters', 'fontweight', 'bold', 'fontsize', 18);
ylabel('Weighted average homogeneity', 'fontweight', 'bold', 'fontsize', 18);

xlim([0, 400]);
ylim([0.28, 0.76]);

hold on;
pos1_x = 70; pos1_y = 0.732; h01 = 0.015;
scatter(pos1_x, pos1_y + h01, 2.5e-5*var_scale, 'filled', 'k'); 
t1 = text(pos1_x + 6, pos1_y + h01, ['Variance 2.5\times10^{-5}']); t1.FontSize = 18; t1.FontWeight = 'bold';
scatter(pos1_x, pos1_y, 5e-5*var_scale, 'filled', 'k'); 
t2 = text(pos1_x + 6, pos1_y, ['Variance 5\times10 ^{-5}']); t2.FontSize = 18; t2.FontWeight = 'bold'; 
scatter(pos1_x, pos1_y - h01, 1e-4*var_scale, 'filled', 'k'); 
t3 = text(pos1_x + 6, pos1_y - h01, ['Variance 10^{-4}']); t3.FontSize = 18; t3.FontWeight = 'bold'; 

legend('Hybrid', 'Anatomical', 'Functional', 'fontweight', 'bold', 'fontsize', 18);
set(legend, 'location', 'northwest');
grid(gca,'minor');
set(gca, 'fontweight', 'bold', 'fontsize', 18);
