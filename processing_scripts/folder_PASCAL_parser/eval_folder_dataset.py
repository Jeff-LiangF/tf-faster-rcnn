# -*- coding: utf-8 -*-

'''Columns in folder_PASCAL.xlsx:
    img_id : The id of the picture
    xmin : The xmin of the bounding box
    ymin : The ymin of the bounding box
    xmax : The xmax of the bounding box
    ymax : The ymax of the bounding box
    xlen : The width of the bounding box
    ylen : The height of the bounding box
    ratio : Height(ylen)/Width(xlen) ratio of the bounding box
    scale : Default receptive field is 16, scale = sqrt(xlen*ylen)/16
'''
import xml.etree.ElementTree as ET
import pandas as pd
import os
import numpy as np
import math
# import matplotlib.pyplot as plt
def GetBboxInfo(xml_path):
    tree = ET.parse(xml_path)
    root = tree.getroot()
    df = pd.DataFrame(columns=['img_id', 'xmin', 'ymin', 'xmax', 'ymax', 'xlen', 'ylen', 'ratio']) # Ratio h/w
    for bbox in root.iter('bndbox'):
        attrib = []
        attrib.append(xml_path[-8:-4])
        for axis in bbox:
            attrib.append(axis.text)
        attrib.append(int(attrib[3]) - int(attrib[1]))
        attrib.append(int(attrib[4]) - int(attrib[2]))
        attrib.append(float(attrib[6])/float(attrib[5]))
        df.loc[len(df)] = attrib
    return df

if __name__ == '__main__':

    if(os.path.exists('./folder_PASCAL.xlsx')):
        df = pd.read_excel('./folder_PASCAL.xlsx')
        #### The histogram of folder scale
        # n, bins, patches = plt.hist(df['scale'], bins=20, range =(4,14), density=True)
        # plt.xlabel('Scale')
        # plt.ylabel('Density') 
        # plt.title('Distribution of Folder Scale')
        #### The histogram of folder ratio
        n, bins, patches = plt.hist(df['ratio'], bins=20, range =(3,8),facecolor='green', density=True)
        plt.xlabel('Ratio')
        plt.ylabel('Density') 
        plt.title('Distribution of Folder Height/Width Ratio')
        plt.show()
        pass
    else:
        df = pd.DataFrame(columns=['img_id', 'xmin', 'ymin', 'xmax', 'ymax', 'xlen', 'ylen', 'ratio'])
        for _, _, xml_files in os.walk('./Annotations'):
            for xml_file in xml_files:
                xml_path = os.path.join('./Annotations', xml_file)
                df2 = GetBboxInfo(xml_path)
                # print(df2.head())
                df = df.append(df2, ignore_index=True)
        df['scale'] = pd.Series(((df['xlen']*df['ylen']).apply(math.sqrt))/16)
        writer = pd.ExcelWriter('./folder_PASCAL.xlsx')
        df.to_excel(writer,'Sheet1')
        writer.save()

