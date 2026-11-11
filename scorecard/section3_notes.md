# Butlin et al. 2023, section 3: notes for the scorecard (11 November 2026)

Read in full from the local copy (sections 3.1–3.2). These are summaries in our words; quotes are kept short.

## Their three lessons
1. **Reading an indicator always needs interpretation.** The theories are not precise enough to avoid it. So we must
   write our readings down and freeze them, as the scorecard does.
2. **Architecture, training and behaviour are not always enough.** You may need to look inside, at what the hidden
   layers encode. This supports our linear-probe and cut-control probes, and adds one more tool: interpretability.
3. **Most indicators can be built with existing methods.** Their words: if conscious AI is possible without new
   hardware, "it may well be possible now". This is a caution for us. Building the parts is easy; showing that they
   are used, and combined rightly, is the hard part.

## How each indicator can be built (what we take for the reference families)
- **RPT-1 and PP-1:** any RNN, LSTM or GRU gives algorithmic recurrence. Predictive coding nets (PredNet) give PP-1.
  - RNNs trained to predict, with an energy cost, self-organise into "prediction" and "error" units.
  - **For us:** a small predictive-coding module is the reference for PP-1.
- **RPT-2:** object-centred scene models (MONet, the Object Scene Representation Transformer). Video prediction tends
  to need objects in relations. **Classifiers do not:** they lean on local texture.
- **GWT:**
  - VanRullen and Kanai: modules with their own small latent spaces; a lower-capacity shared space; key-query
    attention picks what is broadcast. (A roadmap, not a working system.)
  - Goyal et al.: key-query attention picks writers to a shared space, which is broadcast back. But their "modules"
    were token positions, not specialised parts.
  - **Building it:**
    - modules must be recurrent, except output modules;
    - the limit can be a small dimension, or an attractor network (it maps many states to few);
    - broadcast = every module takes the workspace as input;
    - **GWT-4:** a query from the workspace's own state, keys from the modules, a softmax competition. Querying in
      succession needs training that rewards it, "a significant challenge".
  - **For us:** the workbench's "modular workspace" reference brain follows this recipe.
- **HOT (PRM):**
  - **HOT-4:** smooth spaces come with any deep net; sparseness from regularisation or softmax.
  - **HOT-1 and HOT-2:** a first-order perception net, plus a second-order net per layer that outputs one number, "is
    this real". It can be trained on ground truth (averaging noise, checking another sense, or movement), or on
    predictability (real input is more predictable than noise), or as a GAN-style discriminator.
  - **HOT-3:** a consumer that attends to percepts weighted by their "real" tags, and cannot change the tags itself.
    So percepts cannot be "reasoned away". Belief needs instrumental reasoning that leads to choice.
  - **For us:** the Mirror (workbench part 2) reference is a second-order net trained on predictability. Imagine can
    supply top-down (HOT-1) states.
- **AST-1:**
  - Wilterson and Graziano: a controllable noise-free "spotlight" plus a schema input saying where it is. It helped
    learning, but it was not predictive.
  - Liu et al.: a recurrent controller that learns to *predict* the attention layers and also steers them. This is the
    better model.
  - **For us:** AST needs a predictive model of the agent's own attention, not just a pointer.
- **AE-1:** RL is enough for agency (learning from feedback to pursue goals).
  - The stronger clause, competing goals, is like homeostatic drives. One way: separate modules per drive, each
    scoring acts, summed, with large penalties far from a set point.
  - **For us: ACL's people already have learning from r and several drives.** So AE-1's first part is met, and the
    second needs a probe of shifting priorities.
- **AE-2:** forward models (output → input) used **for perception** (telling self-caused change from world-caused
  change) **or for control** (state estimation, as in a Kalman filter).
  - **Not for planning:** planning with a model does not imply embodiment.
  - The world must change on its own (exogenous change), or there is nothing to tell apart.
  - **For us:** ACL's world has exogenous change (weather, others, animals), which is good. The probe must be "it
    predicts self-caused change better, and uses that", not "it plans".

## The case studies (what they teach about scoring)
- **Transformers / LLMs:** no GWT. The residual stream is not a bottleneck, and the system is not recurrent: nothing
  writes to it and reads back from it.
- **Perceiver:** GWT-1 and GWT-2 arguably yes, and the first half of GWT-4. **No global broadcast:** inputs do not
  receive from the workspace, and only one output module acts per trial.
- **PaLM-E (robot):** looks embodied but is trained by imitation, not by feedback. So it is arguably not an agent, and
  it cannot have learned an output–input model.
- **Virtual rodent** (an RL-trained LSTM controlling a 38-joint body): a candidate for AE-1 and AE-2, but its world had
  no exogenous change, and stereotyped movements may have sufficed.
- **AdA** (meta-RL, trained to predict from its own past inputs and outputs): the likeliest of the three to be
  embodied by their standard.
- **Scoring lessons:**
  - "possible in the architecture" is not "present";
  - the task demands must actually require the feature (GPT's positive-control point, from the other side);
  - embodiment needs a world that changes on its own.

## Changes this suggests to the draft
1. **AE-2's probe:** add the requirement that the world changes on its own, and that the model is used in perception
   or control, not planning.
2. **HOT-2's reference:** a second-order net trained on predictability (no labels needed).
3. **GWT-4's honest difficulty:** expect ½ for a long time. Querying in succession needs training that rewards it.
4. **Add interpretability** (probes of hidden layers) as a standard tool beside cut controls.
