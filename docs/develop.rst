Development notes
=================

Sphinx documentation
--------------------

**No tabs**. For the Sphinx documentation-generation program to give the 
expected results, it is crucially important to use *spaces* and **not** *tabs* 
in the ``py`` files.

To get LaTeX code to render correctly, it is often necessary to use a *raw*
string for documentation [#SphinxRaw]_.  A raw docstring starts with ``r"""``
instead of the usual ``"""``.

References
^^^^^^^^^^

.. [#SphinxRaw] "Math support in Sphinx"
   [`link <http://sphinx-doc.org/ext/math.html>`__].
