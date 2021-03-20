function result = modelselorejo()
    warning('off')
   
    data_waduk_SJ = readmatrix('Elevasi X Volume Selorejo.xlsx','Sheet','ElevasixVolume Selorejo','Range','A2:B2000');
    data_elevasi = data_waduk_SJ(isfinite(data_waduk_SJ(:, 1)), 1);
    data_vol = data_waduk_SJ(isfinite(data_waduk_SJ(:, 2)), 2);
    data_Performance_selorejo = readmatrix('Performance Selorejo.xlsx','Sheet','Selorejo','Range','A2:C20000');
    H = data_Performance_selorejo(isfinite(data_Performance_selorejo(:, 1)), 1);
    Q = data_Performance_selorejo(isfinite(data_Performance_selorejo(:, 2)), 2);
    P = data_Performance_selorejo(isfinite(data_Performance_selorejo(:, 3)), 3);

    vol=fit(data_elevasi,data_vol,'poly5');
    ele=fit(data_vol,data_elevasi,'poly9');
    fQ=fit([H, P],Q,'poly55');
    fP=fit([H, Q],P,'poly54');

    f1 = figure('visible','off');
    plot(vol, data_elevasi, data_vol);
    xlabel('Elevation');
    ylabel('Volume');
    exportgraphics(f1, 'app_pjb\\static\\images\\vol.png', 'Resolution', 300);

    f2 = figure('visible','off');
    plot(ele, data_vol, data_elevasi);
    xlabel('Volume');
    ylabel('Elevation');
    exportgraphics(f2, 'app_pjb\\static\\images\\ele.png', 'Resolution', 300);

    f3 = figure('visible','off');
    plot(fQ, [H, P], Q);
    xlabel('H');
    ylabel('P');
    zlabel('Q');
    exportgraphics(f3, 'app_pjb\\static\\images\\fQ.png', 'Resolution', 300);

    f4 = figure('visible','off');
    plot(fP, [H, Q], P);
    xlabel('H');
    ylabel('Q');
    zlabel('P');
    exportgraphics(f4, 'app_pjb\\static\\images\\fP.png', 'Resolution', 300);
    
    result.vol.modeltype = 'Linear Model Poly5';
    result.vol.formula = formula(vol);
    result.vol.coeffnames = coeffnames(vol);
    result.vol.coeffvalues = num2cell(coeffvalues(vol));
    result.ele.modeltype = 'Linear Model Poly9';
    result.ele.formula = formula(ele);
    result.ele.coeffnames = coeffnames(ele);
    result.ele.coeffvalues = num2cell(coeffvalues(ele));
    result.fQ.modeltype = 'Linear Model Poly55';
    result.fQ.formula = formula(fQ);
    result.fQ.coeffnames = coeffnames(fQ);
    result.fQ.coeffvalues = num2cell(coeffvalues(fQ));
    result.fP.modeltype = 'Linear Model Poly54';
    result.fP.formula = formula(fP);
    result.fP.coeffnames = coeffnames(fP);
    result.fP.coeffvalues = num2cell(coeffvalues(fP));
end

