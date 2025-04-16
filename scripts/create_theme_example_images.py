if __name__ == '__main__':
    import numpy as np
    from matplotlib import pyplot as plt

    from paperviz import plot
    from paperviz.plots.base import theme_registry, set_style

    rounds = np.linspace(250, 2900, 30)


    def fake_curve(seed, offset=0):
        np.random.seed(seed)
        base = np.linspace(-550 + offset, -400 + offset, len(rounds))
        noise = np.random.normal(0, 8, size=len(rounds))
        stderr = np.random.uniform(5, 20, size=len(rounds))
        return base + noise, stderr


    averaged_metrics = {
        "forward-method": {
            "round_num": rounds,
            "unique_scores": fake_curve(0)[0],
            "std_error": fake_curve(0)[1],
        },
        "reverse-method": {
            "round_num": rounds,
            "unique_scores": fake_curve(1, -40)[0],
            "std_error": fake_curve(1)[1],
        },
        "baseline": {
            "round_num": rounds,
            "unique_scores": fake_curve(2, -60)[0],
            "std_error": fake_curve(2)[1],
        },
    }

    for theme in theme_registry.keys():
        set_style(theme)

        fig, ax = plot(
            "multiple_std_lines",
            data_dict=averaged_metrics,
            label_map={
                "forward-method": "Forward KL",
                "reverse-method": "Reverse KL",
                "baseline": "No Training",
            },
            style_map={
                "forward-method": "solid",
                "reverse-method": "dashed",
                "baseline": "dotted",
            },
            color_map={
                "forward-method": "#CC79A7",
                "reverse-method": "#0072B2",
                "baseline": "#009E73",
            },
            xlabel="Round Number",
            ylabel="Number of Unique Scores",
            xlim=(250, 2900),
            ylim=(-650, -355),
            x_formatter=lambda x, _: f"{x * 10:.0f}",  # Multiples the axis numbers by 10 and formats in integers
            y_formatter=lambda y, _: f"{y / 100:.1f}",  # Divides the axis number by 100 and formats up to 1 decimal
            save=f"../docs/_static/images/plot_themes/{theme}"
        )

        plt.show()
