function result = modelsiman()
    warning('off')
    Siman = readmatrix('Performance Siman.xlsx','Sheet','Siman','Range','A2:F2000');
    PS1 = Siman(isfinite(Siman(:, 1)), 1);
    QS1 = Siman(isfinite(Siman(:, 2)), 2);
    PS2 = Siman(isfinite(Siman(:, 3)), 3);
    QS2 = Siman(isfinite(Siman(:, 4)), 4);
    PS3 = Siman(isfinite(Siman(:, 5)), 5);
    QS3 = Siman(isfinite(Siman(:, 6)), 6);

    Ps1=fit(QS1,PS1,'poly5');
    Ps2=fit(QS2,PS2,'poly5');
    Ps3=fit(QS3,PS3,'poly5');

    f1 = figure('visible','off');
    plot(Ps1, QS1, PS1);
    xlabel('QS1');
    ylabel('PS1');
    exportgraphics(f1, 'app_pjb\\static\\images\\Ps1.png', 'Resolution', 300);

    f2 = figure('visible','off');
    plot(Ps2, QS2, PS2);
    xlabel('QS2');
    ylabel('PS2');
    exportgraphics(f2, 'app_pjb\\static\\images\\Ps2.png', 'Resolution', 300);

    f3 = figure('visible','off');
    plot(Ps3, QS3, PS3);
    xlabel('QS3');
    ylabel('PS3');
    exportgraphics(f3, 'app_pjb\\static\\images\\Ps3.png', 'Resolution', 300);
    
    result.Ps1.modeltype = 'Linear Model Poly5';
    result.Ps1.formula = formula(Ps1);
    result.Ps1.coeffnames = coeffnames(Ps1);
    result.Ps1.coeffvalues = num2cell(coeffvalues(Ps1));
    result.Ps2.modeltype = 'Linear Model Poly5';
    result.Ps2.formula = formula(Ps2);
    result.Ps2.coeffnames = coeffnames(Ps2);
    result.Ps2.coeffvalues = num2cell(coeffvalues(Ps2));
    result.Ps3.modeltype = 'Linear Model Poly5';
    result.Ps3.formula = formula(Ps3);
    result.Ps3.coeffnames = coeffnames(Ps3);
    result.Ps3.coeffvalues = num2cell(coeffvalues(Ps3));
end

