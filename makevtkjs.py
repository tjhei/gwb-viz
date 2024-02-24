import os
#import paraview
#paraview.compatibility.major = 5
#paraview.compatibility.minor = 10

from paraview.simple import *
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()


def make_vtkjs(output_name, input_files):
    print("producing ", output_name)

    renderView1 = GetActiveViewOrCreate('RenderView')

    inputs = []
    reprs = []
    for f in input_files:
        obj = XMLUnstructuredGridReader(registrationName=f, FileName=[f])
        repr = Show(obj, renderView1, 'UnstructuredGridRepresentation')
        inputs.append(obj)
        reprs.append(repr)
        ColorBy(repr, ('POINTS', 'Temperature'))
        # rescale color and/or opacity maps used to include current data range
        repr.RescaleTransferFunctionToDataRange(True, False)
    ExportView(output_name, view=renderView1, ParaViewGlanceHTML='')
    

if len(sys.argv)<3:
    error("Usage: output.vtkjs input1.vtu input2.vtu ...")

output_name = sys.argv[1]
inputs = sys.argv[2:]
os.remove(output_name)
make_vtkjs(output_name, inputs)
