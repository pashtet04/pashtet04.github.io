from pathlib import Path

path = Path("index.html")
html = path.read_text(encoding="utf-8")

replacements = {
    'Pavel Klyuev — Principal SRE and Platform Engineer. Production Kubernetes for AI, data and real-time voice systems.':
        'Pavel Klyuev — Principal SRE / Platform Engineer helping teams build, stabilize and simplify production infrastructure.',
    'Production Kubernetes for AI, data and voice: infrastructure, delivery, secrets, networking and operations.':
        'Build, stabilize and simplify production infrastructure: Kubernetes, delivery, reliability, secrets, networking and stateful systems.',
    '<div class="panel intro"><p class="eyebrow">Kubernetes platforms / security / AI / voice</p><h1>Pavel Klyuev</h1><span class="role">Principal SRE / Platform Engineer</span><p class="lead">Production Kubernetes for AI, data and voice.</p><p class="focus">10+ years · GKE, AWS, Yandex Cloud, Hetzner · Production systems</p><div class="actions"><a class="button primary" href="#services">Services</a><a class="button" href="#work">Selected work</a><a class="button" href="#contact">Contact</a></div></div>':
        '<div class="panel intro"><p class="eyebrow">Production infrastructure / reliability / platform engineering</p><h1>Pavel Klyuev</h1><span class="role">Principal SRE / Platform Engineer</span><p class="lead">Build, stabilize and simplify production infrastructure.</p><p class="lead-detail">Kubernetes platforms, delivery, secrets, networking and stateful systems — including AI, data and real-time voice.</p><p class="focus">10+ years · GKE, AWS, Yandex Cloud, Hetzner · hands-on production work</p><p class="availability">Available for audits, platform builds, migrations and ongoing SRE work.</p><div class="actions"><a class="button primary" href="#contact">Discuss a project</a><a class="button" href="#work">Selected work</a><a class="button" href="#services">Services</a></div></div>',
    '<article class="panel service"><h3>Infrastructure Audit</h3><p>Review the platform, find operational risks, produce a fix plan.</p>':
        '<article class="panel service"><h3>Infrastructure Audit</h3><p>A focused review of the platform, its failure modes and recovery path.</p>',
    '<article class="panel service"><h3>Platform Engineering</h3><p>Build and standardize Kubernetes platforms and delivery workflows.</p>':
        '<article class="panel service"><h3>Platform Engineering</h3><p>Build a platform teams can deploy to without rebuilding the same infrastructure for every service.</p>',
    '<article class="panel service"><h3>Production Reliability</h3><p>Fix recurring production problems and reduce operational load.</p>':
        '<article class="panel service"><h3>Production Reliability</h3><p>Fix recurring incidents, capacity problems and the parts of production that need constant attention.</p>',
    '<article class="panel service"><h3>Security and Secrets</h3><p>Build and harden secrets management for Kubernetes.</p>':
        '<article class="panel service"><h3>Security and Secrets</h3><p>Make secrets, certificates and access controlled, automated and recoverable.</p>',
    '<article class="panel service"><h3>AI and Voice Infrastructure</h3><p>Run AI, retrieval and real-time voice workloads in production.</p>':
        '<article class="panel service"><h3>AI and Voice Infrastructure</h3><p>Put AI, retrieval and real-time voice workloads into production with the right network, capacity and observability.</p>',
    '<article class="panel contact"><p class="eyebrow">Contact</p><h2>Contact</h2><p>For SRE, platform engineering, Kubernetes and production infrastructure work.</p>':
        '<article class="panel contact"><p class="eyebrow">Contact</p><h2>Contact</h2><p>For audits, platform engineering, reliability work, migrations and production infrastructure.</p>'
}

for old, new in replacements.items():
    if old not in html:
        raise SystemExit(f"Expected homepage fragment not found: {old[:90]}")
    html = html.replace(old, new, 1)

hero_end = '''      </section>\n\n      <section class="section" id="services">'''
outcome_block = '''      </section>\n\n      <section class="outcome-strip" aria-label="Typical production problems">\n        <article><b>Unstable production</b><p>Recurring incidents, overloaded components, unclear failure modes or slow recovery.</p></article>\n        <article><b>Platform growing too fast</b><p>Standardize Kubernetes, delivery, networking and secrets before every team invents its own path.</p></article>\n        <article><b>Too much operational work</b><p>Automate routine changes and recovery, cut recurring toil and make ownership clearer.</p></article>\n        <article><b>Complex workloads going live</b><p>AI, data and voice systems with real requirements around latency, state, isolation and observability.</p></article>\n      </section>\n\n      <section class="section" id="services">'''
if hero_end not in html:
    raise SystemExit("Hero/services boundary not found")
html = html.replace(hero_end, outcome_block, 1)

contact_marker = '''      <section class="section notes-contact" id="contact">'''
hire_block = '''      <section class="hire panel" aria-label="Work together">\n        <div><p class="eyebrow">Work together</p><h2>Production problem that needs an owner?</h2><p>Available for focused audits, architecture work, hands-on implementation and ongoing SRE / platform support.</p></div>\n        <div class="hire-side"><p>Platform audits · reliability · migrations · Kubernetes platforms · AI / data / voice infrastructure</p><a class="button primary" href="mailto:pavel@klyuev.icu">Discuss a project →</a></div>\n      </section>\n\n      <section class="section notes-contact" id="contact">'''
if contact_marker not in html:
    raise SystemExit("Contact marker not found")
html = html.replace(contact_marker, hire_block, 1)

extra_css = '''\n    .lead{color:var(--strong);font-size:clamp(22px,2.3vw,29px);font-weight:600;line-height:1.15;letter-spacing:-.025em}.lead-detail{margin:13px 0 0;max-width:60ch;color:var(--muted);font-size:15px;line-height:1.5}.availability{margin:13px 0 0;color:var(--accent);font:600 11px/1.5 var(--mono)}\n    .outcome-strip{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:1px;margin:0 0 26px;border:1px solid var(--border);background:var(--border)}.outcome-strip article{background:var(--paper);padding:18px;min-width:0}.outcome-strip b{display:block;color:var(--strong);font:700 13px/1.25 var(--mono)}.outcome-strip p{margin:9px 0 0;color:var(--muted);font-size:13px;line-height:1.48}\n    .hire{display:grid;grid-template-columns:minmax(0,1.25fr) minmax(300px,.75fr);gap:34px;align-items:end;margin:26px 0 6px;padding:26px}.hire .eyebrow{margin-bottom:15px}.hire h2{margin:0;color:var(--strong);font-size:clamp(30px,4vw,48px);line-height:.98;letter-spacing:-.05em}.hire>div>p:not(.eyebrow){margin:15px 0 0;color:var(--muted);max-width:68ch}.hire-side{display:flex;flex-direction:column;align-items:flex-start}.hire-side p{font:600 11px/1.6 var(--mono)!important}.hire-side .button{margin-top:18px}\n    @media(max-width:980px){.outcome-strip{grid-template-columns:repeat(2,minmax(0,1fr))}.hire{grid-template-columns:1fr}}\n    @media(max-width:680px){.outcome-strip{grid-template-columns:1fr}.hire{padding:16px}.lead{font-size:22px}}\n'''
style_close = "</style>"
if style_close not in html:
    raise SystemExit("Style close not found")
html = html.replace(style_close, extra_css + style_close, 1)

path.write_text(html, encoding="utf-8")
