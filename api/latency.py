import json
import numpy as np

DATA = [
  {"region":"apac","service":"catalog","latency_ms":188.02,"uptime_pct":98.428},
  {"region":"apac","service":"checkout","latency_ms":129.68,"uptime_pct":98.543},
  {"region":"apac","service":"payments","latency_ms":220.35,"uptime_pct":98.353},
  {"region":"apac","service":"recommendations","latency_ms":219.5,"uptime_pct":97.567},
  {"region":"apac","service":"catalog","latency_ms":177.6,"uptime_pct":98.52},
  {"region":"apac","service":"analytics","latency_ms":202.4,"uptime_pct":98.191},
  {"region":"apac","service":"payments","latency_ms":173.11,"uptime_pct":98.007},
  {"region":"apac","service":"payments","latency_ms":228.75,"uptime_pct":97.659},
  {"region":"apac","service":"support","latency_ms":191.06,"uptime_pct":98.981},
  {"region":"apac","service":"analytics","latency_ms":186.25,"uptime_pct":97.536},
  {"region":"apac","service":"payments","latency_ms":227.95,"uptime_pct":99.096},
  {"region":"apac","service":"recommendations","latency_ms":168.52,"uptime_pct":99.405},
  {"region":"emea","service":"catalog","latency_ms":181.04,"uptime_pct":99.344},
  {"region":"emea","service":"recommendations","latency_ms":119.76,"uptime_pct":99.388},
  {"region":"emea","service":"analytics","latency_ms":106.12,"uptime_pct":97.699},
  {"region":"emea","service":"support","latency_ms":194.31,"uptime_pct":98.969},
  {"region":"emea","service":"payments","latency_ms":171.4,"uptime_pct":98.785},
  {"region":"emea","service":"catalog","latency_ms":141.65,"uptime_pct":99.324},
  {"region":"emea","service":"analytics","latency_ms":138.13,"uptime_pct":97.869},
  {"region":"emea","service":"payments","latency_ms":139.8,"uptime_pct":97.848},
  {"region":"emea","service":"payments","latency_ms":208.01,"uptime_pct":98.192},
  {"region":"emea","service":"catalog","latency_ms":128.47,"uptime_pct":98.252},
  {"region":"emea","service":"analytics","latency_ms":207.31,"uptime_pct":97.791},
  {"region":"emea","service":"recommendations","latency_ms":182.25,"uptime_pct":97.744},
  {"region":"amer","service":"recommendations","latency_ms":147.7,"uptime_pct":98.477},
  {"region":"amer","service":"catalog","latency_ms":160.6,"uptime_pct":98.347},
  {"region":"amer","service":"checkout","latency_ms":147.99,"uptime_pct":97.598},
  {"region":"amer","service":"payments","latency_ms":227.64,"uptime_pct":98.912},
  {"region":"amer","service":"support","latency_ms":132.43,"uptime_pct":97.563},
  {"region":"amer","service":"catalog","latency_ms":176.61,"uptime_pct":98.028},
  {"region":"amer","service":"analytics","latency_ms":220.11,"uptime_pct":99.287},
  {"region":"amer","service":"payments","latency_ms":130.67,"uptime_pct":99.421},
  {"region":"amer","service":"analytics","latency_ms":221.81,"uptime_pct":97.162},
  {"region":"amer","service":"payments","latency_ms":189.63,"uptime_pct":97.148},
  {"region":"amer","service":"checkout","latency_ms":136.81,"uptime_pct":98.554},
  {"region":"amer","service":"analytics","latency_ms":173.3,"uptime_pct":97.844}
]

def handler(request):
    if request.method == "OPTIONS":
        from http import HTTPStatus
        return Response(
            status_code=200,
            headers={
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "POST, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type",
            }
        )

    body = json.loads(request.body)
    regions = body.get("regions", [])
    threshold_ms = body.get("threshold_ms", 180)

    result = {}
    for region in regions:
        records = [d for d in DATA if d["region"] == region]
        if not records:
            continue
        latencies = [r["latency_ms"] for r in records]
        uptimes = [r["uptime_pct"] for r in records]
        n = len(latencies)
        sorted_l = sorted(latencies)
        p95_idx = int(0.95 * n)
        p95 = sorted_l[min(p95_idx, n-1)]
        result[region] = {
            "avg_latency": round(sum(latencies) / n, 4),
            "p95_latency": round(p95, 4),
            "avg_uptime": round(sum(uptimes) / n, 4),
            "breaches": sum(1 for l in latencies if l > threshold_ms)
        }

    return Response(
        body=json.dumps(result),
        headers={
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
        }
    )
