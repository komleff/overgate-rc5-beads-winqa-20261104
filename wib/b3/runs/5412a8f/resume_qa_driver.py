from common import *
stop=json.loads((E/'STOP.json').read_bytes());assert 'FileNotFoundError' in stop['traceback'] and 'dolt' in stop['error']
(E/'STOP.json').rename(E/'QA-HARNESS-STOP-store-path.json')
save('QA-store-path-correction',dict(issue='QA assumed .beads/dolt but real embedded store is .beads/embeddeddolt per metadata',candidate_source_changed=False,native_fault_repeated=False,next='continue at captured after-peer-init checkpoint after exact hash verification'))
import recovery_cases
