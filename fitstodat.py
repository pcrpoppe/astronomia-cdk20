#!/usr/bin/env python

# ****************************************************************
# ***      Universidade Estadual de Feira de Santana           ***
# ***                  	  lss.py                               ***
# ***           Converte a .fits file in .dat file             ***
# ***             compliant to the LNA Standard                ***
# ***                    2018-Dec-28                           ***
# ***For questions contact: antonio.queiroz@ifbaiano.edu.br    ***
# ****************************************************************

import os
import numpy as np
from astropy.io import ascii as asci, fits as pyfits
from astropy.table import Table


def main():

    os.system("clear")
    print("                        LSS - THE LNA SPECTRUM TO STARLIGHT")
    print("")
    file_name = input("Insert the spectrum file: ")
    print("")
    file = pyfits.open(file_name)
	# pylint: disable=no-member
    hdu_list = file[0].header
    arq = file[0].data
    flux = arq[0][0]
    erro = arq[3][0]

    lamb_start = int(hdu_list['CRVAL1'])
    step = hdu_list['CD1_1']
    flux_length = len(flux)


    stop = lamb_start + step * flux_length
    stop = int(stop)


    new_length = stop - lamb_start
    wave = np.linspace(lamb_start, stop, new_length, dtype=int, endpoint=False)
    size_flux = len(flux)
    size = size_flux
    data_flux = flux


    xloc = np.arange(size)
    newsize = new_length
    new_xloc = np.linspace(0, size, newsize)
    new_flux = np.interp(new_xloc, xloc, data_flux)
    new_erro = np.interp(new_xloc, xloc, erro)

    wave_list = [] # Wave Column
    flux_list = [] # Flux Column
    erro_list = [] # Erro column
    zero_list = [] # zero column
    f_columns = [] # Full column

    for i in wave:
        wave_list.append(i)

    for i in new_flux:
        # i = i*2.5E-18/1000
        flux_list.append(i)

    for i in new_erro:
        # i = i*2.5E-18/1000
        erro_list.append(i)

    zero_list = []
    z_list = '0.000'
    for i in flux_list:
        zero_list.append(z_list)

    for i in range(0, len(new_flux)):
        if flux_list[i] != 0.0:
            z_list = [wave_list[i], flux_list[i], erro_list[i], zero_list[i]]
            f_columns.append(z_list)


    spectrum = np.array(f_columns)
    data = Table(spectrum, names=('Wave', 'Flux', 'Error', 'Zero'))
    # filename_1 = file_name[0:-5]
    filename_1 = input("Insert the name of output file: ") # Colocar nome sem o .dat
    asci.write(data, filename_1+".dat", delimiter='\t', format='no_header')
    print("            ######################### DONE #########################")
    print("")
    print("")

if __name__ == "__main__":
    main()
