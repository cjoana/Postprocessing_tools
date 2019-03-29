import h5py as h5
# import yt
import numpy as np
import os


N = 128
L = 128000

# def base attributes
component_names = [  # The order is important: component_0 ... component_nth
    'chi',
    'h11',
    'h12',
    'h13',
    'h22',
    'h23',
    'h33',
    'K',
    'A11',
    'A12',
    'A13',
    'A22',
    'A23',
    'A33',
    'Theta',
    'Gamma1',
    'Gamma2',
    'Gamma3',
    'lapse',
    'shift1',
    'shift2',
    'shift3',
    'B1',
    'B2',
    'B3',
    'phi',
    'Pi',
    'Ham',
    'Ham_ricci',
    'Ham_trA2',
    'Ham_K',
    'Ham_rho',
    'Mom1',
    'Mom2',
    'Mom3'
]
base_attrb = dict()
base_attrb['time'] = 0.0
base_attrb['iteration'] = 0
base_attrb['max_level'] = 0
base_attrb['num_components'] = len(component_names)
base_attrb['num_levels'] = 1
base_attrb['regrid_interval_0'] = 1
base_attrb['steps_since_regrid_0'] = 0
for comp,  name in enumerate(component_names):
    key = 'component_' + str(comp)
    tt = 'S' + str(len(name))
    base_attrb[key] = np.array(name, dtype=tt)


# def Chombo_global attributes
chombogloba_attrb = dict()
chombogloba_attrb['testReal'] = 0.0
chombogloba_attrb['SpaceDim']= 3


# def level0 attributes
level_attrb = dict()
level_attrb['dt']=  250.0
level_attrb['dx']=  1000.0
level_attrb['time']=  0.0
level_attrb['is_periodic_0']=  1
level_attrb['is_periodic_1']=  1
level_attrb['is_periodic_2']=  1
level_attrb['ref_ratio']=  2
level_attrb['tag_buffer_size']=  3
prob_dom = (0, 0, 0, 127, 127, 127)
prob_dt = np.dtype([('lo_i', '<i4'), ('lo_j', '<i4'), ('lo_k', '<i4'),
                    ('hi_i', '<i4'), ('hi_j', '<i4'), ('hi_k', '<i4')])
level_attrb['prob_domain']=  np.array(prob_dom, dtype=prob_dt)


# set dataset
temp_comp = np.zeros( (N, N, N))
dset=dict()
dset['lapse'] = temp_comp + 1.
dset['h11'] = temp_comp + 1.
dset['h22'] = temp_comp + 1.
dset['h33'] = temp_comp + 1.
dset['K'] = temp_comp + -5.94450679035e-06
dset['chi'] = temp_comp + 1.
dset['phi'] = temp_comp + 1.

boxes = np.array([(0, 0, 0, 127, 127, 127)],
      dtype=[('lo_i', '<i4'), ('lo_j', '<i4'), ('lo_k', '<i4'), ('hi_i', '<i4'), ('hi_j', '<i4'), ('hi_k', '<i4')])


""""
Prodution
"""

if os.path.exists("temp.3d.hdf5"):
    os.remove("temp.3d.hdf5")

h5file = h5.File('temp.3d.hdf5','w')  # New hdf5 file I want to create

# base attributes
for key in base_attrb.keys():
    h5file.attrs[key] = base_attrb[key]

# group: Chombo_global
chg = h5file.create_group('Chombo_global')
for key in chombogloba_attrb.keys():
    chg.attrs[key] = chombogloba_attrb[key]

# group: levels
l0 = h5file.create_group('level_0')
for key in level_attrb.keys():
    l0.attrs[key] = level_attrb[key]
sl0 = l0.create_group('data_attributes')
dadt = np.dtype([('intvecti', '<i4'), ('intvectj', '<i4'), ('intvectk', '<i4')])
sl0.attrs['ghost'] = np.array( (3, 3, 3),  dtype = dadt)
sl0.attrs['outputGhost'] = np.array( (0, 0, 0),  dtype = dadt)
sl0.attrs['comps'] = 35
sl0.attrs['objectType'] = np.array('FArrayBox', dtype='S10')

# level datasets
dataset = np.zeros( (base_attrb['num_components'], N, N, N))
for i, comp in enumerate(component_names):
    if comp in dset.keys():
        dataset[i] = dset[comp].T
fdset=[]
for c in range(base_attrb['num_components']):
    fc = dataset[c].T.flatten()
    fdset.extend(fc)
fdset = np.array(fdset)

box_dt = np.dtype([('lo_i', '<i4'), ('lo_j', '<i4'), ('lo_k', '<i4'), ('hi_i', '<i4'),
                ('hi_j', '<i4'), ('hi_k', '<i4')])
l0.create_dataset("Processors", data=np.array([0]))
l0.create_dataset("boxes",  data= boxes )
l0.create_dataset("data:offsets=0",  data=np.array([0, (base_attrb['num_components'])*N**3]))
l0.create_dataset("data:datatype=0",  data=fdset)




h5file.close()

