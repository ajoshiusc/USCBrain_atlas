function [relabeled, K] = relabel( parcels )
% Relabel a parcellation to consecutive label values in case it's not

% input: 
%     parcels (n * 1) array, representing cluster labels for all vertices
% output: 
%     relabeled (n * 1) array, so that the label values s are from 1 to K
%         and permuted to try to avoid similar color label of nb parcels
% modified by yijun
% code originally from https://github.com/sarslancs/parcellation-survey-eval

% zeros are often just background, so don't count them
ids = nonzeros(unique((parcels)));
K = length(ids);

if max(parcels) == K
    relabeled = parcels;
else
    relabeled = zeros(size(parcels));
    rng(2, 'twister')
    new_ids = randperm(K);
    cnt = 1;
    for i = 1 : K
        relabeled(parcels == ids(i)) = new_ids(cnt);
        cnt = cnt + 1;
    end
end





