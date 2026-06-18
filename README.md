# ELK Stack Dashboard - Sample Project

A complete sample project demonstrating **Elasticsearch**, **Logstash**, and **Kibana** (ELK stack) for log ingestion, search, and visualization.

![ELK Stack](https://img.shields.io/badge/ELK-8.12.0-blue) ![Docker](https://img.shields.io/badge/Docker-Compose-blue)

## What's Included

- **Elasticsearch 8.12.0** — Search and analytics engine
- **Logstash 8.12.0** — Log processing pipeline (parses Apache/Nginx combined logs)
- **Kibana 8.12.0** — Visualization dashboard
- **Sample Data** — 5,000 realistic web server access log entries
- **Pre-built Dashboard** — Ready-to-import Kibana dashboard with 7 visualizations

## Dashboard Visualizations

| Visualization | Type | Description |
|---------------|------|-------------|
| Total Requests | Metric | Total number of HTTP requests |
| Avg Response Size | Metric | Average response body size in bytes |
| HTTP Methods | Donut Pie | GET/POST/PUT/DELETE/PATCH distribution |
| Response Codes Over Time | Line Chart | Status codes (200, 404, 500, etc.) over time |
| Top URLs | Table | Most frequently requested endpoints |
| Response Categories | Bar Chart | Success/Redirect/Client Error/Server Error |
| Top Client IPs | Horizontal Bar | Clients generating the most traffic |

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) (v20.10+)
- [Docker Compose](https://docs.docker.com/compose/install/) (v2.0+)
- At least **4GB of available RAM** (Elasticsearch needs memory)

## Quick Start

### 1. Clone and Start

```bash
git clone <this-repo>
cd elk-dashboard-project

# Start the ELK stack
docker compose up -d
```

### 2. Wait for Services

Elasticsearch takes ~30-60 seconds to initialize. Check readiness:

```bash
# Check Elasticsearch
curl -s http://localhost:9200/_cluster/health | python3 -m json.tool

# Check Kibana (wait for "available")
curl -s http://localhost:5601/api/status | python3 -c "import sys,json; print(json.load(sys.stdin)['status']['overall']['level'])"
```

### 3. Setup Dashboard

Once services are healthy, run the setup script to create the data view and import dashboards:

```bash
./scripts/setup-kibana.sh
```

### 4. View Dashboard

Open your browser to: **http://localhost:5601/app/dashboards**

Select "Web Server Logs Dashboard" to see the visualizations.

## Project Structure

```
elk-dashboard-project/
├── docker-compose.yml          # Orchestrates ES, Logstash, Kibana
├── .env                        # Configuration variables
├── .gitignore
├── data/
│   └── sample-access.log       # 5000 sample Apache log entries
├── elasticsearch/              # ES config (extensible)
├── kibana/
│   ├── config/                 # Kibana config (extensible)
│   └── dashboards/
│       └── web-logs-dashboard.ndjson  # Importable dashboard + visualizations
├── logstash/
│   ├── config/
│   │   └── logstash.yml        # Logstash settings
│   └── pipeline/
│       └── logstash.conf       # Parsing pipeline (grok, date, geoip, useragent)
├── scripts/
│   ├── generate-logs.py        # Regenerate sample data
│   └── setup-kibana.sh         # Create data view + import dashboard
└── README.md
```

## Logstash Pipeline Details

The pipeline (`logstash/pipeline/logstash.conf`) processes logs through these stages:

1. **Input** — Reads from the mounted sample log file
2. **Grok** — Parses Apache Combined Log Format into structured fields
3. **Date** — Extracts timestamp into `@timestamp`
4. **Mutate** — Converts `response` and `bytes` to integers
5. **GeoIP** — Resolves client IP to geographic location
6. **UserAgent** — Parses browser/OS from user-agent string
7. **Conditional** — Categorizes responses (Success, Redirect, Client Error, Server Error)
8. **Output** — Sends to Elasticsearch index `web-logs-YYYY.MM.dd`

## Customization

### Use Your Own Logs

Replace `data/sample-access.log` with your own Apache/Nginx access logs (combined format):

```
<ip> - - [<timestamp>] "<method> <path> HTTP/1.1" <status> <bytes> "<referrer>" "<useragent>"
```

Then restart Logstash:

```bash
docker compose restart logstash
```

### Regenerate Sample Data

```bash
python3 scripts/generate-logs.py
docker compose restart logstash
```

### Add More Pipelines

Create additional `.conf` files in `logstash/pipeline/` — Logstash will auto-load them.

### Scale Elasticsearch

For production, modify `docker-compose.yml` to add more ES nodes and remove `discovery.type=single-node`.

## Troubleshooting

| Issue | Solution |
|-------|----------|
| ES won't start | Increase Docker memory to 4GB+. On Linux: `sudo sysctl -w vm.max_map_count=262144` |
| No data in Kibana | Wait 1-2 minutes after startup. Check `docker logs logstash` for errors |
| Port conflict | Edit ports in `docker-compose.yml` or `.env` |
| Kibana shows "no data" | Ensure time range is set to "Last 7 days" in the date picker |

## Stopping

```bash
# Stop and keep data
docker compose down

# Stop and remove all data (fresh start)
docker compose down -v
```

## Next Steps

- Add [Filebeat](https://www.elastic.co/beats/filebeat) for production log shipping
- Enable [Elasticsearch security](https://www.elastic.co/guide/en/elasticsearch/reference/current/security-minimal-setup.html)
- Set up [alerting rules](https://www.elastic.co/guide/en/kibana/current/alerting-getting-started.html) for error rate thresholds
- Add [APM](https://www.elastic.co/apm) for application performance monitoring

## License

MIT
