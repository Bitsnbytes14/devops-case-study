# Autoscaling scope

The CA II reference document lists autoscaling and k6 load testing as an additional full-platform exercise. Those components are not implemented or claimed in this standalone RoomFit allocation service.

The current Kubernetes deployment has three fixed replicas, resource requests and limits, readiness and liveness probes, a rolling-update strategy, and verified rollback. A HorizontalPodAutoscaler and k6 workload should be added only after agreeing a target metric, replica bounds, and load-test acceptance criteria. This scope note prevents the submission from presenting unverified autoscaling evidence as completed work.
