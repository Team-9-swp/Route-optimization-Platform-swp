# Customer Sprint Review Transcript

**Meeting date:** 19 June 2026  
**Duration:** approximately 31 minutes 40 seconds  
**Original language:** Russian  
**Transcript language:** English  
**Participants:** Customer representative and project team members  
**Sanitization:** Personal names and unnecessary identifying details have been omitted. Obvious speech-recognition errors, repetitions, and filler words were removed without changing the meaning.

> **Permission note:** At the beginning of the meeting, the customer explicitly permitted recording and use of a sanitized transcript. The team later confirmed that the sanitized transcript may be stored in the public repository as part of the Assignment 3 submission.

[00:01:04]

**Team:** Hello. May we record this meeting and use a sanitized transcript?

**Customer:** Yes, you may. I confirm.

[00:01:16]

**Customer:** Let us begin with the current status. What were you able to implement this week? Could you explain the work in more detail?

[00:01:28]

**Team — Algorithm:** Two team members are working on the algorithm. One of us continued improving the previous greedy algorithm. After the greedy solution is produced, a local-improvement stage randomly changes parts of the solution and keeps changes that improve the result.

[00:02:13]

**Team — Algorithm:** This gave an improvement of approximately 5–10% compared with the original greedy algorithm in some cases.

[00:02:21]

**Team — Algorithm:** I also tried a different approach using OR-Tools, followed by greedy construction and an additional improvement stage. This performed better, with an improvement of roughly 30% in some tests.

[00:02:47]

**Team — Algorithm:** OR-Tools handles the vehicle-routing constraints well. Loader routes are then assigned greedily and improved afterwards.

[00:03:05]

**Team — Algorithm:** Compared with the provided baseline, our result is about 5% worse on the first, third, and fourth scenarios. On the remaining scenarios, it is between 2% and 40% better. The method performs especially well on larger instances, while the results on smaller instances are currently weaker.

[00:03:43]

**Customer:** How do you handle optional orders? It is important to compare the benefit of accepting an optional order with the additional costs it creates, such as extra loaders or vehicles.

[00:04:14]

**Team — Algorithm:** At the moment, the process is partly greedy. We pass the routing data to OR-Tools, which evaluates transport costs without considering loaders. Loader assignments are added afterwards.

[00:04:30]

**Team — Algorithm:** The improvement stage can add or remove optional orders and check whether the objective value improves. If an optional order is added, the vehicle route and any required loader assignment are also updated.

[00:05:15]

**Customer:** Do you begin with mandatory orders and then add optional ones, or do you initially distribute all orders?

[00:05:27]

**Team — Algorithm:** The vehicle structure is optimized first. A simulated-annealing stage includes operations that can add or remove optional orders. Once the selected orders and vehicle routes are determined, loaders are assigned and then improved separately.

[00:06:28]

**Team — Algorithm:** Adding or removing an optional order is one of the neighborhood operations. The algorithm tries these changes and moves toward a lower-cost solution.

[00:07:03]

**Customer:** So OR-Tools initially compares optional-order revenue with vehicle costs. If the order remains beneficial, you then add loader costs and reassess whether it is still worth serving?

**Team — Algorithm:** Yes, approximately. Loader economics are considered in the later stage.

[00:07:50]

**Customer:** You could improve this by estimating expected loader costs earlier and incorporating those estimates into the weights of optional orders. Then optional orders might be selected more accurately during the first stage.

[00:08:44]

**Customer:** Overall, the development direction is good. Do you have ideas for improving the three remaining scenarios required for the final result?

[00:09:04]

**Team — Algorithm:** For small instances, we may use a different method. Our current approach is designed for larger data sets and is not always optimal for small ones. For smaller instances, we may be able to explore many more alternatives or use a near-exhaustive search to find a better solution.

[00:09:48]

**Customer:** Understood. I have not yet reviewed the repository in detail. I started looking at it late and there is a lot of material. I will try to review it during the day or over the weekend and leave comments if questions arise. Please also help orient me in the repository.

[00:10:20]

**Team — Documentation:** The repository contains the project documentation, prototypes, and an MVP 0 demonstration video. The API has been deployed on the university virtual machine. One endpoint accepts input data, and another endpoint returns the result.

[00:10:40]

**Team:** [inaudible]

[00:11:28]

**Customer:** I saw interface screenshots with routes shown in different colors. Is that intended to be the route-visualization interface?

**Team — Frontend:** Yes.

[00:12:18]

**Customer:** Are you planning to continue working on the interface?

**Team — Frontend:** Yes. We would like feedback on the current prototypes. Next week, we plan to implement the frontend so that you can open it and test the product directly.

[00:12:47]

**Customer:** A map could be useful, for example with OpenStreetMap, but the provided data does not contain real geographic coordinates.

[00:13:33]

**Customer:** Since the scenarios are based on competition benchmarks rather than real geographic data, a real map is not necessary. You can visualize the routes on a two-dimensional coordinate plane instead.

[00:13:57]

**Customer:** You should consider scalability because some scenarios contain up to one thousand orders. The visualization should remain responsive. One thousand points and connecting lines should still be manageable, but route colors must be selected clearly so the display does not become confusing.

[00:14:27]

**Customer:** The frontend is optional, but it would be useful because users want to see the result.

[00:14:38]

**Customer:** The frontend should ideally allow users to start a calculation and monitor its status, for example “calculation in progress” and “calculation completed.” The algorithm has a time limit of up to fifteen minutes, so the status model is important.

[00:14:54]

**Customer:** You should also measure how quickly the calculations are completed. I will later need to validate the system by running it myself.

[00:15:15]

**Customer:** It may also be useful to display the history of previous calculations. The interface should be dynamic: users should be able to start a calculation, monitor the status, and then visualize the result, rather than only seeing a previously calculated static image.

[00:15:47]

**Customer:** It would be interesting to run the same input twice and compare the results to see how stable the algorithm is. Reproducibility was not an explicit requirement, so it will not be assessed, but it can still be valuable from a business perspective.

[00:16:27]

**Customer:** Even when a random seed is fixed, stopping by a time limit may cause a different number of iterations, so the exact calculation path may still differ.

[00:16:43]

**Team — Algorithm:** We use a configurable seed in the calculations. If the algorithm itself is unchanged, the results are approximately deterministic. One or two additional iterations usually do not significantly change the result.

[00:17:09]

**Customer:** This could be supported in the interface, possibly together with calculation history. However, storing history would require a database, and you need to decide how much can realistically be implemented within the available time.

[00:17:31]

**Customer:** Another possible business requirement is balanced workload distribution. Drivers and loaders have similar shifts, so ideally one person should not work one hour while another works twelve hours. This was not included in the original task because the optimization problem was already complex.

[00:18:39]

**Team — Frontend:** Even if workload balancing is not implemented as an objective, we could visualize the schedule using a Gantt-style chart. One view could show routes on a coordinate plane, while another could show each driver or vehicle on a timeline.

[00:19:13]

**Team — Frontend:** We could assign workload balancing a low priority and implement it only if time remains.

[00:19:27]

**Customer:** That is more suitable for a later stage. The main MVP should first achieve the target result and perform better than the baseline. Additional visualization features can be considered afterwards.

[00:20:03]

**Team:** How was the baseline created? Does it include workload balancing?

[00:20:13]

**Customer:** No, workload balancing is not included. The baseline was created to estimate expected running time and the approximate objective value. It was not intended to be a high-quality optimized solution.

[00:20:43]

**Customer:** The task was prepared quickly for a competition. The purpose of the baseline was to show how a simple algorithm performs and to provide a reference value. The competition task is then to find better ideas and cover a wider range of scenarios.

[00:21:28]

**Customer:** The real business problem is somewhat different and more complex. For the competition, it was standardized and simplified to match academic VRP benchmarks.

[00:21:45]

**Customer:** Our internal solver supports more constraints and functionality, but these were not all included in the competition task.

[00:22:14]

**Customer:** The baseline instances were based on standard benchmarks and then extended with our own indicators and weights. This is why I asked about optional orders: the weights may be somewhat unbalanced, and it may be possible to determine in advance whether serving all optional orders is beneficial.

[00:23:18]

**Customer:** The baseline is based on PyVRP. It follows a process similar to yours: first it solves the vehicle-order problem, then it solves the loader problem.

[00:23:38]

**Customer:** Loader routes are also handled as a VRP-like problem. Their time windows are adjusted based on vehicle arrival times. The model uses simplified assumptions about where loaders start and finish and an estimated average distance from the depot.

[00:25:04]

**Customer:** It would be possible to add further iterations that reconsider optional orders, as your algorithm does, but the baseline was not intended to produce an optimal result. That is why exceeding it should be achievable.

[00:25:29]

**Customer:** Returning to the frontend, you could experiment with Gantt charts. They are often used to visualize production schedules and could show when each vehicle or loader is active, which orders are served, and where idle time occurs.

[00:26:31]

**Customer:** This would also make workload imbalance visible, because it would be easy to see that one vehicle or loader is active much longer than another.

[00:27:03]

**Customer:** Again, the frontend is optional. It would be good to have, but it is not a critical requirement.

[00:27:15]

**Team — Documentation:** We will take this into account. The repository also includes the interface prototypes and detailed Docker launch instructions.

[00:27:46]

**Customer:** I will review the repository more thoroughly, try to run the project, and send questions in the chat if necessary.

[00:28:07]

**Team — Frontend:** We also considered storing calculation data, for example in Redis. Would a database be necessary?

[00:28:18]

**Customer:** If you want to provide calculation history rather than only cache a few static results, then a database is appropriate. For a dynamic interface that starts calculations and stores history, a database is definitely needed.

[00:28:53]

**Customer:** There are no special scalability requirements for the database because the calculations and scenarios are relatively small. Almost any reasonable storage solution would be acceptable.

[00:29:12]

**Customer:** For static precomputed results, a database may not be worth the effort. For calculation history, you should also consider retention rules, such as keeping only a certain number of runs or automatically deleting records older than one week.

[00:29:59]

**Customer:** I do not have strict requirements for storage because the current scenarios are limited and the system is not planned for production use. If the product is developed further, the storage model can also be improved later.

[00:30:27]

**Team:** Let us summarize the priorities for next week.

[00:30:32]

**Customer:** First, continue improving the algorithm. You already have several promising ideas, and I hope they work.

[00:30:47]

**Customer:** Second, continue working on the frontend. Visualization would make the result much easier to inspect. You can decide which suggested features are realistic and useful within the available time.

[00:31:18]

**Customer:** Do you have any other questions?

**Team:** No further questions.

[00:31:27]

**Customer:** Thank you, and good luck next week.

**Team:** Thank you. Goodbye, and have a good day.

**Customer:** Thank you. Have a good day. Goodbye.
