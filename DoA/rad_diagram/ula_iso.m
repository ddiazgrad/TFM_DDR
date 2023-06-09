az = -180:180;
el = 0;
fc = 1090e6;
f = [1090e6 2.4e9 5.8e9];
antenna = phased.IsotropicAntennaElement( ...
    'FrequencyRange',[800e6 6e9]);
N = 7;

array = phased.ULA('NumElements',N,'ElementSpacing',0.05,...
    'Element',antenna);
figure (1)
viewArray(array,'ShowNormals',true)
figure(2)
pattern(array,f,az,el,'CoordinateSystem','polar','Type','powerdb',...
    'Normalize',true,'PropagationSpeed',physconst('LightSpeed'))