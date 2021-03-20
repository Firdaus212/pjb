function result = modelsutami2()
    warning('off');
    data_beban = xlsread('data_operasi_sutami');
    elevasi = data_beban(:,1);
    discarge= data_beban(:,2);
    power= data_beban(:,3);
    fungsi_p =fit([elevasi,discarge],power,'poly55');

    f1 = figure('visible','off');
    plot(fungsi_p, [elevasi,discarge], power);
    xlabel('Elevasi');
    ylabel('Discharge');
    zlabel('Power');
    exportgraphics(f1, 'app_pjb\\static\\images\\fungsi_p.png', 'Resolution', 300);
    
    result.fungsi_p.modeltype = 'Linear Model Poly55';
    result.fungsi_p.formula = formula(fungsi_p);
    result.fungsi_p.coeffnames = coeffnames(fungsi_p);
    result.fungsi_p.coeffvalues = num2cell(coeffvalues(fungsi_p));
end