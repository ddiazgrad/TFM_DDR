fs = 8000; 
t = (0:1/fs:1).'; 
f1 = 10;
x1 = cos(2*pi*t*f1);

fsig = 1090e6;

antenna = phased.IsotropicAntennaElement( ...
    'FrequencyRange',[800e6 10e9]);
N = 8;
theta = 360/N;
thetarad = deg2rad(theta);

radius = 0.5;

ang = (0:N-1)*theta;
ang(ang >= 180.0) = ang(ang >= 180.0) - 360.0;

array = phased.ConformalArray('Element',antenna);
array.ElementPosition = [radius.*cosd(ang);...    
radius.*sind(ang);...   
zeros(1,N)];
array.ElementNormal = [ang;zeros(1,N)];


angles = -175:1:175;
num_runs = 100;
angle_diff = zeros(length(angles), num_runs);


estimator = phased.MUSICEstimator2D('SensorArray',array,...
    'OperatingFrequency',fsig,...
    'NumSignalsSource','Property',...
    'DOAOutputPort',true,...
    'AzimuthScanAngles',-180:0.001:180);


SNR_dB = 10;
Ps = norm(x1)^2;
SNR = 10^(10/10);
Pn = Ps/SNR;

max_diff = zeros(length(angles), 1);
rmse_angles = zeros(length(angles), 1);
for i = 1:length(angles)
    doa1(1) = angles(i);
    
    for j = 1:num_runs
        x = collectPlaneWave(array,x1,doa1,fsig);

        noise = sqrt(Ps/Pn)*(randn(size(x))+1i*randn(size(x)));

        [~,doas] = estimator(x + noise);


        angle_diff(i, j) = doas(1) - doa1(1);
        
        if abs(angle_diff(i, j)) > 180
            angle_diff(i, j) = angle_diff(i, j) - sign(angle_diff(i, j)) * 360;
        end
        
    end
    rmse_angles(i) = sqrt(mean(angle_diff(i,:).^2));
    max_diff(i) = max(abs(angle_diff(i,:)));
end
percentile_70 = prctile(abs(angle_diff), 70, 2);
for i = 1:length(angles)
    
    rmse_angles_70(i) = sqrt(mean(percentile_70(i,:).^2));
end

figure(1);
plot(angles, rmse_angles_70, 'g--', 'LineWidth', 1.5);
xlabel('Azimuth');
ylabel('70th Percentile of RMSE (degrees)');

figure(2);
plot(angles, rmse_angles);
xlabel('Azimuth');
ylabel('RMSE');

figure(3);
plot(angles, max_diff);
xlabel('Azimuth');
ylabel('Estimated maximum angle difference (degrees)');

figure (4);
plot(angles, abs(angle_diff));
xlabel('Azimuth');
ylabel('Estimated angle difference (degrees)');