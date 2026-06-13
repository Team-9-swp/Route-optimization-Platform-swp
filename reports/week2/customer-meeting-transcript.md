[00:00:00]

**Team member:** Hello. Can you hear us?

**Customer:** Yes, I can hear you.

**Team member:** Can we record this meeting?

**Customer:** Yes, of course. These meetings will remain with you, correct? You are not publishing them anywhere?

**Team member:** We will use them for the assignment. We will prepare a transcript, and we may need to include it in the repository according to the course requirements.

**Customer:** I understand.

[00:00:31]

**Customer:** Let us go through what has already been done, the current status, and the plan for the next week.

[00:00:50]

**Customer:** Has the team implemented the greedy algorithm?

[00:01:14]

**Team member:** Yes. The vehicle routes are currently built using a greedy approach. They are reasonably optimized, but not fully optimized yet. After that, we add loaders and also optimize their routes using a greedy algorithm. The loader routes are also reasonably good, but there is still room for improvement.

[00:01:37]

**Team member:** Then we use simulated annealing. We randomly change the routes of loaders and vehicles. If the result is better than the previous one, we keep it. If the result is worse, we may still keep it with some probability, so that the algorithm can escape a local minimum.

[00:01:58]

**Team member:** Without this, the algorithm may converge to a local optimum and stop improving.

[00:02:14]

**Customer:** I looked at the algorithm. Overall, the approach is clear. One thing I wanted to note is that the current order sorting is based on the time window, specifically the right boundary of the time window. It seems that the distance matrix is not additionally considered at that stage.

[00:02:48]

**Team member:** Yes, at the moment we mainly consider one parameter there.

[00:02:58]

**Team member:** When choosing where a loader should go during a time window, we iterate through possible options and choose the shortest or most beneficial one at the current step. It may not be globally optimal for the entire route, but it is the best immediate choice.

[00:03:21]

**Customer:** Yes, that is essentially a greedy heuristic.

[00:03:26]

**Customer:** Have you already tried running the algorithm on a scenario?

[00:03:31]

**Team member:** Yes, we tried running it. The results are quite good. We had a question about the baselines. You provided test examples and existing solutions for them, but those baselines seem rather weak. Our greedy-based algorithms already produce better results than the ones you provided. Is that expected?

[00:04:01]

**Customer:** Yes, that is normal. Currently, there are only three test scenarios. I can provide ten more scenarios that already exist, although I have not uploaded their solutions yet. You can test on those as well, because they are larger. The test scenarios are relatively small.

[00:04:31]

**Team member:** Are those the competition instances?

**Customer:** Yes, the competition instances. If I remember correctly, they go up to about 1,500 orders.

[00:04:44]

**Team member:** So the maximum size is around 1,500 orders, correct?

**Customer:** Around that, yes. Possibly a bit less or in that range.

[00:04:53]

**Customer:** The input scenarios are already available and can be downloaded. The solutions have not been published yet.

[00:05:04]

**Team member:** Will you send or upload solutions for the instances?

**Customer:** Yes, I think I will upload them to GitHub.

[00:05:10]

**Team member:** So there will be no additional test data beyond that?

**Customer:** Yes. I have already tried running on those scenarios, and it works. The only issue is that there is not yet a solution to compare against.

[00:05:26]

**Team member:** So the largest scenario is about 1,000 orders?

**Customer:** Yes. But as I said initially, the baselines are simple. If you manage to beat them during the MVP stage, then we will focus further on improving your current logistics algorithm.

[00:05:59]

**Customer:** Have you tried adding visualization to inspect the constructed routes and analyze them?

**Team member:** Not yet.

[00:06:15]

**Customer:** You also sent me preliminary user stories, correct?

**Team member:** Yes. This is part of our course project. One of the assignments requires us to prepare user stories for the project.

[00:06:41]

**Customer:** I reviewed the user stories. I did not find any contradictions. Overall, they look logical. The priorities also seem correct from your side.

[00:07:01]

**Customer:** There are several participants in this solution, and you have covered them properly. You described the value each participant receives from the solution.

[00:07:26]

**Customer:** I also wanted to clarify deployment and infrastructure: where do you plan to run the calculations and deploy the solution? Do you have computing resources?

[00:07:47]

**Team member:** Good question. I wanted to ask you about that as well. We can make a terminal-based launch, or put it into some kind of wrapper or small user interface.

[00:08:06]

**Customer:** Let us first clarify the infrastructure. Do you plan to make it as a desktop application, where everything is calculated locally on the user's machine, or as a server-side solution?

[00:08:28]

**Team member:** At the moment, we are developing it as a desktop/local solution, so the calculations would run on the user's computer.

[00:08:38]

**Customer:** Regarding the interaction interface, a terminal version would generally be enough. However, it would be good if there were also an option to use it through a web interface, for example by deploying a service, moving the computational module into a service, and also deploying a UI.

[00:09:14]

**Customer:** I would describe this as a desirable addition. It is not necessarily mandatory, but it would be a plus.

[00:09:22]

**Team member:** So you mean a remote server where users can upload data and receive results?

**Customer:** Yes.

[00:09:29]

**Customer:** Does the university provide computing resources for deployment and calculations?

**Team member:** Yes, during the project we are provided with resources so that we can test, deploy, and run it.

[00:09:45]

**Customer:** In that case, such a format could work. Right now the task runs quickly and does not require many resources. But by the end of the project, I expect the algorithms to become more complex and require more computational power, so it makes sense to involve a server.

[00:10:14]

**Customer:** In practice, optimization solutions are often not deployed only on a local machine. They typically require computational resources, so following that direction would be reasonable.

[00:10:37]

**Customer:** What are your plans for the next week?

[00:10:50]

**Team member:** We also want to try using PyVRP and nevergrad, similar to the winning approach from last year.

[00:10:56]

**Customer:** You can try that. I would recommend it. VRP solvers, including PyVRP and OR-Tools VRP solvers, use the same types of heuristics that you are currently using, but they are not limited to them. They are also well optimized.

[00:11:25]

**Customer:** At least the vehicle-routing part of your current solution can be run through a VRP solver and compared with your current vehicle routes.

[00:11:42]

**Customer:** You can compare the routes generated by your current algorithm with the routes generated by a VRP solver.

[00:11:57]

**Customer:** At this point, there is a separation: you already have an MVP from the algorithmic side, and now much of the work is about interaction with the model. In terms of MVP, it can be considered okay.

[00:12:20]

**Customer:** Next, you can focus on improving the solution quality. VRP solvers are a reasonable direction.

[00:12:32]

**Customer:** Since you started with heuristics, I can also recommend looking at more advanced algorithms, such as column generation.

[00:12:43]

**Customer:** There are adaptations of column generation for VRP. It involves some mathematical background, but in general, the method helps form route groupings based on matrix constraints.

[00:13:11]

**Customer:** It could be interesting to explore because your current approach is heuristic, and column generation might fit into your heuristic framework.

[00:13:29]

**Customer:** However, it requires linear programming and understanding both column generation itself and solvers for linear programming problems. It may be difficult to implement within the available time, but it is worth reviewing conceptually.

[00:13:59]

**Team member:** Thank you. We will look into it.

[00:14:04]

**Customer:** VRP solvers remain a good option. I think they can give a boost because many heuristics are already built into them, so the results should be at least not worse.

[00:14:26]

**Customer:** For the next week, focus on deployment, think through how users will interact with the algorithm, and continue improving solution quality.

[00:14:41]

**Customer:** I will also add the baselines for the main cases. Run your algorithm on them and see the results.

[00:14:48]

**Customer:** I also have a question about the validation script. Have you used it to calculate the objective function?

[00:15:00]

**Team member:** Yes, that is correct.

[00:15:02]

**Customer:** Did it check for errors, for example time-window violations or other issues?

**Team member:** Yes. No problems were found.

[00:15:15]

**Customer:** Good. If you notice any issues or inaccuracies in the validator, please report them, because there may also be some edge cases there.

[00:15:32]

**Customer:** Do you have any other questions for me? Is there anything that needs to be approved?

[00:15:44]

**Team member:** I think we do not have any additional questions at the moment.

[00:15:52]

**Customer:** How do you feel about the task? Is it interesting or difficult?

[00:16:02]

**Team member:** It is interesting.

[00:16:06]

**Customer:** The task contains a lot of mathematics. You have worked with heuristics so far, but I assume you have also looked in other directions. Was anything particularly difficult or unclear?

[00:16:23]

**Team member:** There was nothing too difficult in principle. When I looked at algorithms used in existing solutions, some approaches were quite interesting.

[00:16:33]

**Team member:** You suggested using third-party solvers. We will try them, because they are likely to be more optimized than our current implementation.

[00:16:44]

**Team member:** Overall, the task is very mathematical.

[00:16:53]

**Customer:** Regarding visualization, there is the Plotly package, which can draw routes. It may not be the most specialized tool, but there are also specialized packages that can visualize routes based on the available data.

[00:17:04]

**Customer:** This is useful because it allows you to visually evaluate how good the routes are, identify where adjustments might be needed, and possibly discover patterns between runs that can later be incorporated into the algorithm.

[00:17:37]

**Customer:** I recommend using some visualization tool at least to see what the routes look like.

[00:17:59]

**Team member:** Then regarding the user stories, can you simply confirm that everything is okay?

**Customer:** Yes.

[00:18:14]

**Team member:** Is confirmation in Telegram enough?

**Customer:** Yes, of course.

[00:18:21]

**Customer:** If there are no more questions, I suggest we finish for today. It is a holiday today.

[00:18:32]

**Team member:** Thank you.

**Customer:** Thank you. Goodbye, and happy holiday.

**Team member:** Goodbye.

**Customer:** Have a good day and a good weekend.

[00:18:40]

**Meeting ended.**

