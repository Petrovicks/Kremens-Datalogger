#include <stdio.h>
#include "Lepton_I2C.h"
#include "leptonSDKEmb32PUB/LEPTON_SDK.h"
#include "leptonSDKEmb32PUB/LEPTON_SYS.h"
#include "leptonSDKEmb32PUB/LEPTON_Types.h"

bool _connected;

LEP_CAMERA_PORT_DESC_T _port;
LEP_SYS_FPA_TEMPERATURE_KELVIN_T fpa_temp_kelvin;
LEP_SYS_AUX_TEMPERATURE_KELVIN_T aux_temp_kelvin;
LEP_RESULT result;

int lepton_connect() {
        result = LEP_OpenPort(1, LEP_CCI_TWI, 400, &_port);
        _connected = true;
        printf("Connected, code: %i\n", result);
        return 0;
}

int lepton_temperature() {
        if(!_connected) {
                lepton_connect();
        }
        result = LEP_GetSysFpaTemperatureKelvin(&_port, &fpa_temp_kelvin);
        printf("FPA temp kelvin: %u , code %i\n", fpa_temp_kelvin, result);

        result = LEP_GetSysAuxTemperatureKelvin(&_port, &aux_temp_kelvin);
        printf("Aux temp kelvin: %u , code %i\n", aux_temp_kelvin, result);
        return 0;
}

void lepton_perform_ffc() {
        if(!_connected) {
                lepton_connect();
        }
        LEP_RunSysFFCNormalization(&_port);
}


int main(int argc, char *argv[])
{
   lepton_temperature();
   return 0;
}

//presumably more commands could go here if desired
