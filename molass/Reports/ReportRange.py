"""
Reports.ReportRange.py
"""
import numpy as np

MINOR_COMPONENT_MAX_PROP = 0.2

def make_v1report_ranges_impl(decomposition, ssd, mapped_curve, area_ratio, debug=False):
    if debug:
        from importlib import reload
        import molass.LowRank.ElementRecords
        reload(molass.LowRank.ElementRecords)
    from molass.LowRank.ElementRecords import make_element_records_impl
    # task: concentration_datatype must have been be set before calling this function.
    elm_recs, elm_recs_uv = make_element_records_impl(decomposition, ssd, mapped_curve, debug=debug)

    components = decomposition.get_xr_components()
    # components = decomposition.get_uv_components()

    if debug:
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots()
        for comp in components:
            icurve = comp.get_icurve()
            ax.plot(icurve.x, icurve.y, label=f'Component {comp.peak_index}')
        ax.set_xlabel('Frames')
        ax.set_ylabel('Intensity')
        ax.set_title('Components Elution Curves')
        ax.legend()
        fig.tight_layout()
        plt.show()

    ranges = []
    areas = []
    for comp in components:
        areas.append(comp.compute_area())
        ranges.append(comp.compute_range(area_ratio))

    area_proportions = np.array(areas)/np.sum(areas)
    if debug:
        print("area_proportions=", area_proportions)

    ret_ranges = []
    for comp, range_, prop in zip(components, ranges, area_proportions):
        minor = prop < MINOR_COMPONENT_MAX_PROP
        ret_ranges.append(comp.make_paired_range(range_, minor=minor, elm_recs=elm_recs_uv, debug=debug))

    return ret_ranges