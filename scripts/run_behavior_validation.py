#!/usr/bin/env python3
"""P04-04 scoped validation for BH-P04 (DCCR-04). Offline and fail-closed.

Independent OWL classification uses ROBOT/HermiT when available; its absence
is BLOCKED, never silently treated as success. No network dereferencing.
"""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET

from rdflib import Graph, Namespace, RDF, RDFS, OWL, XSD, URIRef, Literal, BNode

ROOT = Path(__file__).resolve().parents[1]
DATA = 'examples/p04-04-synthetic-ais-qudt353.ttl'
SHAPES = 'shapes/ship-behavior-p04.shacl.ttl'
BH = Namespace('https://w3id.org/mass-ontology/behavior#')
MAR = Namespace('https://w3id.org/mass-ontology/maritime#')
OBS = Namespace('https://w3id.org/mass-ontology/observation#')
SOSA = Namespace('http://www.w3.org/ns/sosa/')
QUDT = Namespace('http://qudt.org/schema/qudt/')
UNIT = Namespace('http://qudt.org/vocab/unit/')
QK = Namespace('http://qudt.org/vocab/quantitykind/')
TIME = Namespace('http://www.w3.org/2006/time#')
PROV = Namespace('http://www.w3.org/ns/prov#')
NS_CAT = '{urn:oasis:names:tc:entity:xmlns:xml:catalog}uri'
EXPECTED_KERNEL = '1701bbb86e24588660ef717f2ff7f276b63c938d8569d4511dc19c42033aa788'


class Blocked(Exception):
    pass


def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def one(g, s, p, errors, label):
    values = list(g.objects(s, p))
    if len(values) != 1:
        errors.append(f'{label}: expected exactly one {p}, found {len(values)}')
        return None
    return values[0]


def v01(g):
    errors=[]
    tracks=set(g.subjects(RDF.type, BH.Trajectory))
    if not tracks: errors.append('BH-V01: missing populated trajectory')
    for track in tracks:
        vessel=one(g,track,BH.ofVessel,errors,'BH-V01')
        if vessel is not None:
            if not isinstance(vessel,URIRef) or (vessel,RDF.type,MAR.Vessel) not in g:
                errors.append('BH-V01: vessel not explicitly typed maritime:Vessel')
            if (vessel,BH.hasTrajectory,track) not in g:
                errors.append('BH-V01: reciprocal vessel-trajectory link absent')
    return errors


def v02(g):
    errors=[]
    tracks=set(g.subjects(RDF.type,BH.Trajectory))
    all_units=set(g.subjects(RDF.type,BH.TemporalUnit))
    seen=set()
    for track in tracks:
        units=set(g.objects(track,BH.hasTemporalUnit))
        if not units: errors.append('BH-V02: empty trajectory')
        seen.update(units)
        for unit in units:
            if (unit,RDF.type,BH.TemporalUnit) not in g:
                errors.append('BH-V02: temporal unit not explicitly typed')
            parent=one(g,unit,BH.partOfTrajectory,errors,'BH-V02')
            if parent!=track: errors.append('BH-V02: mismatched parent link')
            interval=one(g,unit,BH.hasTemporalExtent,errors,'BH-V02')
            if interval is not None:
                if interval==unit or (interval,RDF.type,TIME.ProperInterval) not in g:
                    errors.append('BH-V02: interval is not a distinct explicitly typed ProperInterval')
    for unit in all_units:
        if unit not in seen: errors.append('BH-V02: unlinked temporal unit')
        parent=one(g,unit,BH.partOfTrajectory,errors,'BH-V02')
        if parent is not None and (parent,BH.hasTemporalUnit,unit) not in g:
            errors.append('BH-V02: missing reciprocal parent membership')
    return errors


def instant(g,node,errors):
    if node is None or (node,RDF.type,TIME.Instant) not in g:
        errors.append('BH-V03: missing explicitly typed Instant')
        return None
    lit=one(g,node,TIME.inXSDDateTimeStamp,errors,'BH-V03')
    if not isinstance(lit,Literal) or lit.datatype!=XSD.dateTimeStamp:
        errors.append('BH-V03: expected xsd:dateTimeStamp')
        return None
    try:
        dt=datetime.fromisoformat(str(lit).replace('Z','+00:00'))
        if dt.tzinfo is None or dt.utcoffset() is None:
            raise ValueError('timezone absent')
        return dt.astimezone(timezone.utc)
    except (ValueError,OverflowError):
        errors.append('BH-V03: invalid or non-offset-aware timestamp')
        return None


def bounds(g,unit,errors):
    extent=one(g,unit,BH.hasTemporalExtent,errors,'BH-V03')
    if extent is None: return None
    a=instant(g,one(g,extent,TIME.hasBeginning,errors,'BH-V03'),errors)
    b=instant(g,one(g,extent,TIME.hasEnd,errors,'BH-V03'),errors)
    if a is None or b is None: return None
    if a>=b: errors.append('BH-V03: reversed or zero-length interval')
    return a,b


def v03(g):
    errors=[]
    for track in g.subjects(RDF.type,BH.Trajectory):
        slots=[]
        for unit in g.objects(track,BH.hasTemporalUnit):
            ind=one(g,unit,BH.segmentIndex,errors,'BH-V03')
            if not isinstance(ind,Literal) or ind.datatype!=XSD.nonNegativeInteger:
                errors.append('BH-V03: index must be xsd:nonNegativeInteger')
                continue
            try: idx=int(str(ind))
            except ValueError:
                errors.append('BH-V03: invalid segment index')
                continue
            b=bounds(g,unit,errors)
            if b is not None: slots.append((idx,unit,*b))
        slots.sort(key=lambda x:x[0])
        if [x[0] for x in slots]!=list(range(len(slots))) or len(slots)!=len(set(g.objects(track,BH.hasTemporalUnit))):
            errors.append('BH-V03: non-contiguous, duplicate or missing indices')
        for i,(_,unit,start,end) in enumerate(slots):
            target=set(g.objects(unit,BH.nextTemporalUnit))
            expected={slots[i+1][1]} if i+1<len(slots) else set()
            if target!=expected: errors.append('BH-V03: invalid nextTemporalUnit sequence')
            if i and start<slots[i-1][3]: errors.append('BH-V03: overlapping intervals')
        # Deliberate synthetic coverage gap must be present and match known interval boundaries.
        if len(slots)==3:
            gap_nodes=list(g.objects(track,OBS.hasCoverageGap))
            if len(gap_nodes)!=1:
                errors.append('BH-V03: missing synthetic coverage-gap record')
            else:
                gap=gap_nodes[0]
                gap_a=one(g,gap,OBS.gapStartsAt,errors,'BH-V03')
                gap_b=one(g,gap,OBS.gapEndsAt,errors,'BH-V03')
                if not isinstance(gap_a,Literal) or not isinstance(gap_b,Literal):
                    errors.append('BH-V03: coverage gap timestamps missing')
                elif len(slots)==3:
                    if str(gap_a)!=slots[1][3].strftime('%Y-%m-%dT%H:%M:%SZ') or str(gap_b)!=slots[2][2].strftime('%Y-%m-%dT%H:%M:%SZ'):
                        errors.append('BH-V03: coverage gap does not equal unobserved interval')
    return errors


def v05(g,behavior_schema):
    errors=[]
    for cls in (BH.PositionState,BH.SpeedState,BH.CourseState):
        if any((cls,OWL.disjointWith,o) in behavior_schema or (o,OWL.disjointWith,cls) in behavior_schema
               for o in (BH.PositionState,BH.SpeedState,BH.CourseState) if o!=cls):
            errors.append('BH-V05: prohibited physical dimension disjointness')
    for unit in g.subjects(RDF.type,BH.TemporalUnit):
        states=list(g.objects(unit,BH.hasPhysicalBehavior))
        for cls in (BH.PositionState,BH.SpeedState,BH.CourseState):
            if not any((s,RDF.type,cls) in g for s in states):
                errors.append(f'BH-V05: {unit} missing dimension {cls}')
    return errors


def v06(g,unit_graph=None,qkind_graph=None,dim_graph=None):
    errors=[]
    descriptions=set(g.subjects(RDF.type,BH.SpeedState)) | set(g.subjects(RDF.type,BH.CourseState))
    if not descriptions: errors.append('BH-V06: no speed/course descriptions')
    expected_by_class={BH.SpeedState:(UNIT.KN,QK.Speed),BH.CourseState:(UNIT.DEG,QK.Angle)}
    for desc in descriptions:
        cls=BH.SpeedState if (desc,RDF.type,BH.SpeedState) in g else BH.CourseState
        expected_unit,_=expected_by_class[cls]
        observations=list(g.objects(desc,BH.supportedByObservation))
        quantities=set(g.objects(desc,BH.hasQuantityValue))
        if not observations or not quantities:errors.append('BH-V06: missing observation/quantity evidence')
        for obs in observations:
            if (obs,RDF.type,SOSA.Observation) not in g:
                errors.append('BH-V06: unsupported observation typing')
            qv=one(g,obs,SOSA.hasResult,errors,'BH-V06')
            if qv is not None and qv not in quantities:
                errors.append('BH-V06: quantity missing reciprocal evidence link')
        for qv in quantities:
            if (qv,RDF.type,QUDT.QuantityValue) not in g:
                errors.append('BH-V06: quantity not explicitly typed QUDT QuantityValue')
            num=one(g,qv,QUDT.numericValue,errors,'BH-V06')
            if not isinstance(num,Literal) or num.datatype!=XSD.decimal:
                errors.append('BH-V06: invalid decimal numeric value')
            unit=one(g,qv,QUDT.hasUnit,errors,'BH-V06')
            if unit!=expected_unit:errors.append(f'BH-V06: invalid speed/course unit {unit}')
            if list(g.objects(qv,QUDT.unit)):
                errors.append('BH-V06: forbidden legacy qudt:unit')
    if unit_graph is None or qkind_graph is None or dim_graph is None:
        raise Blocked('BH-V06: pinned QUDT units/quantitykind/dimensionvector graphs unavailable')
    # Check the exact pinned source graphs, never a hardcoded dimensional assumption.
    for unit,kind in expected_by_class.values():
        uv=set(unit_graph.objects(unit,QUDT.hasDimensionVector))
        kv=set(qkind_graph.objects(kind,QUDT.hasDimensionVector))
        if not uv or not kv or not uv.intersection(kv):
            errors.append(f'BH-V06: external QUDT dimension mismatch for {unit}/{kind}')
        for dim in uv | kv:
            if not list(dim_graph.predicate_objects(dim)):
                errors.append(f'BH-V06: dimension vector {dim} absent from pinned graph')
    return errors


def load_vendor_graphs(repo):
    paths=['qudt-unit-3.5.3.ttl','qudt-quantitykind-3.5.3.ttl','qudt-dimensionvector-3.5.3.ttl']
    gs=[]
    for p in paths:
        f=repo/'vendor/external-rdf/T04-2026'/p
        if not f.is_file(): raise Blocked(f'QUDT RDF snapshot unavailable: {p}')
        g=Graph()
        g.parse(f,format='turtle')
        gs.append(g)
    return gs


def local_catalog_issues(repo, catalog=None, extra_schema=None):
    errors=[]
    cp=catalog or repo/'catalog-v001.xml'
    try: entries=ET.parse(cp).getroot().findall(NS_CAT)
    except Exception as e: return [f'BH-V11: invalid catalog XML: {e}']
    mapping={}
    for entry in entries:
        name=entry.get('name');loc=entry.get('uri')
        if not name or not loc or name in mapping or not name.startswith('https://w3id.org/mass-ontology/'):
            errors.append('BH-V11: invalid/duplicate local ontology IRI mapping')
            continue
        path=repo/loc
        if path.is_symlink() or not path.is_file() or not path.resolve().is_relative_to(repo.resolve()):
            errors.append(f'BH-V11: catalog missing/escaping local file {loc}')
            continue
        g=Graph()
        try:g.parse(path,format='turtle')
        except Exception as e:
            errors.append(f'BH-V11: catalog RDF not parseable: {loc}: {e}')
            continue
        if (URIRef(name),RDF.type,OWL.Ontology) not in g:
            errors.append(f'BH-V11: ontology IRI mismatch: {name}')
        mapping[name]=g
    imports=Graph()
    for g in mapping.values():
        for triple in g.triples((None,OWL.imports,None)): imports.add(triple)
    if extra_schema is not None:
        for triple in extra_schema.triples((None,OWL.imports,None)): imports.add(triple)
    for imp in imports.objects(None,OWL.imports):
        if str(imp) not in mapping:
            errors.append(f'BH-V11: unresolved or external owl:imports: {imp}')
    if not mapping or len(mapping)<11: errors.append('BH-V11: incomplete MASS local ontology catalog')
    return errors


def t04_verify(repo):
    file=repo/'scripts/t04_pin_external_rdf.py'
    if not file.is_file(): raise Blocked('BH-V11: T-04 source integrity script missing')
    spec=importlib.util.spec_from_file_location('t04_verified',file)
    m=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    try:m.verify(repo,require_approved=True)
    except OSError as e: raise Blocked(f'BH-V11: T-04 cannot access pinned files: {e}') from e
    except (ValueError,KeyError) as e:
        message=str(e)
        if any(x in message.lower() for x in ('missing', 'unavailable', 'run --acquire')):
            raise Blocked(f'BH-V11: T-04 source unavailable: {message}') from e
        raise ValueError(f'BH-V11: T-04 locked source integrity violation: {message}') from e


def kernel_hash_ok(path):
    return path.is_file() and sha256(path)==EXPECTED_KERNEL


def robot_check(repo, robot=None):
    executable=robot or shutil.which('robot')
    if not executable: raise Blocked('BH-V05: ROBOT/HermiT executable not installed')
    s=Graph()
    s.parse(repo/'07-behavior/ship-behavior.ttl',format='turtle')
    # Full local Behavior schema plus the revised positive instance fixture.
    # Strip owl:imports in this *temporary reasoner input* so ROBOT cannot fetch
    # mutable live ontologies; authoritative external byte locks are V11's gate.
    relevant=Graph()
    for path in (repo/'07-behavior/ship-behavior.ttl',
                 repo/'07-behavior/behavior-observation-bridge.ttl',repo/DATA):
        gpart=Graph()
        gpart.parse(path,format='turtle')
        for subject,pred,obj in gpart:
            if pred != OWL.imports: relevant.add((subject,pred,obj))
    test_subject=URIRef('https://w3id.org/mass-ontology/validation#coexisting-dimensions')
    for cls in (BH.PositionState,BH.SpeedState,BH.CourseState):
        relevant.add((test_subject,RDF.type,cls))
    def call(gg,path,output):
        gg.serialize(path,format='turtle')
        cmd=[executable,'reason','--reasoner','HermiT','--input',str(path),'--output',str(output)]
        try: return subprocess.run(cmd,cwd=repo,text=True,capture_output=True,timeout=180)
        except (OSError,subprocess.TimeoutExpired) as e: raise Blocked(f'BH-V05: ROBOT failed to execute: {e}') from e
    with tempfile.TemporaryDirectory(prefix='p04-v05-') as td:
        t=Path(td)
        good=call(relevant,t/'good.ttl',t/'good.owl')
        mutated=Graph()
        for tr in relevant: mutated.add(tr)
        mutated.add((BH.SpeedState,OWL.disjointWith,BH.CourseState))
        bad=call(mutated,t/'mutant.ttl',t/'mutant.owl')
        if good.returncode!=0:
            return [f'BH-V05: HermiT rejected clean ontology: {(good.stderr or good.stdout)[-500:]}']
        if bad.returncode==0:
            return ['BH-V05: HermiT failed to reject disjointness mutant']
        text=(bad.stderr+'\n'+bad.stdout).lower()
        if not any(x in text for x in ('inconsisten','unsatisfi','incoheren')):
            return ['BH-V05: mutant failed for non-semantic reason (not a valid reasoner oracle): '+text[-250:]]
    return []


def shacl_issues(repo,data):
    """Run rule-specific SHACL shapes independently; never misattribute failure."""
    try:from pyshacl import validate
    except ImportError as e: raise Blocked('P04 SHACL: pyshacl package unavailable') from e
    source=Graph()
    source.parse(repo/SHAPES,format='turtle')
    target_shapes={'BH-V01':BH.P04TrajectoryShape,
                   'BH-V02':BH.P04TemporalUnitShape,
                   'BH-V06':BH.P04QuantityShape}
    results={}
    for rule,root in target_shapes.items():
        isolated=Graph()
        pending=[root]
        visited=set()
        while pending:
            subject=pending.pop()
            if subject in visited:continue
            visited.add(subject)
            for pred,obj in source.predicate_objects(subject):
                isolated.add((subject,pred,obj))
                if isinstance(obj,BNode):pending.append(obj)
        if not isolated:raise ValueError(f'{rule} SHACL shape missing')
        conforms,report,message=validate(data_graph=data,shacl_graph=isolated,
            inference='none',advanced=False,abort_on_first=False,
            allow_infos=False,allow_warnings=False)
        results[rule]=[] if conforms else [f'{rule} SHACL nonconformity: {message[-2800:]}']
    return results


def legacy_check(repo):
    commands=[('catalog',['make','catalog']),('validate',['make','validate']),
              ('cq',['make','cq']),('test',['make','test']),('kernel',['python3','scripts/verify_sysml_kernel_integrity.py'])]
    evidence=[]
    for name,cmd in commands:
        try:r=subprocess.run(cmd,cwd=repo,capture_output=True,text=True,timeout=150)
        except (OSError,subprocess.TimeoutExpired) as e:
            evidence.append({'command':name,'status':'BLOCKED','detail':str(e)})
            continue
        evidence.append({'command':name,'status':'PASS' if r.returncode==0 else 'FAIL',
                         'exit_code':r.returncode,'tail':(r.stdout+'\n'+r.stderr)[-1600:]})
    return evidence


def evaluate(repo,do_legacy=False,robot=None):
    result={rule:{'status':'PENDING','issues':[]} for rule in ('BH-V01','BH-V02','BH-V03','BH-V05','BH-V06','BH-V11','BH-V12')}
    def record(rule,fun):
        try:
            issues=fun()
            result[rule]={'status':'FAIL' if issues else 'PASS','issues':issues}
        except Blocked as e:
            result[rule]={'status':'BLOCKED','issues':[str(e)]}
        except Exception as e:
            result[rule]={'status':'FAIL','issues':[f'unexpected validation error: {type(e).__name__}: {e}']}
    try:
        g=Graph();g.parse(repo/DATA,format='turtle')
        schema=Graph();schema.parse(repo/'07-behavior/ship-behavior.ttl',format='turtle')
        try:shacl=shacl_issues(repo,g)
        except Blocked as e:shacl={id:[str(e)] for id in ('BH-V01','BH-V02','BH-V06')}
    except Exception as e:
        g=None;schema=None;shacl={id:[f'Cannot parse P04 source: {e}'] for id in ('BH-V01','BH-V02','BH-V06')}
    if g is None:
        for rule in ('BH-V01','BH-V02','BH-V03','BH-V05','BH-V06'):
            result[rule]={'status':'BLOCKED','issues':shacl.get(rule,[])}
    else:
        for id,fun in [('BH-V01',lambda:v01(g)),('BH-V02',lambda:v02(g)),('BH-V03',lambda:v03(g))]:
            record(id,fun)
        def reasoned_v05():
            baseline=v05(g,schema)
            if baseline:return baseline
            return robot_check(repo,robot)
        record('BH-V05',reasoned_v05)
        def qcheck():
            t04_verify(repo)
            return v06(g,*load_vendor_graphs(repo))
        record('BH-V06',qcheck)
        # Every SHACL rule is required; no cross-attribution between rules.
        for id in ('BH-V01','BH-V02','BH-V06'):
            problems=shacl.get(id,[])
            if problems and result[id]['status']=='PASS':
                result[id]={'status':'BLOCKED' if problems[0].startswith('P04 SHACL')
                            else 'FAIL','issues':problems}
    record('BH-V11',lambda:(t04_verify(repo),local_catalog_issues(repo))[1])
    def check_v12():
        src=repo/'baselines/sysml/MASS-SK-1.0/MASSKernel_v1.0.sysml'
        if not kernel_hash_ok(src):return ['BH-V12: MASS-SK-1.0 SHA-256 differs from immutable baseline']
        if not do_legacy:raise Blocked('BH-V12: legacy make catalog/validate/cq and SysML checks not executed; run --legacy')
        logs=legacy_check(repo)
        result['legacy_executions']=logs
        failures=[f"BH-V12: {x['command']} {x['status']}" for x in logs if x['status']!='PASS']
        if failures:return failures
        # make test explicitly run separately, avoiding recursion.
        return []
    record('BH-V12',check_v12)
    git=subprocess.run(['git','rev-parse','HEAD'],cwd=repo,capture_output=True,text=True)
    tested_sha=git.stdout.strip() if git.returncode==0 else None
    lock_path=repo/'docs/standards/T04-external-rdf-lock.json'
    result['_meta']={'profile':'p04','tested_commit':tested_sha,
       'executed_utc':datetime.now(timezone.utc).isoformat(timespec='seconds'),
       'python_version':sys.version.split()[0],
       't04_lock_sha256':sha256(lock_path) if lock_path.is_file() else None,
       'validated_fixture':DATA,
       'fixture_sha256':sha256(repo/DATA) if (repo/DATA).is_file() else None,
       'source_baseline':'baf84cdbd5732d5f243c0625705fce77f2cb5cc3',
       'full_pytest_required_when_legacy_false':True,
       'bh_cq_01_03':'DEFERRED to P04-05'}
    return result


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--profile',required=True,choices=('p04','p05','p09'))
    ap.add_argument('--repo',type=Path,default=ROOT)
    ap.add_argument('--legacy',action='store_true')
    ap.add_argument('--robot',default=None)
    ap.add_argument('--report',type=Path)
    a=ap.parse_args()
    if a.profile!='p04':
        print(f'PROFILE {a.profile}: DEFERRED — only p04 implemented; no false PASS')
        return 2
    repo=a.repo.resolve()
    results=evaluate(repo,a.legacy,a.robot)
    for rule in ('BH-V01','BH-V02','BH-V03','BH-V05','BH-V06','BH-V11','BH-V12'):
        r=results[rule]
        print(f'{rule} {r["status"]}')
        for issue in r['issues'][:4]:print(' ',issue[:400])
    if a.report:
        target=a.report if a.report.is_absolute() else repo/a.report
        target.parent.mkdir(parents=True,exist_ok=True)
        target.write_text(json.dumps(results,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
        print('Report:',target)
    return 0 if all(results[r]['status']=='PASS' for r in ('BH-V01','BH-V02','BH-V03','BH-V05','BH-V06','BH-V11','BH-V12')) else 2

if __name__=='__main__':sys.exit(main())
