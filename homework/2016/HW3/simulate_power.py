"""Measure cycle-average direct-path channel power versus load.
LX4(MOS) is the HSPICE intrinsic channel IDS magnitude for normal bias.
Psc = VDD * average(max(0,min(IDS_p,IDS_n))) over a steady period.
Displacement current and CL switching energy are not called short circuit.
"""
from pathlib import Path
import argparse,csv,json,os,subprocess
H=Path(__file__).resolve().parent
LOADS=[.1,.3,.5,.7,1.0]
def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--hspice',default=os.environ.get('HSPICE','C:/synopsys/Hspice_S-2021.09/WIN64/hspice.com'));ap.add_argument('--model',default=os.environ.get('CIC018_MODEL','D:/cic018.l'));ap.add_argument('--work',default=str(H.parents[2]/'scratch'/('power_'+H.parent.name)))
 a=ap.parse_args();model=Path(a.model).resolve();raw=Path(a.work).resolve()/'power';raw.mkdir(parents=True,exist_ok=True);res=H/'results'/'power';res.mkdir(parents=True,exist_ok=True)
 s=f"* Inverter direct-path power versus CLOAD\n.protect\n.lib '{model.as_posix()}' tt\n.unprotect\n"
 s+='vvdd vdd 0 1.8\nvin in 0 pulse(0 1.8 5n 3n 3n 40n 86n)\nMP out in vdd vdd P_18 W=1.44u L=.18u\nMN out in 0 0 N_18 W=.36u L=.18u\nCL out 0 CLOAD\n.temp 25\n.option measform=3 measdgt=9 delmax=10p\n.param CLOAD=.1p\n.data capvals CLOAD\n.1p\n.3p\n.5p\n.7p\n1p\n.enddata\n.tran 10p 180n sweep DATA=capvals\n'
 s+=".measure tran isc AVG PAR('max(0,min(lx4(mp),lx4(mn)))') from=91n to=177n\n.measure tran peaksc MAX PAR('max(0,min(lx4(mp),lx4(mn)))') from=91n to=177n\n.measure tran ptotal AVG PAR('-1.8*i(vvdd)') from=91n to=177n\n.measure tran psc PARAM='1.8*isc'\n.measure tran elsc PARAM='psc*86n'\n.measure tran out_high FIND v(out) at=175n\n.measure tran out_low FIND v(out) at=125n\n.end\n"
 (H/'power_testbench.sp').write_text(s,encoding='ascii');(raw/'testbench.sp').write_text(s,encoding='ascii')
 p=subprocess.run([a.hspice,'-i','testbench.sp','-o','run'],cwd=raw,capture_output=True,text=True,errors='replace',timeout=180)
 (raw/'console.log').write_text(p.stdout+p.stderr,encoding='utf-8');lis=(raw/'run.lis').read_text(errors='replace') if(raw/'run.lis').exists() else ''
 if p.returncode or 'job concluded' not in lis.lower() or '**error**' in lis.lower():raise RuntimeError('HSPICE failed: '+str(raw))
 lines=(raw/'run.mt0.csv').read_text().splitlines();ms=list(csv.DictReader(l for l in lines if l.strip() and not l.startswith(('$','.'))))
 if len(ms)!=5:raise AssertionError('Expected five load sweeps')
 rows=[]
 for load,m in zip(LOADS,ms):
  v={k:float(x) for k,x in m.items() if k not in ['alter#','temper']}
  assert v['out_high']>=1.6 and v['out_low']<=.2 and v['psc']>=0
  rows.append(dict(CL_pF=load,Psc_uW=v['psc']*1e6,peak_Isc_uA=v['peaksc']*1e6,Eshort_fJ=v['elsc']*1e15,Ptotal_uW=v['ptotal']*1e6,Pload_switching_uW=load*1e-12*1.8**2/86e-9*1e6,Vhigh=v['out_high'],Vlow=v['out_low']))
 with(res/'power_curve.csv').open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
 summary=dict(simulator='HSPICE S-2021.09',model='CIC018 TT local',VDD_V=1.8,temperature_C=25,WP_um=1.44,WN_um=.36,L_um=.18,input_rise_fall_ns=3,period_ns=86,averaging_interval_ns=[91,177],DELMAX_ps=10,definition='VDD * cycle-average max(0,min(LX4(PMOS),LX4(NMOS))); intrinsic channel currents',rows=rows,monotone_decreasing=all(rows[i]['Psc_uW']>rows[i+1]['Psc_uW'] for i in range(4)))
 (res/'summary.json').write_text(json.dumps(summary,indent=2));print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
