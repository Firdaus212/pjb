function result = sms2(input)
    warning('off');
    h0 = input.h0;
    ht = input.ht;
    q_in = input.q_in;
    t = input.t;
    suplesi = input.suplesi;

    M = xlsread('performanceMS','mendalan','A1:K5');
    PM1 = M(:,1);
    QM1 = M(:,2);
    PM2 = M(:,4);
    QM2 = M(:,5);
    PM3 = M(:,7);
    QM3 = M(:,8);
    PM4 = M(:,10);
    QM4 = M(:,11);

    S = xlsread('performanceMS','siman','A1:H5');
    PS1 = S(:,1);
    QS1 = S(:,2);
    PS2 = S(:,4);
    QS2 = S(:,5);
    PS3 = S(:,7);
    QS3 = S(:,8);

    data_waduk = xlsread('data_waduk','aa','A2:B240');
    data_elevasi = data_waduk(:,1);
    data_vol = data_waduk(:,2);
    data_waduk = xlsread('abb','A2:C5991');
    H = data_waduk(:,1);
    Q = data_waduk(:,2);
    P = data_waduk(:,3);
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
    Ps1=fit(QS1,PS1,'poly4');
    Ps2=fit(QS2,PS2,'poly4');
    Ps3=fit(QS3,PS3,'poly4');
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
    else
        Pm_1=0;
    end

    if ismember(Turbin_m,m2)
        Pm_2=Pm2(q_m_stok);
    else
        Pm_2=0;
    end

    if ismember(Turbin_m,m3)
        Pm_3=Pm3(q_m_stok);
    else
        Pm_3=0;
    end

    if ismember(Turbin_m,m4)
        Pm_4=Pm4(q_m_stok);
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
    else
        Ps_1=0;
    end

    if ismember(Turbin_s,s2)
        Ps_2=Ps2(q_s_stok);
    else
        Ps_2=0;
    end

    if ismember(Turbin_s,s3)
        Ps_3=Ps3(q_s_stok);
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

