function result = sms2(input)
    warning('off')
    h0 = input.h0;
    ht = input.ht;
    q_in = input.q_in;
    t = input.t;
    suplesi = input.suplesi;

    Mendalan = readmatrix('Performance Mendalan.xlsx','Sheet','Mendalan','Range','A2:H2000');
    PM1 = Mendalan(isfinite(Mendalan(:, 1)), 1);
    QM1 = Mendalan(isfinite(Mendalan(:, 2)), 2);
    PM2 = Mendalan(isfinite(Mendalan(:, 3)), 3);
    QM2 = Mendalan(isfinite(Mendalan(:, 4)), 4);
    PM3 = Mendalan(isfinite(Mendalan(:, 5)), 5);
    QM3 = Mendalan(isfinite(Mendalan(:, 6)), 6);
    PM4 = Mendalan(isfinite(Mendalan(:, 7)), 7);
    QM4 = Mendalan(isfinite(Mendalan(:, 8)), 8);

    Siman = readmatrix('Performance Siman.xlsx','Sheet','Siman','Range','A2:F2000');
    PS1 = Siman(isfinite(Siman(:, 1)), 1);
    QS1 = Siman(isfinite(Siman(:, 2)), 2);
    PS2 = Siman(isfinite(Siman(:, 3)), 3);
    QS2 = Siman(isfinite(Siman(:, 4)), 4);
    PS3 = Siman(isfinite(Siman(:, 5)), 5);
    QS3 = Siman(isfinite(Siman(:, 6)), 6);

    data_waduk_SJ = readmatrix('Elevasi X Volume Selorejo.xlsx','Sheet','ElevasixVolume Selorejo','Range','A2:B2000');
    data_elevasi = data_waduk_SJ(isfinite(data_waduk_SJ(:, 1)), 1);
    data_vol = data_waduk_SJ(isfinite(data_waduk_SJ(:, 2)), 2);
    data_Performance_selorejo = readmatrix('Performance Selorejo.xlsx','Sheet','Selorejo','Range','A2:C20000');
    H = data_Performance_selorejo(isfinite(data_Performance_selorejo(:, 1)), 1);
    Q = data_Performance_selorejo(isfinite(data_Performance_selorejo(:, 2)), 2);
    P = data_Performance_selorejo(isfinite(data_Performance_selorejo(:, 3)), 3);
    m1=[1 12 13 14 123 124 134 1234];
    m2=[2 12 23 24 123 124 234 1234];
    m3=[3 23 13 34 123 234 134 1234];
    m4=[4 14 24 34 234 134 124 1234];
    s1=[1 12 13 123];
    s2=[2 12 23 123];
    s3=[3 13 23 123];
    vol=fit(data_elevasi,data_vol,'poly5');
    ele=fit(data_vol,data_elevasi,'poly9');
    fQ=fit([H, P],Q,'poly55');
    fP=fit([H, Q],P,'poly54');
    Pm1=fit(QM1,PM1,'poly4');
    Pm2=fit(QM2,PM2,'poly4');
    Pm3=fit(QM3,PM3,'poly4');
    Pm4=fit(QM4,PM4,'poly4');
    Ps1=fit(QS1,PS1,'poly5');
    Ps2=fit(QS2,PS2,'poly5');
    Ps3=fit(QS3,PS3,'poly5');
    v0=vol(h0);
    vt=vol(ht);
    vop=v0-vt+(q_in*t*3600);


    Qout=vop/(3600*t);       
    V0(1)=vol(h0);
    H0(1)=613.17;
    Pm=0;
    if Qout > 9.25
        limpas = Qout-9.25;
    else limpas = 0;
    end
    for i=1:t
        pSj(i)=fP(H0(i),Qout);
        V0(i+1)=V0(i)+(3600*(q_in-Qout));
        H0(i+1)=ele(V0(i+1));
    end
    PSj=round(mean(pSj),1);
    ESj=round(sum(pSj),2);
    if Qout>=7.5
        Turbin_m = 24;
        on_m=2;
    elseif Qout<7.5 && Qout>=4.5
        Turbin_m = 23;
        on_m=2;
    else
        Turbin_m = 4;
        on_m=1;
    end   
    Qin_m=(Qout-limpas);
    q_m_stok=Qin_m/on_m;

    if ismember(Turbin_m,m1)
        Pm_1=Pm1(q_m_stok);
        if or(Pm_1>5.5 ,Pm_1<0)
            Pm_1=5.5;
        end
    else
        Pm_1=0;
    end

    if ismember(Turbin_m,m2)
        Pm_2=Pm2(q_m_stok);
        if or(Pm_2>5.5 ,Pm_2<0)
            Pm_2=5.5;
        end
    else
        Pm_2=0;
    end

    if ismember(Turbin_m,m3)
        Pm_3=Pm3(q_m_stok);
        if or(Pm_3>5.5 ,Pm_3<0)
            Pm_3=5.5;
        end
    else
        Pm_3=0;
    end

    if ismember(Turbin_m,m4)
        Pm_4=Pm4(q_m_stok);
        if or(Pm_4>5.5 ,Pm_4<0)
            Pm_4=5.5;
        end
    else
        Pm_4=0;
    end

    Pm=Pm_1+Pm_2+Pm_3+Pm_4;
    Em= round((t*Pm),2);


    if Qout>=9
        Turbin_s = 123;
        on_s=3;
    elseif Qout<9 && Qout>=5.2
        Turbin_s = 13;
        on_s=2;
    else
        Turbin_s = 23;
        on_s=2;
    end
    Qin_smn = Qin_m + suplesi;
    q_s_stok=Qin_smn/on_s;

    if ismember(Turbin_s,s1)
        Ps_1=Ps1(q_s_stok);
        if or(Ps_1>3.6 ,Ps_1<0)
            Ps_1=3.6;
        end
    else
        Ps_1=0;
    end

    if ismember(Turbin_s,s2)
        Ps_2=Ps2(q_s_stok);
        if or(Ps_2>3.6 ,Ps_2<0)
            Ps_2=3.6;
        end
    else
        Ps_2=0;
    end

    if ismember(Turbin_s,s3)
        Ps_3=Ps3(q_s_stok);
        if or(Ps_3>3.6 ,Ps_3<0)
            Ps_3=3.6;
        end
    else
        Ps_3=0;
    end

    Psmn=Ps_1+Ps_2+Ps_3;
    Esmn= round((t*Psmn),2);

    result = [];
    result.inflow = q_in;
    result.elevasi_awal = h0;
    result.elevasi_akhir = H0(t);
    result.outflow_selorejo = Qout;
    result.daya_output_selorejo = PSj;
    result.energi_output_selorejo = ESj;
    result.inflow_mendalan = Qin_m;
    result.daya_output_mendalan_1 = round(Pm_1,1);
    result.daya_output_mendalan_2 = round(Pm_2,1);
    result.daya_output_mendalan_3 = round(Pm_3,1);
    result.daya_output_mendalan_4 = round(Pm_4,1);
    result.total_daya_output_mendalan = round(Pm,1);
    result.energi_output_mendalan = Em;
    result.suplesi = suplesi;
    result.inflow_siman = Qin_smn;
    result.daya_output_siman_1 = round(Ps_1,1);
    result.daya_output_siman_2 = round(Ps_2,1);
    result.daya_output_siman_3 = round(Ps_3,1);
    result.total_daya_output_siman = round(Psmn, 1);
    result.energi_output_siman = Esmn;
end

