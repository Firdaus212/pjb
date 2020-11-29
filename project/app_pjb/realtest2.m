clc
clear all
start_time = tic();

%Wilayah Selorejo
data_waduk = xlsread('data_waduk','A2:B2386');
data_elevasi = data_waduk(:,1);
data_vol = data_waduk(:,2);
datae_beban = xlsread('data_beban','RAW','B4:AO4');
datae_elevasi = xlsread('data_beban','RAW','A5:A225');
datae_debit =xlsread('data_beban','RAW','B5:AO225');
data_simulasi = xlsread('datareal','datareal1','A2:D2');
real_h0= data_simulasi(:,1);
real_ht= data_simulasi(:,2);
real_qin= data_simulasi(:,3);
suplesi= data_simulasi(:,4);

sim_t1=10;
m1=[1 12 13 14 123 124 134 1234];
m2=[2 12 23 24 123 124 234 1234];
m3=[3 23 13 34 123 234 134 1234];
m4=[4 14 24 34 234 134 124 1234];
s1=[1 12 13 123];
s2=[2 12 23 123];
s3=[3 13 23 123];

for j=1:(length(data_elevasi)-1)
       data_vol2(j)=(data_vol(j)+data_vol(j+1))/2;
end

for xh0=1:length(real_h0)
    
    if real_h0(xh0)==0
        real_h0_new(xh0)=t_hj(xh0-1,(sim_t1*86400));
        vol_0(xh0)=t_vj(xh0-1,(sim_t1*86400));          
    else
        real_h0_new(xh0)=real_h0(xh0);
        
        for x_el=1:length(data_elevasi)
            if round(real_h0_new(xh0),2) == data_elevasi(x_el)
                vol_0(xh0)=data_vol(x_el);
            end
        end
        
    end
    
    for x_el=1:length(data_elevasi)
        if round(real_ht(xh0),2) == data_elevasi(x_el)
            vol_t(xh0)=data_vol(x_el);
        end
    end
    
%     real_h0_new(xh0)
%     vol_0(xh0)
%     vol_t(xh0)
    v_in(xh0)=(real_qin(xh0)*(sim_t1*86400));
    v_opr(xh0)=vol_0(xh0)-vol_t(xh0)+v_in(xh0);
    
%     v_opr(xh0)

    for e_el=1:length(datae_elevasi)
        if round(real_h0_new(xh0),1) == round(datae_elevasi(e_el),1)
            index_el0(xh0)=e_el;
        end
        if round(real_ht(xh0),1) == round(datae_elevasi(e_el),1)
            index_elt(xh0)=e_el;
        end
    end
    
%     index_el0
%     index_elt
    for e_p=1:length(datae_beban)
        if index_elt(xh0)==index_el0(xh0)
            Qeb(xh0,e_p)=datae_debit(index_elt(xh0),e_p);
        else
            Qeb(xh0,e_p)=mean(datae_debit(index_elt(xh0):index_el0(xh0),e_p));
        end    
    end
    
%     Qeb(xh0,e_p)=outflow tiap beban

   q_test(xh0)=v_opr(xh0)/(sim_t1*86400);
   if q_test(xh0)<Qeb(xh0,13)
       index_p(xh0)=13;
   else
       for i=14:40
           if Qeb(xh0,i)>q_test(xh0)
               index_p(xh0)=i-1;
               break;
           end
       end
   end
  
%    index_p(xh0)

   
   
   t_hj(xh0,1)=real_h0(xh0);
   t_qj(xh0,1)=datae_debit(index_el0(xh0),index_p(xh0));
   t_vj(xh0,1)=vol_0(xh0)-t_qj(xh0,1)+real_qin(xh0);
   
   for i=1:(sim_t1*86400)
       if i>1
           for m=1:length(datae_elevasi)
               if round(t_hj(xh0,i-1),1)==datae_elevasi(m)
                   t_qj(xh0,i)=datae_debit(m,index_p(xh0));
                   break;
               end
           end
       end
       
       if i>1
        t_vj(xh0,i)=t_vj(xh0,i-1)-t_qj(xh0,i)+real_qin(xh0);
       end
       
       for k=1:length(data_vol)
           if t_vj(xh0,i)>data_vol2(k)
               t_hj(xh0,i)=data_elevasi(k);
               break;
           end
       end
           
       
       if t_qj(xh0,i)>9.25
           limpas(xh0,i)= t_qj(xh0,i)-9.25;
           t_qm(xh0,i) = 9.25;
       else
           limpas(xh0,i)=0;
           t_qm(xh0,i) = t_qj(xh0,i);
       end
            
       
        on_m(xh0,1)=0;
        if t_qm(xh0,i)>=7.5
            Turbin_m(xh0,i) = 34;
            on_m(xh0,i)=2;
        elseif t_qm(xh0,i)<7.5 && t_qm(xh0,i)>=4.5
            Turbin_m(xh0,i) = 23;
            on_m(xh0,i)=2;
        else
            Turbin_m(xh0,i) = 4;
            on_m(xh0,i)=1;
        end   
        
        q_m_stok(xh0,i)=t_qm(xh0,i)/on_m(xh0,i);
        
        if ismember(Turbin_m(xh0,i),m1)
            Em_1(xh0,i)=((-223.34*(q_m_stok(xh0,i).^2))+(2834.7*q_m_stok(xh0,i))-3632)/1000;
        else
            Em_1(xh0,i)=0;
        end

        if ismember(Turbin_m(xh0,i),m2)
            Em_2(xh0,i)=((-94.658*(q_m_stok(xh0,i).^2))+(2062.3*q_m_stok(xh0,i))-2025.7)/1000;
        else
            Em_2(xh0,i)=0;
        end

        if ismember(Turbin_m(xh0,i),m3)
            Em_3(xh0,i)=((-91.518*(q_m_stok(xh0,i).^2))+(2071*q_m_stok(xh0,i))-2091.5)/1000;
        else
            Em_3(xh0,i)=0;
        end

        if ismember(Turbin_m(xh0,i),m4)
            Em_4(xh0,i)=((-130.28*(q_m_stok(xh0,i).^2))+(2276.5*q_m_stok(xh0,i))-2039.7)/1000;
        else
            Em_4(xh0,i)=0;
        end


        %Wilayah Siman,
        t_qs(xh0,i) = t_qm(xh0,i)+limpas(xh0);
        
        if t_qs(xh0,i)>=9
            Turbin_s(xh0,i) = 123;
            on_s(xh0,i)=3;
        elseif t_qs(xh0,i)<9 && t_qs(xh0,i)>=5.2
            Turbin_s(xh0,i) = 13;
            on_s(xh0,i)=2;
        else
            Turbin_s(xh0,i) = 23;
            on_s(xh0,i)=2;
        end
        
        q_s_stok(xh0,i)=t_qs(xh0,i)/on_s(xh0,i);

        if ismember(Turbin_s(xh0,i),s1)
            Es_1(xh0,i)=(-51.836*(q_s_stok(xh0,i).^2) + (1316*q_s_stok(xh0,i)) - 1045)/1000;
        else
            Es_1(xh0,i)=0;
        end

        if ismember(Turbin_s(xh0,i),s2)
            Es_2(xh0,i)=(-97.66*(q_s_stok(xh0,i).^2) + (1559.4*q_s_stok(xh0,i)) - 1307.1)/1000;
        else
            Es_2(xh0,i)=0;
        end

        if ismember(Turbin_s(xh0,i),s3)
            Es_3(xh0,i)=(-55.813*(q_s_stok(xh0,i).^2) + (1306.2*q_s_stok(xh0,i)) - 1307.1)/1000;
        else
            Es_3(xh0,i)=0;
        end
       
       
       
   end
   
   otpt_qj(xh0)=mean(t_qj(xh0,:));
   otpt_mw_j(xh0)=datae_beban(index_p(xh0));
   otpt_mwh_j(xh0)=otpt_mw_j(xh0)*24;
   otpt_limpas(xh0)=mean(limpas(xh0,:));
   otpt_qm(xh0)=mean(t_qm(xh0,:));
   otpt_mw_m1(xh0)=mean(Em_1(xh0,:));
   otpt_mw_m2(xh0)=mean(Em_2(xh0,:));
   otpt_mw_m3(xh0)=mean(Em_3(xh0,:));
   otpt_mw_m4(xh0)=mean(Em_4(xh0,:));
   otpt_mw_m(xh0)=(sum(Em_1(xh0,:))+sum(Em_2(xh0,:))+sum(Em_3(xh0,:))+sum(Em_4(xh0,:)))/(sim_t1*86400);
   otpt_mwh_m(xh0)=(sum(Em_1(xh0,:))+sum(Em_2(xh0,:))+sum(Em_3(xh0,:))+sum(Em_4(xh0,:)))/3600;
   otpt_qs(xh0)=mean(t_qs(xh0,:));
   otpt_mw_s1(xh0)=mean(Es_1(xh0,:));
   otpt_mw_s2(xh0)=mean(Es_2(xh0,:));
   otpt_mw_s3(xh0)=mean(Es_3(xh0,:));
   otpt_mw_s(xh0)=(sum(Es_1(xh0,:))+sum(Es_2(xh0,:))+sum(Es_3(xh0,:)))/(sim_t1*86400);
   otpt_mwh_s(xh0)=(sum(Es_1(xh0,:))+sum(Es_2(xh0,:))+sum(Es_3(xh0,:)))/3600;

   
   
   outpt(1,1)="inflow selorejo";
   outpt(1,2)="elevasi awal";
   outpt(1,3)="elevasi target";
   outpt(1,4)="elevasi akhir";
   outpt(1,5)="outflow selorejo";
   outpt(1,6)="MW selorejo";
   outpt(1,7)="MWh selorejo";
   outpt(1,8)="limpas";
   outpt(1,9)="inflow/outflow mendalan";
   outpt(1,10)="MW mendalan 1";
   outpt(1,11)="MW mendalan 2";
   outpt(1,12)="MW mendalan 3";
   outpt(1,13)="MW mendalan 4";
   outpt(1,14)="MW mendalan";
   outpt(1,15)="MWh mendalan";
   outpt(1,16)="suplesi siman";
   outpt(1,17)="inflow siman";
   outpt(1,18)="MW siman 1";
   outpt(1,19)="MW siman 2";
   outpt(1,20)="MW siman 3";
   outpt(1,21)="MW siman";
   outpt(1,22)="MWh siman";
   
   outpt((xh0+1),1)=real_qin(xh0);
   outpt((xh0+1),2)=real_h0_new(xh0);
   outpt((xh0+1),3)=real_ht(xh0);
   outpt((xh0+1),4)=t_hj(xh0,(sim_t1*86400));
   outpt((xh0+1),5)=otpt_qj(xh0);
   outpt((xh0+1),6)=otpt_mw_j(xh0);
   outpt((xh0+1),7)=otpt_mwh_j(xh0);
   outpt((xh0+1),8)=otpt_limpas(xh0);
   outpt((xh0+1),9)=otpt_qm(xh0);
   outpt((xh0+1),10)=otpt_mw_m1(xh0);
   outpt((xh0+1),11)=otpt_mw_m2(xh0);
   outpt((xh0+1),12)=otpt_mw_m3(xh0);
   outpt((xh0+1),13)=otpt_mw_m4(xh0);
   outpt((xh0+1),14)=otpt_mw_m(xh0);
   outpt((xh0+1),15)=otpt_mwh_m(xh0);
   outpt((xh0+1),16)=suplesi(xh0);
   outpt((xh0+1),17)=otpt_qs(xh0);
   outpt((xh0+1),18)=otpt_mw_s1(xh0);
   outpt((xh0+1),19)=otpt_mw_s2(xh0);
   outpt((xh0+1),20)=otpt_mw_s3(xh0);
   outpt((xh0+1),21)=otpt_mw_s(xh0);
   outpt((xh0+1),22)=otpt_mwh_s(xh0);
   
end
end_time = toc(start_time)