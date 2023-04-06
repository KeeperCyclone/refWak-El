import qualityOfLife as qol 

# table metadata for the columns

a1_vars = ['p','t','vf','vg','hf','hg','sf','sg']
a1_units = ['psia', 'degF', 'ft^3/lbm','ft^3/lbm','Btu/lbm','Btu/lbm','Btu/lbm-F','Btu/lbm-F']
a1_colidx = qol.listToDict(a1_vars,1)

a2_vars = ['t','p','vf','vg','hf','hg','sf','sg']
a2_units = [ 'degF', 'psia','ft^3/lbm','ft^3/lbm','Btu/lbm','Btu/lbm','Btu/lbm-F','Btu/lbm-F']
a2_colidx = qol.listToDict(a2_vars,1)

a4b_vars = ['p','p2','t','vf','vg','hf','hg','sf','sg']
a4b_units = ['bar','psia','degC','m^3/kg','m^3/kg','kJ/kg','kJ/kg','kJ/kg-K','kJ/kg-K']
a4b_colidx = qol.listToDict(a4b_vars,1)

a4a_vars = ['t','p','p2','vf','vg','hf','hg','sf','sg']
a4a_units = ['degC','bar','psia','m^3/kg','m^3/kg','kJ/kg','kJ/kg','kJ/kg-K','kJ/kg-K']
a4a_colidx = qol.listToDict(a4a_vars,1)

tableColDict = {
    'eng':
        {
        'px':a1_colidx,
        'tx':a2_colidx
        },
    'si':
        {
        'px':a4b_colidx,
        'tx':a4a_colidx
        }
    }

tableUnitDict = {
    'eng':
        {
        'px':a1_units,
        'tx':a2_units
        },
    'si':
        {
        'px':a4b_units,
        'tx':a4a_units
        }
    }


