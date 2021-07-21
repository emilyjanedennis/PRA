# -*- coding: utf-8 -*-
"""

@author: ejdennis with serious borrowing from wanglab
"""

import os, sys, csv, json, shutil, cv2, pickle
import numpy as np
import pandas as pd
import SimpleITK as sitk
import subprocess as sp
from collections import Counter
import tifffile as tif
from utils.imageprocessing import resample_par, color_movie_merger, resample
from utils.imageprocessing import gridcompare, combine_images
from utils.io import makedir, removedir, writer, load_kwargs, convert_to_mhd


def find_downsized_files(src):
    if os.path.exists(os.path.join(src,'reg__downsized_for_atlas.tif')):
        output_src = src
    elif os.path.exists(os.path.join(os.path.dirname(src),'reg__downsized_for_atlas.tif')):
        output_src = os.path.dirname(src)
    else:
        output_src = os.path.dirname(os.path.dirname(src))
    return output_src

def points_resample(src, original_dims, resample_dims, verbose=False):
    """Function to adjust points given resizing by generating a transform matrix

    ***Assumes ZYX and that any orientation changes have already been done.***

    src: numpy array or list of np arrays of dims nx3
    original_dims (tuple)
    resample_dims (tuple)
    """
    src = np.asarray(src)
    assert src.shape[-1] == 3, "src must be a nx3 array"

    # initialize
    d1, d2 = src.shape
    nx4centers = np.ones((d1, d2+1))
    nx4centers[:, :-1] = src

    # acount for resampling by creating transformmatrix
    zr, yr, xr = resample_dims
    z, y, x = original_dims

    # apply scale diff
    trnsfrmmatrix = np.identity(4)*(zr/float(z), yr/float(y), xr/float(x), 1)
    if verbose:
        sys.stdout.write("trnsfrmmatrix:\n{}\n".format(trnsfrmmatrix))

    # nx4 * 4x4 to give transform
    trnsfmdpnts = nx4centers.dot(trnsfrmmatrix)  # z,y,x
    if verbose:
        sys.stdout.write("first three transformed pnts:\n{}\n".format(trnsfmdpnts[0:3]))

    return trnsfmdpnts



def transform_points(src, dst, transformfiles, resample_points=False):
    """

    Inputs
    ---------
    src = numpy file consiting of nx3 (ZYX points)
    dst = folder location to write points
    transformfiles =
        list of all elastix transform files used, and in order of the original transform****
    resample_points = [original_dims, resample_dims] if there was resampling done, use this here
    param_dictionary_for_reorientation = param_dictionary for lightsheet package to use for reorientation
    """
    # load
    cells = np.load(src)
    # optionally resample points
    if resample_points:
        original_dims, resample_dims = resample_points
        cells = points_resample(cells, original_dims, resample_dims)

    # generate text file
    pretransform_text_file = create_text_file_for_elastix(cells, dst)

    # copy over elastix files
    transformfiles = modify_transform_files(transformfiles, dst)

    # run transformix on points
    points_file = point_transformix(pretransform_text_file, transformfiles[-1], dst)

    # convert registered points into structure counts
    unpack_pnts(points_file, dst)

    return




def create_text_file_for_elastix(src, dst):
    """

    Inputs
    ---------
    src = numpy file consiting of nx3 (ZYX points)
    dst = folder location to write points
    """

    print("This function assumes ZYX centers...")

    # setup folder
    if not os.path.exists(dst):
        os.mkdir(dst)

    # create txt file, with elastix header, then populate points
    pth = os.path.join(dst, "zyx_points_pretransform.txt")

    # load
    if type(src) == np.ndarray:
        arr = src
    else:
        arr = np.load(src) if src[-3:] == "npy" else loadmat(src)["cell_centers_orig_coord"]

    # convert
    stringtowrite = "\n".join(["\n".join(["{} {} {}".format(i[0], i[1], i[2])])
                               for i in arr])

    # write file
    sys.stdout.write("writing centers to transfomix input points text file...")
    sys.stdout.flush()
    with open(pth, "w+") as fl:
        fl.write("index\n{}\n".format(len(arr)))
        fl.write(stringtowrite)
        fl.close()
    sys.stdout.write("...done writing centers\n")
    sys.stdout.flush()

    return pth


def modify_transform_files(transformfiles, dst):
    """Function to copy over transform files, modify paths in case registration was done on the cluster, and tether them together

        Inputs
    ---------
    transformfiles =
        list of all elastix transform files used, and in order of the original transform****

    """

    # new
    ntransformfiles = [os.path.join(dst, "order{}_{}".format(
        i, os.path.basename(xx))) for i, xx in enumerate(transformfiles)]

    # copy files over
    [shutil.copy(xx, ntransformfiles[i]) for i, xx in enumerate(transformfiles)]

    # modify each with the path
    for i, pth in enumerate(ntransformfiles):

        # skip first
        if i != 0:

            # read
            with open(pth, "r") as fl:
                lines = fl.readlines()
                fl.close()

            # copy
            nlines = lines

            # iterate
            for ii, line in enumerate(lines):
                if "(InitialTransformParametersFileName" in line:
                    nlines[ii] = "(InitialTransformParametersFileName {})\n".format(
                        ntransformfiles[i-1])

            # write
            with open(pth, "w") as fl:
                for nline in lines:
                    fl.write(str(nline))
                fl.close()

    return ntransformfiles


def point_transformix(pretransform_text_file, transformfile, dst):
    """apply elastix transform to points


    Inputs
    -------------
    pretransform_text_file = list of points that already have resizing transform
    transformfile = elastix transform file
    dst = folder

    Returns
    ---------------
    trnsfrm_out_file = pth to file containing post transformix points

    """
    sys.stdout.write("\n***********Starting Transformix***********")
    from subprocess import check_output
    # set paths
    trnsfrm_out_file = os.path.join(dst, "outputpoints.txt")

    # run transformix point transform
    call = "transformix -def {} -out {} -tp {}".format(pretransform_text_file, dst, transformfile)
    print(check_output(call, shell=True))
    sys.stdout.write("\n   Transformix File Generated: {}".format(trnsfrm_out_file))
    sys.stdout.flush()
    return trnsfrm_out_file



def get_transform_files_from_folder(transformfolder):
    transformfiles=[]
    for file in os.listdir(transformfolder):
        if "TransformParam" in file:
            transformfiles.append(os.path.join(transformfolder,file))
            transformfiles = transformfiles.sort()
    return transformfiles



def unpack_pnts(points_file, dst):
    """
    function to take elastix point transform file and return anatomical locations of those points

    Here elastix uses the xyz convention rather than the zyx numpy convention

    Inputs
    -----------
    points_file = post_transformed file, XYZ

    Returns
    -----------
    dst_fl = path to numpy array, ZYX

    """

    # inputs
    assert type(points_file) == str
    point_or_index = 'OutputPoint'

    # get points
    with open(points_file, "r") as f:
        lines = f.readlines()
        f.close()

    # populate post-transformed array of contour centers
    sys.stdout.write("\n\n{} points detected\n\n".format(len(lines)))
    arr = np.empty((len(lines), 3))
    for i in range(len(lines)):
        arr[i, ...] = lines[i].split()[lines[i].split().index(point_or_index) +
                                       3:lines[i].split().index(point_or_index)+6]  # x,y,z

    # optional save out of points
    dst_fl = os.path.join(dst, "posttransformed_zyx_voxels.npy")
    np.save(dst_fl, np.asarray([(z, y, x) for x, y, z in arr]))

    # check to see if any points where found
    print("output array shape {}".format(arr.shape))

    return dst_fl


def elastix_wrapper(jobid, cores=5, **kwargs):
    '''Wrapper to handle most registration operations.

    jobid =
        0: 'normal registration'
        1: 'cellchannel inverse'
        2: 'injchannel inverse'
    '''
    # inputs
    kwargs = load_kwargs(**kwargs)
    sys.stdout.write('\nElastix in:\n')
    sys.stdout.flush()
    os.system('which elastix')

    # 'normal' registration
    if jobid == 0:
        elastix_registration(jobid, cores=cores, **kwargs)

    # cellchannel inverse
    if jobid == 1:
        make_inverse_transform(
            [xx for xx in kwargs['volumes']][0], cores=cores, **kwargs)

    return


def elastix_registration(jobid, cores=5, **kwargs):
    '''Function to take brainvolumes and register them to
    AtlasFiles using elastix parameters in parameterfolder.
    Inputs
    ---------------
    cores = for parallelization

    optional kwargs:
    secondary_registration (optional):
        False (default) - apply transform determined from
        regch->atlas to other channels
        True - register other channel(s) to regch then apply
        transform determined from regch->atlas
        (useful if imaging conditions were different between
        channel and regch, i.e. added horizontal foci, sheet na...etc)
        kwargs overrides explicit 'secondary_registration' input to function


    Required inputs via kwargs:
            brainname='AnimalID'
            brainpath= pathtofolder
            AtlasFile=pathtoatlas ###atlas is a tif stack
            parameterfolder ##contains parameter files: Order1_filename.txt,
            Order2_filename.txt,....
            svlc=pathtosavedirectory
            maskfile(optional)=creates a nested folder inside svlc and runs
            registration with mask
    To run in parallel use: parallel_elastixlooper
  '''

    # inputs
    outdr = kwargs['outputdirectory']
    kwargs = load_kwargs(outdr)
    AtlasFile = kwargs['AtlasFile']

    # make variables for volumes:
    vols = kwargs['volumes']
    reg_vol = [xx for xx in vols if xx.ch_type == 'regch'][0]

    # images need to have been stitched, resized,
    # and saved into single tiff stack
    # resize to ~220% total size of atlas (1.3x/dim)
    sys.stdout.write('Beginning registration on {}'.format(reg_vol.brainname))
    sys.stdout.flush()
    reg_vol.add_resampled_for_elastix_vol(
        reg_vol.downsized_vol+'_resampledforelastix.tif')
    if not os.path.exists(reg_vol.resampled_for_elastix_vol):
        sys.stdout.write('\n   Resizing {}'.format(reg_vol.downsized_vol))
        sys.stdout.flush()
        resample_par(cores, reg_vol.downsized_vol+'.tif', AtlasFile,
                     svlocname=reg_vol.resampled_for_elastix_vol,
                     singletifffile=True, resamplefactor=1.4)
        [vol.add_registration_volume(
            reg_vol.resampled_for_elastix_vol) for vol in vols]
        sys.stdout.write('...completed resizing\n')
        sys.stdout.flush()

    # find elastix parameters files and sort, set up parameters and logfiles
    parameters = []
    [parameters.append(
        os.path.join(reg_vol.parameterfolder, files)) for files in os.listdir(
        reg_vol.parameterfolder) if files[0] != '.' and files[-1] != '~']
    parameters.sort()
    svlc = os.path.join(outdr, 'elastix')
    makedir(svlc)
    writer(svlc, 'Starting elastix...AtlasFile: {}\n   parameterfolder: {}\n   svlc: {}\n'.format(
        AtlasFile, reg_vol.parameterfolder, svlc))
    writer(svlc, 'Order of parameters used in Elastix:{}\n...\n\n'.format(parameters))

    # optionally generate MHD file for better scaling in elastix (make both mhds if present since one tiff and one mhd doesn't work well)
    resampled_zyx_dims = False
    if False and 'atlas_scale' in kwargs:
        atlasfilecopy = AtlasFile
        AtlasFile = convert_to_mhd(AtlasFile, dims=kwargs['atlas_scale'], dst=os.path.join(
            kwargs['outputdirectory'], os.path.splitext(os.path.basename(kwargs['AtlasFile']))[0])+'.mhd')
        # copy reg vol and calculate effective distance/pixel scale
        reg_volcopy = reg_vol.resampled_for_elastix_vol
        resampled_zyx_dims = [cc*dd for cc, dd in zip(kwargs['xyz_scale'][::-1], [float(bb) / float(
            aa) for aa, bb in zip(tifffile.imread(reg_vol.resampled_for_elastix_vol).shape, reg_vol.fullsizedimensions)])]
        # note convert_to_mhd dims are in XYZ
        reg_vol.add_resampled_for_elastix_vol(convert_to_mhd(reg_vol.resampled_for_elastix_vol, dims=resampled_zyx_dims[::-1], dst=os.path.join(
            kwargs['outputdirectory'], os.path.splitext(os.path.basename(reg_vol.resampled_for_elastix_vol))[0])+'.mhd'))

    # ELASTIX
    e_out_file, transformfile = elastix_command_line_call(
        AtlasFile, reg_vol.resampled_for_elastix_vol, svlc, parameters)

    # Make gridline transform file
    gridfld, tmpgridline = gridcompare(svlc, reg_vol)
    sp.call(['transformix', '-in', tmpgridline, '-out', gridfld, '-tp', transformfile])
    combine_images(str(reg_vol.resampled_for_elastix_vol), AtlasFile, os.path.join(
        gridfld, 'result.tif'), e_out_file, svlc, reg_vol.brainname)
    shutil.rmtree(gridfld)

    # Apply transforms to other channels
    writer(svlc, '\n...\nStarting Transformix on channel files...\n\nChannels to process are {}\n*****\n\n'.format(
        [x.downsized_vol for x in vols]))

    # type of transform and channels to apply transform to
    secondary_registration = kwargs['secondary_registration'] if 'secondary_registration' in kwargs else True
    transform_function = apply_transformix_and_register if secondary_registration else apply_transformix
    vols_to_register = [xx for xx in vols if xx.ch_type != 'regch']

    # appy transform
    [transform_function(vol, reg_vol, svlc, cores, AtlasFile, parameters,
                        transformfile, resampled_zyx_dims) for vol in vols_to_register]
    writer(svlc, '\nPast transformix step')

    # make final output image if a cellch and injch exist
    if any([True for vol in vols_to_register if vol.ch_type == 'cellch']) and any([True for vol in vols_to_register if vol.ch_type == 'injch']):
        injch = [vol.registration_volume for vol in vols_to_register if vol.ch_type == 'injch'][0]
        cellch = [vol.registration_volume for vol in vols_to_register if vol.ch_type == 'cellch'][0]
        inj_and_cells(svlc,  cellch, injch, AtlasFile)

    # check to see if script finished due to an error
    if os.path.exists(e_out_file) == False:
        writer(
            svlc, '****ERROR****GOTTEN TO END OF SCRIPT,\nTHIS ELASTIX OUTPUT FILE DOES NOT EXIST: {0} \n'.format(e_out_file))

    # write out logfile describing parameters input into function
    writer(svlc, "\nelastixlooper has finished using:\nbrainname: {}\nAtlasFile: {}\nparameterfolder: {}\nparameter files {}\nsvlc: {}".format(
        reg_vol.brainname, AtlasFile, reg_vol.parameterfolder, parameters, svlc))

    # update volumes in kwargs and pickle
    vols_to_register.append(reg_vol)
    kwargs.update(dict([('volumes', vols_to_register)]))
    pckloc = os.path.join(outdr, 'param_dict.p')
    pckfl = open(pckloc, 'wb')
    pickle.dump(kwargs, pckfl)
    pckfl.close()
    writer(outdr, "\n\n*************STEP 3************************\nelastix has completed using:\nbrainname: {}\nAtlasFile: {}\nparameterfolder: {}\nparameter files {}\nsvlc: {}\n****************\n".format(
        reg_vol.brainname, AtlasFile, reg_vol.parameterfolder, parameters, svlc))

    return


def sp_call(call):
    print(check_output(call, shell=True))
    return


def elastix_command_line_call(fx, mv, out, parameters, fx_mask=False):
    '''Wrapper Function to call elastix using the commandline, this can be time consuming

    Inputs
    -------------------
    fx = fixed path (usually Atlas for 'normal' noninverse transforms)
    mv = moving path (usually volume to register for 'normal' noninverse transforms)
    out = folder to save file
    parameters = list of paths to parameter files IN ORDER THEY SHOULD BE APPLIED
    fx_mask= (optional) mask path if desired

    Outputs
    --------------
    ElastixResultFile = '.tif' or '.mhd' result file
    TransformParameterFile = file storing transform parameters

    '''
    e_params = ['elastix', '-f', fx, '-m', mv, '-out', out]
    if fx_mask:
        e_params = ['elastix', '-f', fx, '-m', mv, '-fMask', fx_mask, '-out', out]

    # adding elastix parameter files to command line call
    for x in range(len(parameters)):
        e_params.append('-p')
        e_params.append(parameters[x])
    writer(out, 'Elastix Command:\n{}\n...'.format(e_params))

    # set paths
    TransformParameterFile = os.path.join(
        out, 'TransformParameters.{}.txt'.format((len(parameters)-1)))
    ElastixResultFile = os.path.join(out, 'result.{}.tif'.format((len(parameters)-1)))

    # run elastix:
    try:
        print('Running Elastix, this can take some time....\n')
        sp.call(e_params)  # sp_call(e_params)#
        writer(out, 'Past Elastix Commandline Call')
    except RuntimeError as e:
        writer(out, '\n***RUNTIME ERROR***: {} Elastix has failed. Most likely the two images are too dissimiliar.\n'.format(e.message))
        pass
    if os.path.exists(ElastixResultFile) == True:
        writer(out, 'Elastix Registration Successfully Completed\n')
    # check to see if it was MHD instead
    elif os.path.exists(os.path.join(out, 'result.{}.mhd'.format((len(parameters)-1)))) == True:
        ElastixResultFile = os.path.join(out, 'result.{}.mhd'.format((len(parameters)-1)))
        writer(out, 'Elastix Registration Successfully Completed\n')
    else:
        writer(out, '\n***ERROR***Cannot find elastix result file\n: {}'.format(ElastixResultFile))
        return

    return ElastixResultFile, TransformParameterFile


def transformix_command_line_call(src, dst, transformfile):
    '''Wrapper Function to call transformix using the commandline, this can be time consuming

    Inputs
    -------------------
    src = volume path for transformation
    dst = folder to save file
    transformfile = final transform file from elastix registration

    '''
    from subprocess import check_output
    print('Running transformix, this can take some time....\n')
    # sp.call(['transformix', '-in', src, '-out', dst, '-tp', transformfile])
    call = 'transformix -in {} -out {} -tp {}'.format(src, dst, transformfile)
    print(check_output(call, shell=True))
    print('Past transformix command line Call')

    return

def transformix_plus_command_line_call(src, dst, transformfile):
    '''Wrapper Function to call transformix using the commandline, this can be time consuming

    Inputs
    -------------------
    src = volume path for transformation
    dst = folder to save file
    transformfile = final transform file from elastix registration

    '''
    from subprocess import check_output
    print('Running transformix, this can take some time....\n')
    # sp.call(['transformix', '-in', src, '-out', dst, '-tp', transformfile])
    call = 'transformix -jac all -def all -in {} -out {} -tp {}'.format(src, dst, transformfile)
    print(check_output(call, shell=True))
    print('Past transformix command line Call')

    return


def jacobian_command_line_call(dst, transformfile):
    '''Wrapper Function to generate jacobian DETERMINANT
    using the commandline, this can be time consuming

    Inputs
    -------------------

    dst = folder to save file
    transformfile = final transform file from elastix registration

    '''
    from subprocess import check_output
    print('Generating Jacobian determinant, this can take some time....\n')
    call = 'transformix -jac all -out {} -tp {}'.format(dst, transformfile)
    print(check_output(call, shell=True))
    print('Past Jacobian determinant command line Call')

    return


def similarity_transform(fx, mv, dst, nm, level='fast', cleanup=True):
    '''function for similarity transform

    Inputs
    -------------------
    fx = fixed path (usually Atlas for 'normal' noninverse transforms)
    mv = moving path (usually volume to register for 'normal' n
    oninverse transforms)
    dst = location to save
    nm = 'name of file to save'
    level = 'fast', 'intermediate', 'slow' : links to parameter
    files of certain complexity
    cleanup = if False do not remove files

    Returns
    -------------
    path to file
    path to transform file (if cleanup == False)
    '''
    transform_to_use = {'slow': '/jukebox/wang/pisano/Python/lightsheet/supp_files/similarity_transform_slow.txt',
                        'intermediate': '/jukebox/wang/pisano/Python/lightsheet/supp_files/similarity_transform_intermediate.txt',
                        'fast': '/jukebox/wang/pisano/Python/lightsheet/supp_files/similarity_transform_fast.txt'}[level]

    # make dir
    makedir(dst)
    out = os.path.join(dst, 'tmp')
    makedir(out)
    fl, tp = elastix_command_line_call(fx, mv, out=out, parameters=[transform_to_use])

    #move and delete
    if nm[-4:] != '.tif':
        nm = nm+'.tif'
    dstfl = os.path.join(dst, nm)
    shutil.move(fl, dstfl)
    if cleanup:
        shutil.rmtree(out)
    print('saved as {}'.format(dstfl))

    if cleanup:
        return dstfl
    if not cleanup:
        return dstfl, tp


def apply_transformix(vol, reg_vol, svlc, cores, AtlasFile, parameters, transformfile, resampled_zyx_dims):
    '''
    Signature: (vol, svlc, cores, AtlasFile, parameters, transformfile)

    Function to
        1) apply sig/inj -> auto then registration->atlas transform
        2) generate depth coded images

    Contrast this with apply_transformix_and_register: which also includes:
    registration of a sig/inj channel to the autofluro (registration) channel

    (vol, reg_vol, svlc, cores, AtlasFile, parameters, transformfile)

    Inputs
    ----------------
    vol = volume object to apply transform
    reg_vol (unused but needed to keep input the same with
        apply_transformix_and_register)
    svlc = path to 'elastix' folder, where files will be written
    cores = int # of cores
    AtlasFile = path to ABA atlas
    parameters = list in order of application of parameter file paths
    transformfile = output of elastix's transform from reg chan to atlas

    '''

    writer(svlc, '\n\nStarting transform ONLY for: {}...\n\n   to change to transform and registration of channel to regch add "secondary_registration": True to params in run tracing'.format(vol.downsized_vol))

    # set up folder/inputs
    sig_ch_resized = vol.downsized_vol+'.tif'
    trnsfrm_outpath = os.path.join(svlc, os.path.basename(vol.downsized_vol))
    makedir(trnsfrm_outpath)
    sig_ch_resampledforelastix = sig_ch_resized[:-4]+'_resampledforelastix.tif'

    # resample if necessary
    writer(svlc, 'Resizing channel: {}'.format(sig_ch_resized))
    if not vol.ch_type == 'regch':
        resample(
            sig_ch_resized, AtlasFile, svlocname=sig_ch_resampledforelastix,
            singletifffile=True, resamplefactor=1.3)
    # cannot be resample_par because that be a pool inside of pool
    # resample_par(cores, transforminput, AtlasFile,
    # svlocname=transforminput_resized, singletifffile=True, resamplefactor=1.3)

    # optionally convert to mhd, note convert_to_mhd dims are in XYZ
    if resampled_zyx_dims:
        sig_ch_resampledforelastix = convert_to_mhd(
            vol.resampled_for_elastix_vol, dims=resampled_zyx_dims[::-1])

    # run transformix
    sp.call(['transformix', '-in', sig_ch_resampledforelastix,
             '-out', trnsfrm_outpath, '-tp', transformfile])
    writer(svlc, '\n   Transformix File Generated: {}'.format(trnsfrm_outpath))

    if resampled_zyx_dims:
        removedir(sig_ch_resampledforelastix)
        removedir(sig_ch_resampledforelastix+'.raw')

    return vol


def apply_transformix_and_register(
        vol, reg_vol, svlc, cores, AtlasFile,
        parameters, transformfile, resampled_zyx_dims):
    '''Function to
        1) register a sig/inj channel to the autofluro (registration) channel
        2) apply sig/inj -> auto then registration->atlas transform
        3) generate depth coded images

    Contrast this with apply_transformix.

    (vol, reg_vol, svlc, cores, AtlasFile, parameters, transformfile)

    Inputs
    ----------------
    vol = volume object to apply transform
    reg_vol = volume initially used to register to atlas
    svlc = path to 'elastix' folder, where files will be written
    cores = int # of cores
    AtlasFile = path to ABA atlas
    parameters = list in order of application of parameter file paths
    transformfile = output of elastix's transform from reg chan to atlas

    '''

    writer(svlc, '\n\nStarting transform AND REGISTRATION to regch for: {}...\n   to change to transform only add "secondary_registration": False to params in run tracing\n'.format(vol.downsized_vol))

    # set up folder/inputs
    sig_ch_resized = vol.downsized_vol+'.tif'
    sig_out = os.path.join(svlc, os.path.basename(vol.downsized_vol))
    makedir(sig_out)
    sig_to_reg_out = os.path.join(sig_out, 'sig_to_reg')
    makedir(sig_to_reg_out)
    reg_ch_resampledforelastix = reg_vol.resampled_for_elastix_vol
    sig_ch_resampledforelastix = sig_ch_resized[:-4]+'_resampledforelastix.tif'

    # run elastix on sig/inj channel -> reg channel
    # (but don't register reg to itself)
    if not vol.ch_type == 'regch':
        writer(svlc, 'Resizing transforminput: {}'.format(sig_ch_resized))
        resample(
            sig_ch_resized, AtlasFile, svlocname=sig_ch_resampledforelastix,
            singletifffile=True, resamplefactor=1.3)
        # cannot be resample_par because that be a pool inside of pool
        # resample_par(cores, sig_ch_resized, AtlasFile,
        # svlocname=sig_ch_resampledforelastix, singletifffile=True,
        # resamplefactor=1.3)

        ElastixResultFile, TransformParameterFile = elastix_command_line_call(
            reg_ch_resampledforelastix, sig_ch_resampledforelastix,
            sig_to_reg_out, parameters)

    # copy transform paramters to set up transform series:
    [shutil.copy(os.path.join(svlc, xx), os.path.join(sig_to_reg_out, 'regtoatlas_'+xx))
     for xx in os.listdir(svlc) if 'TransformParameters' in xx]

    # connect transforms by setting regtoatlas TP0's initial transform to sig->reg transform
    # might need to go backwards...
    reg_to_atlas_tps = [os.path.join(sig_to_reg_out, xx) for xx in os.listdir(sig_to_reg_out) if 'TransformParameters'
                        in xx and 'regtoatlas' in xx]
    reg_to_atlas_tps.sort()
    sig_to_reg_tps = [os.path.join(sig_to_reg_out, xx) for xx in os.listdir(sig_to_reg_out) if 'TransformParameters'
                      in xx and 'regtoatlas' not in xx]
    sig_to_reg_tps.sort()

    # account for moving the reg_to_atlas_tps:
    [change_transform_parameter_initial_transform(
        reg_to_atlas_tps[xx+1], reg_to_atlas_tps[xx]) for xx in range(len(reg_to_atlas_tps)-1)]

    # now make the initialtransform of the first(0) sig_to_reg be the last's reg_to_atlas transform
    change_transform_parameter_initial_transform(reg_to_atlas_tps[0], sig_to_reg_tps[-1])

    # optionally convert to mhd, note convert_to_mhd dims are in XYZ
    if resampled_zyx_dims:
        sig_ch_resampledforelastix = convert_to_mhd(
            vol.resampled_for_elastix_vol, dims=resampled_zyx_dims[::-1])

    # run transformix
    sp.call(['transformix', '-in', sig_ch_resampledforelastix,
             '-out', sig_out, '-tp', reg_to_atlas_tps[-1]])

    if resampled_zyx_dims:
        removedir(sig_ch_resampledforelastix)
        removedir(sig_ch_resampledforelastix+'.raw')

    writer(svlc, '\n   Transformix File Generated: {}'.format(sig_out))

    return vol


def change_transform_parameter_initial_transform(fl, initialtrnsformpth):
    '''
    (InitialTransformParametersFileName "NoInitialTransform")
    initialtrnsformpth = 'NoInitialTransform' or 'pth/to/transform.0.txt'
    '''
    fl1 = fl[:-5]+'0000.txt'

    with open(fl, 'r') as f, open(fl1, 'w') as new:
        for line in f:
            new.write('(InitialTransformParametersFileName "{}")\n'.format(initialtrnsformpth)
                      ) if 'InitialTransformParametersFileName' in line else new.write(line)

    # overwrite original transform file
    shutil.move(fl1, fl)
    return


def change_interpolation_order(fl, order=3):
    '''Function to change FinalBSplineInterpolationOrder of elastix file.
    This is import when pixel values need to be the same or exact

    '''
    fl1 = fl[:-5]+'0000.txt'

    with open(fl, 'r') as f, open(fl1, 'w') as new:
        for line in f:
            new.write('(FinalBSplineInterpolationOrder "{}")\n'.format(order)
                      ) if 'FinalBSplineInterpolationOrder' in line else new.write(line)

    # overwrite original transform file
    shutil.move(fl1, fl)
    return fl


def change_bspline_interpolation_order(fl, order=3):
    '''Function to change (BSplineTransformSplineOrder 3) of elastix file.
    This is import when pixel values need to be the same or exact

    '''
    fl1 = fl[:-5]+'0000.txt'

    with open(fl, 'r') as f, open(fl1, 'w') as new:
        for line in f:
            new.write('(BSplineTransformSplineOrder "{}")\n'.format(order)
                      ) if 'BSplineTransformSplineOrder' in line else new.write(line)

    # overwrite original transform file
    shutil.move(fl1, fl)
    return fl

def make_inverse_transform(vol_to_process, cores=5, **kwargs):
    '''Script to perform inverse transform and return path to elastix inverse parameter file

    Returns:
    ---------------
    transformfile
    '''

    sys.stdout.write('starting make_inverse_transform, this will take time...')
    # inputs
    kwargs = load_kwargs(kwargs['outputdirectory'])
    outdr = kwargs['outputdirectory']
    vols = kwargs['volumes']
    reg_vol = [xx for xx in vols if xx.ch_type == 'regch'][0]
    AtlasFile = reg_vol.atlasfile
    parameterfolder = reg_vol.parameterfolder

    ###############
    ###images need to have been stitched, resized, and saved into single tiff stack ###
    ###resize to ~220% total size of atlas (1.3x/dim) ###
    reg_vol.add_resampled_for_elastix_vol(reg_vol.downsized_vol+'_resampledforelastix.tif')
    #resample_par(cores, reg_vol, AtlasFile, svlocname=reg_vol_resampled, singletifffile=True, resamplefactor=1.2)
    if not os.path.exists(reg_vol.resampled_for_elastix_vol):
        print('Resizing')
        #resample(reg_vol, AtlasFile, svlocname=reg_vol_resampled, singletifffile=True, resamplefactor=1.3)
        resample_par(cores, reg_vol.downsized_vol+'.tif', AtlasFile,
                     svlocname=reg_vol.resampled_for_elastix_vol, singletifffile=True, resamplefactor=1.3)
        print('Past Resizing')

    vol_to_process.add_resampled_for_elastix_vol(
        vol_to_process.downsized_vol+'_resampledforelastix.tif')

    if not os.path.exists(vol_to_process.resampled_for_elastix_vol):
        print('Resizing')
        resample_par(cores, vol_to_process.downsized_vol+'.tif', AtlasFile,
                     svlocname=vol_to_process.resampled_for_elastix_vol, singletifffile=True, resamplefactor=1.3)
        print('Past Resizing')

    # setup
    parameters = []
    [parameters.append(os.path.join(parameterfolder, files))
     for files in os.listdir(parameterfolder) if files[0] != '.' and files[-1] != '~']
    parameters.sort()

    # set up save locations
    svlc = os.path.join(outdr, 'elastix_inverse_transform')
    makedir(svlc)
    svlc = os.path.join(svlc, '{}_{}'.format(vol_to_process.ch_type, vol_to_process.brainname))
    makedir(svlc)

    # Creating LogFile
    #writer(svlc, 'Starting elastix...AtlasFile: {}\n   parameterfolder: {}\n   svlc: {}\n'.format(AtlasFile, parameterfolder, svlc))
    writer(svlc, 'Order of parameters used in Elastix:{}\n...\n\n'.format(parameters))

    # register: 1) atlas->reg 2) reg->sig NOTE these are intentionally backwards so applying point transform can be accomplished
    # atlas(mv)->reg (fx)
    atlas2reg = os.path.join(
        svlc, reg_vol.resampled_for_elastix_vol[reg_vol.resampled_for_elastix_vol.rfind('/')+1:-4]+'_atlas2reg')
    makedir(atlas2reg)
    e_out_file, e_transform_file = elastix_command_line_call(
        fx=reg_vol.resampled_for_elastix_vol, mv=AtlasFile, out=atlas2reg, parameters=parameters)

    # reg(mv)->sig(fx)
    reg2sig = os.path.join(
        svlc, vol_to_process.resampled_for_elastix_vol[vol_to_process.resampled_for_elastix_vol.rfind('/')+1:-4]+'_reg2sig')
    makedir(reg2sig)
    e_out_file, e_transform_file = elastix_command_line_call(
        fx=vol_to_process.resampled_for_elastix_vol, mv=reg_vol.resampled_for_elastix_vol, out=reg2sig, parameters=parameters)

    # set up transform series:
    atlas2reg2sig = os.path.join(
        svlc, vol_to_process.resampled_for_elastix_vol[vol_to_process.resampled_for_elastix_vol.rfind('/')+1:-4]+'_atlas2reg2sig')
    makedir(atlas2reg2sig)
    # copy transform paramters
    [shutil.copy(os.path.join(reg2sig, xx), os.path.join(atlas2reg2sig, 'reg2sig_'+xx))
     for xx in os.listdir(reg2sig) if 'TransformParameters' in xx]
    [shutil.copy(os.path.join(atlas2reg, xx), os.path.join(atlas2reg2sig, 'atlas2reg_'+xx))
     for xx in os.listdir(atlas2reg) if 'TransformParameters' in xx]

    # connect transforms by setting regtoatlas TP0's initial transform to sig->reg transform
    tps = [os.path.join(atlas2reg2sig, xx)
           for xx in os.listdir(atlas2reg2sig) if 'TransformParameters' in xx]
    # they are now in order recent to first, thus first is regtoatlas_TransformParameters.1.txt
    tps.sort(reverse=True)
    for x in range(len(tps)):
        if not x == len(tps)-1:
            change_transform_parameter_initial_transform(tps[x], tps[x+1])

    assert os.path.exists(tps[0])
    writer(svlc, '***Elastix Registration Successfully Completed***\n')
    writer(svlc, '\ne_transform_file is {}'.format(tps[0]))
    ####################
    sys.stdout.write('complted make_inverse_transform')
    return tps[0]

    ############################################################################################################
    ######################apply point transform and make transformix input file#################################
    ############################################################################################################
    # find centers and add 1's to make nx4 array for affine matrix multiplication to account for downsizing
    # everything is in PIXELS


def point_transformix(txtflnm, transformfile, dst=False):
    '''apply elastix transform to points


    Inputs
    -------------
    txtflnm = list of points that have resizingtransform
    transformfile = elastix transform file
    dst = optional folder

    Returns
    ---------------
    trnsfrm_out_file = pth to file containing post transformix points

    '''
    sys.stdout.write('\n***********Starting Transformix***********')
    from subprocess import check_output
    # set paths
    if not dst:
        trnsfrm_outpath = os.path.join(os.path.dirname(transformfile), 'posttransformix')
        makedir(trnsfrm_outpath)
    if dst:
        trnsfrm_outpath = os.path.join(dst, 'posttransformix')
        makedir(trnsfrm_outpath)
    trnsfrm_out_file = os.path.join(trnsfrm_outpath, 'outputpoints.txt')

    # run transformix point transform
    call = 'transformix -def {} -out {} -tp {}'.format(txtflnm, trnsfrm_outpath, transformfile)
    print(check_output(call, shell=True))
    writer(trnsfrm_outpath, '\n   Transformix File Generated: {}'.format(trnsfrm_out_file))
    return trnsfrm_out_file


def collect_points_post_transformix(src, point_or_index='point'):
    '''
    src = output text file from point transformix

    returns array XYZ
    '''

    idx = 'OutputPoint' if point_or_index == 'point' else 'OutputIndexFixed'

    with open(src, 'r') as fl:
        lines = fl.readlines()
        fl.close()

    # populate post-transformed array of contour centers
    arr = np.empty((len(lines), 3))
    for i in range(len(lines)):
        arr[i, ...] = lines[i].split()[lines[i].split().index(
            idx)+3:lines[i].split().index(idx)+6]  # x,y,z

    return arr
