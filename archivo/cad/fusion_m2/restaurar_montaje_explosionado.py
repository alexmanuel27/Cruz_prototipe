"""Run in Fusion's Python API to restore the positions saved before the exploded view.
Do not run on a modified assembly without first preserving the changes.
"""
import adsk.core, adsk.fusion, json

def run(_context):
    app = adsk.core.Application.get()
    design = adsk.fusion.Design.cast(app.activeProduct)
    source = '/Users/alex/Nube /repos/Cruz_prototipe/archivo/cad/fusion_m2/restaurar_posiciones_explosionado.json'
    with open(source) as handle:
        records = json.load(handle)
    by_path = {o.fullPathName: o for o in design.rootComponent.allOccurrences}
    missing = [r['path'] for r in records if r['path'] not in by_path]
    if missing:
        raise RuntimeError('No se encontraron componentes: ' + ', '.join(missing))
    for record in records:
        matrix = adsk.core.Matrix3D.create()
        if not matrix.setWithArray(record['matrix']):
            raise RuntimeError('No se pudo leer la matriz de ' + record['path'])
        by_path[record['path']].transform2 = matrix
    app.activeViewport.fit()
    app.activeViewport.refresh()
    print('Montaje restaurado:', len(records), 'componentes')
