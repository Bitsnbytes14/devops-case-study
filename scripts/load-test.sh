#!/usr/bin/env bash
for i in $(seq 1 100); do curl -s -o /dev/null http://localhost:5000/api/v1/sample || true; done
