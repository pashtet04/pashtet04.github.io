from pathlib import Path

path = Path("index.html")
text = path.read_text(encoding="utf-8")

replacements = {
    'content="Pavel Klyuev — Principal SRE / Platform Engineer helping teams build, stabilize and simplify production infrastructure."': 'content="Pavel Klyuev — Principal SRE / Platform Engineer. Kubernetes, cloud infrastructure and production systems."',
    'content="Build, stabilize and simplify production infrastructure: Kubernetes, delivery, reliability, secrets, networking and stateful systems."': 'content="Kubernetes, cloud infrastructure, reliability, networking, databases and observability."',
    '<p class="eyebrow">Production infrastructure / reliability / platform engineering</p>': '<p class="eyebrow">SRE / Platform Engineering / Production</p>',
    '<p class="lead">Build, stabilize and simplify production infrastructure.</p>': '<p class="lead">Build and run reliable production systems.</p>',
    '<p class="lead-detail">Kubernetes platforms, delivery, secrets, networking and stateful systems — including AI, data and real-time voice.</p>': '<p class="lead-detail">Kubernetes, cloud, CI/CD, networking, databases and observability. AI, data and voice workloads when needed.</p>',
    '<p class="focus">10+ years · GKE, AWS, Yandex Cloud, Hetzner · hands-on production work</p>': '<p class="focus">10+ years in production · GKE · AWS · Yandex Cloud · Hetzner</p>',
    '<p class="availability">Available for audits, platform builds, migrations and ongoing SRE work.</p>': '<p class="availability">Available for audits, migrations, platform work and ongoing SRE support.</p>',
    '<div class="cycle-head"><h2>Production systems, end to end</h2><p>6 stages / one production loop</p></div>': '<div class="cycle-head"><h2>How I work</h2><p>from design to operations</p></div>',
    '<b>Plan</b><p>Architecture, capacity, risks and ownership.</p><small>OUTPUT: design + rollback</small>': '<b>Plan</b><p>Architecture, risks, capacity and rollback.</p>',
    '<b>Build</b><p>Infrastructure, clusters, delivery and secrets as code.</p><small>OUTPUT: Terraform + Helm</small>': '<b>Build</b><p>Infrastructure, Kubernetes, networking and secrets.</p>',
    '<b>Release</b><p>CI/CD, GitOps, migrations and health checks.</p><small>OUTPUT: repeatable deploy</small>': '<b>Release</b><p>CI/CD, GitOps, migrations and checks.</p>',
    '<b>Improve</b><p>Fix recurring failures. Automate manual work.</p><small>OUTPUT: fewer failure modes</small>': '<b>Improve</b><p>Fix recurring issues and reduce manual work.</p>',
    '<b>Observe</b><p>SLIs, SLOs, metrics, logs, traces and alerts.</p><small>OUTPUT: known system state</small>': '<b>Observe</b><p>Metrics, logs, traces, alerts and SLOs.</p>',
    '<b>Operate</b><p>Traffic, stateful services, incidents and recovery.</p><small>OUTPUT: stable production</small>': '<b>Operate</b><p>Traffic, databases, queues, incidents and recovery.</p>',
    '<article><b>Unstable production</b><p>Recurring incidents, overloaded components, unclear failure modes or slow recovery.</p></article>': '<article><b>Production is unstable</b><p>Incidents repeat, capacity runs out or recovery takes too long.</p></article>',
    '<article><b>Platform growing too fast</b><p>Standardize Kubernetes, delivery, networking and secrets before every team invents its own path.</p></article>': '<article><b>Infrastructure is hard to change</b><p>Deploys and infrastructure changes take too much effort or carry too much risk.</p></article>',
    '<article><b>Too much operational work</b><p>Automate routine changes and recovery, cut recurring toil and make ownership clearer.</p></article>': '<article><b>Too much manual work</b><p>Routine operations, maintenance and recovery consume engineering time.</p></article>',
    '<article><b>Complex workloads going live</b><p>AI, data and voice systems with real requirements around latency, state, isolation and observability.</p></article>': '<article><b>Complex workloads need a platform</b><p>AI, data and voice workloads need the right network, capacity and observability.</p></article>',
    '<h2>Production problem that needs an owner?</h2>': '<h2>Need help with production infrastructure?</h2>',
    '<p>Available for focused audits, architecture work, hands-on implementation and ongoing SRE / platform support.</p>': '<p>Available for audits, migrations, platform builds and ongoing SRE work.</p>',
    '<p>Platform audits · reliability · migrations · Kubernetes platforms · AI / data / voice infrastructure</p>': '<p>Audits · reliability · migrations · Kubernetes · AI / data / voice infrastructure</p>',
}

missing = []
for old, new in replacements.items():
    if old not in text:
        missing.append(old)
    else:
        text = text.replace(old, new)

if missing:
    raise SystemExit("Missing expected text:\n" + "\n---\n".join(missing))

# With OUTPUT lines removed, the lifecycle can be more compact.
text = text.replace('min-height:530px', 'min-height:430px')
text = text.replace('min-height:174px', 'min-height:138px')

path.write_text(text, encoding="utf-8")
