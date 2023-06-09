az = -180:180;
el = 0;
fc = 1091e6;
antenna = phased.IsotropicAntennaElement( ...
    'FrequencyRange',[800e6 6e9]);
f = [1091e6 2.4e9 5.8e9];
N = 8;
theta = 360/N;
thetarad = deg2rad(theta);

radius = 0.5;

ang = (0:N-1)*theta;
ang(ang >= 180.0) = ang(ang >= 180.0) - 360.0;

radius_variado = radius + radius * variacion * (rand(1, N) - 0.5);
ang_variado = ang + variacion * (rand(1, N) - 0.5) * theta;
ang_variado = wrapTo180(ang_variado);

array = phased.ConformalArray;
array.ElementPosition = [radius_variado.*cosd(ang_variado);...
    radius_variado.*sind(ang_variado);...
    zeros(1,N)];
array.ElementNormal = [ang_variado;zeros(1,N)];
figure (3)
viewArray(array,'ShowNormals',true)
view(0,90)
figure(2)
pattern(array,f,az,el,'CoordinateSystem','polar','Type','powerdb',...
    'Normalize',true,'PropagationSpeed',physconst('LightSpeed'))