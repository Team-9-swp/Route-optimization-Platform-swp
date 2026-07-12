# Sprint Review — Meeting Transcript

> **Meeting date:** 10 July 2026
> **Duration:** ~20 minutes
> **Attendees:** Team Member A (presenter), Team Member B (technical), Customer
> **Recording source:** Video call recording (transcribed via Whisper)
> **Sanitised for:** Public repository (no PII, roles used instead of names)

---

## Pre-meeting context

**Team Member A:** Will [Team Member C] be there? They won't be — they're in class, sitting in for me. They had tasks related to interviews.

**Team Member B:** Related to what?

**Team Member A:** To interviews. They were supposed to conduct interviews.

**Team Member B:** What kind of questions? What specific items?

**Team Member A:** They were supposed to discuss the transition and the sprint review.

**Team Member B:** Sprint review — we do that every week anyway.

**Team Member A:** Well, sprint review, yes, I agree, but the transition — there we needed to get some practice and all that. Let's see now.

---

## Meeting start

**Customer:** Hello. Finally I got through to you. Strange — I couldn't log in, it gave an error and wouldn't let me in. From different devices, too. Anyway, I managed to get in. Great.

**Customer:** We'll start with the status. May I record the meeting and publish the transcript?

**Team Member A:** Yes, you can.

**Customer:** Thank you.

---

## Sprint 4 status

**Team Member A:** This week we focused on the algorithm and some organisational matters. Specifically, we need to get ready to hand over our product to the customer — i.e., to you.

**Customer:** Let's start with the user acceptance tests. Are there any user exception tests?

**Team Member A:** Regarding tests, I'll tell you now. Last time we checked whether our algorithm is deterministic, right? Last time it wasn't deterministic. This time we fixed it, and it is deterministic. I think that's all — from user tests. Everything else you've already accepted: history viewing, validation, creation, and the actual launch of the algorithm. All that, right?

**Customer:** Yes, yes, everything is fine. I can show at the end of the meeting which networks we ran on and how deterministic it is. But for now, let's discuss the transition.

---

## Transition discussion

**Customer:** The transition of our project to you. So — what we need to do on our side, and what you need to do on yours so that you can get it running. On our side, practically everything is ready. Some nuances remain on the frontend and technical side. Overall, the algorithm works, but there are planned improvements for the next time. Next week, final.

**Customer:** By the way, we have reached the baseline. I can later send a table to the group with the baseline results and what we achieved. So — we didn't pass the fourth test, and our algorithm beat it by about half a percent.

**Team Member A:** Is that at the level of randomness? Random seed?

**Team Member B:** Well, everything runs on the same seed. Seed 42 — so it'll work in 15 minutes.

**Customer:** Okay.

**Customer:** Look — to check, I'll need the address or the branch name of the repository where the latest algorithm is stored. That is, I can take the release version for independent run, because here I'll be checking, among other things, what's under the hood — I'll run the scenario separately, not through the form.

**Team Member B:** Yes, good. Right.

**Team Member B:** We currently have a small problem in the algorithm. I added returning drivers to the depot. And when our algorithm calculates the cost, there's a thing where these driver routes are split by zeros. That is, if a driver suddenly went somewhere and then continued further, it counts as two drivers. So if we fix that moment — but the validator seems to show correct numbers. If we fix the fact that the return is counted incorrectly — they are counted as different — so right now everything works.

**Customer:** Okay. I'm noting that, including. But I think I won't test this weekend, no. I'll do it next week. At the beginning of the week, most likely. I'll run everything — work with the algorithm, check, and so on.

**Customer:** Regarding service transfer, how does that happen? We remain within your perimeter, right? That is, there's no need to deploy the service on some local machine of mine and test it. So here, transfer implies that I essentially go through something like a demo. Then I make some report that everything works, everything is done, I accept it. And accordingly, that's the end of the verification and acceptance.

**Team Member A:** Well, I thought a bit differently. That is, you should get our repository and try to deploy it yourself. That's the first option. What does that imply? That you will be able to contribute to our project later. And then you will improve it from your side if needed. Or change something. That is, if it's deployed from our side, you won't be able to do anything. You need full access so you can change or fix things if necessary.

**Customer:** Okay, deploy it — I'll deploy it and try then during next week as well. I won't be able to do it on the weekend.

**Customer:** So, after deployment, will it be enough just to say the words I say? Or do I need to record something again, check, show that everything is up locally?

**Team Member A:** It's enough that you accept this item.

**Customer:** Okay. Then I understand. We can move on.

---

## Product delivery format

**Team Member A:** Do you want to receive the project purely as an algorithm or in a website wrapper?

**Customer:** With a wrapper, of course. So I'll deploy it with the interface, so I need to be able to spin everything up through a single container without any shamanism.

**Team Member A:** So then it turns out either you give me a pointer that from such-and-such a branch, such-and-such a release can be taken. If it's already ready, just send it to the chat, please, so that I don't bother you further and minimise waiting.

**Team Member B:** Done. Everything working is on master. We push there what worked on our site. And we check there.

**Customer:** Okay. So I understand that I can immediately evaluate against that baseline. Improved or not improved. Right?

**Team Member B:** That's correct. I can send the table.

**Customer:** You can look at it now. In any case, I will run the algorithm from sources. And I understand, I also need to run it through the form — not through the form, but through the interface. Here too, synchronise so that everything matches. All versions of the algorithm.

**Team Member B:** Okay. Well, I'll run it, then tell you what I did. If something is wrong, we'll adjust it then.

---

## Product features and next steps

**Customer:** Do you have any comments? Or do you want to add something to the product? Or can we do that next week?

**Customer:** So — last time we agreed to display calculation time on the dashboard. That feature is already there by status. Were we developing it? Did we touch it or not? Not yet, right? And, if I'm not mistaken, we also talked about working on visualisation of work schedules for vehicles and loaders as a Gantt chart. Also a question here — do you plan to finish it, or is that off the table?

**Team Member B:** Yes. The Gantt chart is in this sprint.

**Customer:** In this sprint, yes?

**Team Member B:** Uh-huh.

**Customer:** Overall, regarding next week's issues — I may have limited access to the Russian network. So, most likely, I won't be able to have a teleconference next week. I think maybe we can arrange a Zoom link. They seem to still work here.

**Team Member B:** Zoom works.

**Customer:** Well, if anything, I'll see what alternatives are possible and then send it.

---

## Algorithm technical deep-dive

**Customer:** Let's perhaps go a bit into detail about what changed in the algorithm that allowed us to beat the fourth case.

**Team Member B:** So — I'll now roughly explain how our algorithm works. There is Nevergrad, which distributes, builds hyperparameters, selects — for example, what we have there. Penalties for unfulfilled orders. Penalties for… I'll say more in a moment. In general, there are several hyperparameters that Nevergrad computes. And from several runs, the best is selected. Then with the best we proceed. We optimise with PyVRP. And we also greedily assign these loaders. And we check with simulated annealing. We run it for optimisation.

**Team Member B:** Why did it get better? Because some optional orders are skipped. Somewhere I changed the probability. I think for small orders, they are skipped less. Or more. But I might be lying. Maybe I did the opposite. I tested where the result was better. And we also have the driver return to depot. That also contributes. Maybe that's the improvement. I think we talked about this before. In the end, it worked.

**Customer:** Great.

---

## Determinism and stability

**Team Member B:** Regarding stability — a small comment. This is a big problem. There are existing solvers that contain sets of algorithms. And for them, the main focus initially was not on performance, but on reliability. To reliably produce the same solution. Because optimal solutions can also be obtained in some set. It could be an infinite set. Or finite, but with many variants. And when using them, getting different solutions on the same data turned out to be very critical. Therefore, when developing these solvers, the emphasis shifted specifically to reliability, to solution stability. But this problem was solved. Basically, Nevergrad just generated its own random seeds. We just needed to give it our own seed, which we used everywhere. Something like that.

**Customer:** Great that we were able to easily get rid of instability.

---

## Meeting close

**Customer:** Anything else? I have no questions for you. On my side, once I start interacting with your repository, if any questions arise, I'll write immediately. But I hope everything is transparent. And I'll be able to do everything independently, without additional consultations, and deploy it.

**Team Member A:** Yes, good.

**Customer:** Any questions for me?

**Team Member A:** Then I suggest we wrap up today — it turned out quite concise. Thank you.

**Customer:** Thank you for the meeting. And have a good day. Goodbye.

**Team Member A:** Have a good day to you too. And you too. Goodbye.

---

## Key decisions and action items

| # | Item | Owner | Due |
|---|------|-------|-----|
| 1 | Customer to deploy the project independently from protected `main` | Customer | Week 7 |
| 2 | Customer to run the algorithm from sources and verify against baseline | Customer | Week 7 |
| 3 | Customer to run the algorithm through the web interface and verify consistency | Customer | Week 7 |
| 4 | Customer to verify determinant behaviour across multiple runs | Customer | Week 7 |
| 5 | Team to provide a release pointer after remaining fixes (completed after the meeting with Week 6 release `v1.4.0`) | Team | Completed after meeting |
| 6 | Validate the completed Gantt chart during customer-side testing | Team | Week 7 |
| 7 | Calculation time on dashboard — status confirmed (feature present) | Team | Sprint 4 |
| 8 | Customer to use Zoom for next meeting due to network limitations | Customer | Week 7 |

---

*Transcript sanitised and translated from Russian. No personal data retained. Roles used instead of names.*
