# MIT 600

## Recursion

Divide and Conquer
* small problems are easier to solve than the original one
* the solutions to the small problem can easily be combined to solve the big problem

### Recursion
* way of describing problems
* way of designing solutions (D & Q)

* Base Case
  * direct answer
* Inductive Case
  * reduce to a simpler version of the same problem plus some more simple operations
  
## Debugging
* Not to eliminate one bug quickly but rather to move towards a bug-free program.
* Search for bugs using binary search
* How could it have produced the result it did ? rather than Why didn't it produce the result I wanted?
---
* Study available data
  * program text
  * test results
* Form hypothesis consistent with data
* Design & run a *repeatable* experiment
  * Potential to refute hypothesis
  
---
* If program deals with user input, find smaller input on which program fails
* No such thing as *the* bug
* Use a test harness

## Efficiency and order of growth
* Efficiency is about algorithms, not about coding details
* When confronted with a problem, we want to reduce it to a previously solved problem.
* How do we think about efficiency ?
  * Think about it in 2 dimensions, space and time
  * we can trade one for the other
* Big O -> gives us an upper bound for the aymptotic growth of the function
* O(1) - constant
* O(log n)
* O(n)
* O(n logn) - log linear
* O(n^c) - polynomial
* O(c^n) - exponential
* The moral is try not to do anything worse than log linear if you possibly can.


## Memory and Search Methods
* Indirection
  * In Python a list is list of objects each of the same size because each object is a pointer
  * All Object Oriented languages use this
  * Problem: Too many levels of indirection
    * Can be a problem because values maybe be too far apart in memory which may disturb behaviors in caches
    
## Hashing and Classes
* Module - collection of related functions
* Class - collection of data and functions (operate on data)
  * method is a function associated with an object
  
## OOP and Inheritance
* Abstract Data Type
  * Interface - explains what the method do at the level of the user, not how they do it
  * Specifications - tells what that method does
  * Implementations
  * Data hiding - no direct access to instance variable and class variables
* Programs don't depend on, in any way, on the in which people chose to implement those built in types because you
programmed to the specification of the types, not to the implementation.

## Intro to Simulation and Random Walks
* When returning a property of a class use an interface (a function), that way if you choose to change the implementation
in the future, you don't affect other developers who are using your class
* `yield` - a generator
  * is a little bit like a return but with one big exception
  * with a regular return, it returns the object/value and is done. Any information about the function gets popped of the
  stack frame. 
  * `yield` is a little different. A generator is a function that remembers the point in the body where it was. It remembers
  the point in the function body where it last returned, plus all the local variables. So if you call the function again,
  it will pick up where it left off.
  
* Analytic methods - lead to things like Calculus, probability theory, understanding the microscopic physical world, 
  * is something that lets you precisely predict the behavior of a system, just based on some initial
  conditions and a set of parameters.
  * its nice but it doesn't always work, better off with simulation methods
* Simulation methods
  * reasons for simulations methods
    * The idea was that there were going to be some places where it's really hard to build a model. So in fact, places where
    this comes up
      * sometimes we have systems that are not mathematically tractable
      * ex: weather forecasting
    * As things get more complex, we're better off just successively refining a series of simulations.
    * Its often easier to extract useful intermediate results from a simulations than it is to try and build a detailed
    analytic model
    * computers
  * simulations means giving me an estimate, rather than a prediction
  * Idea of a simulation
    * build a model with the following property
      * gives useful information about behavior of a system
      * approximation to reality
      * simulation models are descriptive, not prescriptive 
  * Brownian motion is an example of random walk (Random walks are an incredibly useful way of building simulations.)
  * Random walk idea - If I've got a system of interacting objects could be pollen particles. I want to model what happens
  in that system under the assumption that each one of those things is going to move at each time step under some random
  distribution. It's going to move in a particular direction. I want to model what the overall system does.
    * really useful in modeling physical processes (ex: modeling weather, modeling all molecules in the air is just one big
    random walk), biological processes (ex: the kinetics of displacement of RNA from heteroduplexes of DNA), social
    processes (ex: movement of the stock market is definitely a random walk, expert for the day when the markets are all
    crashing for unfortunate reasons.)