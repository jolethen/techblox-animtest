from manim import *

class CatalystForgeStory(Scene):
    def construct(self):
        # Base Scene Configuration
        self.camera.background_color = "#0b0d14"
        CYAN_HEX = "#00FFFF"

        # =====================================================================
        # ACT 1: LORE INTRO (Terminal Narrative)
        # =====================================================================
        location_tag = Text("[ LOCATION: SECTOR 4 - CATALYST FORGE ]", font_size=16, color=TEAL_C)
        location_tag.to_corner(UL, buff=0.5)

        quote_line1 = Text('"We\'re pushing past 50 Mana units this time."', font_size=24, color=WHITE)
        quote_line2 = Text('"The curve isn\'t linear, Rook. Watch the telemetry."', font_size=22, color=GREY_A, slant=ITALIC)
        
        narrative_box = VGroup(quote_line1, quote_line2).arrange(DOWN, buff=0.25)
        
        # Terminal Box Surround
        border = SurroundingRectangle(narrative_box, color=BLUE_E, buff=0.4, stroke_width=1.5)
        bg_fill = BackgroundRectangle(border, color="#121624", fill_opacity=0.85)
        intro_group = VGroup(bg_fill, border, narrative_box).center()

        self.play(FadeIn(location_tag, shift=DOWN), run_time=0.6)
        self.play(Create(border), FadeIn(bg_fill), run_time=0.8)
        self.play(AddTextLetterByLetter(quote_line1), run_time=1.2)
        self.play(FadeIn(quote_line2, shift=UP * 0.2), run_time=1.0)
        self.wait(2.0)

        # Clean up Act 1
        self.play(
            FadeOut(intro_group, shift=UP),
            FadeOut(location_tag),
            run_time=0.8
        )

        # =====================================================================
        # ACT 2: GAUNTLET CHARGE VISUALIZER (In-World Technology)
        # =====================================================================
        charge_title = Text("SYSTEM: ROOK'S GAUNTLET CALIBRATION", font_size=20, color=CYAN_HEX)
        charge_title.to_edge(UP, buff=0.6)

        # Central Energy Ring
        core_ring = Circle(radius=1.2, color=BLUE_E, stroke_width=3)
        core_glow = Circle(radius=1.2, color=CYAN_HEX, stroke_width=8, fill_opacity=0.0)
        core_center = Dot(point=ORIGIN, radius=0.15, color=WHITE)
        
        # Dynamic Counter setup (Efficient DecimalNumber instead of Pango Text re-render)
        mana_units = ValueTracker(10)
        
        mana_num = Integer(10, font_size=28, color=CYAN_HEX)
        mana_label = Text(" MANA", font_size=28, color=CYAN_HEX)
        unit_counter = VGroup(mana_num, mana_label).arrange(RIGHT, buff=0.15).move_to(core_ring.get_center())
        
        mana_num.add_updater(lambda m: m.set_value(int(mana_units.get_value())))
        unit_counter.add_updater(lambda c: c.move_to(core_ring.get_center()))

        self.play(Write(charge_title), Create(core_ring), FadeIn(core_center), FadeIn(unit_counter), run_time=1.0)
        self.wait(0.3)

        # Step-by-Step Power Pulse Sequence
        self.play(core_ring.animate.set_color(TEAL), run_time=0.4)
        self.wait(0.4)

        # 40 Units
        self.play(
            mana_units.animate.set_value(40),
            core_ring.animate.scale(1.15).set_color(BLUE_B),
            run_time=1.0
        )
        self.wait(0.4)

        # 80 Units - Critical Charge
        self.play(
            mana_units.animate.set_value(80),
            core_ring.animate.scale(1.2).set_color(LIGHT_PINK),
            Create(core_glow),
            run_time=1.2
        )
        
        strike_text = Text("STRIKE EXECUTED!", weight=BOLD, font_size=24, color=RED_B)
        strike_text.next_to(core_ring, DOWN, buff=0.5)
        
        # Smooth Shockwave Effect
        shockwave = Circle(radius=0.1, color=WHITE, stroke_width=10)
        self.play(
            Write(strike_text),
            shockwave.animate.scale(35).set_stroke(width=0.5, opacity=0),
            run_time=0.8
        )
        self.wait(1.0)

        # Clean up Act 2 (Clear updaters before fading)
        unit_counter.clear_updaters()
        self.play(
            FadeOut(charge_title),
            FadeOut(core_ring),
            FadeOut(core_glow),
            FadeOut(core_center),
            FadeOut(unit_counter),
            FadeOut(strike_text),
            run_time=0.8
        )

        # =====================================================================
        # ACT 3: TELEMETRY DATA & EXPONENTIAL SCALING GRAPH
        # =====================================================================
        header_tag = Text("TELEMETRY LOG #0492", font_size=18, color=GREY_A)
        header_title = Text("Mana-to-Damage Yield Curve", font_size=28, weight=BOLD, color=CYAN_HEX)
        header_group = VGroup(header_tag, header_title).arrange(DOWN, aligned_edge=LEFT, buff=0.1).to_corner(UL, buff=0.5)

        # Graph Axes
        axes = Axes(
            x_range=[0, 100, 20],
            y_range=[0, 500, 100],
            x_length=6.0,
            y_length=3.5,
            axis_config={
                "color": GREY_B,
                "stroke_width": 2,
                "include_numbers": True,
                "font_size": 16,
            },
            tips=False
        ).shift(DOWN * 0.5 + LEFT * 0.8)

        x_label = axes.get_x_axis_label("Mana Units", edge=RIGHT, direction=RIGHT * 0.3).scale(0.55).set_color(TEAL_B)
        y_label = axes.get_y_axis_label("Damage Output", edge=UP, direction=UP * 0.3).scale(0.55).set_color(LIGHT_PINK)

        # Formula: D(m) = 0.25 * m^1.5
        def yield_curve(m):
            return 0.25 * (m ** 1.5)

        curve = axes.plot(yield_curve, x_range=[0, 100], color=CYAN_HEX, stroke_width=3.5)
        curve_glow = curve.copy().set_stroke(color=BLUE_B, width=7, opacity=0.35)

        # Dynamic Tracker Point
        graph_tracker = ValueTracker(10)

        tracker_dot = AlwaysRedraw(
            lambda: Dot(
                point=axes.c2p(graph_tracker.get_value(), yield_curve(graph_tracker.get_value())),
                color=WHITE,
                radius=0.07
            )
        )
        
        # Robust Guideline coordinates via screen space
        guidelines = AlwaysRedraw(
            lambda: axes.get_lines_to_point(
                axes.c2p(graph_tracker.get_value(), yield_curve(graph_tracker.get_value())),
                color=GREY_A,
                stroke_width=1,
                stroke_opacity=0.5
            )
        )

        # Telemetry Stat Box Setup
        stat_box = RoundedRectangle(corner_radius=0.1, height=2.0, width=3.2, fill_color="#121624", fill_opacity=0.9, stroke_color=BLUE_E)
        stat_box.move_to(RIGHT * 4.0 + UP * 0.2)
        
        stat_header = Text("READOUT", font_size=14, color=GREY_A).next_to(stat_box.get_top(), DOWN, buff=0.15)
        
        # Dynamic numerical readouts using Integers (Fast & No wobbly text)
        mana_readout_val = Integer(10, font_size=16, color=TEAL_B)
        mana_readout_lbl = Text("Mana: ", font_size=16, color=TEAL_B)
        mana_readout_unit = Text(" U", font_size=16, color=TEAL_B)
        readout_mana_grp = VGroup(mana_readout_lbl, mana_readout_val, mana_readout_unit).arrange(RIGHT, buff=0.1)
        readout_mana_grp.move_to(stat_box.get_center() + UP * 0.25)

        dmg_readout_val = Integer(8, font_size=16, color=LIGHT_PINK)
        dmg_readout_lbl = Text("Damage: ", font_size=16, color=LIGHT_PINK)
        dmg_readout_unit = Text(" HP", font_size=16, color=LIGHT_PINK)
        readout_dmg_grp = VGroup(dmg_readout_lbl, dmg_readout_val, dmg_readout_unit).arrange(RIGHT, buff=0.1)
        readout_dmg_grp.move_to(stat_box.get_center() + DOWN * 0.25)

        # Fast Updaters
        mana_readout_val.add_updater(lambda m: m.set_value(int(graph_tracker.get_value())))
        dmg_readout_val.add_updater(lambda d: d.set_value(int(yield_curve(graph_tracker.get_value()))))

        # Entrance Animations
        self.play(Write(header_group), Create(axes), FadeIn(x_label), FadeIn(y_label), run_time=1.2)
        self.play(Create(curve_glow), Create(curve), run_time=1.2)
        self.play(
            FadeIn(stat_box),
            FadeIn(stat_header),
            FadeIn(tracker_dot),
            Create(guidelines),
            FadeIn(readout_mana_grp),
            FadeIn(readout_dmg_grp),
            run_time=0.8
        )

        # Dynamic Sweep matching story progression
        self.wait(0.5)
        
        # 10 -> 40 Mana
        self.play(graph_tracker.animate.set_value(40), run_time=1.5, rate_func=smooth)
        self.wait(0.3)

        # 40 -> 80 Mana
        self.play(graph_tracker.animate.set_value(80), run_time=2.0, rate_func=smooth)
        
        # Highlight Callout at Strike Point
        callout_label = Text("Exponential Yield Threshold", font_size=15, color=YELLOW)
        callout_label.next_to(tracker_dot, LEFT, buff=0.4).shift(UP * 0.3)
        callout_arrow = Arrow(start=callout_label.get_right(), end=tracker_dot.get_left(), color=YELLOW, buff=0.1, max_tip_length_to_length_ratio=0.25)

        self.play(Write(callout_label), Create(callout_arrow), run_time=0.8)
        self.wait(2.5)
        
