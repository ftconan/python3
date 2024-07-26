"""
# @author: magician
# @file:   str2nc.py
# @date:   2024/7/25
"""
import netCDF4 as nc
import numpy as np


def str2nc(my_string):

    # 创建一个新的NetCDF文件
    nc_file = nc.Dataset('example.nc', 'w', format='NETCDF4')

    # 创建一个维度，因为字符串需要一个维度
    string_dim = nc_file.createDimension('string_dim', len(my_string))

    # 创建一个字符变量
    string_var = nc_file.createVariable('my_string', 'S1', ('string_dim',))

    # 将字符串转换为字节数组并写入变量
    string_var[:] = np.array(list(my_string), dtype='S1')

    # 添加一些属性（可选）
    # nc_file.description = '这是一个包含字符串的示例NetCDF文件。'

    # 关闭文件
    nc_file.close()

    print("NetCDF 文件已创建并保存为 'example.nc'")


def str2nc2(my_string, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        # 将字符串写入文件
        my_string = my_string.replace(' ', '')
        file.write(my_string)

    print(f"Text has been written to {filename}")


if __name__ == '__main__':
    s = 'H1*G71*M15*  X9953Y0*  M14*  X9942Y79*  X9871Y266*  X9840Y337*  X9782Y456*  X9724Y558*  X9688Y614*  X9608Y724*  X9566Y776*  X9476Y877*  X9428Y927*  X9301Y1045*  X9229Y1106*  X9091Y1215*  X8881Y1363*  M19*X8909Y1404*  M15*  X8881Y1363*  M14*  X8630Y1526*  X8458Y1629*  X8289Y1724*  X8123Y1809*  X7875Y1926*  X7707Y1998*  X7241Y2176*  M15*  X7241Y2176*  M14*  X7269Y2250*  X7268Y2349*  X7262Y2431*  X7246Y2527*  X7221Y2634*  X7169Y2787*  M19*X7216Y2805*  M15*  X7169Y2787*  M14*  X7130Y2862*  X7083Y2933*  X7059Y2961*  X7017Y3000*  X6926Y3063*  X6793Y3128*  X6759Y3199*  X7185Y3404*  X7451Y3533*  X7669Y3643*  X8098Y3869*  X8429Y4054*  X8671Y4199*  M19*X8697Y4157*  M15*  X8671Y4199*  M14*  X8738Y4242*  M19*X8765Y4200*  M15*  X8738Y4242*  M14*  X8967Y4398*  X9067Y4473*  X9188Y4572*  X9258Y4633*  X9390Y4762*  X9471Y4852*  X9527Y4921*  X9580Y4991*  X9677Y5139*  X9763Y5294*  X9800Y5373*  X9864Y5528*  X9917Y5683*  X9942Y5766*  X9954Y5845*  M15*  X9954Y5845*  M14*  X12099Y5520*  M19*X12091Y5471*  M15*  X12099Y5520*  M14*  X14460Y5163*  M15*  X14460Y5163*  M14*  X14460Y2906*  M19*X14410Y2906*  M15*  X14460Y2906*  M14*  X14460Y648*  M15*  X14460Y648*  M14*  X12212Y325*  X12099Y309*  M19*X12092Y358*  M15*  X12099Y309*  M14*  X9953Y0*  M15*M0*'
    # str2nc(s)

    str2nc2(s, 'example2.nc')
