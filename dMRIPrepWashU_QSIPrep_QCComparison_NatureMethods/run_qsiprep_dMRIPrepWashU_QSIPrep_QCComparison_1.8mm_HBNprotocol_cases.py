import flywheel
import datetime

fw = flywheel.Client()

qsiprep = fw.lookup('gears/qsiprep-fw-hpc')
project = fw.projects.find_first("label=ReproBrainChart")

now = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M")
analysis_label = 'washU_QCscorecomp_qsiprep_{}_{}'.format(qsiprep.gear.version, now) 

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
            'output_resolution': 1.8,
            'output_space': 'T1w',
            'sloppy': False,
            'unringing_method': 'mrdegibbs'
        }

inputs = {
    "freesurfer_license": project.files[2],
}

washu_caseset1 = ['sub-NDARAD615WLJ','sub-NDARAH304ED7','sub-NDARBL935ZUA','sub-NDARBV167RMU','sub-NDARCH001CN2','sub-NDARCZ915NC1','sub-NDARDZ627XFA','sub-NDARFJ179MG0','sub-NDARJP146GT9','sub-NDARJZ526HN3','sub-NDARKN346XZH','sub-NDARLE417FRX','sub-NDARLU111UYF','sub-NDARME736MN8','sub-NDARMJ495DE0','sub-NDARMN043YKC','sub-NDARNT043XGH','sub-NDARPG847LB8','sub-NDARRB338YZ0','sub-NDARRP384BVX','sub-NDARTA819MF0','sub-NDARVH033CA4','sub-NDARWJ064WYP','sub-NDARWM848AKP','sub-NDARXB889WUB','sub-NDARYJ301DYN','sub-NDARYK164AEJ']


sessions_to_run = []
for session in project.sessions():
    for i in washu_caseset1:
        desired_case = (str(i) in session.subject.label)
        if desired_case:
            sessions_to_run.append(session)

analysis_ids = []
fails = []
for ses in sessions_to_run:
    try:
        _id = qsiprep.run(analysis_label=analysis_label,
                          config=config, inputs=inputs, destination=ses)
        analysis_ids.append(_id)
    except Exception as e:
        print(e)
        fails.append(ses)

#Write analysis IDs and failed sessions to files
with open('{}_{}_{}_analysisIDS.txt'.format(qsiprep.gear.name,qsiprep.gear.version,now), 'w') as f: 
    for id in analysis_ids:
        f.write("%s\n" % id)

with open('{}_{}_{}_failSES.txt'.format(qsiprep.gear.name,qsiprep.gear.version,now), 'w') as a:
    for ses in fails:
        a.write("%s\n" % ses) 
