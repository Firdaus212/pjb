function [outputArg1] = opt_sengguruh(input)
    inflow_sengguruh = input.inflow_sengguruh;
    %%Perhitungan Beban
    q_out = inflow_sengguruh/2;
    %eff_1 = (2E-05*(q_out.^3)-0.0042*(q_out.^2)+0.2722*(q_out)+91.858)/100;
    %eff_2 = (4E-05*(q_out.^3)-0.0076*(q_out.^2)+0.4678*(q_out)+88.107)/100;

    beban_1 = q_out/4.309422746;
    beban_2 = q_out/4.433817476;

    %Beban Total
    beban_1_tot = (beban_1*24);
    beban_2_tot = (beban_2*24);

    outputArg1.beban_1 = round(beban_1, 4);
    outputArg1.beban_2 = round(beban_2, 4);
    outputArg1.energi_1 = round(beban_1_tot, 4);
    outputArg1.energi_2 = round(beban_2_tot, 4);
    outputArg1.total_beban = round(beban_1 + beban_2, 4);
    outputArg1.total_energi = round(beban_1_tot + beban_2_tot, 4);
end