function result = modelsutami()
    warning('off');
    %% Data Sutami
    waduk_sutami = xlsread('data_waduk','waduk_sutami');
    elevasi_sutami = waduk_sutami(:,1);
    volume_sutami = waduk_sutami(:,2);
    %% Persamaan 
    f_vol_sutami=fit(elevasi_sutami,volume_sutami,'poly5');

    f1 = figure('visible','off');
    plot(f_vol_sutami, elevasi_sutami, volume_sutami);
    xlabel('Elevasi');
    ylabel('Volume');
    exportgraphics(f1, 'app_pjb\\static\\images\\f_vol_sutami.png', 'Resolution', 300);
    
    result.f_vol_sutami.modeltype = 'Linear Model Poly5';
    result.f_vol_sutami.formula = formula(f_vol_sutami);
    result.f_vol_sutami.coeffnames = coeffnames(f_vol_sutami);
    result.f_vol_sutami.coeffvalues = num2cell(coeffvalues(f_vol_sutami));
end