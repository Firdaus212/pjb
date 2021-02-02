function outputArg = sutami_wlingi_basah(input)
     warning('off');
    %% Input Value
    elevasi_awal = input.elevasi_awal;
    elevasi_akhir = input.elevasi_akhir;
    inflow_min = input.inflow_min; %error range -10 m^3/s dari rata-rata inflow
    inflow_max = input.inflow_max; %error range +10 m^3/s dari rata-rata inflow
    t1 = cell2mat(input.t1); %Jam Operasi sutami 1
    t2 = cell2mat(input.t2); %Jam Operasi sutami 2
    t3 = cell2mat(input.t3); %Jam Operasi sutami 3

    elevasi_awal_wlingi = input.elevasi_awal_wlingi;
    elevasi_akhir_wlingi = input.elevasi_akhir_wlingi;
    r_basin_min = input.r_basin_min; %error range -5 m^3/s dari rata-rata remain basin
    r_basin_max = input.r_basin_max; %error range -5 m^3/s dari rata-rata remain basin
    %% Waktu operasi total
    time = (t1(2)-t1(1))+t2(2)-t2(1)+t3(2)-t3(1);
    %% Data Sutami
    waduk_sutami = xlsread('data_waduk','waduk_sutami');
    elevasi_sutami = waduk_sutami(:,1);
    volume_sutami = waduk_sutami(:,2);
    waduk_lahor= xlsread('data_waduk','waduk_lahor');
    elevasi_lahor = waduk_lahor(:,1);
    volume_lahor = waduk_lahor(:,2);
    data_beban = xlsread('data_operasi_sutami');
    elevasi = data_beban(:,1);
    discarge= data_beban(:,2);
    power= data_beban(:,3);
    %% Persamaan 
    f_vol_sutami=fit(elevasi_sutami,volume_sutami,'poly5');
    f_vol_lahor=fit(elevasi_lahor,volume_lahor,'poly5','robust','LAR');
    %f_ell_sutami=fit(volume_sutami,elevasi_sutami,'poly5');
    %f_ell_lahor=fit(volume_lahor,elevasi_lahor,'poly5','robust','LAR');
    %fungsi_q =fit([elevasi,power],discarge,'poly55');
    fungsi_p =fit([elevasi,discarge],power,'poly55');
    inflow = inflow_min+(inflow_max-inflow_min).*rand(86400,1);
    %% Volume_tersedia
    vol_sutami = f_vol_sutami(elevasi_awal)-f_vol_sutami(elevasi_akhir);
    vol_lahor  = f_vol_lahor(elevasi_awal)-f_vol_lahor(elevasi_akhir);
    vol_tersedia = vol_sutami+vol_lahor+sum(inflow);
    %% Operasi_Sutami
    q_out = vol_tersedia/(24*3600);
    ell=elevasi_awal;
    for a=1:86400
        %% Turbin Sutami 1
        if a>=t1(1)*3600 && a<=t1(2)*3600
            q_sutami_1(a)=q_out/3;
            beban_sutami_1(a)=(0.9995+(1.015-0.9985).*rand(1,1))*fungsi_p([ell,q_out/3]);
        else
            q_sutami_1(a)=0;
            beban_sutami_1(a)=0;
        end
        %% Turbin Sutami 2
        if a>=t2(1)*3600 && a<=t2(2)*3600
            q_sutami_2(a)=q_out/3;
            beban_sutami_2(a)=(0.9995+(1.015-0.9985).*rand(1,1))*fungsi_p([ell,q_out/3]);
        else
            q_sutami_2(a)=0;
            beban_sutami_2(a)=0;
        end
        %% Turbin Sutami 3
        if a>=t3(1)*3600 && a<=t3(2)*3600
            q_sutami_3(a)=q_out/3;
            beban_sutami_3(a)=(0.9995+(1.015-0.9985).*rand(1,1))*fungsi_p([ell,q_out/3]);
        else
            q_sutami_3(a)=0;
            beban_sutami_3(a)=0;
        end 
        q_sutami(a)=q_sutami_1(a)+q_sutami_2(a)+q_sutami_3(a);
    end
    %% Operasi Wlingi
    r_basin = r_basin_min+(r_basin_max-r_basin_min).*rand(86400,1);
    q_wlingi = q_sutami;
    d_elevasi = (elevasi_awal_wlingi-elevasi_akhir_wlingi)/86400;
    elevasi_wlingi = elevasi_awal_wlingi;
    for b=1:length(q_wlingi)
        q_wlingi(b)=q_wlingi(b)+r_basin(b);
        outflow_wlingi(b) = q_wlingi(b)-(d_elevasi*360*3600);%berdasarkan persamaan swc data p.nur
        if elevasi_wlingi>=163.38
            swc_wlingi(b) = 5.3;
        elseif elevasi_wlingi<163.38 && elevasi_wlingi>=163.13
            swc_wlingi(b) = 5.375;
        elseif elevasi_wlingi<163.13 && elevasi_wlingi>=162.88
            swc_wlingi(b) = 5.45;
        elseif elevasi_wlingi<162.88 && elevasi_wlingi>=162.63
            swc_wlingi(b) = 5.563;
        elseif elevasi_wlingi<162.62 && elevasi_wlingi>=162.38
            swc_wlingi(b) = 5.675;
        elseif elevasi_wlingi<162.38 && elevasi_wlingi>=162.13
            swc_wlingi(b) = 5.788;
        else
            swc_wlingi(b) = 5.9;
        end
        beban_wlingi_total(b)=outflow_wlingi(b)/swc_wlingi(b);%total 2 mesin jalan;
        elevasi_wlingi = elevasi_wlingi-d_elevasi;
    end

    %Output
    beban_sutami_1_mean = sum(beban_sutami_1)/86400;
    beban_sutami_2_mean = sum(beban_sutami_2)/86400;
    beban_sutami_3_mean = sum(beban_sutami_3)/86400;
    energi_sutami_1 = sum(beban_sutami_1)/3600;
    energi_sutami_2 = sum(beban_sutami_2)/3600;
    energi_sutami_3 = sum(beban_sutami_3)/3600;
    energi_total_sutami = energi_sutami_1+energi_sutami_2+energi_sutami_3;
    beban_wlingi_perjam = [sum(beban_wlingi_total(1:(1*3600)))/3600;...
        sum(beban_wlingi_total(((1*3600)+1):(2*3600)))/3600;...
        sum(beban_wlingi_total(((2*3600)+1):(3*3600)))/3600;...
        sum(beban_wlingi_total(((3*3600)+1):(4*3600)))/3600;...
        sum(beban_wlingi_total(((4*3600)+1):(5*3600)))/3600;...
        sum(beban_wlingi_total(((5*3600)+1):(6*3600)))/3600;...
        sum(beban_wlingi_total(((6*3600)+1):(7*3600)))/3600;...
        sum(beban_wlingi_total(((7*3600)+1):(8*3600)))/3600;...
        sum(beban_wlingi_total(((8*3600)+1):(9*3600)))/3600;...
        sum(beban_wlingi_total(((9*3600)+1):(10*3600)))/3600;...
        sum(beban_wlingi_total(((10*3600)+1):(11*3600)))/3600;...
        sum(beban_wlingi_total(((11*3600)+1):(12*3600)))/3600;...
        sum(beban_wlingi_total(((12*3600)+1):(13*3600)))/3600;...
        sum(beban_wlingi_total(((13*3600)+1):(14*3600)))/3600;...
        sum(beban_wlingi_total(((14*3600)+1):(15*3600)))/3600;...
        sum(beban_wlingi_total(((15*3600)+1):(16*3600)))/3600;...
        sum(beban_wlingi_total(((16*3600)+1):(17*3600)))/3600;...
        sum(beban_wlingi_total(((17*3600)+1):(18*3600)))/3600;...
        sum(beban_wlingi_total(((18*3600)+1):(19*3600)))/3600;...
        sum(beban_wlingi_total(((19*3600)+1):(20*3600)))/3600;...
        sum(beban_wlingi_total(((20*3600)+1):(21*3600)))/3600;...
        sum(beban_wlingi_total(((21*3600)+1):(22*3600)))/3600;...
        sum(beban_wlingi_total(((22*3600)+1):(23*3600)))/3600;...
        sum(beban_wlingi_total(((23*3600)+1):(24*3600)))/3600];
    energi_wlingi = sum(beban_wlingi_total)/3600;
    
    outputArg.beban_sutami_1_mean = beban_sutami_1_mean;
    outputArg.beban_sutami_2_mean = beban_sutami_2_mean;
    outputArg.beban_sutami_3_mean = beban_sutami_3_mean;
    outputArg.energi_sutami_1 = energi_sutami_1;
    outputArg.energi_sutami_2 = energi_sutami_2;
    outputArg.energi_sutami_3 = energi_sutami_3;
    outputArg.energi_total_sutami = energi_total_sutami;
    outputArg.beban_wlingi_perjam = num2cell(beban_wlingi_perjam);
    outputArg.energi_wlingi = energi_wlingi;
end

