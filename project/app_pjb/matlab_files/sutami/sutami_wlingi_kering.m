function [outputArg] = sutami_wlingi_k(input)
    warning('off');
    %% Input Value
    elevasi_awal = input.elevasi_awal;
    elevasi_akhir = input.elevasi_akhir;
    inflow_min = input.inflow_min;
    inflow_max = input.inflow_max;
    t1 = cell2mat(input.t1);
    t2 = cell2mat(input.t2);
    t3 = cell2mat(input.t3);

    elevasi_awal_wlingi = input.elevasi_awal_wlingi;
    beban_wlingi = input.beban_wlingi;
    jam_end = input.jam_end; %Jam akhir operasi.

    %% Waktu operasi total
    time = (t1(2)-t1(1))+t2(2)-t2(1)+t3(2)-t3(1);
    %% Data Sutami
    waduk_sutami = xlsread('data_waduk_sutami');
    elevasi_sutami = waduk_sutami(:,1);
    volume_sutami = waduk_sutami(:,2);
    waduk_lahor= xlsread('data_waduk_wlingi');
    elevasi_lahor = waduk_lahor(:,1);
    volume_lahor = waduk_lahor(:,2);
    data_beban = xlsread('data_operasi_sutami');
    elevasi = data_beban(:,1);
    discarge= data_beban(:,2);
    power= data_beban(:,3);
    %% Persamaan 
    f_vol_sutami=fit(elevasi_sutami,volume_sutami,'poly5');
    f_vol_lahor=fit(elevasi_lahor,volume_lahor,'poly5','robust','LAR');
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
    %% WLINGI
    q_wlingi = q_sutami;
    ell_wlingi_isi = elevasi_awal_wlingi;
    for b=1:(17*3600)  %Operasi mulai jam 17.00, apabila elevasi mencapai 163.5 sebelum jam 17.00, maka dioperasikan sebelum jam 17.00
        if ell_wlingi_isi<=163.5
            d_isi(b) = q_wlingi(b)/(360*3600);
            ell_wlingi_isi = ell_wlingi_isi+d_isi(b);
            index_el_w = b;
        else
            break;
        end
    end
    elevasi_wlingi = ell_wlingi_isi;
    for c=(index_el_w+1):length(q_wlingi)
        if elevasi_wlingi>=163.38
            swc_wlingi(c) = 5.3;
        elseif elevasi_wlingi<163.38 && elevasi_wlingi>=163.13
            swc_wlingi(c) = 5.375;
        elseif elevasi_wlingi<163.13 && elevasi_wlingi>=162.88
            swc_wlingi(c) = 5.45;
        elseif elevasi_wlingi<162.88 && elevasi_wlingi>=162.63
            swc_wlingi(c) = 5.563;
        elseif elevasi_wlingi<162.62 && elevasi_wlingi>=162.38
            swc_wlingi(c) = 5.675;
        elseif elevasi_wlingi<162.38 && elevasi_wlingi>=162.13
            swc_wlingi(c) = 5.788;
        else
            swc_wlingi(c) = 5.9;
        end
        d_out(c) = (q_wlingi(c)-(beban_wlingi*swc_wlingi(c)))/(360*3600); %berdasarkan persamaan swc data p.nur
        elevasi_wlingi = elevasi_wlingi+d_out(c);
    end

    %% Output Program
    beban_sutami_1_mean = sum(beban_sutami_1)/86400;
    beban_sutami_2_mean = sum(beban_sutami_2)/86400;
    beban_sutami_3_mean = sum(beban_sutami_3)/86400;
    energi_sutami_1 = sum(beban_sutami_1)/3600;
    energi_sutami_2 = sum(beban_sutami_2)/3600;
    energi_sutami_3 = sum(beban_sutami_3)/3600;
    energi_total_sutami = energi_sutami_1+energi_sutami_2+energi_sutami_3;
    beban_wlingi_komulatif = beban_wlingi;
    jam_start = index_el_w/3600;
    jam_mati = jam_end;
    elevasi_ketika_start = ell_wlingi_isi;
    elevasi_ketika_mati = elevasi_wlingi;
    
    %% Send output to python backend
    outputArg.beban_sutami_1_mean = beban_sutami_1_mean;
    outputArg.beban_sutami_2_mean = beban_sutami_2_mean;
    outputArg.beban_sutami_3_mean = beban_sutami_3_mean;
    outputArg.energi_sutami_1 = energi_sutami_1;
    outputArg.energi_sutami_2 = energi_sutami_2;
    outputArg.energi_sutami_3 = energi_sutami_3;
    outputArg.energi_total_sutami = energi_total_sutami;
    outputArg.beban_wlingi_komulatif = beban_wlingi_komulatif;
    outputArg.jam_start = jam_start;
    outputArg.jam_mati = jam_mati;
    outputArg.elevasi_ketika_start = elevasi_ketika_start;
    outputArg.elevasi_ketika_mati = elevasi_ketika_mati;
end