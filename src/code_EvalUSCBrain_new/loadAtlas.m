function [label, atlas_type] = loadAtlas(model_name)
%   Yijun
% 
%   atlas_type: "anat" / "func" / "hybrid"

     data_root = '/hd2/research/Connectivity/data/';
     folder_32k = '/hd2/research/Connectivity/data/Essens_Files/32K/Common_Anatomy/';
    
     format1_atlases = ["uscbrain-130", "bci-dni-66",  "AAL", "AALv3-96", "AALv3-96", "Yeo-17", "Yeo-7"];
     
     if ismember(model_name, format1_atlases)
        cort32k = load([folder_32k, 'IdxNaN.mat']);
        
        switch model_name
            
            case "uscbrain-130"
                model = load([data_root 'Atlases/USCBrain_grayordinate_labels_clean.mat']);
                atlas_type = "hybrid";
                
            case "bci-dni-66"
                model = load([data_root 'Atlases/BCI-DNI_brain_grayordinate_labels.mat']);
                atlas_type = "anat";
                
            case "AAL"
                model = load([data_root '/Atlases/AALv3_grayordinate_labels.mat']);
                atlas_type = "anat";
            
            case "AALv3-96"
                model = load([data_root '/Atlases/AALv3_grayordinate_labels.mat']);
                atlas_type = "anat";
                
            case "Yeo-7"
                model = cifti_read([data_root '/Atlases/Yeo/Yeo2011_7Networks_N1000.dlabel.nii']);
                atlas_type = "func";
                
            case "Yeo-17"
                model = cifti_read([data_root '/Atlases/Yeo/Yeo2011_17Networks_N1000.dlabel.nii']);
                atlas_type = "func";
                
        end
        
        if strcmp(model_name, "Yeo-17") || strcmp(model_name, "Yeo-7")
            label= model.cdata;    
        else
            label= model.labels;
        end
        
        label_l = label(1: 32492); 
        label_r = label(32493: 64984);
        label_l = label_l(~cort32k.idxNaNL);
        
        if strcmp(model_name, "Yeo-17") || strcmp(model_name, "Yeo-7")
            label_r = label_r(~cort32k.idxNaNR); 
        else
            label_r = label_r(~cort32k.idxNaNR) + max(label_l);
        end
        label = [label_l; label_r];   
        
        return
     end
                
     model_name_parts = split(model_name, '-');
     
     if strcmp(model_name_parts(1), "schaefer")
         
        parcel_cnt = convertStringsToChars(model_name_parts(2));
        cort32k = load([folder_32k, 'IdxNaN.mat']);
        label = cifti_read([data_root 'Atlases/Schaefer_Yeo18/Schaefer2018_' num2str(parcel_cnt) ...
                                'Parcels_17Networks_order.dlabel.nii']);
        label = label.cdata;
        label_l = label(1: 32492); label_r = label(32493: end);
        label = [label_l(~cort32k.idxNaNL); label_r(~cort32k.idxNaNR)];
        
        atlas_type = "func";
        
        
     elseif strcmp(model_name_parts(1), "schaefer11k")
         
        parcel_cnt = convertStringsToChars(model_name_parts(2));
        label = load([data_root 'Atlases/Schaefer_Yeo18/Schaefer2018_' num2str(parcel_cnt) ...
                                'Parcels_7Networks_order_11k.mat']);
        label = label.label;
        atlas_type = "func";
         
     else
    
         switch model_name

            case "yeo-51"
                model1 = load([data_root 'Atlases/Yeo/Yeo_7Networks_Split_Yeolab_32k.mat']);    
                atlas_type = "func";

            case "yeo-114"
                model1 = load([data_root 'Atlases/Yeo/Yeo_17Networks_Split_Yeolab_32k.mat']);
                atlas_type = "func";

            case "gordon-333"
                model1 = load([data_root 'Atlases/HCP_Gordon_L161R172_32k.mat']);
                atlas_type = "func";

            case "gordon2-333"
                model1 = load([data_root 'Atlases/NeuroIm18_Gordon_L161R172_32k.mat']);
                atlas_type = "func";

            case "glasser-360"
                model1 = load([data_root 'Atlases/HCP_Glasser_L180R180_32k.mat']);
                atlas_type = "hybrid";

            case "ica-43"
                model1 = load([data_root 'Atlases/HCP_ICA_L21R22_32k.mat']);
                atlas_type = "func";

            case "ica-76"
                model1 = load([data_root 'Atlases/HCP_ICA_L36R40_32k.mat']);        
                atlas_type = "func";

            case "shen-200"
                model1 = load([data_root 'Atlases/NeuroIm18_Shen_L102R98_32k.mat']);
                atlas_type = "func";
                
            case "power-130"
                model1 = load([data_root 'Atlases/NeuroIm18_Power_L65R65_32k.mat']);
                atlas_type = "func";
                
            case "destrieux-150"
                model1 = load([data_root 'Atlases/NeuroIm18_Destrieux_L75R75_32k.mat']);
                atlas_type = "anat";
                
            case "desikan-70"
                model1 = load([data_root 'Atlases/NeuroIm18_Desikan_L35R35_32k.mat']);
                atlas_type = "anat";
                
            case "brainnetome-210"
                model1 = load([data_root 'Atlases/NeuroIm18_Brainnectome_L105R105_32k.mat']);
                atlas_type = "hybrid";
                
         end
         
         label = model1.label;
         
     end

end