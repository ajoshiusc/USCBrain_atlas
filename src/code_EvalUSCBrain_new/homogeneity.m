function [homos_nan, parcel_sizes, avg_weighted_homos, weighted_var ] = homogeneity( parcels, Z )
%  this script is adapted from the code from
%   https://github.com/sarslancs/parcellation-survey-eval
% 
%   Parcel homogeneity.
% 
%   Homogeneity of a parcel is measured by calculating the average
%   temporal correlation between every pair of vertices assigned to it. 
% 
%   A global homogeneity value for the entire parcellation can be obtained by 
%   averaging the homogeneity values across all parcels.
% 
%
%   INPUT
%   =====
%   parcels: (n * 1) array, denoting a parcellation
%   Z: A functional connenctivity (correlation) matrix 
%       (should be Fisher's r-to-z transformed).
%
%   OUTPUT
%   ======
%   weighted_homos: (#parcel * 1) array: Homogeneity values for each parcel
%
%   Author: Salim Arslan, April 2017 (name.surname@imperial.ac.uk)
    
    assert(size(parcels, 1) == size(Z, 1), ...
        'dim of parcellation and homogeneity matrix does not match!');
    
    K = max(parcels);
    homos = zeros(K,1);
    parcel_sizes = zeros(K,1);
    vars = zeros(K,1);

%   not counting parcels marked as 0 (background)
    for i = 1 : K  
        in_members = (parcels == i);
        nk = sum(in_members); 

        if nk <= 0
            ak = nan;
        elseif nk == 1 % In case there are parcels with only 1 element (may happen with NCUTS)
            ak = 1;
            cur_var = 0;
        else
            corrs = Z(in_members,in_members)';
            corrs(logical(eye(length(corrs)))) = 0;
            means_in = sum(corrs, 2) / (nk-1);
            ak = mean(means_in);
            cur_var = var(means_in);
        end

        parcel_sizes(i) = nk;
        homos(i) = ak;
        vars(i) = cur_var;
    end
    
    
    parcel_sizes = parcel_sizes(~isnan(homos));
    
    homos_nan = homos;
    
    homos = homos(~isnan(homos));
    vars = vars(~isnan(homos));

    avg_weighted_homos = sum(homos .* (parcel_sizes / sum(parcel_sizes)));
    weighted_var = sum((parcel_sizes / sum(parcel_sizes)).^2 .* vars);

end
