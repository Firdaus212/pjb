function Y=per_volume(h,elevasi,volume)
for i= 1:length(elevasi)
    if h==elevasi(i)
        Y=volume(i);
    end
end

