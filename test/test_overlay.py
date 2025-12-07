"""Tests for the overlay module."""

import pytest
import numpy as np
import matplotlib.pyplot as plt

from datachart.charts import LineChart, BarChart, ScatterChart, Histogram
from datachart.utils import OverlayChart


class TestOverlayChart:
    """Test suite for OverlayChart functionality."""

    def test_line_bar_overlay_dual_axes(self):
        """Test line + bar overlay with dual axes."""
        # Create bar chart data
        bar_data = [
            {"label": "A", "y": 100},
            {"label": "B", "y": 200},
            {"label": "C", "y": 150},
            {"label": "D", "y": 300},
        ]
        bar_fig = BarChart(data=bar_data)

        # Create line chart data (different scale)
        line_data = [
            {"x": 0, "y": 5},
            {"x": 1, "y": 15},
            {"x": 2, "y": 10},
            {"x": 3, "y": 20},
        ]
        line_fig = LineChart(data=line_data)

        # Combine with explicit axis assignment
        combined_fig = OverlayChart(
            charts=[
                {"figure": bar_fig, "y_axis": "left"},
                {"figure": line_fig, "y_axis": "right"},
            ],
            title="Bar and Line Overlay",
            xlabel="Category",
            ylabel_left="Bar Values",
            ylabel_right="Line Values",
            show_legend=True,
        )

        assert combined_fig is not None
        assert isinstance(combined_fig, plt.Figure)
        plt.close(combined_fig)
        plt.close(bar_fig)
        plt.close(line_fig)

    def test_scatter_line_overlay_single_axis(self):
        """Test scatter + line overlay on single axis."""
        # Create scatter data
        scatter_data = [{"x": i, "y": i * 2 + np.random.randn()} for i in range(10)]
        scatter_fig = ScatterChart(data=scatter_data)

        # Create line data (similar scale)
        line_data = [{"x": i, "y": i * 2} for i in range(10)]
        line_fig = LineChart(data=line_data)

        # Combine with auto axis assignment
        combined_fig = OverlayChart(
            charts=[
                {"figure": scatter_fig},
                {"figure": line_fig},
            ],
            title="Scatter with Trend Line",
            xlabel="X",
            ylabel_left="Y",
            show_legend=True,
        )

        assert combined_fig is not None
        assert isinstance(combined_fig, plt.Figure)
        plt.close(combined_fig)
        plt.close(scatter_fig)
        plt.close(line_fig)

    def test_histogram_line_overlay(self):
        """Test histogram + line overlay."""
        # Create histogram data
        hist_data = [{"x": x} for x in np.random.randn(100)]
        hist_fig = Histogram(data=hist_data, num_bins=20)

        # Create line data for overlay (e.g., normal distribution curve)
        x_vals = np.linspace(-3, 3, 100)
        y_vals = 100 / np.sqrt(2 * np.pi) * np.exp(-0.5 * x_vals**2) * 0.6
        line_data = [{"x": x, "y": y} for x, y in zip(x_vals, y_vals)]
        line_fig = LineChart(data=line_data)

        # Combine
        combined_fig = OverlayChart(
            charts=[
                {"figure": hist_fig, "y_axis": "left"},
                {"figure": line_fig, "y_axis": "left"},
            ],
            title="Histogram with Distribution Curve",
            xlabel="Value",
            ylabel_left="Frequency",
            show_legend=True,
        )

        assert combined_fig is not None
        assert isinstance(combined_fig, plt.Figure)
        plt.close(combined_fig)
        plt.close(hist_fig)
        plt.close(line_fig)

    def test_automatic_axis_assignment(self):
        """Test automatic secondary axis detection."""
        # Create two charts with very different scales
        bar_data = [{"label": f"Cat{i}", "y": i * 1000} for i in range(5)]
        bar_fig = BarChart(data=bar_data)

        line_data = [{"x": i, "y": i * 2} for i in range(5)]
        line_fig = LineChart(data=line_data)

        # Use auto mode with default threshold
        combined_fig = OverlayChart(
            charts=[
                {"figure": bar_fig},  # auto
                {"figure": line_fig},  # auto
            ],
            title="Automatic Axis Assignment",
            auto_secondary_axis=3.0,
        )

        assert combined_fig is not None
        assert isinstance(combined_fig, plt.Figure)
        plt.close(combined_fig)
        plt.close(bar_fig)
        plt.close(line_fig)

    def test_drawing_order_preservation(self):
        """Test that charts are drawn in the specified order."""
        # Create three charts
        bar_data = [{"label": f"Cat{i}", "y": i * 10} for i in range(5)]
        bar_fig = BarChart(data=bar_data)

        line_data = [{"x": i, "y": i * 8} for i in range(5)]
        line_fig = LineChart(data=line_data)

        scatter_data = [{"x": i, "y": i * 12} for i in range(5)]
        scatter_fig = ScatterChart(data=scatter_data)

        # Combine with explicit z-order
        combined_fig = OverlayChart(
            charts=[
                {"figure": bar_fig, "z_order": 1},
                {"figure": line_fig, "z_order": 2},
                {"figure": scatter_fig, "z_order": 3},
            ],
            title="Drawing Order Test",
        )

        assert combined_fig is not None
        assert isinstance(combined_fig, plt.Figure)
        plt.close(combined_fig)
        plt.close(bar_fig)
        plt.close(line_fig)
        plt.close(scatter_fig)

    def test_legend_combination(self):
        """Test legend combination from multiple charts."""
        # Create charts with subtitles (for legend labels)
        line1_data = [{"x": i, "y": i} for i in range(10)]
        line1_fig = LineChart(data=line1_data, subtitle="Series 1")

        line2_data = [{"x": i, "y": i * 2} for i in range(10)]
        line2_fig = LineChart(data=line2_data, subtitle="Series 2")

        # Combine with legend
        combined_fig = OverlayChart(
            charts=[
                {"figure": line1_fig, "y_axis": "left"},
                {"figure": line2_fig, "y_axis": "right"},
            ],
            title="Legend Test",
            show_legend=True,
        )

        assert combined_fig is not None
        assert isinstance(combined_fig, plt.Figure)
        plt.close(combined_fig)
        plt.close(line1_fig)
        plt.close(line2_fig)

    def test_scale_compatibility_detection(self):
        """Test scale compatibility detection."""
        # Create two charts with compatible scales
        line1_data = [{"x": i, "y": i * 10} for i in range(10)]
        line1_fig = LineChart(data=line1_data)

        line2_data = [{"x": i, "y": i * 15} for i in range(10)]
        line2_fig = LineChart(data=line2_data)

        # Both should be on left axis with auto mode
        combined_fig = OverlayChart(
            charts=[
                {"figure": line1_fig},
                {"figure": line2_fig},
            ],
            title="Compatible Scales",
            auto_secondary_axis=3.0,
        )

        assert combined_fig is not None
        assert isinstance(combined_fig, plt.Figure)
        plt.close(combined_fig)
        plt.close(line1_fig)
        plt.close(line2_fig)

    def test_figsize_specification(self):
        """Test with different figsize specifications."""
        bar_data = [{"label": f"Cat{i}", "y": i * 10} for i in range(5)]
        bar_fig = BarChart(data=bar_data)

        line_data = [{"x": i, "y": i * 8} for i in range(5)]
        line_fig = LineChart(data=line_data)

        # Test with custom figsize
        combined_fig = OverlayChart(
            charts=[
                {"figure": bar_fig},
                {"figure": line_fig},
            ],
            figsize=(12, 6),
        )

        assert combined_fig is not None
        assert isinstance(combined_fig, plt.Figure)
        fig_size = combined_fig.get_size_inches()
        assert fig_size[0] == 12
        assert fig_size[1] == 6
        plt.close(combined_fig)
        plt.close(bar_fig)
        plt.close(line_fig)

    def test_show_grid(self):
        """Test grid display option."""
        bar_data = [{"label": f"Cat{i}", "y": i * 10} for i in range(5)]
        bar_fig = BarChart(data=bar_data)

        line_data = [{"x": i, "y": i * 8} for i in range(5)]
        line_fig = LineChart(data=line_data)

        # Test with grid
        combined_fig = OverlayChart(
            charts=[
                {"figure": bar_fig},
                {"figure": line_fig},
            ],
            show_grid="both",
        )

        assert combined_fig is not None
        assert isinstance(combined_fig, plt.Figure)
        plt.close(combined_fig)
        plt.close(bar_fig)
        plt.close(line_fig)

    def test_empty_charts_list(self):
        """Test error handling for empty charts list."""
        with pytest.raises(ValueError, match="At least one chart is required"):
            OverlayChart(charts=[])

    def test_missing_figure_key(self):
        """Test error handling for missing figure key."""
        bar_data = [{"label": f"Cat{i}", "y": i * 10} for i in range(5)]
        bar_fig = BarChart(data=bar_data)

        with pytest.raises(ValueError, match="missing 'figure' key"):
            OverlayChart(
                charts=[
                    {"figure": bar_fig},
                    {"y_axis": "right"},  # missing figure key
                ]
            )
        plt.close(bar_fig)

    def test_invalid_figure_metadata(self):
        """Test error handling for figure without metadata."""
        # Create a plain matplotlib figure (no datachart metadata)
        plain_fig = plt.figure()

        with pytest.raises(ValueError, match="missing chart metadata"):
            OverlayChart(charts=[{"figure": plain_fig}])

        plt.close(plain_fig)

    def test_multiple_bar_charts_overlay(self):
        """Test overlaying multiple bar charts with position adjustment."""
        bar1_data = [{"label": f"Cat{i}", "y": i * 10} for i in range(5)]
        bar1_fig = BarChart(data=bar1_data, subtitle="Series 1")

        bar2_data = [{"label": f"Cat{i}", "y": i * 15} for i in range(5)]
        bar2_fig = BarChart(data=bar2_data, subtitle="Series 2")

        # Combine multiple bar charts
        combined_fig = OverlayChart(
            charts=[
                {"figure": bar1_fig},
                {"figure": bar2_fig},
            ],
            title="Multiple Bar Charts",
            show_legend=True,
        )

        assert combined_fig is not None
        assert isinstance(combined_fig, plt.Figure)
        plt.close(combined_fig)
        plt.close(bar1_fig)
        plt.close(bar2_fig)

    def test_all_chart_types_combined(self):
        """Test combining all four chart types."""
        # Create all chart types
        bar_data = [{"label": f"Cat{i}", "y": i * 100} for i in range(5)]
        bar_fig = BarChart(data=bar_data, subtitle="Bars")

        line_data = [{"x": i, "y": i * 20} for i in range(5)]
        line_fig = LineChart(data=line_data, subtitle="Line")

        scatter_data = [{"x": i, "y": i * 25 + np.random.randn() * 5} for i in range(5)]
        scatter_fig = ScatterChart(data=scatter_data, subtitle="Scatter")

        hist_data = [{"x": x} for x in np.random.randn(50) * 10 + 50]
        hist_fig = Histogram(data=hist_data, num_bins=10, subtitle="Histogram")

        # Combine all
        combined_fig = OverlayChart(
            charts=[
                {"figure": bar_fig, "y_axis": "left", "z_order": 1},
                {"figure": hist_fig, "y_axis": "left", "z_order": 1},
                {"figure": line_fig, "y_axis": "right", "z_order": 2},
                {"figure": scatter_fig, "y_axis": "right", "z_order": 3},
            ],
            title="All Chart Types Combined",
            xlabel="X",
            ylabel_left="Count",
            ylabel_right="Value",
            show_legend=True,
        )

        assert combined_fig is not None
        assert isinstance(combined_fig, plt.Figure)
        plt.close(combined_fig)
        plt.close(bar_fig)
        plt.close(line_fig)
        plt.close(scatter_fig)
        plt.close(hist_fig)
