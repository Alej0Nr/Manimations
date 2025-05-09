from manim import *
import numpy as np
from scipy.integrate import *

beta = 0.003
nu = 1
class SIRPlot(Scene):
    def construct(self):
        axes = Axes(
            x_range=[0, 12, 1],
            y_range=[0, 1000, 50],
            # x_length=10,
            axis_config={"color": GREEN},
            x_axis_config={
                "numbers_to_include": np.arange(0, 12.01, 1),
                "numbers_with_elongated_ticks": np.arange(0, 12.01, 1),
            },
            tips=False,
        )

        self.add(axes)

        def SIR(t, z, nu, beta, u=0):
            s, i, r = z
            dsdt = -(1-u)*beta*s*i
            didt = (1-u)*beta*s*i - nu*i
            drdt = nu*i

            return [dsdt, didt, drdt]
        sol = solve_ivp(SIR, (0,12), [999,1,0], t_eval= np.linspace(0, 12, 500), args= [1,0.003], method='RK45')
        t_vals = sol.t
        S_vals = sol.y[0]
        I_vals = sol.y[1]
        R_vals = sol.y[2]
        S_points = [axes.c2p(t, y) for t, y in zip(t_vals, S_vals)]
        I_points = [axes.c2p(t, y) for t, y in zip(t_vals, I_vals)]
        R_points = [axes.c2p(t, y) for t, y in zip(t_vals, R_vals)]
        S_curve = VMobject(color=BLUE).set_points_smoothly(S_points)
        I_curve = VMobject(color=RED).set_points_smoothly(I_points)
        R_curve = VMobject(color=YELLOW).set_points_smoothly(R_points)
        self.play(Create(S_curve),Create(I_curve),Create(R_curve))
        self.wait()