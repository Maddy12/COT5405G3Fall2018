# Preferential deletion in dynamic models of web-like networks by Narsingh Deo and Aurel Cami (2007)
### Setting up environment
Please see environment-setup.pdf and set up schiapp_assigment3.yml so that all the necessary packages are installed. 
If you prefer to install packages on your own, the following are required:
* numpy
* networkx
* matplotlib
* progressbar2

The python version required is 2.7.

### Running the program
The program will run in the command line with: 

```bash
python preferential_deletion.py
```

You can also run the program within the python interface. An example is: 
```python
np.random.seed(12)
    time_steps = 5000
    t_degree = 4000
    p_births = [.6, .75, .9, .8]
    simulations = 30
    markers = ("^", "s", "D", "D")
    ylim = 4000
    time_steps_collect = range(1000, 6000, 1000)

    # Run Simulation
    nodes_dict, edges_dict, degree_dist_dict = run_simulation(p_births=p_births, simulations=simulations,
                                                              time_steps=time_steps,
                                                              time_steps_collect=time_steps_collect,
                                                              t_degree=t_degree)

    # Plot expected against simulated
    plot_expected(time_steps, nodes_dict, p_births, markers, E_func=run_expected_nodes, ylim=ylim,
                  time_steps_collect=time_steps_collect, title='expected_nodes')
    plot_expected(time_steps, edges_dict, p_births, markers, E_func=run_expected_edges, ylim=ylim,
                  time_steps_collect=time_steps_collect, title='expected_edges')
    plot_degree_dist(degree_dist_dict)
```

The plots will appear as the program runs in addition to being saved in the local directory in which the program is being run. 

### Questions
If you have any questions, please contact madelineschiappa@knights.ucf.edu.
