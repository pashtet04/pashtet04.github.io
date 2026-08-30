from pathlib import Path
import re

path = Path("index.html")
text = path.read_text(encoding="utf-8")

replacements = {
    'content="Pavel Klyuev — Principal SRE / Platform Engineer. Kubernetes, cloud infrastructure and production systems."': 'content="Pavel Klyuev — Principal SRE / Platform Engineer. Kubernetes and production infrastructure."',
    '<p class="eyebrow">SRE / Platform Engineering / Production</p>': '<p class="eyebrow">SRE / Platform Engineering</p>',
    '<p class="lead">Build and run reliable production systems.</p>': '<p class="lead">Production infrastructure and Kubernetes.</p>',
    '<p class="lead-detail">Kubernetes, cloud, CI/CD, networking, databases and observability. AI, data and voice workloads when needed.</p>': '<p class="lead-detail">Reliability, CI/CD, networking, databases, secrets and observability. AI, data and voice workloads.</p>',
    '<p class="focus">10+ years in production · GKE · AWS · Yandex Cloud · Hetzner</p>': '<p class="focus">10+ years · GKE · AWS · Yandex Cloud · Hetzner</p>',
    '<p class="availability">Available for audits, migrations, platform work and ongoing SRE support.</p>': '<p class="availability">Available for audits, migrations and SRE / platform work.</p>',
    '>Discuss a project</a>': '>Contact</a>',
    '>Selected work</a>': '>Work</a>',
    '<div class="cycle-head"><h2>How I work</h2><p>from design to operations</p></div>': '<div class="cycle-head"><h2>How I work</h2><p>design → operations</p></div>',
    '<b>Build</b><p>Infrastructure, Kubernetes, networking and secrets.</p>': '<b>Build</b><p>Infrastructure, Kubernetes, networking, secrets.</p>',
    '<b>Release</b><p>CI/CD, GitOps, migrations and checks.</p>': '<b>Release</b><p>CI/CD, GitOps, migrations, checks.</p>',
    '<b>Improve</b><p>Fix recurring issues and reduce manual work.</p>': '<b>Improve</b><p>Recurring issues and automation.</p>',
    '<b>Observe</b><p>Metrics, logs, traces, alerts and SLOs.</p>': '<b>Observe</b><p>Metrics, logs, traces, alerts, SLOs.</p>',
    '<b>Operate</b><p>Traffic, databases, queues, incidents and recovery.</p>': '<b>Operate</b><p>Traffic, databases, queues, incidents, recovery.</p>',
    '<section class="outcome-strip" aria-label="Typical production problems">': '<section class="outcome-strip" aria-label="Areas of work">',
    '<article><b>Production is unstable</b><p>Incidents repeat, capacity runs out or recovery takes too long.</p></article>': '<article><b>Reliability</b><p>Incidents, capacity and recovery.</p></article>',
    '<article><b>Infrastructure is hard to change</b><p>Deploys and infrastructure changes take too much effort or carry too much risk.</p></article>': '<article><b>Delivery</b><p>CI/CD, GitOps and infrastructure changes.</p></article>',
    '<article><b>Too much manual work</b><p>Routine operations, maintenance and recovery consume engineering time.</p></article>': '<article><b>Operations</b><p>Automation, maintenance and runbooks.</p></article>',
    '<article><b>Complex workloads need a platform</b><p>AI, data and voice workloads need the right network, capacity and observability.</p></article>': '<article><b>Workloads</b><p>AI, data and voice infrastructure.</p></article>',
    '<h3>Infrastructure Audit</h3><p>A focused review of the platform, its failure modes and recovery path.</p>': '<h3>Infrastructure Audit</h3><p>Architecture, Kubernetes, networking, secrets, delivery, monitoring and recovery.</p>',
    '<h3>Platform Engineering</h3><p>Build a platform teams can deploy to without rebuilding the same infrastructure for every service.</p>': '<h3>Platform Engineering</h3><p>Kubernetes platforms, infrastructure as code, GitOps, CI/CD, GitLab and cloud networking.</p>',
    '<h3>Production Reliability</h3><p>Fix recurring incidents, capacity problems and the parts of production that need constant attention.</p>': '<h3>Production Reliability</h3><p>Incidents, SLOs, capacity, performance, backups and recovery.</p>',
    '<h3>Security and Secrets</h3><p>Make secrets, certificates and access controlled, automated and recoverable.</p>': '<h3>Security and Secrets</h3><p>OpenBao, Vault, External Secrets, KMS, workload identity and TLS.</p>',
    '<h3>AI and Voice Infrastructure</h3><p>Put AI, retrieval and real-time voice workloads into production with the right network, capacity and observability.</p>': '<h3>AI and Voice Infrastructure</h3><p>LLM/RAG, GPU, vector search, SIP, RTP and WebRTC.</p>',
    '<h3>Production Kubernetes platform from image build to operations</h3>': '<h3>Kubernetes platform on Hetzner and Talos</h3>',
    '<p>Production platform with immutable nodes, automated delivery, networking, storage, monitoring, backups and stateful services.</p>': '<p>Built and operated a Kubernetes platform on Hetzner with Talos.</p>',
    '<div class="cell"><b>Foundation</b><span>Packer-built Talos images, automated bootstrap, upgrades and worker node groups.</span></div>': '<div class="cell"><b>Foundation</b><span>Talos images, bootstrap, upgrades and worker node groups.</span></div>',
    '<div class="cell"><b>Networking</b><span>Cilium, cloud controllers, load balancers, ingress, DNS and certificate automation.</span></div>': '<div class="cell"><b>Networking</b><span>Cilium, cloud controllers, load balancers, ingress, DNS and TLS.</span></div>',
    '<div class="cell"><b>Operations</b><span>VictoriaMetrics, Grafana, Alertmanager, Fluent Bit, capacity controls and runbooks.</span></div>': '<div class="cell"><b>Operations</b><span>VictoriaMetrics, Grafana, Alertmanager, Fluent Bit and runbooks.</span></div>',
    '<div class="cell"><b>Stateful</b><span>CloudNativePG, PXC, RabbitMQ, Valkey, S3 backups and WAL archiving.</span></div>': '<div class="cell"><b>Stateful</b><span>PostgreSQL, MySQL, RabbitMQ, Valkey and S3 backups.</span></div>',
    '<p>Raft storage, Cloud KMS auto-unseal, External Secrets, isolated snapshots, TLS monitoring and tested recovery.</p>': '<p>OpenBao on GKE with Raft, Cloud KMS auto-unseal, External Secrets, snapshots and recovery tests.</p>',
    '<p>LLM gateways, embedding inference, ingestion, pgvector and Milvus retrieval, evaluation and GPU workloads.</p>': '<p>Kubernetes infrastructure for LLMs, embeddings, RAG, pgvector, Milvus and GPU workloads.</p>',
    '<p>Public SIP ingress, RTP media, OpenSIPS routing, WebRTC, private connectivity and workload isolation.</p>': '<p>SIP, RTP and WebRTC infrastructure with OpenSIPS, PostgreSQL and private networking.</p>',
    '<p>One Argo CD and Helm delivery model for AI, data and voice workloads across three cloud platforms.</p>': '<p>Argo CD and Helm delivery across GKE, AWS and Yandex Cloud.</p>',
    '<p>External PostgreSQL, authenticated Redis, object storage, dedicated runners, Artifact Registry and health checks.</p>': '<p>GitLab on GKE with PostgreSQL, Redis, object storage, runners and Artifact Registry.</p>',
    '<p>IPsec gateways, routes, firewall rules, Cloud NAT and private access for enterprise environments.</p>': '<p>Terraform-managed IPsec, routes, firewall rules, Cloud NAT and private access.</p>',
    '<div class="section-head"><span class="index">03 / stack</span><h2>Technology stack</h2></div>': '<div class="section-head"><span class="index">03 / stack</span><h2>Stack</h2></div>',
    '<article class="land"><h3>Platforms and runtime</h3>': '<article class="land"><h3>Platforms</h3>',
    '<article class="land"><h3>Security and secrets</h3>': '<article class="land"><h3>Security</h3>',
    '<article class="land"><h3>Databases, messaging and storage</h3>': '<article class="land"><h3>Databases and messaging</h3>',
    '<article class="land"><h3>Data, ML and AI</h3>': '<article class="land"><h3>Data and AI</h3>',
    '<article class="land"><h3>Networking and access</h3>': '<article class="land"><h3>Networking</h3>',
    '<article class="land"><h3>Voice and real-time</h3>': '<article class="land"><h3>Voice</h3>',
    '<p>For audits, platform engineering, reliability work, migrations and production infrastructure.</p>': '<p>SRE, platform engineering, audits and migrations.</p>',
}

for old, new in replacements.items():
    if old not in text:
        print(f"not found: {old[:100]}")
    text = text.replace(old, new)

# The separate hire block repeats the same call to action as the hero and Contact section.
text = re.sub(r'\n\s*<section class="hire panel" aria-label="Work together">.*?</section>\n', '\n', text, flags=re.S)

path.write_text(text, encoding="utf-8")
