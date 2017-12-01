# Fire-simulation
A model to simulate how plant traits and disturbance interact. It'll have a name
at some point. Despite the title, it doesn't have fire in it yet. :(

Created by Sam Flake, North Carolina State University

This project is currently in rough shape, but the goal is to build a growth model 
that can simulate how trees with different attributes alter vegetation-fire
feedbacks. The model is a distance-independent (non-spatially-explicit) model
driven by leaf mass, which is then related to other tree components through
allometric relationships. This gives it a lot of flexibility to tune different
life history strategies to relate their traits to stand dynamics (hopefully!).

It is based largely upon Falster, Brannstrom, Dieckmann, and Westoby. 2011.
Journal of Ecology, which uses a metapopulation structure to simplify their model.
Currently, this model borrows much of the allometry and physiological components
but does not use their metapopulation model. This model is, so far, very computationally
intensive and totall stochastic, without the metapopulation logic.

Plans to extend this model include incorporating a model of the grass layer and using
this to develop a fuels component for modeling fire. Fire will then feed back into
the tree growth  model through tree mortality and leaf damage. This is a ways down the
road though.

The program lives in fire evol sim.py, and the parameters all live in parameters.py. 
When it's time to tune the program, it should be possible just to edit parameters.py,
run fire evol sim.py, and loop through different traits. Right now fire evol sim.py
doesn't produce any output that's usable, but the goal is to wrap it in another 
script that does the iteration over different traits, etc.
