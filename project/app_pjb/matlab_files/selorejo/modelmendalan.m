function result = modelmendalan()
    warning('off')
    Mendalan = readmatrix('Performance Mendalan.xlsx','Sheet','Mendalan','Range','A2:H2000');
    PM1 = Mendalan(isfinite(Mendalan(:, 1)), 1);
    QM1 = Mendalan(isfinite(Mendalan(:, 2)), 2);
    PM2 = Mendalan(isfinite(Mendalan(:, 3)), 3);
    QM2 = Mendalan(isfinite(Mendalan(:, 4)), 4);
    PM3 = Mendalan(isfinite(Mendalan(:, 5)), 5);
    QM3 = Mendalan(isfinite(Mendalan(:, 6)), 6);
    PM4 = Mendalan(isfinite(Mendalan(:, 7)), 7);
    QM4 = Mendalan(isfinite(Mendalan(:, 8)), 8);

    Pm1=fit(QM1,PM1,'poly4');
    Pm2=fit(QM2,PM2,'poly4');
    Pm3=fit(QM3,PM3,'poly4');
    Pm4=fit(QM4,PM4,'poly4');

    f1 = figure('visible','off');
    plot(Pm1, QM1, PM1);
    xlabel('QM1');
    ylabel('PM1');
    exportgraphics(f1, 'app_pjb\\static\\images\\Pm1.png', 'Resolution', 300);

    f2 = figure('visible','off');
    plot(Pm2, QM2, PM2);
    xlabel('QM2');
    ylabel('PM2');
    exportgraphics(f2, 'app_pjb\\static\\images\\Pm2.png', 'Resolution', 300);

    f3 = figure('visible','off');
    plot(Pm3, QM3, PM3);
    xlabel('QM3');
    ylabel('PM3');
    exportgraphics(f3, 'app_pjb\\static\\images\\Pm3.png', 'Resolution', 300);

    f4 = figure('visible','off');
    plot(Pm4, QM4, PM4);
    xlabel('QM4');
    ylabel('PM4');
    exportgraphics(f1, 'app_pjb\\static\\images\\Pm4.png', 'Resolution', 300);
    
    result.Pm1.modeltype = 'Linear Model Poly4';
    result.Pm1.formula = formula(Pm1);
    result.Pm1.coeffnames = coeffnames(Pm1);
    result.Pm1.coeffvalues = num2cell(coeffvalues(Pm1));
    result.Pm2.modeltype = 'Linear Model Poly4';
    result.Pm2.formula = formula(Pm2);
    result.Pm2.coeffnames = coeffnames(Pm2);
    result.Pm2.coeffvalues = num2cell(coeffvalues(Pm2));
    result.Pm3.modeltype = 'Linear Model Poly4';
    result.Pm3.formula = formula(Pm3);
    result.Pm3.coeffnames = coeffnames(Pm3);
    result.Pm3.coeffvalues = num2cell(coeffvalues(Pm3));
    result.Pm4.modeltype = 'Linear Model Poly4';
    result.Pm4.formula = formula(Pm4);
    result.Pm4.coeffnames = coeffnames(Pm4);
    result.Pm4.coeffvalues = num2cell(coeffvalues(Pm4));
end

