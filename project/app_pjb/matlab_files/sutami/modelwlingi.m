function result = modelwlingi()
    warning('off');
    %% Data Sutami
    waduk_lahor= xlsread('data_waduk_wlingi');
    elevasi_lahor = waduk_lahor(:,1);
    volume_lahor = waduk_lahor(:,2);
    %% Persamaan 
    f_vol_lahor=fit(elevasi_lahor,volume_lahor,'poly5','robust','LAR');

    f1 = figure('visible','off');
    plot(f_vol_lahor, elevasi_lahor, volume_lahor);
    xlabel('Elevasi');
    ylabel('Volume');
    exportgraphics(f1, 'app_pjb\\static\\images\\f_vol_lahor.png', 'Resolution', 300);
    
    result.f_vol_lahor.modeltype = 'Linear Model Poly5';
    result.f_vol_lahor.formula = formula(f_vol_lahor);
    result.f_vol_lahor.coeffnames = coeffnames(f_vol_lahor);
    result.f_vol_lahor.coeffvalues = num2cell(coeffvalues(f_vol_lahor));
end