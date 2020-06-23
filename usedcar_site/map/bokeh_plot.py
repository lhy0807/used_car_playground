from bokeh.io import show, output_notebook
from bokeh.models import (CDSView, ColorBar, ColumnDataSource,
                          CustomJS, CustomJSFilter, 
                          GeoJSONDataSource, HoverTool,
                          LinearColorMapper, Slider)
from bokeh.layouts import column, row, widgetbox
# pylint: disable=no-name-in-module
from bokeh.palettes import brewer
from bokeh.plotting import figure
from bokeh.embed import file_html
from bokeh.resources import CDN

def plot(ny):
        # Input GeoJSON source that contains features for plotting
        ny_source = GeoJSONDataSource(geojson = ny.to_json())
        # Define color palettes
        palette = brewer['OrRd'][8]
        palette = palette[::-1] # reverse order of colors so higher values have darker colors
        # Instantiate LinearColorMapper that linearly maps numbers in a range, into a sequence of colors.
        color_mapper = LinearColorMapper(palette = palette, low = ny['Points'].min(), high = ny['Points'].max())


        # Create color bar.
        color_bar = ColorBar(color_mapper = color_mapper, 
                        label_standoff = 8,
                        width = 500, height = 20,
                        border_line_color = None,
                        location = (0,0), 
                        orientation = 'horizontal')

        # Create figure object.
        p = figure(title = 'Calculated Weighted Points', 
                plot_height = 650 ,
                plot_width = 950, 
                toolbar_location = 'below',
                tools = "pan, wheel_zoom, box_zoom, reset",
                output_backend="webgl")
        p.xgrid.grid_line_color = None
        p.ygrid.grid_line_color = None
        # Add patch renderer to figure.
        states = p.patches('xs','ys', source = ny_source,
                        fill_color = {'field' :'Points',
                                        'transform' : color_mapper},
                        line_color = "gray", 
                        line_width = 0.25, 
                        fill_alpha = 1)
        # Create hover tool
        p.add_tools(HoverTool(renderers = [states],
                        tooltips = [('PO Name','@PO_NAME'),
                                        ('Points','@Points')
                                        ]))

        color_bar = ColorBar(color_mapper = color_mapper, 
                        label_standoff = 8,
                        width = 950, height = 20,
                        border_line_color = None,
                        location = (0,0), 
                        orientation = 'horizontal')
        p.add_layout(color_bar, 'below')
        #show(p)
        return(file_html(p, CDN, "my plot"))