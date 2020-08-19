import flywheel
import pandas as pd
from tqdm import tqdm
import time

# initiate flywheel client
fw = flywheel.Client()
project = fw.projects.find_first("label=ReproBrainChart")

# identify HBN subjects/sessions
HBN_sessions = []
for session in project.sessions():
    desired_case = (('ses-HBNsiteRU' in session.label) or ('ses-HBNsiteCBIC' in session.label))
    #has_dwi = (('dwi' in [acq.label for acq in session.acquisitions()]) and (('ses-HBNsiteRU' in session.label) or ('ses-HBNsiteCBIC' in session.label)))
    if desired_case:
        HBN_sessions.append(session)

# create metadata extracter function
def get_seq_info(acq_id):
    acqdata = fw.get(acq_id)
    sequenceinfo = acqdata.files[0].info
    Case = sequenceinfo['BIDS']['Path']
    acqlabel = acqdata.label
    result = {
        "Case": Case,
        "acqlabel": acqlabel,
        "acq_id": acq_id,
        "PhaseEncodingDirection_dwi": "Missing",
        "EffectiveEchoSpacing_dwi": "Missing",
        "TotalReadoutTime_dwi": "Missing",
        "RepetitionTime_dwi": "Missing",
        "EchoTime_dwi": "Missing"
        }
    if 'PhaseEncodingDirection' in sequenceinfo:
        result["PhaseEncodingDirection_dwi"] = sequenceinfo['PhaseEncodingDirection']

    if 'EffectiveEchoSpacing' in sequenceinfo:
        result['EffectiveEchoSpacing_dwi'] = sequenceinfo['EffectiveEchoSpacing']

    if 'TotalReadoutTime' in sequenceinfo:
        result['TotalReadoutTime_dwi'] = sequenceinfo['TotalReadoutTime']

    if 'RepetitionTime' in sequenceinfo:
        result['RepetitionTime_dwi'] = sequenceinfo['RepetitionTime']

    if 'EchoTime' in sequenceinfo:
        result['EchoTime_dwi'] = sequenceinfo['EchoTime']
    return result

num_tries = 10
seq_info = []

# extract metadata from HBN sessions with dwi acquisitions
for session in tqdm(HBN_sessions):
    for acq in session.acquisitions():
        acqid = acq.id
        try:
            if 'Modality' in acq.files[0].info['BIDS']:
                has_dwi = 'dwi' in acq.files[0].info['BIDS']['Modality']
                if has_dwi:   

                    # attempt to extract data from Flywheel multiple times, in case of dropped connection
                    for trynum in range(num_tries):
                        result = None
                        try:
                            result = get_seq_info(acqid)
                        except Exception:
                            time.sleep(3)
                        if result:
                            break

                    if result is None:
                        raise Exception("Too many tries!!")
                    seq_info.append(result)
        except:
            print("acqid error")
status = pd.DataFrame(seq_info)
status.to_csv("HBN_MetaData_DWI_8192020.csv")


        
