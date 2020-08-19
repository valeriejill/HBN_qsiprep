import flywheel

client = flywheel.Client()

qsiprep = client.lookup('gears/qsiprep-fw-hpc')
project = client.projects.find_first("label=ReproBrainChart")

sessions_to_check = []
washu_caseset1 = ['sub-NDARAD615WLJ','sub-NDARAH304ED7','sub-NDARBL935ZUA','sub-NDARBV167RMU','sub-NDARCH001CN2','sub-NDARCZ915NC1','sub-NDARDZ627XFA','sub-NDARFJ179MG0','sub-NDARJP146GT9','sub-NDARJZ526HN3','sub-NDARKN346XZH','sub-NDARLE417FRX','sub-NDARLU111UYF','sub-NDARME736MN8','sub-NDARMJ495DE0','sub-NDARMN043YKC','sub-NDARNT043XGH','sub-NDARPG847LB8','sub-NDARRB338YZ0','sub-NDARRP384BVX','sub-NDARTA819MF0','sub-NDARVH033CA4','sub-NDARWJ064WYP','sub-NDARWM848AKP','sub-NDARXB889WUB','sub-NDARYJ301DYN','sub-NDARYK164AEJ']

for session in project.sessions():
    for i in washu_caseset1:
        desired_case = (str(i) in session.subject.label)
        if desired_case:
            sessions_to_check.append(session)

sessions = []
sessions = [client.get(x.id) for x in sessions_to_check]

for i in sessions: 
    print(i.subject.label) 
    filtered_qsiprep = [x for x in i.analyses if 'washU_QCscorecomp_qsiprep' in x.label and x.job.state == 'complete']      
    if filtered_qsiprep:
        print("job completed")
    else:
        print("job NOT completed")    
