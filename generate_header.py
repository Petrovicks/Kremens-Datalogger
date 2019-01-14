import numpy as np

def generate_header(folder,filename,time,fpa,aux,geo=0):
    headerParameters = {}
    headerParameters['fileName'] = filename
    headerParameters['time'] = time
    headerParameters['fpa'] = fpa
    headerParameters['aux'] = aux
    headerParameters['geo'] = geo

    headerText = '''HEADER
    description = {fileName}
    time = {time}
    geo = {geo}
    fpa = {fpa}
    aux = {aux}'''.format(**headerParameters)

    headerFile = open(folder+'/'+filename+'.txt','w')
    headerFile.write(headerText)
    headerFile.close()

if __name__ == '__main__':
    generate_header('image', 5, np.ones((6,6)), np.ones((3,3))/4.0)
