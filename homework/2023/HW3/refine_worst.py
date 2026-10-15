"""Reproduce the worst-transition timestep refinement and its actual waveform.

Reads results/summary.json and the unchanged rca.sp. Standard-library Python
handles HSPICE, parsing and CSV/JSON export. Matplotlib, if installed, also
regenerates worst_transition.png; --no-plot skips that optional figure.
The process library remains external and raw simulator files go to --work.
"""
from pathlib import Path
import argparse,csv,hashlib,json,os,shutil,subprocess,tempfile

HERE=Path(__file__).resolve().parent
INS=['x0','x1','x2','y0','y1','y2','cin']
OUTS=['s0','s1','s2','cout']

def arithmetic(word):return (word&7)+((word>>3)&7)+(word>>6)
def net_hash(path):return hashlib.sha256(path.read_bytes().replace(b'\r\n',b'\n')).hexdigest()

def make_deck(summary,model,step):
    w=summary['worst_measured'];old,new=w['old'],w['new']
    vdd=summary['voltage_V'];slew=summary['input_slew_ps'];temperature=summary['temperature_C']
    assert old^new==1<<INS.index(w['input']), 'Expected a single-input transition'
    s=f"""* 2023 HW3 independent worst-transition refinement, case {w['case']}
.protect
.lib '{model.as_posix()}' {summary['corner']}
.unprotect
.include 'rca.sp'
VDD vdd 0 {vdd:g}
.option post=0 measform=3 measdgt=10 numdgt=10 ingold=2 lis_new=1 delmax={step:g}p
.temp {temperature:g}
XADD cin x0 x1 x2 y0 y1 y2 s0 s1 s2 cout vdd 0 rca
"""
    for n in OUTS:s+=f"C{n} {n} 0 {summary['output_load_fF']:g}f\n"
    end_ramp=1e-9+slew*1e-12
    s+=f'VREF ref 0 pwl(0 0 1n 0 {end_ramp:.12e} {vdd:g} 3n {vdd:g})\n'
    for bit,n in enumerate(INS):
        a,b=vdd*(old>>bit&1),vdd*(new>>bit&1)
        s+=f'V{n} {n} 0 pwl(0 {a:g} 1n {a:g} {end_ramp:.12e} {b:g} 3n {b:g})\n'
    s+=f".tran {step:g}p 3n\n.print tran v({w['input']}) "+' '.join(f'v({n})' for n in OUTS)+'\n'
    for n in OUTS:
        s+=f'.meas tran pre_{n} find v({n}) at=0.9n\n.meas tran post_{n} find v({n}) at=2.9n\n'
        s+=f'.meas tran d_{n} trig v(ref) val={vdd/2:g} rise=1 targ v({n}) val={vdd/2:g} cross=last\n'
    input_edge='rise' if new>old else 'fall'
    s+=f".meas tran input_mid when v({w['input']})={vdd/2:g} {input_edge}=1\n"
    s+=f".meas tran output_mid when v({w['output']})={vdd/2:g} {w['direction']}=last\n.end\n"
    return s

def trace(path,names_needed):
    lines=path.read_text(errors='replace').splitlines();rows={};names=[];armed=False
    for i,line in enumerate(lines):
        if line.strip().lower().startswith('time '):
            names=lines[i+1].lower().split();armed=True;continue
        if not armed:continue
        try:vals=[float(x.replace('D','e')) for x in line.split()]
        except ValueError:continue
        if len(vals)==len(names)+1:rows.setdefault(vals[0],{}).update(dict(zip(names,vals[1:])))
    return [(t,d) for t,d in sorted(rows.items()) if all(k in d for k in names_needed)]

def plot(rows,result,folder):
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
    except ImportError:
        print('Matplotlib unavailable: CSV/JSON regenerated; PNG skipped. Install matplotlib to regenerate the figure.')
        return False
    inp=result['input'];signals=[inp,*OUTS]
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11})
    fig,ax=plt.subplots(figsize=(10.4,5.4))
    colors={inp:'#334155','s0':'#2563eb','s1':'#059669','s2':'#dc2626','cout':'#9333ea'}
    for name in signals:
        ax.plot([t*1e9 for t,d in rows],[d[name] for t,d in rows],label=name,color=colors[name],
                linewidth=1.7 if name in [inp,result['output']] else 1.2,linestyle='--' if name==inp else '-')
    ti,to=result['input_crossing_ns'],result['output_crossing_ns']
    ax.axhline(result['voltage_V']/2,color='#64748b',linewidth=.9,linestyle=':')
    ax.axvline(ti,color='#334155',linewidth=.9,linestyle=':');ax.axvline(to,color='#dc2626',linewidth=.9,linestyle=':')
    ax.annotate('',xy=(to,1.6),xytext=(ti,1.6),arrowprops={'arrowstyle':'<->','color':'#b91c1c','linewidth':1.3})
    ax.text((ti+to)/2,1.68,f"{inp} to {result['output']} {result['direction']}: {result['refined_delay_ps']:.3f} ps",ha='center',color='#b91c1c',fontsize=10)
    ax.set(xlim=(.8,2.2),ylim=(-.08,result['voltage_V']+.18),xlabel='Time (ns)',ylabel='Voltage (V)')
    fig.suptitle(f"2023 HW3: original worst-transition case {result['case']}",x=.08,y=.99,ha='left',fontweight='bold',fontsize=15)
    old,new=result['old'],result['new']
    desc=f"(x,y,cin): ({old&7},{old>>3&7},{old>>6}) to ({new&7},{new>>3&7},{new>>6})"
    fig.text(.08,.93,desc+f" | sum+carry: {result['initial_result']} to {result['final_result']} | {result['corner']}, {result['voltage_V']:g} V, {result['temperature_C']:g} C, {result['output_load_fF']:g} fF/output",fontsize=9,color='#475569')
    ax.grid(True,alpha=.18);ax.legend(loc='upper right',ncol=5,frameon=False)
    for side in ['top','right']:ax.spines[side].set_visible(False)
    fig.subplots_adjust(top=.86,bottom=.12,left=.08,right=.98)
    fig.savefig(folder/'worst_transition.png',dpi=180,bbox_inches='tight');plt.close(fig)
    return True

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--hspice',default=os.getenv('HSPICE','C:/synopsys/Hspice_S-2021.09/WIN64/hspice.com'))
    p.add_argument('--model',type=Path,default=os.getenv('CIC018_MODEL','D:/cic018.l'))
    p.add_argument('--work',type=Path,default=Path(tempfile.gettempdir())/'intro-vlsi-2023-hw3-refinement')
    p.add_argument('--results',type=Path,default=HERE/'results')
    p.add_argument('--max-step-ps',type=float,default=1)
    p.add_argument('--no-plot',action='store_true')
    a=p.parse_args();a.model=a.model.resolve();a.work=a.work.resolve();a.results=a.results.resolve()
    summary=json.loads((a.results/'summary.json').read_text());w=summary['worst_measured']
    assert net_hash(HERE/'rca.sp')==summary['netlist_sha256'], 'Netlist differs from the sweep baseline; regenerate the sweep first'
    if not a.model.is_file():raise FileNotFoundError('Local model file required: '+str(a.model))
    if not a.max_step_ps>0:raise ValueError('Maximum timestep must be positive')
    a.work.mkdir(parents=True,exist_ok=True);a.results.mkdir(parents=True,exist_ok=True)
    shutil.copyfile(HERE/'rca.sp',a.work/'rca.sp')
    (a.work/'refinement.sp').write_text(make_deck(summary,a.model,a.max_step_ps),encoding='ascii')
    proc=subprocess.run([a.hspice,'-i','refinement.sp','-o','refinement'],cwd=a.work,capture_output=True,timeout=180)
    (a.work/'console.log').write_bytes(proc.stdout+proc.stderr)
    lis=(a.work/'refinement.lis').read_text(errors='replace') if (a.work/'refinement.lis').exists() else ''
    if proc.returncode or 'job concluded' not in lis.lower() or '**error**' in lis.lower():raise RuntimeError('HSPICE failed; inspect '+str(a.work))
    lines=(a.work/'refinement.mt0.csv').read_text().splitlines()
    row=list(csv.DictReader(l for l in lines if l.strip() and not l.startswith(('$','.'))))[0]
    # Unchanged outputs can have failed/undefined delay measurements; level checks remain required.
    vals={k.strip().lower():float(v) for k,v in row.items() if 'failed' not in v.lower()}
    waves=trace(a.work/'refinement.printtr0',[w['input'],*OUTS]);assert len(waves)>100
    with (a.results/'worst_transition_waveform.csv').open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=['time_ns',*[n+'_V' for n in [w['input'],*OUTS]]]);writer.writeheader()
        writer.writerows(dict(time_ns=t*1e9,**{n+'_V':d[n] for n in [w['input'],*OUTS]}) for t,d in waves)
    before,after=arithmetic(w['old']),arithmetic(w['new'])
    for j,n in enumerate(OUTS):
        for phase,word in [('pre',before),('post',after)]:
            v=vals[f'{phase}_{n}'];target=(word>>j)&1
            assert .9*summary['voltage_V']<=v<=1.02*summary['voltage_V'] if target else -.02<=v<=.12*summary['voltage_V']
    delay=vals['d_'+w['output']]*1e12;assert delay>0
    model_sha=hashlib.sha256(a.model.read_bytes()).hexdigest()
    result={'status':'PASS',**{k:w[k] for k in ['case','old','new','input','output','direction']},
            'original_max_timestep_ps':summary['max_timestep_ps'],'refined_max_timestep_ps':a.max_step_ps,
            'original_delay_ps':w['delay_ps'],'refined_delay_ps':delay,'difference_ps':delay-w['delay_ps'],
            'relative_difference_percent':100*(delay-w['delay_ps'])/w['delay_ps'],
            'input_crossing_ns':vals['input_mid']*1e9,'output_crossing_ns':vals['output_mid']*1e9,
            'all_logic_levels_pass':True,'initial_result':before,'final_result':after,'waveform_points':len(waves),
            'same_original_netlist':True,'same_original_model':model_sha==summary.get('model_sha256'),
            'model_sha256':model_sha,'netlist_sha256':net_hash(HERE/'rca.sp'),
            'voltage_V':summary['voltage_V'],'corner':summary['corner'],'temperature_C':summary['temperature_C'],
            'output_load_fF':summary['output_load_fF'],'input_slew_ps':summary['input_slew_ps'],
            'refined_other_output_delays_ps':{n:vals['d_'+n]*1e12 for n in OUTS if 'd_'+n in vals},
            'scope':'Refinement of the original sweep worst transition, not a second full sweep.'}
    result['plot_generated']=False if a.no_plot else plot(waves,result,a.results)
    (a.results/'refinement.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
