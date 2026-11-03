#!/usr/bin/env python3
"""Deterministic, offline, synthetic AIS-like observation fixture generator.

This is NOT an AIS payload decoder. It only accepts complete, prevalidated UTC
seconds and decimal physical values, with explicit unavailable-value flags.
"""
import argparse
from datetime import datetime, timedelta, timezone
from decimal import Decimal, InvalidOperation
from pathlib import Path
import json
import re
import hashlib

from rdflib import Graph, Namespace, RDF, XSD, Literal, URIRef

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "tests/observation/fixtures/p04-03-synthetic-input.json"
OUTPUT = ROOT / "examples/p04-03-synthetic-ais.ttl"
EX = Namespace("https://w3id.org/mass-ontology/p04-03/example#")
BH = Namespace("https://w3id.org/mass-ontology/behavior#")
MAR = Namespace("https://w3id.org/mass-ontology/maritime#")
OBS = Namespace("https://w3id.org/mass-ontology/observation#")
SOSA = Namespace("http://www.w3.org/ns/sosa/")
QUDT = Namespace("http://qudt.org/schema/qudt/")
UNIT = Namespace("http://qudt.org/vocab/unit/")
TIME = Namespace("http://www.w3.org/2006/time#")
PROV = Namespace("http://www.w3.org/ns/prov#")


def strict_utc(s):
    if not isinstance(s, str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", s):
        raise ValueError("full-utc-second-timestamp-required")
    try:
        return datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    except ValueError as exc:
        raise ValueError("invalid-utc-timestamp") from exc


def iso(dt):
    return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def stamp(dt):
    return Literal(iso(dt), datatype=XSD.dateTimeStamp)


def decimal(value, field):
    if isinstance(value, bool) or not isinstance(value, str):
        raise ValueError(f"{field}-must-be-decimal-string-or-missing")
    try:
        d = Decimal(value)
    except InvalidOperation as exc:
        raise ValueError(f"invalid-{field}") from exc
    if not d.is_finite():
        raise ValueError(f"nonfinite-{field}")
    return d


def accepted_measurement(row, field, status, unit_key, unit_policy, expected):
    if row.get(status, "valid") == "unavailable":
        if row.get(field) is not None:
            raise ValueError(f"{field}-sentinel-cannot-be-valid-numeric")
        return None
    if row.get(status, "valid") != "valid":
        raise ValueError(f"{field}-invalid-availability-status")
    if row.get(field) is None:
        raise ValueError(f"{field}-missing-with-valid-status")
    if unit_policy.get(unit_key) != expected:
        raise ValueError(f"{field}-invalid-unit-policy")
    return decimal(row[field], field)


def build_graph(cfg):
    if cfg.get("schema_version") != "p04-03-synthetic-1.0" or cfg.get("synthetic_only") is not True:
        raise ValueError("synthetic-p04-03-input-required")
    if cfg.get("source_kind") != "prevalidated-AIS-like-position-report":
        raise ValueError("raw-ais-decoding-outside-p04-03")
    if cfg.get("source_event_time_quality") != "provided-complete-utc":
        raise ValueError("untrusted-or-reconstructed-event-time")
    if cfg.get("message_type") != 1:
        raise ValueError("unexpected-synthetic-message-profile")
    if cfg.get("coordinate_reference_system") != "http://www.opengis.net/def/crs/EPSG/0/4326":
        raise ValueError("unsupported-crs")
    if cfg.get("course_reference") != "degrees true, COG, not heading":
        raise ValueError("unknown-course-reference")
    segmentation = cfg["segmentation"]
    if (segmentation.get("method_id"), segmentation.get("version"), segmentation.get("sample_assignment"), segmentation.get("thresholds")) != ("fixed-boundary-synthetic", "1.0.0", "[start,end)", None):
        raise ValueError("unapproved-segmentation-policy")
    segments = segmentation["segments"]
    if len(segments) != 3 or [s["index"] for s in segments] != [0, 1, 2]:
        raise ValueError("expected-three-indexed-segments")
    ranges = [(strict_utc(s["start"]), strict_utc(s["end"])) for s in segments]
    if any(a >= b for a, b in ranges) or any(ranges[i][1] > ranges[i+1][0] for i in range(2)):
        raise ValueError("invalid-segment-intervals")
    if ranges[1][1] >= ranges[2][0]:
        raise ValueError("expected-deliberate-gap")
    offsets = cfg["message_time_offsets_seconds"]
    if offsets != {"received": 1, "result": 2, "ingested": 3}:
        raise ValueError("unapproved-time-offset-policy")
    g = Graph()
    def put(s,p,o): g.add((s,p,o))
    vessel, traj, run, proc, gap = EX.vessel_001, EX.trajectory_001, EX.segmentation_run, EX.processing_run, EX.coverage_gap_001
    put(vessel,RDF.type,MAR.Vessel)
    put(vessel,BH.hasTrajectory,traj)
    put(traj,RDF.type,BH.Trajectory)
    put(traj,BH.ofVessel,vessel)
    put(traj,PROV.wasGeneratedBy,run)
    put(traj,OBS.hasCoverageGap,gap)
    for activity in (run,proc):put(activity,RDF.type,PROV.Activity)
    put(run,OBS.segmentationMethodId,Literal("fixed-boundary-synthetic"))
    put(run,OBS.segmentationVersion,Literal("1.0.0"))
    put(run,OBS.sampleAssignmentPolicy,Literal("[start,end)"))
    put(gap,RDF.type,OBS.CoverageGap)
    put(gap,OBS.gapStartsAt,stamp(ranges[1][1]))
    put(gap,OBS.gapEndsAt,stamp(ranges[2][0]))
    for i, (a,b) in enumerate(ranges):
        unit, interval, begin, end = [EX[x] for x in (f"unit_{i:03}",f"interval_{i:03}",f"begin_{i:03}",f"end_{i:03}")]
        put(traj,BH.hasTemporalUnit,unit)
        put(unit,RDF.type,BH.TemporalUnit)
        put(unit,BH.partOfTrajectory,traj)
        put(unit,BH.hasTemporalExtent,interval)
        put(unit,BH.segmentIndex,Literal(i,datatype=XSD.nonNegativeInteger))
        put(unit,PROV.wasGeneratedBy,run)
        put(interval,RDF.type,TIME.ProperInterval)
        put(interval,TIME.hasBeginning,begin)
        put(interval,TIME.hasEnd,end)
        for instant,ts in ((begin,a),(end,b)):
            put(instant,RDF.type,TIME.Instant)
            put(instant,TIME.inXSDDateTimeStamp,stamp(ts))
        for kind,cls in (("position",BH.PositionState),("speed",BH.SpeedState),("course",BH.CourseState)):
            state=EX[f"{kind}_{i:03}"]
            put(state,RDF.type,cls)
            put(unit,BH.hasPhysicalBehavior,state)
            put(state,PROV.wasGeneratedBy,proc)
        if i+1<len(ranges):put(unit,BH.nextTemporalUnit,EX[f"unit_{i+1:03}"])
    samples=cfg["samples"]
    if not samples or len({s.get("id") for s in samples})!=len(samples):
        raise ValueError("duplicate-or-missing-sample-id")
    for row in samples:
        name=row["id"]
        if not re.fullmatch(r"\d{3}",name):raise ValueError("invalid-sample-id")
        event=strict_utc(row["event_time"])
        memberships=[i for i,(a,b) in enumerate(ranges) if a<=event<b]
        if len(memberships)!=1:raise ValueError("sample-outside-segment-or-overlap")
        i=memberships[0]
        msg=EX[f"raw_{name}"]
        instant=EX[f"event_{name}"]
        put(msg,RDF.type,OBS.PrevalidatedAISRecord)
        put(msg,OBS.messageType,Literal(cfg["message_type"],datatype=XSD.integer))
        put(msg,OBS.eventTimeQuality,Literal("provided-complete-utc"))
        put(msg,OBS.receivedAtTime,stamp(event+timedelta(seconds=1)))
        put(msg,OBS.ingestedAtTime,stamp(event+timedelta(seconds=3)))
        put(msg,PROV.wasGeneratedBy,proc)
        put(EX[f"unit_{i:03}"],PROV.wasDerivedFrom,msg)
        put(instant,RDF.type,TIME.Instant)
        put(instant,TIME.inXSDDateTimeStamp,stamp(event))
        sog=accepted_measurement(row,"sog_kn","sog_status","sog",cfg["unit_policy"],str(UNIT.KN))
        cog=accepted_measurement(row,"cog_deg","cog_status","cog",cfg["unit_policy"],str(UNIT.DEG))
        if sog is not None and sog<0:raise ValueError("negative-sog")
        if cog is not None and not (0<=cog<360):raise ValueError("invalid-cog")
        if sog is None:put(msg,OBS.sourceAvailability,Literal("SOG:unavailable"))
        if cog is None:put(msg,OBS.sourceAvailability,Literal("COG:unavailable"))
        kinds=[("sog",sog,OBS.SpeedOverGround,BH.SpeedState,UNIT.KN,"speed"),
               ("cog",cog,OBS.CourseOverGround,BH.CourseState,UNIT.DEG,"course")]
        lat=decimal(row["lat_deg"],"lat_deg") if row.get("lat_deg") is not None else None
        lon=decimal(row["lon_deg"],"lon_deg") if row.get("lon_deg") is not None else None
        if (lat is None)!=(lon is None):raise ValueError("partial-position-not-permitted")
        if lat is not None and (not -90<=lat<=90 or not -180<=lon<=180):raise ValueError("invalid-coordinate")
        for kind,value,property_iri,state_cls,unit,short in kinds:
            if value is None:continue
            obs=EX[f"observation_{kind}_{name}"]
            qv=EX[f"quantity_{kind}_{name}"]
            state=EX[f"{short}_{i:03}"]
            put(obs,RDF.type,SOSA.Observation)
            put(obs,SOSA.hasFeatureOfInterest,vessel)
            put(obs,SOSA.observedProperty,property_iri)
            put(obs,SOSA.phenomenonTime,instant)
            put(obs,SOSA.resultTime,stamp(event+timedelta(seconds=2)))
            put(obs,SOSA.hasResult,qv)
            put(obs,PROV.wasDerivedFrom,msg)
            put(obs,PROV.wasGeneratedBy,proc)
            put(qv,RDF.type,QUDT.QuantityValue)
            put(qv,QUDT.numericValue,Literal(str(value),datatype=XSD.decimal))
            put(qv,QUDT.unit,unit)
            put(state,BH.supportedByObservation,obs)
            put(state,BH.hasQuantityValue,qv)
        if lat is None:
            put(msg,OBS.sourceAvailability,Literal("POSITION:unavailable"))
        if lat is not None:
            pos=EX[f"position_result_{name}"]
            obs=EX[f"observation_position_{name}"]
            state=EX[f"position_{i:03}"]
            put(pos,RDF.type,OBS.PositionResult)
            put(pos,OBS.latitudeDegrees,Literal(str(lat),datatype=XSD.decimal))
            put(pos,OBS.longitudeDegrees,Literal(str(lon),datatype=XSD.decimal))
            put(pos,OBS.coordinateReferenceSystem,URIRef(cfg["coordinate_reference_system"]))
            put(obs,RDF.type,SOSA.Observation)
            put(obs,SOSA.hasFeatureOfInterest,vessel)
            put(obs,SOSA.observedProperty,OBS.GeodeticPosition)
            put(obs,SOSA.phenomenonTime,instant)
            put(obs,SOSA.resultTime,stamp(event+timedelta(seconds=2)))
            put(obs,SOSA.hasResult,pos)
            put(obs,PROV.wasDerivedFrom,msg)
            put(obs,PROV.wasGeneratedBy,proc)
            put(state,BH.supportedByObservation,obs)
    return g


def deterministic_turtle(cfg):
    graph=build_graph(cfg)
    # N-Triples is a strict subset of Turtle, with no blank nodes, so sorting
    # yields byte-deterministic valid Turtle while preserving exact RDF terms.
    lines=sorted(x.strip() for x in graph.serialize(format="nt").splitlines() if x.strip())
    return ("# P04-03 SYNTHETIC PREVALIDATED AIS-LIKE DATA; not actual AIS bitstream.\n"
            "# Auto-generated; run scripts/generate_p04_03_fixture.py --check.\n"
            "# Sorted N-Triples triples (valid Turtle); no blank nodes.\n"+"\n".join(lines)+"\n")


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--check",action="store_true",help="Compare generated bytes, do not write")
    ap.add_argument("--input",type=Path,default=INPUT)
    ap.add_argument("--output",type=Path,default=OUTPUT)
    args=ap.parse_args()
    cfg=json.loads(args.input.read_text(encoding="utf-8"))
    result=deterministic_turtle(cfg).encode("utf-8")
    if args.check:
        if not args.output.exists() or args.output.read_bytes()!=result:
            raise SystemExit("P04-03 fixture reproducibility: FAIL")
        print("P04-03 fixture reproducibility: PASS; SHA-256:",hashlib.sha256(result).hexdigest())
    else:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_bytes(result)
        print("Wrote",args.output,"SHA-256",hashlib.sha256(result).hexdigest())

if __name__=="__main__":main()
