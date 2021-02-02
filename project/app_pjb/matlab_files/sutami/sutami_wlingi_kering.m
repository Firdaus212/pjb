function outputArg = sutami_wlingi_kering(input)
    warning('off');
    %% Input Value
    elevasi_awal = input.elevasi_awal;
    elevasi_akhir = input.elevasi_akhir;
    inflow = input.inflow;
    t1 = cell2mat(input.t1);
    t2 = cell2mat(input.t2);
    t3 = cell2mat(input.t3);

    beban_wlingi = input.beban_wlingi;
    elevasi_real_wlingi = input.elevasi_real_wlingi;
    elevasi_target_wlingi = input.elevasi_target_wlingi;
    q_wlingi_yesterday = input.q_wlingi_yesterday;
    jam_mati_wlingi_kemarin = input.jam_mati_wlingi_kemarin;

    %% Waktu operasi total
    time = (t1(2)-t1(1))+t2(2)-t2(1)+t3(2)-t3(1);

    %% WILAYAH SUTAMI
    waduk_sutami = xlsread('data_waduk','waduk_sutami');
    elevasi_sutami = waduk_sutami(:,1);
    volume_sutami = waduk_sutami(:,2);
    waduk_lahor= xlsread('data_waduk','waduk_lahor');
    elevasi_lahor = waduk_lahor(:,1);
    volume_lahor = waduk_lahor(:,2);
    beban_sutami = xlsread('data_beban_sutami','2009');
    beban_elevasi = beban_sutami(1,:);
    beban_power = beban_sutami(:,1);

    %% Volume Tersedia
    vol_sutami = per_volume(elevasi_awal,elevasi_sutami,volume_sutami)-...
        per_volume(elevasi_akhir,elevasi_sutami,volume_sutami);
    vol_lahor = per_volume(elevasi_awal,elevasi_lahor,volume_lahor)-...
        per_volume(elevasi_akhir,elevasi_lahor,volume_lahor);
    vol_inflow = inflow*24*3600;
    vol_tersedia = vol_sutami+vol_lahor+vol_inflow;

    %% OPERASI SUTAMI
    if elevasi_awal==elevasi_akhir
        for aa=1:length(beban_elevasi)
            if elevasi_awal==beban_elevasi(aa)
                index_el_awal = aa;
            end
        end
        for bb=1:length(beban_power)
            q_out_rata_beban(bb) = beban_sutami(bb,index_el_awal);
            vol_digunakan(bb) = q_out_rata_beban(bb)*time*3600;
            if vol_digunakan(bb)<= vol_tersedia
                index_beban = bb;
                beban_mw = beban_power(bb);
            end
        end
        vol_dum=per_volume(elevasi_awal,elevasi_sutami,volume_sutami)+...
            per_volume(elevasi_awal,elevasi_lahor,volume_lahor);
        qt=q_out_rata_beban(index_beban);
        d_vol = 0;
        for cc=1:(24*3600)
           vol_sec(cc)=vol_dum+d_vol;
           vol_dum=vol_sec(cc);
           d_vol=inflow-qt;
           %% Operasi Turbin 1 Sutami
            if cc>=t1(1)*3600 && cc<=t1(2)*3600
                q_sec_1(cc)=q_out_rata_beban(index_beban);
                beban_sutami_1(cc)=beban_mw;
            else
                q_sec_1(cc)=0;
                beban_sutami_1(cc)=0;
            end
            %% Operasi Turbin 2 Sutami
            if cc>=t2(1)*3600 && cc<=t2(2)*3600
                q_sec_2(cc)=q_out_rata_beban(index_beban);
                beban_sutami_2(cc)=beban_mw;
            else
                q_sec_2(cc)=0;
                beban_sutami_2(cc)=0;
            end
            %% Operasi Turbin 3 Sutami
            if cc>=t3(1)*3600 && cc<=t3(2)*3600
                q_sec_3(cc)=q_out_rata_beban(index_beban);
                beban_sutami_3(cc)=beban_mw;
            else
                q_sec_3(cc)=0;
                beban_sutami_3(cc)=0;
            end
            %% Perubahan elevasi persecond
            q_sutami_sec(cc)=qt;
            qt=q_sec_1(cc)+q_sec_2(cc)+q_sec_3(cc);
            beban_sutami_sec(cc)=beban_sutami_1(cc)+beban_sutami_2(cc)...
                +beban_sutami_3(cc);
        end

    else %jika elevasi awal tidak sama dengan elevasi akhir
        %% debit rata-rata yang digunakan pada semua beban terhadap rentang elevasi tertentu
        interval = elevasi_akhir-elevasi_awal;
        interval_elevasi = round(abs(interval)/0.01);
        elevasi_0 = elevasi_awal;
        for a=1:interval_elevasi+1
            elevasi_operasi(a) = elevasi_0;
            if interval<0
                elevasi_0 = round((elevasi_operasi(a)-0.01),2);
            else
                elevasi_0 = round((elevasi_operasi(a)+0.01),2);
            end
        end
        for b=1:length(elevasi_operasi)
            for c=1:length(beban_elevasi)
                if elevasi_operasi(b)==beban_elevasi(c)
                    q_out(:,b)= beban_sutami(:,c);
                end
            end
        end

        %% Beban konstan yang optimal digunakan
        for d=1:length(beban_power)
            q_out_rata_beban(d) = mean(q_out(d,:));
            vol_digunakan(d) = q_out_rata_beban(d)*time*3600; %time=waktu operasi turbin (1+2+3)
            if vol_digunakan(d)<= vol_tersedia
                index_beban = d;
                beban_mw = beban_power(d);
            end
        end

        %% Volume komulatif pada elevasi tertentu
        for e=1:length(elevasi_operasi)
            vol_komulatif(e)= per_volume(elevasi_operasi(e),elevasi_sutami,volume_sutami)+...
                per_volume(elevasi_operasi(e),elevasi_lahor,volume_lahor);
        end

        %% Perubahan Elevasi dan Debit Per-detik
        q_temp_1= q_out(index_beban,:);
        %q_temp_2= q_out((index_beban+1),:);
        vol_dum=vol_komulatif(1);
        %vol_dum_2=vol_komulatif(1);
        qt=q_temp_1(1);
        %qu=q_temp_2(1);
        d_vol = 0;
        %d_vol_2 = 0;
        for f=1:(24*3600)
            vol_sec(f)= vol_dum+d_vol;
            vol_dum = vol_sec(f);
            d_vol = inflow - qt;
            %% Operasi Turbin 1 Sutami
            if f>=t1(1)*3600 && f<=t1(2)*3600
                for g=1:(length(q_temp_1)-1)
                    if vol_sec(f)<(vol_komulatif(g)+vol_komulatif(g+1))/2
                        q_sec_1(f)=q_temp_1(g);
                        break
                    else
                        q_sec_1(f)=q_temp_1(length(q_temp_1));
                    end
                end
                beban_sutami_1(f)=beban_mw;
            else
                q_sec_1(f)=0;
                beban_sutami_1(f)=0;
            end
            %% Operasi Turbin 2 Sutami
            if f>=t2(1)*3600 && f<=t2(2)*3600
                for h=1:(length(q_temp_1)-1)
                    if vol_sec(f)<(vol_komulatif(h)+vol_komulatif(h+1))/2
                        q_sec_2(f)=q_temp_1(h);
                        break
                    else
                        q_sec_2(f)=q_temp_1(length(q_temp_1));
                    end
                end
                beban_sutami_2(f)=beban_mw;
            else
                q_sec_2(f)=0;
                beban_sutami_2(f)=0;
            end
            %% Operasi Turbin 3 Sutami
            if f>=t3(1)*3600 && f<=t3(2)*3600
                for i=1:(length(q_temp_1)-1)
                    if vol_sec(f)<(vol_komulatif(i)+vol_komulatif(i+1))/2
                        q_sec_3(f)=q_temp_1(i);
                        break
                    else
                        q_sec_3(f)=q_temp_1(length(q_temp_1));
                    end
                end
                beban_sutami_3(f)=beban_mw;
            else
                q_sec_3(f)=0;
                beban_sutami_3(f)=0;
            end
            %% Perubahan elevasi persecond
            if interval<0
                for j=1:(length(elevasi_operasi)-1)
                    if vol_sec(f)>(vol_komulatif(j)+vol_komulatif(j+1))/2
                        elevasi_sec(f)=elevasi_operasi(j);
                        break
                    else
                        elevasi_sec(f)=elevasi_operasi(length(elevasi_operasi));
                    end
                end
            else
                for j=1:(length(elevasi_operasi)-1)
                    if vol_sec(f)<(vol_komulatif(j)+vol_komulatif(j+1))/2
                        elevasi_sec(f)=elevasi_operasi(j);
                        break
                    else
                        elevasi_sec(f)=elevasi_operasi(length(elevasi_operasi));
                    end
                end
            end
            q_sutami_sec(f)=qt;
            qt=q_sec_1(f)+q_sec_2(f)+q_sec_3(f);
            beban_sutami_sec(f)=beban_sutami_1(f)+beban_sutami_2(f)+beban_sutami_3(f);

        end
    end
    %% WILAYAH WLINGI
    %inflow_wlingi
    inflow_wlingi = q_sutami_sec;
    %rata-rata debit dalam jam
    q_wlingi_from_sutami = [mean(inflow_wlingi(1:3600));mean(inflow_wlingi(3601:7200));...
        mean(inflow_wlingi(7201:10800));mean(inflow_wlingi(10801:14400));...
        mean(inflow_wlingi(14401:18000));mean(inflow_wlingi(18001:21600));...
        mean(inflow_wlingi(21601:25200));mean(inflow_wlingi(25201:28800));...
        mean(inflow_wlingi(28801:32400));mean(inflow_wlingi(32401:36000));...
        mean(inflow_wlingi(36001:39600));mean(inflow_wlingi(39601:43200));...
        mean(inflow_wlingi(43201:46800));mean(inflow_wlingi(46801:50400));...
        mean(inflow_wlingi(50401:54000));mean(inflow_wlingi(54001:57600));...
        mean(inflow_wlingi(57601:61200));mean(inflow_wlingi(61201:64800));...
        mean(inflow_wlingi(64801:68400));mean(inflow_wlingi(68401:72000));...
        mean(inflow_wlingi(72001:75600));mean(inflow_wlingi(75601:79200));...
        mean(inflow_wlingi(79201:82800));mean(inflow_wlingi(82801:86400))];
    %delay operasi -> air mencapai PLTA wlingi 4 jam
    q_wlingi_today = [q_wlingi_yesterday;q_wlingi_yesterday;q_wlingi_yesterday;q_wlingi_yesterday;...
        q_wlingi_from_sutami];
    %waktu penampungan hingga elevasi max
    for k=1:length(q_wlingi_today)
        elevasi_real_wlingi = elevasi_real_wlingi+(q_wlingi_today(k)/360);
        if elevasi_real_wlingi>= 163.50
            break;
        end
    end
    %% waktu mencapai max_elevasi
    elevasi_operasi_wlingi = elevasi_real_wlingi;
    waktu_pengisian = k;
    jam_mulai_operasi_today=jam_mati_wlingi_kemarin+waktu_pengisian;
    %% waktu operasi wlingi
    for l=1:length(q_wlingi_today)
        if elevasi_operasi_wlingi>=163.38
            outflow = beban_wlingi*5.3;
        elseif elevasi_operasi_wlingi<163.38 && elevasi_operasi_wlingi>=163.13
            outflow = beban_wlingi*5.375;
        elseif elevasi_operasi_wlingi<163.13 && elevasi_operasi_wlingi>=162.88
            outflow = beban_wlingi*5.45;
        elseif elevasi_operasi_wlingi<162.88 && elevasi_operasi_wlingi>=162.63
            outflow = beban_wlingi*5.563;
        elseif elevasi_operasi_wlingi<162.62 && elevasi_operasi_wlingi>=162.38
            outflow = beban_wlingi*5.675;
        elseif elevasi_operasi_wlingi<162.38 && elevasi_operasi_wlingi>=162.13
            outflow = beban_wlingi*5.788;
        else
            outflow = beban_wlingi*5.9;
        end
        selisih_flow(l) = q_wlingi_today(waktu_pengisian+1)-outflow;
        elevasi_operasi_wlingi = elevasi_operasi_wlingi+(selisih_flow(l)/360);
        if elevasi_operasi_wlingi<= elevasi_target_wlingi
            break;
        end
    end
    waktu_operasi_wlingi = l;
    jam_mati_operasi_wlingi = jam_mulai_operasi_today+waktu_operasi_wlingi;
    %% CASCADE KOMULATIF
    vol_used = sum(q_sutami_sec);
    volume_sisa = vol_tersedia-vol_used;
    beban_total_sutami = sum(beban_sutami_sec)/3600;
    beban_total_wlingi = beban_wlingi*waktu_operasi_wlingi;
    energi_cascade=beban_total_sutami+beban_total_wlingi;

    %% Output Program
    outputArg.vol_tersedia = vol_tersedia;
    outputArg.vol_used = vol_used;
    outputArg.volume_sisa = volume_sisa;
    outputArg.mean_beban_sutami_1 = mean(beban_sutami_1);
    outputArg.mean_beban_sutami_2 = mean(beban_sutami_2);
    outputArg.mean_beban_sutami_3 = mean(beban_sutami_3);
    outputArg.sum_beban_sutami_1 = sum(beban_sutami_1)/3600;
    outputArg.sum_beban_sutami_2 = sum(beban_sutami_2)/3600;
    outputArg.sum_beban_sutami_3 = sum(beban_sutami_3)/3600;
    outputArg.beban_total_sutami = beban_total_sutami;
    outputArg.beban_total_wlingi = beban_total_wlingi;
    outputArg.jam_mulai_operasi_today = jam_mulai_operasi_today;
    outputArg.jam_mati_operasi_wlingi = jam_mati_operasi_wlingi;
    outputArg.waktu_operasi_wlingi = waktu_operasi_wlingi;
    outputArg.energi_cascade = energi_cascade;
end

