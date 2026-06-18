#!/bin/bash
# Setup Kibana dashboards and index patterns
# Run this after the ELK stack is fully up and data has been ingested

KIBANA_URL="http://localhost:5601"
ES_URL="http://localhost:9200"

echo "============================================"
echo "  ELK Dashboard Setup Script"
echo "============================================"
echo ""

# Wait for Kibana to be ready
echo "[1/5] Waiting for Kibana to be ready..."
until curl -s "$KIBANA_URL/api/status" | grep -q '"level":"available"'; do
    echo "  Kibana not ready yet, waiting 10s..."
    sleep 10
done
echo "  Kibana is ready!"
echo ""

# Wait for data to be indexed
echo "[2/5] Waiting for log data to be indexed..."
sleep 15
DOCS=$(curl -s "$ES_URL/web-logs-*/_count" | python3 -c "import sys,json; print(json.load(sys.stdin).get('count', 0))" 2>/dev/null)
echo "  Found $DOCS documents indexed"
echo ""

# Create data view (index pattern)
echo "[3/5] Creating data view for 'web-logs-*'..."
curl -s -X POST "$KIBANA_URL/api/data_views/data_view" \
  -H "kbn-xsrf: true" \
  -H "Content-Type: application/json" \
  -d '{
    "data_view": {
      "title": "web-logs-*",
      "timeFieldName": "@timestamp",
      "name": "Web Server Logs"
    }
  }' | python3 -c "import sys,json; d=json.load(sys.stdin); print(f\"  Created data view: {d.get('data_view',{}).get('id','unknown')}\")" 2>/dev/null
echo ""

# Import saved objects (dashboards, visualizations)
echo "[4/5] Importing dashboard and visualizations..."
curl -s -X POST "$KIBANA_URL/api/saved_objects/_import?overwrite=true" \
  -H "kbn-xsrf: true" \
  --form file=@"$(dirname "$0")/../kibana/dashboards/web-logs-dashboard.ndjson"
echo ""
echo ""

# Final status
echo "[5/5] Setup complete!"
echo ""
echo "============================================"
echo "  Access your dashboard at:"
echo "  $KIBANA_URL/app/dashboards"
echo ""
echo "  Elasticsearch: $ES_URL"
echo "  Logstash monitoring: http://localhost:9600"
echo "============================================"
