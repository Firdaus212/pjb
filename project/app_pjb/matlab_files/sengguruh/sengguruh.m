function outputArg = opt_sengguruh(input)
    %% Input Value
    inflow_min = input.inflow_min;%perkiraan inflow min pada hari tersebut
    inflow_max = input.inflow_max;%perkiraan inflow max pada hari tersebut
    inflow = inflow_min+(inflow_max-inflow_min).*rand(86400,1); %random value pada inflow terdistribusi normal pada interval min-max
    %%Perhitungan Beban
    for i=1:86400
        q_out(i) = inflow(i)/2; %pembagian debit pada setiap mesin
        %eff_1 = (2E-05*(q_out.^3)-0.0042*(q_out.^2)+0.2722*(q_out)+91.858)/100;
        %eff_2 = (4E-05*(q_out.^3)-0.0076*(q_out.^2)+0.4678*(q_out)+88.107)/100;
        beban_1(i) = q_out(i)/4.509422746;%SWC berdasarkan manual book
        beban_2(i) = q_out(i)/4.633817476;%SWC berdasarkan manual book
    end
    %Beban Total
    outputArg.beban_1_total= sum(beban_1)/86400; %output beban rata-rata mesin 1 (MW)
    outputArg.beban_2_total= sum(beban_2)/86400; %output beban rata-rata mesin 2 (MW)
    outputArg.energi_1= sum(beban_1)/(3600); %total energi perjam mesin 1(MWH)
    outputArg.energi_2= sum(beban_2)/(3600); %total energi perjam mesin 1(MWH)
    outputArg.q_mean = mean(q_out)*2; %rata-rata debit yang digunakan perdetik
end