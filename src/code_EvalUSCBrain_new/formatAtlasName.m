function out = formatAtlasName(in)

    if strcmp(in, "bci-dni-66")
        out = "BCI-DNI";
        return;
        
    elseif strcmp(in, "uscbrain-130")
        out = "USCBrain";
        return
        
    elseif strcmp(in, "AALv3-96")
        out = "AAL";
        return;
        
    end    
    
    if contains(in, '-')
        model_name_parts = split(in, '-');  
        
        if ismember(model_name_parts(1), ["schaefer", "yeo"])
            first_part = in;
        else
            first_part = model_name_parts(1);
        end
    else
    
            first_part = in;
    
    end    
    first_part_char = str2char(first_part);
    first_letter = char2str(upper(first_part_char(1)));
    other_letter = first_part_char(2:end);
    out = first_letter + other_letter;
    

end