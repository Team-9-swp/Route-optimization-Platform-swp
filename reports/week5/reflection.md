# Week 5 Reflection

**Project:** Route Optimization Platform
**Team:** Team-9-swp
**Date:** 2026-07-05

## Overall Team Reflection

Week 5 was a critical culmination of our efforts, focusing on reflection, documentation, and presenting a polished MVP v2 increment to our customer. This success was built upon the solid foundation established in Assignment 4 (Quality, Reliability, UAT).

## Key Learnings & Insights

### 1. Documenting Architecture (and ADRs)
Documenting the system architecture was not a bureaucratic exercise but a highly valuable clarifying process. Creating a unified view of the system (using PlantUML diagrams for architecture, dataflow, and domain model) forced us to explicitly define and agree upon component boundaries and interactions. The use of **Architecture Decision Records (ADRs)** proved exceptionally beneficial for tracking the rationale behind key choices like the solver transition.

### 2. Refining the Workflow
Our Git workflow matured. The consistent use of feature branches, pull requests with CI checks, and a protected `main` branch instilled discipline and a sense of responsibility for quality. The successful execution of 5 UAT scenarios in Assignment 4 validated that our workflow delivers software that meets customer expectations.

### 3. Managing Configuration
The challenge of managing configuration across local development, Docker Compose, and the deployment environment was a recurring theme. While we have a robust system with `.env.example` files and separate Docker Compose profiles (e.g., `docker-compose.prod.yml`), we learned that clear, up-to-date documentation on this process is essential to prevent friction.

### 4. Delivering MVP v2
Delivering MVP v2 was a satisfying milestone. The new features, particularly the solution export, directly addressed customer feedback. We successfully demonstrated a functional, integrated system with persistent storage and reporting, moving beyond a proof-of-concept. We also benefited from the PyVRP solver implemented in Assignment 4, which the customer confirmed produces noticeably better routes than the earlier version.

### 5. Reviewing the Increment with the Customer
The Sprint Review was the highlight of the week. Building on the successful Assignment 4 UAT sessions, we presented the MVP v2 increment. Seeing the customer interact with the platform and understand the new features validated our work and reinforced the importance of frequent, tangible deliveries. The feedback on UX and the desire for a permanently accessible environment directly informed our planned process changes.

## Conclusion

Week 5 was a success. We delivered a functional MVP v2, built on a solid quality and reliability base from Assignment 4. We also took a critical step back to evaluate our process, solidify our documentation, and learn from our experience. The team is more aligned, our processes are more refined, and we have a clear set of improvements to pursue in the next sprint. The skills gained in architecture documentation, workflow management, and customer communication are invaluable for our continued development.
