function [outputArg1] = test(real_h0, real_ht)
    h0 = real_h0
    lg = length(h0)
    for x = 1:length(h0)
        a = h0(x)
    end
    ht = real_ht
    lt = length(ht)
    for x = 1:length(ht)
        a = ht(x)
    end
    outputArg1.a = 5;
end