# Reflection and report

The full assessment report is [RoomFit_DevOps_Case_Studies.docx](RoomFit_DevOps_Case_Studies.docx). It answers Q1 Netflix and Q2 Amazon, then connects those cases to RoomFit readiness probes, replicas, controlled faults, independently deployable service boundaries, and rollback. The accompanying [five slide deck](RoomFit_DevOps_Slides.pptx) covers architecture, pipeline flow, challenges, lessons learned, and results.

The strongest practical lesson from this build is that verification must follow the service path. The Kubernetes NodePort availability test remained available through replacement, while a Pod specific port forward did not. The evidence preserves both results and labels the valid service level test.
