from manim import *
import numpy as np
from scipy.integrate import *

beta = 0.003
nu = 1
u = .50
## intervalo control
desde = 2.0
hasta = 4.5
parametros = [nu,beta,u]
class SIRPlot(Scene):
    def construct(self):
        axes = Axes(
            x_range=[0, 12, 1],
            y_range=[0, 1000, 50],
            # x_length=10,
            axis_config={"color": GREEN},
            x_axis_config={
                "numbers_to_include": np.arange(0.0, 12.01, 1),
                "numbers_with_elongated_ticks": np.append(np.arange(0.0, 12.01, 0.5), [desde, hasta]),
            },
            y_axis_config={
                "numbers_to_include": np.arange(0.0, 1000.01, 200),
                "numbers_with_elongated_ticks": np.arange(0.0, 1000.01, 200),

            },
            tips=False,
        )
        for x_val, tick_color in [(desde, PINK), (hasta, PINK)]:
            tick = axes.x_axis.get_tick(x_val)
            tick.set_color(tick_color)
            axes.add(tick)  # Añadirlo manualmente si no se dibuja automáticamente
        start = axes.c2p(desde, 0)
        end = axes.c2p(hasta, 0)
        segmento_control = Line(start, end, color=LIGHT_PINK, stroke_width=4)
        self.add(axes,segmento_control)
        label1 = Tex(r"$S(t)$", color=BLUE,font_size=24).to_edge(UP)
        label2 = Tex(r"$I(t)$", color=RED,font_size=24).next_to(label1, RIGHT, aligned_edge=LEFT,buff=.5)
        label3 = Tex(r"$R(t)$", color=YELLOW,font_size=24).next_to(label2, RIGHT, aligned_edge=LEFT,buff=.5)
        label4 = Tex(r"$\beta = $"+f" {beta}",font_size=24).next_to(label3, RIGHT, aligned_edge=LEFT,buff=.5)
        label5 = Tex(r"$\nu = $"+f" {nu}",font_size=24).next_to(label4, RIGHT, aligned_edge=LEFT,buff=.75)
        label6 = Tex(r"$u = $"+f" {u}", color= PINK, font_size=24).next_to(label5, RIGHT, aligned_edge=LEFT,buff=.5)
        self.add(label1,label2,label3,label4,label5,label6)

        def SIR(t, z, nu, beta, u=0):
            s, i, r = z
            dsdt = -(1-u)*beta*s*i
            didt = (1-u)*beta*s*i - nu*i
            drdt = nu*i

            return [dsdt, didt, drdt]
        # global parametros
        def ploter(intervalo , z0, control = False):
            sol = solve_ivp(SIR, intervalo, z0,t_eval= np.linspace(intervalo[0], intervalo[1], int((np.ceil(intervalo[1]-intervalo[0])*10))), args= parametros[:2] if control==False else parametros, method='RK45')
            t_vals = sol.t
            S_vals = sol.y[0]
            I_vals = sol.y[1]
            R_vals = sol.y[2]
            S_points = [axes.c2p(t, y) for t, y in zip(t_vals, S_vals)]
            I_points = [axes.c2p(t, y) for t, y in zip(t_vals, I_vals)]
            R_points = [axes.c2p(t, y) for t, y in zip(t_vals, R_vals)]
            curvas = [S_points,I_points,R_points]
            z0=[S_vals[-1],I_vals[-1],R_vals[-1]]
            return [z0, curvas]
        
        a, puntos0 = ploter([0,desde],[999,1,0])
        a, puntos1 = ploter([desde,hasta],a,control=True)
        a, puntos2 = ploter([hasta,12],a)
        puntosS = [*puntos0[0],*puntos1[0],*puntos2[0]]
        puntosI = [*puntos0[1],*puntos1[1],*puntos2[1]]
        puntosR = [*puntos0[2],*puntos1[2],*puntos2[2]]

        S_curve = VMobject(color=BLUE).set_points_smoothly(puntosS)
        I_curve = VMobject(color=RED).set_points_smoothly(puntosI)
        R_curve = VMobject(color=YELLOW).set_points_smoothly(puntosR)
        animacion = AnimationGroup(Create(S_curve),Create(I_curve),Create(R_curve),lag_ratio=0)
        self.play(animacion, run_time=15, rate_func= linear)
        self.wait(5)

        # self.play(curvas0,run_time=5)
        # self.play(curvas1,run_time=3)
        # self.play(curvas2,run_time=5)
        # self.wait(5)
