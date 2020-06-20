from sridentify import Sridentify
ident = Sridentify()
# from file
ident.from_file('/Users/olgabuchel/Downloads/ba_comunas/ba_comunas.prj')
print(ident.get_epsg())

'''
# from WKT
ident = Sridentify(prj="""GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137,298.257223563]],PRIMEM["Greenwich",0],UNIT["Degree",0.017453292519943295]])
ident.get_epsg()
4326/Users/olgabuchel/Downloads/ba_comunas/ba_comunas.prj 

'''
