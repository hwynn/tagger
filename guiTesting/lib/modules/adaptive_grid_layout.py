#!/usr/bin/env python
from kivy.lang import Builder
from collections import OrderedDict
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock



class Adaptive_GridLayout(GridLayout):
    """
    Adaptive height and row heights for grid layouts.

    Note this should not be used as a root layout and '_refresh_y_dimension()' method should be used by
    children widgets that change height to update all attached instances of Adaptive_GridLayout (this layout).

    Copyright AGPL-3.0 2019 S0AndS0
    """

    def __init__(self, grow_cols = False, grow_rows = False, **kwargs):
        self.c_debug = False
        if self.c_debug: print("Adaptive_GridLayout.__init__():", self)
        super(Adaptive_GridLayout, self).__init__(**kwargs)
        self.grow_cols = grow_cols
        self.grow_rows = grow_rows
        self.size_hint_y = None
        self.trigger_refresh_y_dimension = Clock.create_trigger(lambda _: self._refresh_y_dimension(), 0)

    def _yield_tallest_of_each_row(self):
        """ Yields tallest child of each row within gridlayout. """
        if self.c_debug: print("\t\t\t\tAdaptive_GridLayout._yield_tallest_of_each_row():", self)
        current_tallest = None
        for i, c in enumerate(list(reversed(self.children))):
            if current_tallest is None:
                current_tallest = c

            if c.height > current_tallest.height:
                current_tallest = c

            ## Should work around grids without value for 'cols'
            if self.cols is None or self.cols is 0:
                if self.c_debug: print("\t\t\t\t", current_tallest)
                yield current_tallest
                current_tallest = None
            ## Reached last item of current row... Fizzbuzz!
            elif ((i + 1) % self.cols == 0) is True:
                if self.c_debug: print("\t\t\t\t", current_tallest)
                yield current_tallest
                current_tallest = None

    def _calc_child_padding_y(self, child):
        """ Returns total padding for a given child. """
        if self.c_debug: print("\t\t\t\tAdaptive_GridLayout._calc_child_padding_y():", self, child)
        ## May be faster than asking permission with an if statement as most widgets seem to have padding
        try:
            child_padding = child.padding
        except AttributeError as e:
            child_padding = [0]

        len_child_padding = len(child_padding)
        if len_child_padding is 1:
            padding = child_padding[0] * 2
        elif len_child_padding is 2:
            padding = child_padding[1] * 2
        elif len_child_padding > 2:
            padding = child_padding[1] + child_padding[3]
        else:
            padding = 0
        if self.c_debug: print("\t\t\t\t", padding)
        return padding

    def _calc_min_height(self):
        """ Returns total height required to display tallest children of each row plus spacing between widgets. """
        if self.c_debug: print("\t\t\tAdaptive_GridLayout._calc_min_height():", self)
        min_height = 0
        for c in self._yield_tallest_of_each_row():
            min_height += c.height
        if self.c_debug: print("\t\t\t", min_height)
        return min_height

    def _calc_rows_minimum(self):
        """ Returns ordered dictionary of how high each row should be to accommodate tallest children of each row. """
        if self.c_debug: print("\t\t\tAdaptive_GridLayout._calc_rows_minimum():", self)
        rows_minimum = OrderedDict()
        for i, c in enumerate(self._yield_tallest_of_each_row()):
            rows_minimum.update({i: c.height})
        if self.c_debug: print("\t\t\t", rows_minimum)
        return rows_minimum

    def _refresh_height(self):
        """ Resets 'self.height' using value returned by '_calc_min_height' method. """
        if self.c_debug: print("\t\tAdaptive_GridLayout._refresh_height():", self)
        if self.c_debug: print("\t\tself.height before:", self.height)
        if self.c_debug: print("\t\tself.minimum_height before:", self.minimum_height)
        self.height = self._calc_min_height()
        #self._update_minimum_size() #this doesn't work, but it should do the same thing
        if self.c_debug: print("\t\tself.height after:", self.height)

    def _refresh_rows_minimum(self):
        """ Resets 'self.rows_minimum' using value returned by '_calc_rows_minimum' method. """
        if self.c_debug: print("\t\tAdaptive_GridLayout._refresh_rows_minimum():", self)
        if self.c_debug: print("\t\tself.rows_minimum before:", self.rows_minimum)
        self.rows_minimum = self._calc_rows_minimum()
        if self.c_debug: print("\t\tself.rows_minimum after:", self.rows_minimum)

    def _refresh_y_dimension(self):
        """ Updates 'height' and 'rows_minimum' first for spawn, then for self, and finally for any progenitors. """
        if self.c_debug: print("\tAdaptive_GridLayout._refresh_y_dimension():", self)
        spawn = [x for x in self.walk(restrict = True) if hasattr(x, '_refresh_y_dimension') and x is not self]
        for item in spawn:
            item._refresh_rows_minimum()
            item._refresh_height()

        self._refresh_rows_minimum()
        self._refresh_height()

        progenitors = [x for x in self.walk_reverse() if hasattr(x, '_refresh_y_dimension') and x is not self]
        for progenitor in progenitors:
            progenitor._refresh_rows_minimum()
            progenitor._refresh_height()

    def on_children(self, instance, value):
        """ If 'grow_cols' or 'grow_rows' is True this will grow layout that way if needed instead of erroring out. """
        if self.c_debug: print("Adaptive_GridLayout.on_children():", self, instance, value)
        if not self.rows or not self.cols:
            return super(Adaptive_GridLayout, self).on_children(instance, value)

        max_widgets = self.rows * self.cols
        widget_count = len(value)

        differance = widget_count - max_widgets
        if widget_count > max_widgets:
            if self.grow_cols:
                self.cols += differance
            elif self.grow_rows:
                self.rows += differance

        return super(Adaptive_GridLayout, self).on_children(instance, value)

    def on_parent(self, instance, value):
        """ Some adjustments maybe needed to get top row behaving on all platforms. """
        if self.c_debug: print("Adaptive_GridLayout.on_parent():", self, instance, value)
        self.trigger_refresh_y_dimension()