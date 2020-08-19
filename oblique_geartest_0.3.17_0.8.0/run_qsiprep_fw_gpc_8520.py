import flywheel
import datetime

fw = flywheel.Client()

qsiprep = fw.lookup('gears/qsiprep-fw')
project = fw.projects.find_first("label=ReproBrainChart")

now = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M")
analysis_label = 'HBN_oblique_test_qsiprep_{}_{}'.format(qsiprep.gear.version, now)

config = {
            "hmc_model": "eddy",
            "use_syn_sdc": False,
            'b0_threshold': 100,
            'save_outputs': True,
            'dwi_denoise_window': 5,
            'do_reconall': False,
            'b0_to_t1w_transform': 'Rigid',
            'combine_all_dwis': False,
            'intramodal_template_iters': 0,
            'force_spatial_normalization': True,
            'shoreline_iters': 0,
            'output_resolution': 1.5,
            'output_space': 'T1w',
            'sloppy': False,
            'unringing_method': 'mrdegibbs'
        }

inputs = {
    "freesurfer_license": project.files[2],
}

sessions_to_run = []
for session in project.sessions():
    desired_case = (('sub-NDARCH001CN2' in session.subject.label) or ('sub-NDARUR126CFH' in session.subject.label) or ('sub-NDARXB889WUB' in session.subject.label) or ('sub-NDARBV167RMU' in session.subject.label))
#    desired_case = (('sub-NDARVH033CA4' in session.subject.label) or ('sub-NDARLE417FRX' in session.subject.label) or ('sub-NDARJZ526HN3' in session.subject.label) or ('sub-NDARCH001CN2' in session.subject.label) or ('sub-NDARMU053YEU' in session.subject.label) or ('sub-NDARUR126CFH' in session.subject.label) or ('sub-NDARXB889WUB' in session.subject.label) or ('sub-NDARFJ179MG0' in session.subject.label) or ('sub-NDARBV167RMU' in session.subject.label) or ('sub-NDARAD615WLJ' in session.subject.label))
    if desired_case:
        sessions_to_run.append(session)

analysis_ids = []
fails = []
#single_sess = [sessions_to_run[0]] #Can use this line if want to append all sessions with acq-64dir_dwi to sessions_to_run, but only run a few of them
for ses in sessions_to_run:
    try:
        _id = qsiprep.run(analysis_label=analysis_label,
                          config=config, inputs=inputs, destination=ses, tags=['vm-n1-highmem-4_disk-300GB_swap-30G'])
        analysis_ids.append(_id)
    except Exception as e:
        print(e)
        fails.append(ses)

with open('{}_{}_{}_analysisIDS.txt'.format(qsiprep.gear.name,qsiprep.gear.version,now), 'w') as f: 
    for id in analysis_ids:
        f.write("%s\n" % id)

with open('{}_{}_{}_failSES.txt'.format(qsiprep.gear.name,qsiprep.gear.version,now), 'w') as a:
    for ses in fails:
        a.write("%s\n" % ses) 
